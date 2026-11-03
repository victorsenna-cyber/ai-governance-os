"""Esqueleto da COMPOSICAO-VSL.md a partir de um roteiro do G6.

Uso:  py -I -X utf8 composicao-vsl.py <roteiro G6.md> <saida COMPOSICAO-VSL.md> [<TEMPO-funil-B.md>]

Com a linha do tempo (de tempo-vsl.py), acrescenta a página 3 em esqueleto: "o que cada
elemento faz, e quando", com o tempo de entrada de cada elemento.

Lê os títulos `# BLOCO n · NOME`, `### Dxx · elemento` e `# APÊNDICE`, conta as
palavras de fala de cada elemento (sem marcações [..], marcadores [[..]], linhas
>>> <<<, tabelas e citações) e grava a tabela bloco → elementos → palavras.
A coluna "O que faz" sai com {{...}} para o orquestrador preencher em uma linha,
junto com promessa, mecanismo e pivô. Método: 100-métodos/METODO-PRODUCAO-VSL-POR-AGENTES.md §4.4.
Contagem calibrada contra um roteiro de VSL de referência.
"""
import io
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
texto = io.open(src, encoding="utf-8").read().split("\n# CONTAGEM E DURAÇÃO")[0]


def palavras(trecho):
    total, ponte, em_ponte = 0, 0, False
    for linha in trecho.split("\n"):
        l = linha.strip()
        if l.startswith("[PONTE NOVA]"):
            em_ponte = True
            continue
        if not l or l.startswith(("#", ">>>", "---", "|", ">")):
            if not l:
                em_ponte = False
            continue
        l = re.sub(r"\[\[.*?\]\]", "", l)
        l = re.sub(r"\[[^\]]*\]", "", l)
        n = len([w for w in l.split() if re.search(r"\w", w)])
        if em_ponte:
            ponte += n
        else:
            total += n
    return total, ponte


blocos, atual = [], None
for parte in re.split(r"^(# .*|### .*)$", texto, flags=re.M):
    if parte.startswith("# BLOCO") or parte.startswith("# APÊNDICE"):
        atual = {"nome": parte[2:].strip(), "elementos": [], "ponte": 0}
        blocos.append(atual)
    elif parte.startswith("### ") and atual is not None:
        m = re.match(r"### (D\d+A?) · (.*)", parte)
        if m:
            atual["elementos"].append([m.group(1), m.group(2).strip(), 0])
    elif atual is not None:
        n, p = palavras(parte)
        if atual["elementos"]:
            atual["elementos"][-1][2] += n
        atual["ponte"] += p

L = ["# Composição da VSL · {{produto}}", "",
     f"> Roteiro: `{src}` · estrutura-base: {{{{referência escalada}}}} · gerado por `40-operacao-rotinas/ferramentas/composicao-vsl.py`", "",
     "**Promessa:** {{uma frase}}", "**Mecanismo:** {{uma frase}} · **Apelido:** {{nome}}",
     "**Pivô (E · Mas · Por isso):** {{uma frase}} · ponto da virada: {{elemento}}", "",
     "| # | Elemento | O que faz | Palavras |", "|---|---|---|---:|"]
total_b = 0
for i, b in enumerate(blocos, 1):
    soma = sum(e[2] for e in b["elementos"]) + b["ponte"]
    rot = "A" if b["nome"].startswith("APÊNDICE") else str(i)
    if rot != "A":
        total_b += soma
    L.append(f"| **{rot}** | **{b['nome'].split('·', 1)[-1].strip()}** | | **{soma:,}** |".replace(",", "."))
    for cod, nome, n in b["elementos"]:
        L.append(f"| {cod} | {nome} | {{{{o que faz}}}} | {n} |")
    if b["ponte"]:
        L.append(f"| — | ponte | {{{{texto da ponte}}}} | {b['ponte']} |")
L += ["", f"**Total (sem apêndice):** {total_b:,} palavras ≈ {total_b / 170:.1f} min a 170/min".replace(",", "."), "",
      "**Fora desta versão:** {{...}} · **Desvios de dose declarados:** {{...}} · **Estado:** {{grava? mídia?}}"]
if len(sys.argv) > 3:
    inicio = {}
    for linha in io.open(sys.argv[3], encoding="utf-8"):
        mm = re.match(r"\| (\d\d:\d\d) \| (\S+) ", linha)
        if mm and mm.group(2) not in inicio:
            inicio[mm.group(2)] = mm.group(1)
    L += ["", '<div style="page-break-before: always"></div>', "", "## O que cada elemento faz, e quando", "",
          "> O que quem ouve passa a **saber, sentir ou decidir**, e em que segundo. Contra a linha do tempo de compreensão da referência.", "",
          "| Tempo | Elemento | O que o ouvinte passa a ter |", "|---|---|---|"]
    L += [f"| {t} | {e} | {{{{o que o ouvinte passa a ter}}}} |" for e, t in inicio.items() if e != "ponte"]
    L += ["", "**Contra a referência:** {{marco a marco}}"]
io.open(dst, "w", encoding="utf-8", newline="").write("\n".join(L) + "\n")
print(f"ok · {len(blocos)} blocos · {sum(len(b['elementos']) for b in blocos)} elementos · {total_b} palavras")
