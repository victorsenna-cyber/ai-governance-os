# -*- coding: utf-8 -*-
"""
autonomia.py — escada de autonomia por tipo de decisão (A1–A3), a partir do histórico
recomendação × escolha do {{OPERADOR}}.

Histórico: 40-operacao-rotinas/tarefas/log/DECISOES.jsonl, uma linha por decisão:
  {"id": "D-...", "tipo": "remuneracao_parceiro", "recomendado": "A", "escolhido": "A",
   "data": "AAAA-MM-DD", "hora": "HH:MM", "veto": false}

DEFAULT INVERTIDO.
  Dentro da casa, ATO reversível se faz e se avisa. Só a LISTA_FECHADA abaixo pede a palavra do {{OPERADOR}}.
  Esta lista é a FONTE ÚNICA: o CLAUDE.md (seção de autonomia) a cita por extenso e o verificar-propagacao.py reprova
  se as duas divergirem. Mudar a lista = mudar aqui e no CLAUDE.md no mesmo ato.
  python3 autonomia.py --ato "corrigir transcrever-audio.py"   → R  (faz, testa, registra, avisa)
  python3 autonomia.py --ato "enviar o PDF ao cliente"         → L3 (A1: pede a palavra)
  python3 autonomia.py --lista                                  → a lista fechada (e as exceções por palavra do {{OPERADOR}})
  EXCECOES["atendente"]: o item 3 tem exceção para a origem "atendente", com as travas do evolution/atendente.json
  (excecao_atendente(jid)): lista ligada, ou geral ligado só em privada; dinheiro, contrato e escopo continuam com o {{OPERADOR}}.

ESTADO FINAL (CLAUDE.md, seção de autonomia): o pedido literal que descreve a coisa funcionando
  ("roda todo dia", "na nuvem", "no ar", "ligado") é a palavra que o item 5 exige para os atos sem os quais o
  estado não existe; o teste antes de ligar é nosso. Itens 1 a 4 continuam pedindo a palavra sobre o próprio ato.

Escada das DECISÕES com cartão (o que já está na lista e acumula histórico):
  A1  o sistema recomenda e o {{OPERADOR}} escolhe (padrão de entrada, também para tipo novo)
  A2  o sistema decide e avisa, janela de veto de 24 h: acerto >= 90% em >= 10 decisões do tipo
  A3  o sistema decide e registra: acerto >= 95% em >= 20 decisões em A2, sem veto
  Veto ou reversão num tipo em A2/A3 devolve o tipo a A1 até refazer a contagem.
  Teto: dinheiro, contrato e mensagem a cliente começam em A1 e só sobem com
  "aprovado" literal, tipo a tipo (lista TETO abaixo).

  python3 autonomia.py                 → tabela por tipo
  python3 autonomia.py --tipo X        → nível de um tipo (imprime A1..A3)
  python3 autonomia.py --registrar D-001 tipo A B [--veto] [--ficha 30-comercial/assessoria-prospects/<pasta> | clientes/<Conta>]
  python3 autonomia.py --resultado D-001 aceite|recusa|perdido   → o fecho da proposta, na linha da decisão

Tipo `oferta_catalogo` (qual produto do catálogo recomendar a uma pessoa; método 100-métodos/METODO-DECISAO-DE-OFERTA.md).
  Nasce em A1 (o sistema recomenda, o {{OPERADOR}} escolhe no cartão). Regra própria (REGRA_OFERTA abaixo):
    A2 com 10 acertos e taxa >= 90% · A3 com as 20 últimas seguidas sem troca, todas com resultado registrado,
    e aceite delas não pior que o das anteriores com resultado · 2 trocas do {{OPERADOR}} sobre o mesmo produto
    recomendado em 28 dias devolvem o tipo a A1.
  `produto_novo` e `oferta_preco` (preço ou desconto fora de tabela) entram no TETO: A1 até a palavra dele, tipo a tipo.
  O resultado entra pelo acoes_do_painel.py quando a ficha vai a aceite ou perdido (resultado_por_ficha).
"""
import argparse, datetime, io, json, os, re, sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIST = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas", "log", "DECISOES.jsonl")
TETO = {"dinheiro", "preco", "desconto", "cobranca", "contrato", "clausula", "mensagem_cliente", "publicacao", "remuneracao_parceiro",
        "produto_novo", "oferta_preco"}   # os dois da escada de oferta (são dinheiro: item 1 da lista fechada)
RESULTADOS = ("aceite", "recusa", "perdido")
REGRA_OFERTA = {"tipo": "oferta_catalogo", "a2_acertos": 10, "a2_taxa": 0.90, "a3_seguidas": 20, "trocas_volta": 2, "janela_trocas_dias": 28}

# A LISTA FECHADA. (título, o que cobre, palavras que acusam o ato). Fonte única: ver o docstring.
LISTA_FECHADA = [
    ("Dinheiro", "preço, desconto, cobrança, pagamento, compra, despesa, repasse",
     r"pre[çc]o|desconto|cobran|cobrar|pagamento|pagar|compra[rs]?\b|despesa|repasse|reembolso|pix|boleto|fatura|assinatura paga|verba"),
    ("Contrato e cláusula", "redigir vale; assinar, enviar ou mudar termo acordado, não",
     r"contrato|cl[áa]usula|termo de|assinar|aditivo|distrato"),
    ("Mensagem a terceiro e publicação em nome do operador", "cliente, prospect, parceiro, fornecedor, em qualquer canal; post, story, e-mail de saída",
     r"enviar|mandar|mensagem a|mensagem para|responder (a|ao|à)|e-?mail para|whatsapp|publicar post|postar|story|stories|disparar|telegram para"),
    ("Apagar de vez e tirar do ar peça em uso", "o que o git não desfaz, e o que alguém está usando",
     r"apagar de vez|deletar permanente|excluir de vez|force-?push|reset --hard|tirar do ar|despublicar|derrubar|purgar hist"),
    ("Infraestrutura compartilhada", "VPS, serviços que rodam sozinhos, DNS, chaves, agendador do Windows, número de automação; código se escreve e testa, o deploy é dele",
     r"\bvps\b|deploy|systemd|servi[çc]o\b.*(vps|reinici)|\bdns\b|chave de api|token|senha|segredo|schtasks|agendador|evolution|n[úu]mero de automa"),
    ("Componente externo entrando na Governança", "repo, ferramenta, plugin, MCP de fora; teste isolado vale, entrar só com plano aprovado",
     r"instalar (plugin|mcp|pacote|repo)|plugin|\bmcp\b|repo externo|clonar .* para a governan"),
    ("Divergir de regra escrita da casa", "pede-se antes, com a leitura; CORRIGIR falha do kernel não é divergir (ver a seção de autonomia do CLAUDE.md)",
     r"divergir|contrariar|ignorar a regra|exce[çc][ãa]o [àa] regra|revogar"),
]


# EXCEÇÕES POR PALAVRA DO OPERADOR SOBRE O PRÓPRIO ATO (a lista fechada não muda: a exceção vale só onde está escrita).
# Item 3 (mensagem a terceiro): o atendente do número de automação responde sozinho as conversas ligadas em
# ferramentas/evolution/atendente.json, com a autorização literal do {{OPERADOR}} registrada ali.
# Dinheiro (1), contrato (2) e escopo ou regra nova (7) continuam fora: o atendente nunca os decide e sempre os leva ao {{OPERADOR}}.
EXCECOES = {
    "atendente": {"item": 3, "origem": "atendente",
                  "vale_para": "origem 'atendente', com as travas do evolution/atendente.json: conversa ligada na lista; ou, com o geral ligado, "
                               "privada com o número de automação que não seja comandante, número nosso nem relacao 'ignorar' (grupo só listado)",
                  "nunca": (1, 2, 7),
                  "fonte": "autorização literal do {{OPERADOR}}, registrada no evolution/atendente.json"},
    # A mesma exceção cobre FABRICAR e ENVIAR a peça da conta (arte, criativo, carrossel, PDF, copy,
    # estratégia) e PUBLICAR a página de venda DELA no subdomínio do agente, só em conversa ligada com `fabricar` no
    # atendente.json e só dos tipos listados ali (excecao_fabricar). Preço nosso, contrato e proposta continuam fora.
    "fabricar": {"item": 3, "origem": "atendente (evolution/fabricante.py)",
                 "vale_para": "fabricar e enviar peça e publicar página da conta, em conversa ligada com `fabricar` no evolution/atendente.json "
                              "(só os tipos listados; teto por dia e uma página por vez no fabricante.py)",
                 "nunca": (1, 2, 7),
                 "fonte": "autorização literal do {{OPERADOR}}, registrada no evolution/atendente.json (`autorizacao_fabricar`)"},
}
ATENDENTE_JSON = os.path.join(RAIZ, "40-operacao-rotinas", "ferramentas", "evolution", "atendente.json")
MAPA_JSON = os.path.join(RAIZ, "40-operacao-rotinas", "ferramentas", "evolution", "mapa.json")


def excecao_atendente(jid):
    """True se o atendente pode responder este jid sem o ✅ (exceção do item 3). Arquivo ausente ou ilegível = False.
    O comandante e os números nossos o atendente.py e o mensageiro barram também (eles conhecem o .env)."""
    try:
        with io.open(ATENDENTE_JSON, encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError):
        return False
    if not cfg.get("ativo", True):
        return False
    lista = next((c for c in cfg.get("conversas", []) if c.get("jid") == jid), None)
    if lista is not None:
        return lista.get("ligado") is True
    if not (cfg.get("geral") or {}).get("ligado") or jid.endswith("@g.us"):
        return False
    nossos = {x for v in (cfg.get("nossos") or {}).values() for x in v}
    d = re.sub(r"\D", "", jid.split("@")[0]) if jid.endswith("@s.whatsapp.net") else ""
    if jid in nossos or (d and any(d[-8:] == re.sub(r"\D", "", x)[-8:] for x in nossos if "@" not in x)):
        return False
    try:
        with io.open(MAPA_JSON, encoding="utf-8") as f:
            mapa = json.load(f)
    except (OSError, ValueError):
        mapa = {}
    for c in mapa.get("conversas", []):
        if c.get("relacao") == "ignorar" and (c.get("jid") == jid or (d and c.get("telefone") and re.sub(r"\D", "", c["telefone"])[-8:] == d[-8:])):
            return False
    return True


def excecao_fabricar(jid, tipo):
    """True se a conversa `jid` está ligada (excecao_atendente) e tem `tipo` na lista `fabricar` do atendente.json."""
    if not excecao_atendente(jid):
        return False
    try:
        with io.open(ATENDENTE_JSON, encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError):
        return False
    conv = next((c for c in cfg.get("conversas", []) if c.get("jid") == jid), None)
    return bool(conv and tipo in (conv.get("fabricar") or []) and (conv.get("autorizacao_fabricar") or {}).get("literal"))


def classificar_ato(descricao):
    """R (reversível dentro do repo: faz e avisa) ou L<n> (item n da lista fechada: pede a palavra)."""
    import re
    d = (descricao or "").lower()
    for i, (_, _, rx) in enumerate(LISTA_FECHADA, 1):
        if re.search(rx, d):
            return f"L{i}"
    return "R"


def ler():
    if not os.path.exists(HIST):
        return []
    out = []
    for l in io.open(HIST, encoding="utf-8"):
        try:
            out.append(json.loads(l))
        except ValueError:
            pass
    return out


def _catalogo():
    """Nomes da camada 1 do inventário (30-comercial/INVENTARIO-DE-CAPACIDADES.md): a chave de produto da escada de oferta."""
    try:
        import importlib.util as u
        s = u.spec_from_file_location("inventario", os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario-capacidades.py"))
        m = u.module_from_spec(s); s.loader.exec_module(m)
        inv = m._ler(RAIZ, m.INV)
        c1 = m._trecho(inv, "## 1. Camada 1", "## 2. Camada 2")
        return {m._chave(m._nome_celula(c[0])): m._nome_celula(c[0]) for c in m._linhas_tabela(c1) if c}, m._chave
    except Exception:  # noqa: BLE001
        return {}, (lambda s: (s or "").strip().lower())


def chave_oferta(texto, cat=None):
    """'Produto A + Módulo B' → 'produto a+modulo b'.
    Peça que não casa com produto da camada 1 vira 'fora:<texto>' (combo fora do catálogo)."""
    cat, ch = cat if cat else _catalogo()
    partes = []
    for p in re.split(r"\s*\+\s*", texto or ""):
        k = ch(re.sub(r"\(.*?\)", "", p))
        if not k:
            continue
        achado = next((c for c in sorted(cat, key=len, reverse=True) if c and (k == c or k.startswith(c) or c in k)), None)
        partes.append(achado if achado else "fora:" + k)
    return "+".join(sorted(set(partes)))


def _acerto(h):
    a, b = h.get("recomendado_chave") or h.get("recomendado"), h.get("escolhido_chave") or h.get("escolhido")
    return bool(a) and a == b


def _nivel_oferta(hist, hoje=None):
    """oferta_catalogo : A1 de nascença; A2 por acertos; A3 por 20 seguidas com resultado; trocas devolvem a A1.
    Só conta `saida: recomendacao` (ou sem saida). Hipótese de entrada e recomendação humana anterior ao método ficam
    no histórico como dado, fora da contagem. Duas trocas no mesmo produto em 28 dias recomeçam a contagem dali."""
    r = REGRA_OFERTA
    hist = [h for h in hist if h.get("saida", "recomendacao") == "recomendacao"]
    corte = max((i for i, h in enumerate(hist) if h.get("veto")), default=-1)
    trocas = defaultdict(list)
    for i, h in enumerate(hist):
        if _acerto(h):
            continue
        try:
            d = datetime.date.fromisoformat(h.get("data", ""))
        except ValueError:
            continue
        k = h.get("recomendado_chave") or h.get("recomendado")
        trocas[k] = [x for x in trocas[k] if (d - x).days <= r["janela_trocas_dias"]] + [d]
        if len(trocas[k]) >= r["trocas_volta"]:
            corte, trocas[k] = max(corte, i), []
    janela = hist[corte + 1:]
    n = len(janela)
    acertos = sum(1 for h in janela if _acerto(h))
    taxa = acertos / n if n else 0.0
    ult = janela[-r["a3_seguidas"]:]
    if len(ult) == r["a3_seguidas"] and all(_acerto(h) and h.get("resultado") in RESULTADOS for h in ult):
        tx = lambda xs: sum(1 for h in xs if h["resultado"] == "aceite") / len(xs)
        ok = True
        for prod in {h.get("recomendado_chave") or h.get("recomendado") for h in ult}:   # aceite não pior, produto a produto
            antes = [h for h in janela[:-r["a3_seguidas"]] if h.get("resultado") in RESULTADOS
                     and (h.get("recomendado_chave") or h.get("recomendado")) == prod]
            agora = [h for h in ult if (h.get("recomendado_chave") or h.get("recomendado")) == prod]
            if antes and tx(agora) < tx(antes):
                ok = False
        if ok:
            return "A3", n, taxa
    if acertos >= r["a2_acertos"] and taxa >= r["a2_taxa"]:
        return "A2", n, taxa
    return "A1", n, taxa


def nivel(tipo, hist=None):
    hist = [h for h in (hist if hist is not None else ler()) if h.get("tipo") == tipo]
    if tipo == REGRA_OFERTA["tipo"]:
        return _nivel_oferta(hist)
    if not hist:
        return "A1", 0, 0.0   # tipo novo entra recomendando
    # reinicia a contagem depois do último veto/reversão
    ult_veto = max((i for i, h in enumerate(hist) if h.get("veto")), default=-1)
    janela = hist[ult_veto + 1:]
    n = len(janela)
    acertos = sum(1 for h in janela if h.get("recomendado") and h.get("recomendado") == h.get("escolhido"))
    taxa = acertos / n if n else 0.0
    if tipo in TETO and not any(h.get("liberado_pelo_operador") for h in hist):
        return "A1", n, taxa
    if n >= 20 and taxa >= 0.95:
        return "A3", n, taxa
    if n >= 10 and taxa >= 0.90:
        return "A2", n, taxa
    return "A1", n, taxa


def resultado(id_, res, hist_path=None):
    """Grava o fecho (aceite|recusa|perdido) na ÚLTIMA linha com esse id. Devolve o registro ou None."""
    if res not in RESULTADOS:
        raise ValueError(f"resultado inválido: {res} (vale {', '.join(RESULTADOS)})")
    hp = hist_path or HIST
    if not os.path.exists(hp):
        return None
    linhas = io.open(hp, encoding="utf-8").read().splitlines()
    alvo = None
    for i in range(len(linhas) - 1, -1, -1):
        try:
            h = json.loads(linhas[i])
        except ValueError:
            continue
        if h.get("id") == id_:
            alvo = i
            break
    if alvo is None:
        return None
    h = json.loads(linhas[alvo])
    h["resultado"], h["data_resultado"] = res, datetime.date.today().isoformat()
    linhas[alvo] = json.dumps(h, ensure_ascii=False)
    io.open(hp, "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
    return h


def resultado_por_ficha(ficha, res, hist_path=None):
    """Chamado pelo acoes_do_painel.py: fecha a última recomendação oferta_catalogo daquela ficha que ainda não tem resultado."""
    ficha = (ficha or "").strip().strip("/")
    hp = hist_path or HIST
    cand = [h for h in (ler() if hist_path is None else [json.loads(l) for l in io.open(hp, encoding="utf-8") if l.strip()])
            if h.get("tipo") == REGRA_OFERTA["tipo"] and (h.get("ficha") or "").strip("/") == ficha and not h.get("resultado")]
    return resultado(cand[-1]["id"], res, hp) if cand else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tipo")
    ap.add_argument("--registrar", nargs=4, metavar=("ID", "TIPO", "RECOMENDADO", "ESCOLHIDO"))
    ap.add_argument("--veto", action="store_true")
    ap.add_argument("--ficha", help="com --registrar: a pasta da ficha (liga a decisão ao fecho da proposta)")
    ap.add_argument("--resultado", nargs=2, metavar=("ID", "RESULTADO"), help="aceite | recusa | perdido")
    ap.add_argument("--saida", default="recomendacao", choices=("recomendacao", "hipotese", "pre_metodo"),
                    help="oferta_catalogo: só 'recomendacao' conta na escada; hipótese de entrada e decisão anterior ao método ficam como dado")
    ap.add_argument("--ato", help="descrição de um ato: devolve R (faz e avisa) ou L<n> (pede a palavra)")
    ap.add_argument("--lista", action="store_true", help="imprime a lista fechada")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.lista:
        for i, (t, c, _) in enumerate(LISTA_FECHADA, 1):
            print(f"{i}. {t}: {c}")
        for n, x in EXCECOES.items():
            print(f"   exceção '{n}' ao item {x['item']}: {x['vale_para']} · nunca os itens {', '.join(map(str, x['nunca']))} · {x['fonte']}")
        return
    if a.ato is not None:
        c = classificar_ato(a.ato)
        if c == "L3" and re.search(r"atendente|fabric", a.ato, re.I):   # a exceção por palavra do operador sobre o ato
            x = EXCECOES["fabricar" if re.search(r"fabric|arte|criativo|carross|p[áa]gina|pdf|copy|estrat", a.ato, re.I) else "atendente"]
            print(f"L3 · coberto pela exceção ao item 3 ({x['vale_para']}): faz, registra e avisa; nunca os itens "
                  f"{', '.join(map(str, x['nunca']))} · {x['fonte'][:160]}…")
            return
        if c == "R":
            print("R · reversível dentro da casa: faz, testa, registra em uma linha, avisa no fecho")
        else:
            t = LISTA_FECHADA[int(c[1:]) - 1][0]
            print(f"{c} · {t}: pede a palavra do operador (A1, com recomendação)")
        return
    if a.resultado:
        h = resultado(*a.resultado)
        print("resultado gravado:" if h else "id não encontrado:", h or a.resultado[0]); return
    if a.registrar:
        os.makedirs(os.path.dirname(HIST), exist_ok=True)
        i, t, r, e = a.registrar
        reg = {"id": i, "tipo": t, "recomendado": r, "escolhido": e, "veto": a.veto,
               "data": datetime.date.today().isoformat(), "hora": datetime.datetime.now().strftime("%H:%M")}
        if a.ficha:
            reg["ficha"] = a.ficha.strip().strip("/")
        if t == REGRA_OFERTA["tipo"]:
            cat = _catalogo()
            reg["saida"] = a.saida
            reg["recomendado_chave"], reg["escolhido_chave"] = chave_oferta(r, cat), chave_oferta(e, cat)
            if "fora:" in reg["recomendado_chave"]:
                print("⚠️ recomendado com peça fora da camada 1 do inventário: isso é oferta_preco ou produto_novo, não oferta_catalogo")
        io.open(HIST, "a", encoding="utf-8").write(json.dumps(reg, ensure_ascii=False) + "\n")
        print("registrado:", reg); return
    hist = ler()
    if a.tipo:
        print(nivel(a.tipo, hist)[0]); return
    tipos = sorted({h.get("tipo") for h in hist} | {REGRA_OFERTA["tipo"]})
    print("| tipo | nível | decisões na janela | acerto | fechos (aceite/recusa/perdido) |\n|---|---|---:|---:|---|")
    for t in tipos:
        n, c, taxa = nivel(t, hist)
        fx = [h.get("resultado") for h in hist if h.get("tipo") == t and h.get("resultado")]
        fechos = "/".join(str(fx.count(x)) for x in RESULTADOS) if fx else "—"
        print(f"| {t} | {n} | {c} | {taxa:.0%} | {fechos} |")


if __name__ == "__main__":
    main()
