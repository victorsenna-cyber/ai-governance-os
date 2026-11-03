# -*- coding: utf-8 -*-
"""
medir-contexto.py — carga fixa de contexto por sessão, a partir dos arquivos do repo.

Soma o que entra antes do primeiro pedido (CLAUDE.md, 00-core/* sem roteador e _legado,
a memória do Claude Code) e o que cada árvore e o STATUS.md custam quando carregados,
mais as descrições das skills e agentes locais (.claude/skills, .claude/agents), que
entram em toda sessão. Conversão: 1 token ≈ 3,5 caracteres (português).

  python3 medir-contexto.py              → imprime e grava 40-operacao-rotinas/tokens/CARGA-FIXA.md
  python3 medir-contexto.py --teto 60000 → marca ✅/🔴 contra um teto em tokens
"""
import argparse, datetime, glob, io, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CPT = 3.5


def chars(p):
    try:
        return len(io.open(p, encoding="utf-8", errors="replace").read())
    except OSError:
        return 0


def descricao(p):
    t = io.open(p, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---", t, re.S)
    if not m:
        return 0
    d = re.search(r"(?m)^description:\s*(.*)$", m.group(1))
    return len(d.group(1)) if d else 0


def tok(c):
    return int(c / CPT)


def fmt(n):
    return f"{n:,}".replace(",", ".")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--teto", type=int, default=0); a = ap.parse_args()
    linhas = [f"# CARGA FIXA DE CONTEXTO — medida em {datetime.date.today():%d/%m/%Y}", "",
              "> Gerado por `40-operacao-rotinas/ferramentas/medir-contexto.py`. 1 token ≈ 3,5 caracteres. "
              "**Sempre** = entra em toda sessão. **Por árvore** = quando a árvore é carregada. **STATUS** = quando lido.", ""]
    sempre = [("CLAUDE.md", chars(os.path.join(RAIZ, "CLAUDE.md")))]
    for p in sorted(glob.glob(os.path.join(RAIZ, "00-core", "*.md"))):
        sempre.append(("00-core/" + os.path.basename(p), chars(p)))
    mem = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    for p in glob.glob(os.path.join(mem, "*", "memory", "MEMORY.md")):
        if "Governan" in p:
            sempre.append(("memória MEMORY.md (índice)", chars(p)))
    sk = 0; n_sk = 0
    for p in glob.glob(os.path.join(RAIZ, ".claude", "skills", "*", "SKILL.md")):
        sk += descricao(p); n_sk += 1
    ag = 0; n_ag = 0
    for p in glob.glob(os.path.join(RAIZ, ".claude", "agents", "*.md")):
        ag += descricao(p); n_ag += 1
    sempre.append((f".claude/skills — descrições de {n_sk} skills", sk))
    sempre.append((f".claude/agents — descrições de {n_ag} agentes", ag))

    linhas += ["## Sempre (antes do primeiro pedido)", "", "| peça | caracteres | tokens |", "|---|---:|---:|"]
    tot = 0
    for nome, c in sempre:
        tot += c; linhas.append(f"| {nome} | {fmt(c)} | {fmt(tok(c))} |")
    linhas.append(f"| **total sempre** | {fmt(tot)} | **{fmt(tok(tot))}** |")
    if a.teto:
        linhas.append(f"\nTeto: {fmt(a.teto)} tokens → {'✅ abaixo' if tok(tot) <= a.teto else '🔴 ACIMA'} ({fmt(tok(tot))}).")
    linhas += ["", "## Por árvore (uma por pedido)", "", "| árvore | caracteres | tokens | sessão com esta árvore |", "|---|---:|---:|---:|"]
    for p in sorted(glob.glob(os.path.join(RAIZ, "00-core", "roteador", "ARVORE-*.md"))):
        c = chars(p); linhas.append(f"| {os.path.basename(p)} | {fmt(c)} | {fmt(tok(c))} | {fmt(tok(tot + c))} |")
    st = chars(os.path.join(RAIZ, "STATUS.md"))
    linhas += ["", "## STATUS.md (quando lido inteiro)", "", f"- {fmt(st)} caracteres ≈ **{fmt(tok(st))} tokens**; sessão típica (sempre + árvore média + STATUS) ≈ {fmt(tok(tot + st) + 1000)} tokens antes do pedido.", ""]
    txt = "\n".join(linhas)
    os.makedirs(os.path.join(RAIZ, "40-operacao-rotinas", "tokens"), exist_ok=True)
    io.open(os.path.join(RAIZ, "40-operacao-rotinas", "tokens", "CARGA-FIXA.md"), "w", encoding="utf-8").write(txt + "\n")
    sys.stdout.reconfigure(encoding="utf-8"); print(txt)


if __name__ == "__main__":
    main()
