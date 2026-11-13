#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inventario-capacidades.py — confere o inventário do que podemos oferecer (30-comercial/INVENTARIO-DE-CAPACIDADES.md).

Tipo: gate (N0, sem modelo) · Plano: 60-planos/autonomia-de-oferta/PLANO-AUTONOMIA-DE-OFERTA.md §3.1
Método que o lê: 100-métodos/METODO-DECISAO-DE-OFERTA.md (passo 2)

Confere:
  camada 1 · todo produto da tabela de ofertas do POLITICAS-DE-DECISAO.md §5 tem linha no inventário
           · nenhuma linha da camada 1 escreve preço ("R$"): o preço mora no §5, o inventário só aponta
  camada 2 · toda capacidade tem dor escrita (sem "sem dor escrita") e evidência com caminho que existe
           · estado pela Regra Nº 2 dentro do vocabulário
Sem modelo, sem rede, não altera nada.

Uso:
  python3 -X utf8 40-operacao-rotinas/ferramentas/inventario-capacidades.py               confere e sai 1 se falhar
  python3 -X utf8 40-operacao-rotinas/ferramentas/inventario-capacidades.py --candidatas  lista métodos (Tipo: método)
       e ferramentas que ainda não aparecem no inventário: candidatos à camada 2, só se já entregues a alguém
Chamado também pelo verificar-propagacao.py (função conferir).
"""
import io, os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INV = os.path.join("30-comercial", "INVENTARIO-DE-CAPACIDADES.md")
POL = os.path.join("00-core", "POLITICAS-DE-DECISAO.md")
ESTADOS = ("escalado", "em escala", "testando", "nunca vendido", "entregue")



def _em_repo_nao_clonado(raiz, caminho):
    """Verdadeiro se `caminho` cai dentro de um repo listado num repositorios.json
    (clientes/<C>/entregaveis/ ou parceiros/<P>/) cuja pasta não existe aqui."""
    import glob, json
    for reg in glob.glob(os.path.join(raiz, "clientes", "*", "entregaveis", "repositorios.json")) + \
               glob.glob(os.path.join(raiz, "parceiros", "*", "repositorios.json")):
        base = os.path.dirname(reg)
        try:
            repos = json.load(open(reg, encoding="utf-8")).get("repos", [])
        except Exception:
            continue
        for r in repos:
            pasta = os.path.join(base, r.get("pasta", ""))
            rel = os.path.relpath(pasta, raiz).replace(os.sep, "/")
            if caminho.rstrip("/").startswith(rel.rstrip("/") + "/") and not os.path.isdir(pasta):
                return True
    return False

def _ler(raiz, rel):
    with io.open(os.path.join(raiz, rel), encoding="utf-8") as f:
        return f.read()


def _chave(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def _nome_celula(cel):
    m = re.search(r"\*\*(.+?)\*\*", cel)
    t = m.group(1) if m else cel
    t = re.sub(r"\*\(.*?\)\*", "", t)
    t = t.replace("⭐", "").replace("✅", "").replace("🟡", "")
    t = re.sub(r"\(.*?\)", "", t)
    return re.sub(r"\s+", " ", t).strip(" *·")


def _trecho(texto, inicio, fim):
    i = texto.find(inicio)
    if i < 0:
        return ""
    j = texto.find(fim, i + len(inicio))
    return texto[i:] if j < 0 else texto[i:j]


def _linhas_tabela(bloco):
    out = []
    for l in bloco.split("\n"):
        l = l.rstrip("\r")
        if not l.startswith("| ") or l.startswith("|---") or re.match(r"^\|\s*(Oferta|Produto|Capacidade)\s*\|", l):
            continue
        out.append([c.strip() for c in l.strip().strip("|").split("|")])
    return out


def produtos_do_s5(raiz=RAIZ):
    s5 = _trecho(_ler(raiz, POL), "## 5. Pricing", "## 5-ter")
    tab = _trecho(s5, "| Oferta | Preço |", "\n\n")
    return [_nome_celula(c[0]) for c in _linhas_tabela(tab) if c and c[0]]


def conferir(raiz=RAIZ):
    """Devolve (ok, linhas_do_relatorio)."""
    rel, ok = [], True
    if not os.path.exists(os.path.join(raiz, INV)):
        return False, ["🔴 falta `30-comercial/INVENTARIO-DE-CAPACIDADES.md`"]
    inv = _ler(raiz, INV)
    c1 = _trecho(inv, "## 1. Camada 1", "## 2. Camada 2")
    c2 = _trecho(inv, "## 2. Camada 2", "## 3.")
    linhas1 = _linhas_tabela(c1)
    nomes1 = {_chave(_nome_celula(c[0])) for c in linhas1 if c}
    s5 = produtos_do_s5(raiz)
    faltam = [p for p in s5 if _chave(p) not in nomes1]
    if faltam:
        ok = False
        rel.append("🔴 produto do §5 sem linha na camada 1: " + "; ".join(faltam))
    com_preco = [_nome_celula(c[0]) for c in linhas1 if any("R$" in x for x in c)]
    if com_preco:
        ok = False
        rel.append("🔴 preço escrito na camada 1 (o preço mora no §5, aponta-se): " + "; ".join(com_preco))
    linhas2 = _linhas_tabela(c2)
    sem_dor, sem_prova, estado_ruim, nao_clonado = [], [], [], []
    for c in linhas2:
        if len(c) < 6:
            continue
        nome, dor, evid, _, _, estado = c[:6]
        n = _nome_celula(nome)
        if not dor or "sem dor escrita" in dor.lower():
            sem_dor.append(n)
        caminhos = re.findall(r"`([^`]+)`", evid)
        if not caminhos or not any(os.path.exists(os.path.join(raiz, p.rstrip("/"))) for p in caminhos):
            # caminho dentro de repo vivo registrado (§11.6) que não foi clonado
            # nesta máquina (a nuvem sem credencial) não se confere aqui: aviso, não reprova
            if caminhos and all(_em_repo_nao_clonado(raiz, p) for p in caminhos):
                nao_clonado.append(n)
            else:
                sem_prova.append(n)
        if not any(e in estado.lower() for e in ESTADOS):
            estado_ruim.append(n)
    if sem_dor:
        rel.append("⚠️ capacidade sem dor escrita (não entra em oferta): " + "; ".join(sem_dor))
    if nao_clonado:
        rel.append("⚠️ evidência em repo vivo não clonado nesta máquina (conferir onde ele existe): " + "; ".join(nao_clonado))
    if sem_prova:
        ok = False
        rel.append("🔴 capacidade sem evidência com caminho que existe: " + "; ".join(sem_prova))
    if estado_ruim:
        ok = False
        rel.append("🔴 estado fora do vocabulário (escalado · em escala · testando · nunca vendido · entregue): " + "; ".join(estado_ruim))
    rel.insert(0, "%s camada 1: %d linhas, %d produtos no §5, %d sem linha · camada 2: %d capacidades"
               % ("✅" if ok else "🔴", len(linhas1), len(s5), len(faltam), len(linhas2)))
    return ok, rel


def candidatas(raiz=RAIZ):
    inv = _ler(raiz, INV) if os.path.exists(os.path.join(raiz, INV)) else ""
    out = []
    pm = os.path.join(raiz, "100-métodos")
    for nome in sorted(os.listdir(pm)):
        if not nome.endswith(".md"):
            continue
        t = _ler(raiz, os.path.join("100-métodos", nome))
        m = re.search(r"^> \*\*Tipo:\*\*\s*(.+)$", t, re.M)
        if m and m.group(1).strip().lower().startswith(("método", "metodo")) and nome[:-3] not in inv:
            out.append("100-métodos/" + nome)
    pf = os.path.join(raiz, "40-operacao-rotinas", "ferramentas")
    for nome in sorted(os.listdir(pf)):
        if nome.startswith(("_", ".")) or nome.endswith((".txt", ".json")):
            continue
        if nome not in inv:
            out.append("40-operacao-rotinas/ferramentas/" + nome)
    return out


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--candidatas" in sys.argv:
        print("Candidatas à camada 2 (entram só se já entregues a alguém, com dor e evidência):")
        for c in candidatas():
            print("-", c)
        return
    ok, rel = conferir()
    print("# INVENTÁRIO DE CAPACIDADES — conferência")
    print("\n".join("- " + l for l in rel))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
