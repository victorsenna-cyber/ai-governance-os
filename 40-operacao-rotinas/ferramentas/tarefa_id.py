#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tarefa_id.py — o gerador único de id de task (T-AAAA-MM-DD-NNN), igual no PC, na VPS e na nuvem.

Por quê: duas tasks ganharam o mesmo id no mesmo minuto, uma aberta no PC e outra por um serviço na VPS. Cada gerador
contava só os arquivos da própria máquina; as duas se mesclaram na main com o mesmo id.

Como não repete:
  1. FAIXA POR ORIGEM no NNN (o formato que as réguas e o painel leem não muda):
       pc 001–499 · vps 500–799 · nuvem 800–999
     Duas máquinas diferentes nunca disputam o mesmo número, mesmo sem se verem.
  2. Dentro da faixa, o próximo é o maior já usado + 1, olhando as pastas-estado locais E a origin/main já buscada
     (`git ls-tree`, só leitura; sem rede, sem mudar estado) — pega o que outra sessão da mesma origem já publicou.
  3. RESERVA atômica (O_EXCL) em ~/.cache/continuum-tarefa-id/<dia>/ — dois processos na mesma máquina, no mesmo
     segundo (ordens.service e contexto.service dividem o clone na VPS), não pegam o mesmo número.
  O dia é o de Brasília (UTC-3) em toda máquina: a VPS roda em UTC e, sem isso, abriria a task no dia seguinte.

Origem: CONTINUUM_ORIGEM=pc|vps|nuvem manda; senão CLAUDE_CODE_REMOTE → nuvem; Linux com /srv/ordens ou clone em /srv → vps;
outro Linux → nuvem; Windows → pc.

Uso:
  from tarefa_id import proximo           # proximo() → "T-2026-11-13-007"
  python3 tarefa_id.py                         # imprime o próximo id (quem abre task à mão ou pelo modelo usa isto)
  python3 tarefa_id.py --origem vps --dia 2026-11-13
  python3 tarefa_id.py --duplicados            # lista id repetido entre as pastas-estado (o verificar-propagacao.py reprova)
  python3 tarefa_id.py --teste                 # teste de colisão: duas máquinas, mesmo minuto, mesmo repo visto
"""
import argparse
import datetime
import io
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
TAREFAS = os.path.normpath(os.path.join(AQUI, "..", "tarefas"))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
BRT = datetime.timezone(datetime.timedelta(hours=-3))
FAIXAS = {"pc": (1, 499), "vps": (500, 799), "nuvem": (800, 999)}
PASTAS_ESTADO = ("fila", "executando", "revisao", "decisao", "entregue", "falhou")
RE_ID = re.compile(r"^(T-\d{4}-\d{2}-\d{2})-(\d{3})\.md$", re.I)


def hoje():
    return datetime.datetime.now(BRT).date().isoformat()


def origem_atual():
    o = (os.environ.get("CONTINUUM_ORIGEM") or "").strip().lower()
    if o in FAIXAS:
        return o
    if (os.environ.get("CLAUDE_CODE_REMOTE") or "").strip().lower() in ("1", "true", "sim", "yes"):
        return "nuvem"
    if os.name == "nt":
        return "pc"
    if os.path.exists("/srv/ordens") or AQUI.startswith("/srv/"):
        return "vps"
    return "nuvem"


def _numeros_locais(tarefas, dia):
    nums = set()
    if not os.path.isdir(tarefas):
        return nums
    for p in os.listdir(tarefas):
        pd = os.path.join(tarefas, p)
        if p == "modelos" or not os.path.isdir(pd):
            continue
        for x in os.listdir(pd):
            m = RE_ID.match(x)
            if m and m.group(1) == "T-" + dia:
                nums.add(int(m.group(2)))
    return nums


def _numeros_origin_main(tarefas, dia):
    """Só leitura: o que a origin/main (já buscada) tem para o dia. Sem git ou sem ref, devolve vazio."""
    try:
        r = subprocess.run(["git", "ls-tree", "-r", "--name-only", "origin/main", "--", "."], cwd=tarefas,
                           capture_output=True, text=True, timeout=15, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            return set()
    except Exception:
        return set()
    nums = set()
    for linha in r.stdout.splitlines():
        m = RE_ID.match(os.path.basename(linha.strip()))
        if m and m.group(1) == "T-" + dia:
            nums.add(int(m.group(2)))
    return nums


def _dir_reservas(dia, base=None):
    base = base or os.environ.get("CONTINUUM_ID_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "continuum-tarefa-id")
    try:
        os.makedirs(base, exist_ok=True)
    except Exception:
        base = os.path.join(tempfile.gettempdir(), "continuum-tarefa-id")
        os.makedirs(base, exist_ok=True)
    try:  # limpa dias velhos (reserva só serve no dia)
        for d in os.listdir(base):
            if re.match(r"^\d{4}-\d{2}-\d{2}$", d) and d < dia:
                pd = os.path.join(base, d)
                for x in os.listdir(pd):
                    os.remove(os.path.join(pd, x))
                os.rmdir(pd)
    except Exception:
        pass
    pd = os.path.join(base, dia)
    os.makedirs(pd, exist_ok=True)
    return pd


def proximo(dia=None, tarefas=None, origem=None, olhar_origin=True, cache=None):
    """O próximo id livre para `dia` (AAAA-MM-DD, Brasília por padrão) na faixa da origem, já reservado."""
    dia = dia or hoje()
    tarefas = tarefas or TAREFAS
    origem = origem or origem_atual()
    lo, hi = FAIXAS[origem]
    usados = _numeros_locais(tarefas, dia)
    if olhar_origin:
        usados |= _numeros_origin_main(tarefas, dia)
    res = _dir_reservas(dia, cache)
    usados |= {int(x) for x in os.listdir(res) if x.isdigit()}
    na_faixa = [n for n in usados if lo <= n <= hi]
    n = max(na_faixa) + 1 if na_faixa else lo
    while n <= hi:
        try:
            fd = os.open(os.path.join(res, "%03d" % n), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, origem.encode())
            os.close(fd)
            return "T-%s-%03d" % (dia, n)
        except FileExistsError:
            n += 1
    raise RuntimeError("faixa %s (%03d–%03d) esgotada em %s" % (origem, lo, hi, dia))


# ---------- conferência: id repetido entre as pastas-estado ----------
def _campo(caminho, chave):
    try:
        cab = io.open(caminho, encoding="utf-8", errors="replace").read(3000)
    except Exception:
        return ""
    m = re.search(r"(?m)^%s:[ \t]*(.*)$" % re.escape(chave), cab)
    return m.group(1).strip() if m else ""


def duplicados(tarefas=None):
    """{id: [(pasta, titulo, recorrencia)]} só dos ids repetidos que NÃO são a mesma task recorrente
    (a recorrente fica em entregue/ ou falhou/ e renasce em fila/ com o mesmo id — despachar.py recorrer())."""
    tarefas = tarefas or TAREFAS
    vistos = {}
    for p in PASTAS_ESTADO:
        pd = os.path.join(tarefas, p)
        if not os.path.isdir(pd):
            continue
        for x in os.listdir(pd):
            m = RE_ID.match(x)
            if m:
                c = os.path.join(pd, x)
                vistos.setdefault(x[:-3].upper(), []).append((p, _campo(c, "titulo"), _campo(c, "recorrencia")))
    ruins = {}
    for tid, ocs in vistos.items():
        if len(ocs) < 2:
            continue
        titulos = {o[1] for o in ocs}
        recorrente = any(o[2] for o in ocs)
        if len(titulos) == 1 and recorrente:
            continue
        ruins[tid] = ocs
    return ruins


def conferir(raiz=None):
    """(ok, linhas) para o verificar-propagacao.py."""
    tarefas = os.path.join(raiz, "40-operacao-rotinas", "tarefas") if raiz else TAREFAS
    ruins = duplicados(tarefas)
    if not ruins:
        return True, ["✅ nenhum id de task repetido entre as pastas-estado"]
    linhas = []
    for tid, ocs in sorted(ruins.items()):
        linhas.append("🔴 %s em %d arquivos: %s — renumere um com `python3 tarefa_id.py` (e troque o id: e as citações)"
                      % (tid, len(ocs), " × ".join("%s/ «%s»" % (o[0], o[1][:60]) for o in ocs)))
    return False, linhas


# ---------- teste de colisão ----------
def teste():
    import shutil
    import threading
    base = tempfile.mkdtemp(prefix="tarefa-id-teste-")
    falhou = []
    try:
        dia = "2026-11-12"
        # o repo que as duas máquinas veem no mesmo minuto: ...-019 já existe dos dois lados
        for maquina in ("pc", "vps"):
            for p in PASTAS_ESTADO:
                os.makedirs(os.path.join(base, maquina, "tarefas", p))
            io.open(os.path.join(base, maquina, "tarefas", "fila", "T-%s-019.md" % dia), "w").write("titulo: x\n")
        a = proximo(dia, os.path.join(base, "pc", "tarefas"), "pc", False, os.path.join(base, "cache-pc"))
        b = proximo(dia, os.path.join(base, "vps", "tarefas"), "vps", False, os.path.join(base, "cache-vps"))
        c = proximo(dia, os.path.join(base, "vps", "tarefas"), "nuvem", False, os.path.join(base, "cache-nuvem"))
        print("pc → %s · vps → %s · nuvem → %s" % (a, b, c))
        if len({a, b, c}) != 3:
            falhou.append("duas máquinas no mesmo minuto deram o mesmo id")
        if not (a.endswith("-020") and b.endswith("-500") and c.endswith("-800")):
            falhou.append("faixa errada")
        # mesma máquina, oito processos ao mesmo tempo, sem gravar o arquivo da task
        saida, trava = [], threading.Lock()

        def um():
            t = proximo(dia, os.path.join(base, "vps", "tarefas"), "vps", False, os.path.join(base, "cache-vps"))
            with trava:
                saida.append(t)
        th = [threading.Thread(target=um) for _ in range(8)]
        [t.start() for t in th]
        [t.join() for t in th]
        if len(set(saida)) != 8 or b in saida:
            falhou.append("mesma máquina, concorrência: %s" % saida)
        # a conferência: colisão reprova, recorrente não
        tar = os.path.join(base, "pc", "tarefas")
        io.open(os.path.join(tar, "revisao", "T-%s-019.md" % dia), "w").write("titulo: outra\n")
        io.open(os.path.join(tar, "entregue", "T-%s-005.md" % dia), "w").write("titulo: diaria\nrecorrencia: diaria\n")
        io.open(os.path.join(tar, "fila", "T-%s-005.md" % dia), "w").write("titulo: diaria\nrecorrencia: diaria\n")
        d = duplicados(tar)
        if set(d) != {"T-%s-019" % dia}:
            falhou.append("conferência errada: %s" % sorted(d))
    finally:
        shutil.rmtree(base, ignore_errors=True)
    print("✅ teste de colisão passou" if not falhou else "🔴 " + " · ".join(falhou))
    return not falhou


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="gerador único de id de task")
    ap.add_argument("--origem", choices=sorted(FAIXAS))
    ap.add_argument("--dia")
    ap.add_argument("--duplicados", action="store_true")
    ap.add_argument("--teste", action="store_true")
    a = ap.parse_args()
    if a.teste:
        sys.exit(0 if teste() else 1)
    if a.duplicados:
        ok, linhas = conferir()
        print("\n".join(linhas))
        sys.exit(0 if ok else 1)
    print(proximo(a.dia, origem=a.origem))


if __name__ == "__main__":
    main()
