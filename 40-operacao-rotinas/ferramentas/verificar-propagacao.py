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
E o destino de entregável: clientes/<Conta>/entregaveis/<AAAA-MM-DD - nome>/.
E, quando a ferramenta existe na pasta (senão o passo é pulado): a esteira de entregáveis (entregaveis.py: V-ENT-1..7),
os cartões de decisão abertos (decisoes_cartao.py: V-DEC-1..6; molde em tarefas/modelos/cartao-decisao.md), o inventário
de capacidades (inventario-capacidades.py: reprova) e os derivados (derivados.py, aviso).
E as fichas de prospect com produto sem oferta_recomendada (aviso).

Uso:  python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py
Sai com código 1 se houver falha. Não altera nenhum arquivo.
"""
import io, json, os, re, sys, time, unicodedata
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

# --- destino de entregável ---
# Conta com a marca no entregaveis/README.md (o molde de conta-nova traz) é conferida a sério.
# As demais só geram aviso, menos entregas-cliente/ em conta nova, que reprova.
MARCA_ENTREGAVEIS = "padrão de entregáveis"
LEGADO_ENTREGAS_CLIENTE = set()  # contas com pasta anterior à regra: aviso até migrar (nomes de pasta)
def _arquivos(p):
    return any(fs for _, _, fs in os.walk(p))
linhas_entrega = []
_base = os.path.join(RAIZ, "clientes")
for conta in sorted(os.listdir(_base)) if os.path.isdir(_base) else []:
    pc = os.path.join(_base, conta)
    if conta.startswith("_") or not os.path.isdir(pc): continue
    nome = unicodedata.normalize("NFC", conta)
    pe = os.path.join(pc, "entregaveis")
    readme = ""
    if os.path.exists(os.path.join(pe, "README.md")):
        with io.open(os.path.join(pe, "README.md"), encoding="utf-8") as h: readme = h.read()
    readme_nfc = unicodedata.normalize("NFC", readme)
    estrita = MARCA_ENTREGAVEIS in readme_nfc
    ach = []
    if _arquivos(os.path.join(pc, "entregas-cliente")):
        ach.append("tem entregas-cliente/" + ("" if nome in LEGADO_ENTREGAS_CLIENTE else " (FALHA)"))
        if nome not in LEGADO_ENTREGAS_CLIENTE: falhas += 1
    soltas = sorted(x for x in os.listdir(pc) if x.startswith("ENTREGA-") and os.path.isfile(os.path.join(pc, x)))
    if soltas: ach.append("ENTREGA-* na raiz: %d" % len(soltas))
    fora = []
    if os.path.isdir(pe):
        repos = set()
        rj = os.path.join(pe, "repositorios.json")
        if os.path.exists(rj):
            with io.open(rj, encoding="utf-8") as h:
                repos = {r.get("pasta") for r in json.load(h).get("repos", [])}
        for x in sorted(os.listdir(pe)):
            xn = unicodedata.normalize("NFC", x)
            if os.path.isfile(os.path.join(pe, x)):
                if x not in ("README.md", "repositorios.json"): fora.append(xn)
            elif re.match(r"^\d{4}-\d{2}-\d{2} - .+", xn):
                if estrita and xn not in readme_nfc: fora.append(xn + " (sem linha no README)")
            elif x not in repos and not x.startswith("repo-"):
                fora.append(xn)
    if fora: ach.append("fora do padrão em entregaveis/: " + ", ".join(fora[:4]) + (" +%d" % (len(fora) - 4) if len(fora) > 4 else ""))
    if estrita and (soltas or fora):
        falhas += 1
        linhas_entrega.append("🔴 %s: %s" % (nome, " · ".join(ach)))
    elif ach:
        linhas_entrega.append("⚠️ %s: %s" % (nome, " · ".join(ach)))

# --- lista fechada: kernel §5.2 × autonomia.py (pulado se o kernel não tem o §5.2 ou a ferramenta não existe) ---
import importlib.util as _u
def _modulo(nome, arq):
    """Carrega uma ferramenta irmã; devolve None se ela não existe nesta pasta (o passo é pulado)."""
    caminho = os.path.join(RAIZ, "40-operacao-rotinas", "ferramentas", arq)
    if not os.path.exists(caminho): return None
    sp = _u.spec_from_file_location(nome, caminho)
    m = _u.module_from_spec(sp); sp.loader.exec_module(m)
    return m
_aut = _modulo("autonomia", "autonomia.py")
s52 = trecho(claude, "### 5.2", "## 6.")
bloco_lista = trecho(s52, "**A lista fechada**", "🔴 **O kernel")
if _aut is None or not s52:
    linha_lista = "pulado (sem autonomia.py ou sem o §5.2 no kernel)"
else:
    itens_kernel = re.findall(r"^\d+\. \*\*", bloco_lista, re.M)
    faltam_lista = [t for t, _, _ in _aut.LISTA_FECHADA if ("**" + t) not in bloco_lista]
    lista_ok = bool(bloco_lista) and not faltam_lista and len(itens_kernel) == len(_aut.LISTA_FECHADA)
    falhas += 0 if lista_ok else 1
    linha_lista = ("✅ %d itens, iguais nos dois" % len(_aut.LISTA_FECHADA) if lista_ok else
                   "🔴 divergem: kernel tem %d itens, autonomia.py %d; faltam no kernel: %s"
                   % (len(itens_kernel), len(_aut.LISTA_FECHADA), ", ".join(faltam_lista) or "—"))

# --- pasta de cliente sem conta e nome em clientes/ e prospects ao mesmo tempo ---
def _chave(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", n).strip("-")
_pros = os.path.join(RAIZ, "30-comercial", "assessoria-prospects")
_fichas = {_chave(x): x for x in os.listdir(_pros)} if os.path.isdir(_pros) else {}
linhas_conta = []
for conta in sorted(os.listdir(_base)) if os.path.isdir(_base) else []:
    pc = os.path.join(_base, conta)
    if conta.startswith(("_", ".")) or not os.path.isdir(pc): continue
    nome = unicodedata.normalize("NFC", conta)
    sem_conta = not any(os.path.exists(os.path.join(pc, x)) for x in ("PAINEL.md", "STATUS.md", "LEIA-ME.md", "CLAUDE.md"))
    dup = _fichas.get(_chave(conta))
    if sem_conta and dup:
        linhas_conta.append("⚠️ %s: sem conta aberta e com ficha em `30-comercial/assessoria-prospects/%s/`: fundir na ficha" % (nome, dup))
    elif sem_conta:
        linhas_conta.append("⚠️ %s: pasta em clientes/ sem PAINEL nem STATUS (conta nasce pelo aceite ou pela palavra do operador, com fase prospecto)" % nome)
    elif dup:
        linhas_conta.append("⚠️ %s: conta aberta e ficha de prospect `%s/` ao mesmo tempo (a ficha vira histórico)" % (nome, dup))

# --- ferramentas opcionais: inventário de capacidades, esteira de entregáveis, derivados, cartões de decisão ---
def _conferir_opcional(nome, arq):
    global falhas
    m = _modulo(nome, arq)
    if m is None: return ["pulado (sem %s nesta pasta)" % arq]
    ok, linhas = m.conferir(RAIZ)
    if not ok: falhas += 1
    return linhas
inv_linhas = _conferir_opcional("inventario", "inventario-capacidades.py")   # inventário de capacidades (reprova)
ent_linhas = _conferir_opcional("entregaveis", "entregaveis.py")             # esteira de entregáveis: V-ENT-1..7
der_linhas = _conferir_opcional("derivados", "derivados.py")                 # derivados (§11.7): aviso de porte atrasado; reprova só registro quebrado
dec_linhas = _conferir_opcional("decisoes_cartao", "decisoes_cartao.py")     # cartões de decisão: V-DEC-1..6, face e lastro
linhas_oferta = []
for _p in sorted(os.listdir(_pros)) if os.path.isdir(_pros) else []:
    _arq = os.path.join(_pros, _p, "PAINEL.md")
    if not os.path.exists(_arq): continue
    with io.open(_arq, encoding="utf-8") as h: _t = h.read()
    _fm = dict(re.findall(r"^([a-z_]+):[ \t]*(.*?)[ \t]*$", _t.split("\n---", 1)[0], re.M))
    if _fm.get("etapa") in ("aceite", "perdido"): continue
    if _fm.get("produto") and not _fm.get("oferta_recomendada"):
        linhas_oferta.append("⚠️ %s: produto preenchido sem `oferta_recomendada` (rodar o METODO-DECISAO-DE-OFERTA)" % _p)

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
print("\n## Destino de entregável (`entregaveis/<AAAA-MM-DD - nome>/`)\n")
print("\n".join("- " + l for l in linhas_entrega) or "- tudo no padrão")
print("\n## Autonomia (`CLAUDE.md` §5.2 × `autonomia.py`)\n")
print("- **Lista fechada:**", linha_lista)
print("\n## Inventário de capacidades e fichas de oferta (`METODO-DECISAO-DE-OFERTA`)\n")
print("\n".join("- " + l for l in inv_linhas + linhas_oferta))
print("\n## Esteira de entregáveis (`entregaveis.py --verificar`, V-ENT-1..7)\n")
print("\n".join("- " + l for l in ent_linhas))
print("\n## Cartões de decisão (`decisoes_cartao.py`, V-DEC-1..6)\n")
print("\n".join("- " + l for l in dec_linhas))
print("\n## Derivados (`derivados.py`, CLAUDE.md §11.7, aviso)\n")
print("\n".join("- " + l for l in der_linhas))
print("\n## Pastas de conta (`clientes/` × `assessoria-prospects/`, aviso)\n")
print("\n".join("- " + l for l in linhas_conta) or "- nenhuma anomalia")
print("\n**Resultado:**", "✅ nada a propagar" if falhas == 0 else "🔴 %d pendência(s)" % falhas)
sys.exit(0 if falhas == 0 else 1)
