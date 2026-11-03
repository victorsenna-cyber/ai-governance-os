#!/usr/bin/env python3
"""Avalia se o Laya decide a ARVORE de um pedido (CLAUDE.md §6, primeira decisao do roteador).

Uso (com o python do venv da pasta laya-teste, fora da Governança):
  avaliar.py                 gera o dataset e mede zero-shot
  avaliar.py --treinar       idem + fine-tune em CPU (limite de relogio) + reavaliacao
"""
import argparse, json, os, random, re, shutil, subprocess, sys, threading, time
from collections import Counter
import os
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]                      # raiz da Governanca (a que contem este script)
DADOS = AQUI / "dados"
LAYA_HOME = Path(os.environ.get("LAYA_HOME", Path.home() / "laya"))
os.environ.setdefault("HF_HOME", str(LAYA_HOME / "hf-cache"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")   # nao baixar nada
os.environ.setdefault("USE_TF", "0")

ARVORES = ["NEGOCIO", "CONTA", "LEITURA", "ESCRITA", "OPERACAO", "CASA", "JURIDICO"]
ACENTO = {"NEGÓCIO": "NEGOCIO", "OPERAÇÃO": "OPERACAO", "JURÍDICO": "JURIDICO"}
LIMITE_TREINO_S = 25 * 60
MODELO_REPO = AQUI / "modelo-arvore"
MODELO_FORA = LAYA_HOME / "modelo-arvore"


# ----------------------------------------------------------------- limpeza
def limpar(t):
    t = re.sub(r"\*\([^)]*\)\*", " ", t)          # notas em italico *(...)*
    t = re.sub(r"\([^)]*\)", " ", t)               # parenteses
    for x in ("**", "`", "🔴", "⭐"):
        t = t.replace(x, "")
    t = re.sub(r"[\"“”]", "", t)
    t = re.sub(r"\s+", " ", t).strip(" .;:—-–*")
    return t


def dividir(celula):
    """Separa frases-sinal por virgula ou ' · ' fora de parenteses."""
    partes, atual, prof, i = [], [], 0, 0
    while i < len(celula):
        c = celula[i]
        if c == "(":
            prof += 1
        elif c == ")":
            prof = max(0, prof - 1)
        if prof == 0 and c == ",":
            partes.append("".join(atual)); atual = []
        elif prof == 0 and celula[i:i + 3] == " · ":
            partes.append("".join(atual)); atual = []; i += 2
        else:
            atual.append(c)
        i += 1
    partes.append("".join(atual))
    return partes


def sinais_do_arquivo(path):
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"^##[^\n]*Linhas[^\n]*\n(.*?)(?=^## |\Z)", txt, re.S | re.M)
    if not m:
        raise SystemExit("sem secao Linhas em %s" % path)
    out = []
    for lin in m.group(1).splitlines():
        if not lin.startswith("|") or lin.startswith("|---") or lin.startswith("| Sinais"):
            continue
        for p in dividir(lin.split("|")[1]):
            f = limpar(p)
            if len(f) >= 4:
                out.append(f)
    return out


def descricoes():
    """Coluna 'O pedido e sobre...' do CLAUDE.md §6, por arvore."""
    txt = (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
    d = {}
    for lin in txt.splitlines():
        m = re.match(r"\| \*\*([A-ZÁÉÍÓÚÃÕÇ]+)\*\* \| (.*?) \| .*? \| `00-core/roteador/ARVORE-", lin)
        if m:
            nome = ACENTO.get(m.group(1), m.group(1))
            if nome in ARVORES:
                d[nome] = re.sub(r"\s+", " ", m.group(2).replace("**", "").replace("`", "")).strip()
    assert set(d) == set(ARVORES), sorted(d)
    return d


# ----------------------------------------------------------------- dataset
def gerar_dados():
    desc = descricoes()
    vistos, linhas = set(), []

    def add(texto, arvore, fonte):
        k = texto.lower()
        if k not in vistos:
            vistos.add(k)
            linhas.append({"texto": texto, "arvore": arvore, "fonte": fonte})

    for a in ARVORES:
        arq = RAIZ / "00-core" / "roteador" / ("ARVORE-%s.md" % a)
        for f in sinais_do_arquivo(arq):
            add(f, a, arq.name)
    for a in ARVORES:  # frases da coluna "O pedido e sobre" (CLAUDE.md §6)
        cel = desc[a].split(":", 1)[1] if ":" in desc[a][:60] else desc[a]
        for p in dividir(cel):
            f = limpar(p)
            if len(f) >= 4:
                add(f, a, "CLAUDE.md §6")
    rng = random.Random(42)
    treino, prova = [], []
    for a in ARVORES:
        g = [l for l in linhas if l["arvore"] == a]
        rng.shuffle(g)
        n_p = max(1, round(len(g) * 0.2))
        prova += g[:n_p]; treino += g[n_p:]
    rng.shuffle(treino); rng.shuffle(prova)
    DADOS.mkdir(exist_ok=True)
    for nome, conj in (("arvore-todos", linhas), ("treino", treino), ("prova", prova)):
        with open(DADOS / (nome + ".jsonl"), "w", encoding="utf-8") as f:
            for l in conj:
                f.write(json.dumps(l, ensure_ascii=False) + "\n")
    cont = {nome: Counter(l["arvore"] for l in conj) for nome, conj in
            (("todos", linhas), ("treino", treino), ("prova", prova))}
    return desc, treino, prova, cont


def pergunta(desc):
    return {"arvore": {"type": "choice",
                       "instructions": "Qual árvore do roteador trata este pedido?",
                       "criteria": {a: desc[a] for a in ARVORES}}}


# ----------------------------------------------------------------- avaliacao
def avaliar_modelo(agent, desc, prova, rotulo):
    q = pergunta(desc)
    qi = {"arvore": dict(q["arvore"], option_order=list(range(len(ARVORES)))[::-1])}
    pred, pred_inv, lat = [], [], []
    for ex in prova:
        t0 = time.perf_counter()
        r = agent.predict(ex["texto"], q)
        lat.append(time.perf_counter() - t0)
        pred.append(r["answers"]["arvore"]["choice"])
        pred_inv.append(agent.predict(ex["texto"], qi)["answers"]["arvore"]["choice"])
    ys = [e["arvore"] for e in prova]
    mat = {y: {p: 0 for p in ARVORES} for y in ARVORES}
    for y, p in zip(ys, pred):
        mat[y][p] += 1
    return {"rotulo": rotulo, "n": len(ys),
            "acuracia": sum(p == y for p, y in zip(pred, ys)) / len(ys),
            "acuracia_ordem_invertida": sum(p == y for p, y in zip(pred_inv, ys)) / len(ys),
            "mudaram_na_inversao": sum(a != b for a, b in zip(pred, pred_inv)),
            "latencia_media_ms": 1000 * sum(lat) / len(lat),
            "matriz": mat,
            "erros": [(e["texto"], e["arvore"], p) for e, p in zip(prova, pred) if e["arvore"] != p]}


def imprimir(m):
    print("\n== %s ==" % m["rotulo"])
    print("n=%d  acuracia=%.3f  acuracia(ordem invertida)=%.3f  mudaram=%d/%d  latencia=%.1f ms"
          % (m["n"], m["acuracia"], m["acuracia_ordem_invertida"], m["mudaram_na_inversao"], m["n"],
             m["latencia_media_ms"]))
    print("real\\prev " + " ".join("%8s" % a[:8] for a in ARVORES))
    for y in ARVORES:
        print("%-9s " % y[:9] + " ".join("%8d" % m["matriz"][y][p] for p in ARVORES))


# ----------------------------------------------------------------- treino
def arquivo_treino_laya(desc, treino):
    q = pergunta(desc)
    p = DADOS / "treino-laya.jsonl"
    with open(p, "w", encoding="utf-8") as f:
        for e in treino:
            f.write(json.dumps({"state": e["texto"], "questions": q,
                                "expected": {"arvore": e["arvore"]}}, ensure_ascii=False) + "\n")
    return str(p)


def treinar(desc, treino, epocas, saida):
    """finetune num subprocesso, com limite de relogio. Retorna (ok, segundos, cauda do log)."""
    dados = arquivo_treino_laya(desc, treino)
    cod = ("import sys;from laya.train import TrainConfig, finetune;"
           "c=TrainConfig(epochs=%d,micro_batch=8,grad_accum=2,seed=42,log_every=5);"
           "s=finetune(sys.argv[1],'multilingual',sys.argv[2],c,device='cpu');print('FIM',s.get('output_dir'))"
           % epocas)
    t0 = time.time()
    p = subprocess.Popen([sys.executable, "-c", cod, dados, str(saida)], stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    buf = []
    th = threading.Thread(target=lambda: [buf.append(l) for l in p.stdout], daemon=True)
    th.start()
    while p.poll() is None and time.time() - t0 < LIMITE_TREINO_S:
        time.sleep(2)
    if p.poll() is None:
        p.kill(); th.join(5)
        return False, time.time() - t0, "INTERROMPIDO no limite de %d s\n%s" % (LIMITE_TREINO_S, "".join(buf)[-3000:])
    th.join(5)
    return p.returncode == 0, time.time() - t0, "".join(buf)[-3000:]


def tamanho_mb(p):
    return sum(f.stat().st_size for f in Path(p).rglob("*") if f.is_file()) / 1e6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--treinar", action="store_true")
    ap.add_argument("--epocas", type=int, default=3)
    a = ap.parse_args()
    desc, treino, prova, cont = gerar_dados()
    print("contagem por arvore:")
    for k in ("todos", "treino", "prova"):
        print(" %-6s total=%d  %s" % (k, sum(cont[k].values()), dict(cont[k])))
    import laya
    res = {"contagem": {k: dict(v) for k, v in cont.items()}}
    ag = laya.load("convaiinnovations/laya", subfolder="multilingual", device="cpu")
    ag.predict("aquecimento", pergunta(desc))
    zs = avaliar_modelo(ag, desc, prova, "zero-shot (multilingual)")
    imprimir(zs); res["zero_shot"] = zs
    if a.treinar:
        saida = Path(os.environ.get("TEMP", ".")) / "modelo-arvore-tmp"
        ok, seg, log = treinar(desc, treino, a.epocas, saida)
        res["treino"] = {"ok": ok, "segundos": seg, "epocas": a.epocas, "log": log}
        print("\ntreino ok=%s em %.0f s" % (ok, seg))
        if not ok:
            print(log)
        else:
            mb = tamanho_mb(saida)
            destino = MODELO_REPO if mb < 500 else MODELO_FORA
            if destino.exists():
                shutil.rmtree(destino)
            shutil.copytree(saida, destino)
            res["treino"].update(tamanho_mb=mb, destino=str(destino))
            print("modelo %.0f MB -> %s" % (mb, destino))
            ag2 = laya.load(str(destino), device="cpu")
            ag2.predict("aquecimento", pergunta(desc))
            tr = avaliar_modelo(ag2, desc, prova, "treinado (%d epocas)" % a.epocas)
            imprimir(tr); res["treinado"] = tr
    with open(DADOS / "resultado.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
