#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rascunhos_do_painel.py — o rascunho que o operador escreve na aba Entregáveis do sistema chega ao repo.

Pedido de origem: uma tela só para os entregáveis da conta, em projetos, onde o operador adiciona rascunhos e vê o
progresso de cada entregável.

  python3 rascunhos_do_painel.py             # uma rodada: leva ao repo o que está pendente no Supabase e carimba
  python3 rascunhos_do_painel.py --estado    # os rascunhos pendentes, sem mexer em nada
  python3 rascunhos_do_painel.py --dry-run   # mostra o que faria, sem gravar nem carimbar
  python3 rascunhos_do_painel.py --testar    # roda os casos num repo de mentira (sem Supabase)

Caminho: aba Entregáveis → adicionar_rascunho() → public.entregaveis_rascunhos (013-rascunhos.sql) → AQUI, na VPS, a cada
passada do contexto.service (chamado pelo decisoes-do-painel.py): rascunhos_pendentes(token) →
  · com task: o texto, literal, vai para RASCUNHOS.md na pasta do entregável (a de `saida:`), a task ganha a linha em
    `insumos:` e no Log. Se ela estava pronta em revisao/, VOLTA para fila/ (estado pronta): material novo do operador
    sobre peça pronta é peça para refazer, e a esteira da nuvem a pega na próxima rodada. Em entregue/, só registra.
  · sem task: entregável novo pelo entregaveis.py (molde, id, pasta), com o rascunho como insumo e fonte "o operador, painel".
→ rascunhos_marcar(token). Quem publica é o decisoes-do-painel.py (sincronizar.py), na mesma passada.
"""
import argparse, contextlib, datetime, importlib.util, io, os, re, shutil, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BRT = datetime.timezone(datetime.timedelta(hours=-3))
ESTADOS = ("fila", "executando", "revisao", "decisao", "entregue", "falhou")


def _mod(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, AQUI / arquivo)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ent = _mod("entregaveis", "entregaveis.py")          # molde, id, pasta da conta, slug — a esteira é a fonte


def agora():
    return datetime.datetime.now(BRT)


def quando(iso_ts):
    try:
        return datetime.datetime.fromisoformat(str(iso_ts).replace("Z", "+00:00")).astimezone(BRT).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return agora().strftime("%d/%m/%Y %H:%M")


def achar_task(tid):
    for p in ESTADOS:
        f = Path(ent.TAR) / p / f"{tid}.md"
        if f.exists():
            return f, p
    return None, None


def campo(txt, nome):
    m = re.search(rf"^{nome}:[ \t]*(.*)$", txt, re.M)
    return m.group(1).strip() if m else ""


def por_campo(txt, nome, valor):
    if re.search(rf"^{nome}:", txt, re.M):
        return re.sub(rf"^{nome}:[ \t]*.*$", f"{nome}: {valor}", txt, count=1, flags=re.M)
    return re.sub(r"^---\n", f"---\n{nome}: {valor}\n", txt, count=1)


def no_log(txt, linha):
    if re.search(r"^## Log\s*$", txt, re.M):
        return re.sub(r"(^## Log\s*\n)", lambda m: m.group(1) + linha + "\n", txt, count=1, flags=re.M)
    return txt.rstrip("\n") + "\n\n## Log\n" + linha + "\n"


def gravar_rascunho(pasta_rel, r):
    """Acrescenta o rascunho, literal, ao RASCUNHOS.md da pasta do entregável. Nunca reescreve o que já está lá."""
    pasta = Path(ent.RAIZ) / pasta_rel
    pasta.mkdir(parents=True, exist_ok=True)
    arq = pasta / "RASCUNHOS.md"
    novo = not arq.exists()
    with io.open(arq, "a", encoding="utf-8", newline="\n") as f:
        if novo:
            f.write("# Rascunhos do operador\n\n> Escritos na aba Entregáveis do sistema e trazidos ao repo pelo "
                    "`rascunhos_do_painel.py`. Texto literal, o mais novo embaixo. É insumo da produção: a peça incorpora "
                    "ou explica por escrito por que não.\n")
        f.write(f"\n## {quando(r.get('criado_em'))} · rascunho R-{r['id']}"
                + (f" · {r['titulo']}" if r.get("titulo") else "") + "\n\n" + r["texto"].rstrip() + "\n")
    return (Path(pasta_rel) / "RASCUNHOS.md").as_posix()


def aplicar_em_task(r, dry=False):
    f, onde = achar_task(r["task_id"])
    if not f:
        raise ValueError(f"task {r['task_id']} não existe em tarefas/")
    txt = f.read_text(encoding="utf-8")
    if campo(txt, "tipo") != "entregavel":
        raise ValueError(f"task {r['task_id']} não é entregável")
    if ent.nfc(campo(txt, "conta")) != ent.nfc(r["conta"]):
        raise ValueError(f"task {r['task_id']} é da conta '{campo(txt, 'conta')}', não de '{r['conta']}'")
    saida = campo(txt, "saida")
    pasta_rel = Path(saida).parent.as_posix() if saida else ""
    if not pasta_rel or pasta_rel == ".":
        raise ValueError(f"task {r['task_id']} sem saida: — não sei a pasta do entregável")
    volta = onde == "revisao"
    if dry:
        return f"{r['task_id']} ({onde}/) ← R-{r['id']} em {pasta_rel}/RASCUNHOS.md" + (" · volta para fila/" if volta else "")
    rel = gravar_rascunho(pasta_rel, r)
    ins = campo(txt, "insumos")
    if rel not in ins:
        txt = por_campo(txt, "insumos", (ins + ", " if ins else "") + rel)
    linha = f"- {agora().strftime('%d/%m %H:%M')} · rascunho R-{r['id']} do operador pelo sistema → `{rel}`"
    if volta:
        txt = por_campo(txt, "estado", "pronta")
        txt = por_campo(txt, "pronto_em", "")
        linha += " · estava pronta: volta para fila/ para incorporar"
    txt = no_log(txt, linha)
    destino = f.parent.parent / "fila" / f.name if volta else f
    io.open(destino, "w", encoding="utf-8", newline="\n").write(txt)
    if volta:
        f.unlink()
    return None


def criar_entregavel(r, dry=False):
    base, pc = ent.pasta_conta(r["conta"])
    if not pc:
        raise ValueError(f"conta '{r['conta']}' não existe em clientes/ nem parceiros/")
    titulo = (r.get("titulo") or "").strip()
    pasta_rel = f"{base}/{ent.nfc(r['conta'])}/entregaveis/{ent.hoje().isoformat()} - {ent.slug(titulo)}"
    rasc_rel = pasta_rel + "/RASCUNHOS.md"
    if dry:
        return f"novo: '{titulo}' em {pasta_rel}/ ← R-{r['id']}"
    a = argparse.Namespace(
        fonte=f"o operador, sistema (aba Entregáveis), {quando(r.get('criado_em'))}: rascunho R-{r['id']}",
        forma="documento", conta=r["conta"], prometido_em=None, prometido_para=r.get("prazo"), nome=titulo,
        o_que=titulo, prazo_duro=False, arvore="ESCRITA", insumos=rasc_rel, destinatario="", dinheiro=False,
        estado_inicial="fila", dry_run=False)
    saida = io.StringIO()
    try:
        with contextlib.redirect_stdout(saida):
            ent.nova(a)
    except SystemExit as e:
        raise ValueError(str(e.code))
    m = re.search(r"T-\d{4}-\d{2}-\d{2}-\d{3}", saida.getvalue())
    if not m:
        raise ValueError("entregaveis.py não devolveu o id: " + saida.getvalue().strip()[:200])
    gravar_rascunho(pasta_rel, r)
    gk = Path(ent.RAIZ) / pasta_rel / ".gitkeep"
    if gk.exists():
        gk.unlink()
    return m.group(0)


def aplicar(lista, dry=False):
    """Devolve [(id, task_criada, erro)] e se o repo mudou."""
    out, mudou = [], False
    for r in lista:
        try:
            if r.get("task_id"):
                info = aplicar_em_task(r, dry)
                out.append((r["id"], None, None, info))
            else:
                tid = criar_entregavel(r, dry)
                out.append((r["id"], None if dry else tid, None, tid if dry else f"novo {tid}"))
            mudou = mudou or not dry
        except Exception as e:  # noqa: BLE001
            out.append((r["id"], None, f"{type(e).__name__}: {e}"[:500], None))
    return out, mudou


def rodar(tk, dry=False, so_estado=False):
    mdp = _mod("mensagens_do_painel", "mensagens_do_painel.py")
    pend = mdp.rpc("rascunhos_pendentes", {"token": tk}) or []
    if so_estado or not pend:
        for r in pend:
            print(f"R-{r['id']} · {r['conta']} · {r.get('task_id') or 'novo: ' + (r.get('titulo') or '?')} · {quando(r.get('criado_em'))}")
        return len(pend), False
    res, mudou = aplicar(pend, dry)
    for rid, tid, erro, info in res:
        print(f"{'🔴' if erro else '✅'} R-{rid}: {erro or info or tid or ''}")
        if not dry:
            mdp.rpc("rascunhos_marcar", {"token": tk, "p_id": rid, "p_task_criada": tid, "p_sha": None, "p_erro": erro})
    return len(res), mudou


# ---------- teste num repo de mentira ----------
def testar():
    tmp = Path(tempfile.mkdtemp(prefix="rasc-"))
    try:
        (tmp / "clientes" / "Conta Teste").mkdir(parents=True)
        for p in ESTADOS + ("modelos",):
            (tmp / "40-operacao-rotinas" / "tarefas" / p).mkdir(parents=True)
        shutil.copy(ent.MOLDE, tmp / "40-operacao-rotinas" / "tarefas" / "modelos" / "entregavel.md")
        ent.RAIZ, ent.TAR = str(tmp), str(tmp / "40-operacao-rotinas" / "tarefas")
        ent.MOLDE = os.path.join(ent.TAR, "modelos", "entregavel.md")
        ok = 0
        # 1. entregável novo
        r1 = {"id": 1, "conta": "Conta Teste", "task_id": None, "titulo": "Plano de teste", "texto": "linha 1\nlinha 2",
              "prazo": None, "criado_em": "2026-11-10T20:00:00Z"}
        res, _ = aplicar([r1])
        tid = res[0][1]
        assert tid and not res[0][2], res
        t = next(Path(ent.TAR, "fila").glob(f"{tid}.md")).read_text(encoding="utf-8")
        assert "RASCUNHOS.md" in campo(t, "insumos"), campo(t, "insumos")
        rasc = next((tmp / "clientes" / "Conta Teste" / "entregaveis").glob("*/RASCUNHOS.md")).read_text(encoding="utf-8")
        assert "linha 2" in rasc and "R-1" in rasc
        ok += 1
        # 2. rascunho em task pronta (revisao) → volta para fila, acrescenta sem apagar
        f = Path(ent.TAR, "fila", f"{tid}.md")
        f.rename(Path(ent.TAR, "revisao", f.name))
        p = Path(ent.TAR, "revisao", f.name)
        p.write_text(por_campo(p.read_text(encoding="utf-8"), "estado", "pronto"), encoding="utf-8")
        r2 = dict(r1, id=2, task_id=tid, titulo=None, texto="ajuste do operador")
        res, _ = aplicar([r2])
        assert not res[0][2], res
        assert Path(ent.TAR, "fila", f"{tid}.md").exists() and not p.exists()
        t = Path(ent.TAR, "fila", f"{tid}.md").read_text(encoding="utf-8")
        assert campo(t, "estado") == "pronta" and "R-2" in t
        rasc = next((tmp / "clientes" / "Conta Teste" / "entregaveis").glob("*/RASCUNHOS.md")).read_text(encoding="utf-8")
        assert "linha 2" in rasc and "ajuste do operador" in rasc
        assert campo(t, "insumos").count("RASCUNHOS.md") == 1
        ok += 1
        # 3. task de outra conta → erro, nada muda
        res, _ = aplicar([dict(r2, id=3, conta="Outra")])
        assert res[0][2] and "conta" in res[0][2], res
        ok += 1
        # 4. task que não existe → erro
        res, _ = aplicar([dict(r2, id=4, task_id="T-2026-01-01-999")])
        assert res[0][2] and "não existe" in res[0][2], res
        ok += 1
        # 5. conta que não existe → erro, nenhuma task criada
        antes = len(list(Path(ent.TAR, "fila").glob("*.md")))
        res, _ = aplicar([dict(r1, id=5, conta="Ninguém")])
        assert res[0][2] and len(list(Path(ent.TAR, "fila").glob("*.md"))) == antes
        ok += 1
        print(f"✅ {ok}/5 casos")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--testar", action="store_true")
    a = ap.parse_args()
    if a.testar:
        return testar()
    mdp = _mod("mensagens_do_painel", "mensagens_do_painel.py")
    tk = mdp.token()
    if not tk:
        sys.exit("sem token (DECISOES_TOKEN, /srv/ordens/.env ou ~/.continuum/decisoes-token.txt)")
    rodar(tk, dry=a.dry_run, so_estado=a.estado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
