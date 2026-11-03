#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar-propagacao.py — a REGRA Nº 1 do CLAUDE.md §8, mecanizada.

Tipo: gate (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Alçada {{OPERADOR}} · inclui a guarda G5 (roteador em árvores)

Por que existe: a propagação de método novo, feita à mão, depende de atos
lembrados de memória, e ato que depende de memória pode ser pulado sem que
ninguém perceba. Checklist que depende de lembrar não é checklist.

Confere, para cada artefato de 100-métodos/:
  Tipo: válido · ALCANCE (está em alguma árvore ou no nível 1) · §7 mapa ·
  veto na tabela do gate de congruência · menção no STATUS
E, no roteador em árvores (G5):
  as 7 árvores existem e estão no nível 1 · cada árvore tem os 6 lugares do
  PROCESSO · sinais repetidos entre árvores (aviso, não falha: o desempate resolve)
E a sincronia do AGENTS.md.

Uso:  python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py
Sai com código 1 se houver falha. Não altera nenhum arquivo.
"""
import io, os, re, sys, time
from collections import defaultdict

# console do Windows em cp1252 quebrava no "→" e saía com 1 sem veredito
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def ler(rel):
    with io.open(os.path.join(RAIZ, rel), encoding="utf-8") as f:
        return f.read()
def trecho(texto, inicio, fim):
    i = texto.find(inicio)
    if i < 0: return ""
    j = texto.find(fim, i + len(inicio))
    return texto[i:] if j < 0 else texto[i:j]

VOCAB = ("framework", "método", "metodo", "política", "politica", "gate",
         "trilho", "blueprint", "registro", "ponteiro", "índice", "indice")
PREFIXO_REGISTRO = ("AUDITORIA-", "VERIFICACAO-", "PROMOCAO-")
ARVORES = ["NEGOCIO", "CONTA", "LEITURA", "ESCRITA", "OPERACAO", "CASA", "JURIDICO"]
SLOTS = ["framework", "trilho", "método", "blueprint", "política", "gate"]

claude = ler("CLAUDE.md"); agents = ler("AGENTS.md"); status = ler("STATUS.md")
gate = ler("100-métodos/METODO-GATE-DE-CONGRUENCIA.md")
s6 = trecho(claude, "## 6. ROTEADOR", "## 7. MAPA")
s7 = trecho(claude, "## 7. MAPA", "## 8. REGRAS")
s3 = trecho(gate, "## 3.", "## 4.")

falhas = 0
avisos = []

# --- árvores (G5) ---
arv_txt = {}
linhas_arv = []
for a in ARVORES:
    p = "00-core/roteador/ARVORE-%s.md" % a
    existe = os.path.exists(os.path.join(RAIZ, p))
    no_n1 = ("ARVORE-%s.md" % a) in s6
    txt = ler(p) if existe else ""
    arv_txt[a] = txt
    proc = trecho(txt, "## 2.", "## 3.")
    faltam = [s for s in SLOTS if ("| **%s** |" % s) not in proc]
    ok = existe and no_n1 and not faltam
    falhas += 0 if ok else 1
    linhas_arv.append((a, "ok" if existe else "FALTA", "ok" if no_n1 else "FALTA",
                       "ok" if not faltam else "FALTA: " + ", ".join(faltam)))

# sinais repetidos entre árvores (aviso)
onde = defaultdict(set)
for a, txt in arv_txt.items():
    tab = trecho(txt, "## 3.", "## 4.")
    for l in tab.split("\n"):
        if not l.startswith("| ") or l.startswith("| Sinais") or l.startswith("|---"):
            continue
        cel = l.split("|")[1]
        for termo in re.split(r",|·", cel):
            t = re.sub(r"[*\"“”()]", "", termo).strip().lower()
            if len(t) >= 4:
                onde[t].add(a)
colisoes = sorted((t, sorted(v)) for t, v in onde.items() if len(v) > 1)

todas_arvores = "\n".join(arv_txt.values())

# --- artefatos de 100-métodos ---
linhas = []
pasta = os.path.join(RAIZ, "100-métodos")
for nome in sorted(os.listdir(pasta)):
    if not nome.endswith(".md"): continue
    base = nome[:-3]
    txt = ler("100-métodos/" + nome)
    primeira = txt.lstrip().split("\n", 1)[0]
    m = re.search(r"^> \*\*Tipo:\*\*\s*(.+)$", txt, re.M)
    tipo_ok = bool(m) and m.group(1).strip().lower().startswith(VOCAB)
    if primeira.startswith("# PONTEIRO"): classe = "ponteiro"
    elif base.startswith(PREFIXO_REGISTRO): classe = "registro"
    else: classe = "conhecimento"
    f = lambda b: "ok" if b else "FALTA"
    if classe != "conhecimento":
        falhas += 0 if tipo_ok else 1
        linhas.append((base, classe, f(tipo_ok), "—", "—", "—", "—")); continue
    alcance = base in s6 or base in todas_arvores
    em7 = base in s7
    veto = base in s3 or base == "METODO-GATE-DE-CONGRUENCIA"  # o gate não veta a si mesmo
    emst = base in status
    ok = tipo_ok and alcance and em7 and veto and emst
    falhas += 0 if ok else 1
    linhas.append((base, classe, f(tipo_ok), f(alcance), f(em7), f(veto), f(emst)))

# --- AGENTS ---
# AGENTS.md é réplica do kernel, para quem opera com Codex ou GPT como principal: o corpo é o do CLAUDE.md.
corpo_c = claude[claude.find("## 1. PAPEL"):].replace("este `CLAUDE.md`", "este `AGENTS.md`").strip()
corpo_a = agents[agents.find("## 1. PAPEL"):].strip()
agents_ok = corpo_c == corpo_a
falhas += 0 if agents_ok else 1

limite = time.time() - 8 * 86400
recentes = sum(1 for p in ("100-métodos", "00-core", "90-templates")
               for dp, _, fs in os.walk(os.path.join(RAIZ, p))
               for x in fs if x.endswith(".md") and os.path.getmtime(os.path.join(dp, x)) >= limite)

print("# VERIFICAÇÃO DE PROPAGAÇÃO —", time.strftime("%d/%m/%Y %H:%M"))
print("\n## Roteador em árvores (G5)\n")
print("| Árvore | arquivo | no nível 1 (§6) | 6 lugares do processo |")
print("|---|---|---|---|")
for l in linhas_arv: print("| %s | %s | %s | %s |" % l)
print("\n## Artefatos de `100-métodos/`\n")
print("| Arquivo | Classe | `Tipo:` válido | alcance (árvore/§6) | §7 mapa | veto no gate | STATUS |")
print("|---|---|---|---|---|---|---|")
for l in linhas: print("| `%s` | %s | %s | %s | %s | %s | %s |" % l)
print("\n**AGENTS.md:**", "réplica do kernel, em sincronia" if agents_ok else "🔴 fora de sincronia com o CLAUDE.md: rode o sincronizar.py, que regenera a réplica")
print("**Sinais repetidos entre árvores (aviso — o desempate resolve; podar se ambíguo):**",
      len(colisoes), "·", "; ".join("%s → %s" % (t, "/".join(v)) for t, v in colisoes[:12]) or "nenhum")
print("**Arquivos .md alterados em 100-métodos/, 00-core/ e 90-templates/ nos últimos 8 dias:**", recentes)
print("\n**Resultado:**", "✅ nada a propagar" if falhas == 0 else "🔴 %d pendência(s)" % falhas)
sys.exit(0 if falhas == 0 else 1)
