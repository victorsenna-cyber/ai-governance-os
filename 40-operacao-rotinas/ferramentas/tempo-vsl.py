"""Linha do tempo falada de um roteiro de VSL do G6: cada frase com o segundo em que começa.

Uso:  py -I -X utf8 tempo-vsl.py <roteiro G6.md> <saida TEMPO.md> [--funil a] [--ppm 170]

Lê só a fala (sem [marcações], [[marcadores]], >>> <<<, tabelas, citações e títulos),
na ordem em que o espectador ouve. Funil B: D01 a D36. Funil A: o apêndice (D01A–D04A)
no lugar de D01–D04. Grava uma tabela `tempo · elemento · frase`, que o auditor de
compreensão (A7, `METODO-PRODUCAO-VSL-POR-AGENTES.md` §2) usa para medir em que segundo
cada coisa fica clara para quem ouve. Contagem igual à do `composicao-vsl.py`.
"""
import io
import re
import sys

args = sys.argv[1:]
src, dst = args[0], args[1]
funil_a = "--funil" in args and args[args.index("--funil") + 1].lower() == "a"
ppm = float(args[args.index("--ppm") + 1]) if "--ppm" in args else 170.0

texto = io.open(src, encoding="utf-8").read().split("\n# CONTAGEM E DURAÇÃO")[0]
partes = re.split(r"^(# .*|### .*)$", texto, flags=re.M)

elementos, atual, bloco, no_bloco = [], None, "", False
for p in partes:
    if p.startswith("# BLOCO") or p.startswith("# APÊNDICE"):
        bloco, no_bloco, atual = p[2:].strip(), True, None
    elif p.startswith("### ") and no_bloco:
        m = re.match(r"### (D\d+A?) · (.*)", p)
        atual = [m.group(1), m.group(2).strip(), bloco, ""] if m else None
        if atual:
            elementos.append(atual)
    elif no_bloco:
        if atual is not None:
            atual[3] += p
        elif "[PONTE NOVA]" in p:
            elementos.append(["ponte", "ponte", bloco, p])

def fala(t):
    linhas = []
    for linha in t.split("\n"):
        l = linha.strip()
        if not l or l.startswith(("#", ">>>", "---", "|", ">")):
            continue
        l = re.sub(r"\[\[.*?\]\]", "", l)
        l = re.sub(r"\[[^\]]*\]", " ", l)
        l = re.sub(r"\s+", " ", l).strip()
        if l and re.search(r"\w", l):
            linhas.append(l)
    return " ".join(linhas)

principais = [e for e in elementos if not e[0].endswith("A")]
apendice = [e for e in elementos if e[0].endswith("A")]
if funil_a:
    ordem = apendice + [e for e in principais if e[0] == "ponte" or int(e[0][1:]) > 4]
else:
    ordem = principais

L = [f"# Linha do tempo falada · {'funil A' if funil_a else 'funil B'} · {ppm:.0f} palavras/min",
     "", f"> Fonte: `{src}` · gerado por `40-operacao-rotinas/ferramentas/tempo-vsl.py`.", "",
     "| Tempo | Elemento | Frase |", "|---|---|---|"]
palavras = 0
for cod, nome, bloco, corpo in ordem:
    for frase in re.split(r"(?<=[.!?…])\s+", fala(corpo)):
        n = len([w for w in frase.split() if re.search(r"\w", w)])
        if not n:
            continue
        s = int(palavras / ppm * 60)
        L.append(f"| {s // 60:02d}:{s % 60:02d} | {cod} {nome} | {frase} |")
        palavras += n
s = int(palavras / ppm * 60)
L += ["", f"**Total:** {palavras} palavras · {s // 60:02d}:{s % 60:02d}"]
io.open(dst, "w", encoding="utf-8", newline="").write("\n".join(L) + "\n")
print(f"ok · {palavras} palavras · {s // 60:02d}:{s % 60:02d}")
