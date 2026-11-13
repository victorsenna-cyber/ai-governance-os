"""comercial_regras.py — o funil e a receita para a área Comercial e a área Operação do sistema.

Quem usa: painel-projetos.py (payload do sistema) e, depois, os agentes da VPS.

Fontes:
  30-comercial/assessoria-prospects/<pasta>/PAINEL.md   ficha do prospect (molde: 90-templates/prospect/PAINEL.md)
  clientes/<Conta>/PAINEL.md com fase prospecto|proposta   a conta que ainda é proposta
  clientes/<Conta>/PAINEL.md com recorrencia/mensalidade   a receita contratada das contas em entrega
"""
import datetime as dt
import os
import re

ETAPAS = ("contato", "g0", "ancoras", "proposta", "aceite", "perdido")
NOME_ETAPA = dict(contato="Contato", g0="G0", ancoras="Âncoras", proposta="Proposta", aceite="Aceite → D0", perdido="Perdido")
PROB = dict(contato=10, g0=25, ancoras=40, proposta=60, aceite=100, perdido=0)
FASE_PARA_ETAPA = dict(prospecto="contato", proposta="proposta")


def _d(s):
    if not s:
        return None
    try:
        return dt.date.fromisoformat(str(s).strip()[:10])
    except ValueError:
        return None


def _num(s):
    if s in (None, ""):
        return None
    t = str(s).strip().replace("R$", "").replace(" ", "")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", t):
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def ficha(texto):
    """Frontmatter plano (chave: valor). Devolve dict; sem frontmatter, None."""
    m = re.match(r"^﻿?---\r?\n(.*?)\r?\n---", texto, re.S)
    if not m:
        return None
    fm = {}
    for linha in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", linha)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return fm


def _item(nome, pasta_rel, fm, hoje, toque, origem_tipo):
    etapa = (fm.get("etapa") or "").strip().lower()
    if etapa not in ETAPAS:
        etapa = None
    valor = _num(fm.get("valor"))
    rec = (fm.get("recorrencia") or "").strip().lower() or None
    meses = _num(fm.get("meses"))
    prob = _num(fm.get("probabilidade"))
    prob = prob if prob is not None else PROB.get(etapa or "", 0)
    # valor do contrato inteiro, para o ponderado: mensal × meses (12 se não dito), projeto = valor
    total = None
    if valor is not None:
        total = valor * (meses or 12) if rec == "mensal" else valor
    validade, prox = _d(fm.get("validade")), _d(fm.get("proximo_prazo"))
    toques = [d for d in (_d(fm.get("ultimo_toque")), toque) if d]
    ult = max(toques) if toques else None
    sem_toque = (hoje - ult).days if ult else None
    alertas = []
    vivo = etapa not in ("aceite", "perdido", None)
    if vivo and validade is not None:
        dv = (validade - hoje).days
        if dv < 0:
            alertas.append(dict(nivel="vermelho", texto=f"proposta vencida há {-dv} d", ato="renovar a validade por escrito ou dar como perdida"))
        elif dv <= 3:
            alertas.append(dict(nivel="amarelo", texto=f"proposta vence em {dv} d", ato="follow-up com a validade"))
    if vivo and prox is not None and prox < hoje:
        alertas.append(dict(nivel="amarelo", texto=f"próximo passo vencido há {(hoje - prox).days} d", ato=fm.get("proximo_passo") or "dar o próximo passo"))
    if vivo and sem_toque is not None and sem_toque > 7:
        alertas.append(dict(nivel="vermelho" if sem_toque > 21 else "amarelo", texto=f"sem toque há {sem_toque} d",
                            ato="mensagem com um pedido concreto (silêncio esfria proposta)"))
    if vivo and not fm.get("proximo_passo"):
        alertas.append(dict(nivel="amarelo", texto="sem próximo passo", ato="escrever o próximo ato e a data na ficha"))
    checklist = {k: (fm.get("embarque_" + k) or "").strip().lower() for k in ("jornada", "primeiro_valor", "plano")}
    if etapa == "proposta" and any(v != "sim" for v in checklist.values()):
        faltam = [dict(jornada="jornada de onboarding", primeiro_valor="primeiro valor datado", plano="esboço do plano")[k] for k, v in checklist.items() if v != "sim"]
        alertas.append(dict(nivel="amarelo", texto="Embarque incompleto: " + ", ".join(faltam),
                            ato="a proposta leva a jornada, o primeiro valor com data e o esboço do plano (método §3)"))
    if etapa == "aceite" and origem_tipo == "prospect":
        alertas.append(dict(nivel="vermelho", texto="aceite sem conta aberta", ato="abrir a conta em clientes/ com onb_d0 = data do aceite (trilho, etapa 0)"))
    # METODO-DECISAO-DE-OFERTA (passo 1, procedência): só ficha de prospect, só viva
    dor = (fm.get("dor") or "").strip()
    mf = re.match(r"^\s*([DOIVdoiv])(?![A-Za-zÀ-ú])", fm.get("dor_fonte") or "")   # a letra da classe vem primeiro; "<operador>, <data>" não é V
    fonte = mf.group(1).upper() if mf else ""
    oferta = (fm.get("produto") or fm.get("oferta_recomendada") or "").strip()
    if vivo and origem_tipo == "prospect":
        if not dor:
            alertas.append(dict(nivel="amarelo", texto="ficha sem dor", ato="escrever a dor em uma linha e a fonte (D, O, I ou V) no PAINEL.md"))
        elif oferta and fonte in ("I", "V"):
            quem = "de indicador" if fonte == "I" else "de leitura nossa"
            alertas.append(dict(nivel="vermelho", texto=f"oferta com dor só {quem}",
                                ato="a primeira pergunta da conversa confirma a dor com a pessoa (vira D); até lá é hipótese de entrada, não proposta"))
        if (fm.get("produto") or "").strip() and not (fm.get("oferta_recomendada") or "").strip():
            alertas.append(dict(nivel="amarelo", texto="produto sem recomendação registrada", ato="rodar o METODO-DECISAO-DE-OFERTA e preencher oferta_recomendada e oferta_gatilho"))
    return dict(
        nome=nome, pasta=pasta_rel, origem_tipo=origem_tipo, etapa=etapa, etapa_nome=NOME_ETAPA.get(etapa) if etapa else "sem etapa",
        produto=fm.get("produto", ""), valor=valor, recorrencia=rec, meses=meses, valor_total=total,
        probabilidade=prob, ponderado=round(total * prob / 100, 2) if total is not None else None,
        validade=validade.isoformat() if validade else None, proximo_passo=fm.get("proximo_passo", ""),
        proximo_prazo=prox.isoformat() if prox else None, decisor=fm.get("decisor", ""), origem=fm.get("origem", ""),
        ultimo_toque=ult.isoformat() if ult else None, sem_toque_dias=sem_toque, checklist=checklist,
        aceite=fm.get("aceite") or None, motivo_perda=fm.get("motivo_perda", ""),
        dor=dor, dor_fonte=fonte or None, oferta_recomendada=fm.get("oferta_recomendada", ""), oferta_gatilho=fm.get("oferta_gatilho", ""),
        dor_sem_produto=(fm.get("dor_sem_produto") or "").strip().lower() == "sim", alertas=alertas)


def montar(raiz, contas_fm, hoje, ler, ultimo_toque_pasta):
    """contas_fm: [(nome, fase, fm)] das contas em clientes/. ler(p) -> str. ultimo_toque_pasta(pasta) -> date|None."""
    base = os.path.join(raiz, "30-comercial", "assessoria-prospects")
    itens, sem_ficha = [], []
    nomes_contas = {n.lower() for n, _, _ in contas_fm}
    if os.path.isdir(base):
        for p in sorted(os.listdir(base)):
            pasta = os.path.join(base, p)
            if not os.path.isdir(pasta) or p.startswith(("_", ".")):
                continue
            arq = os.path.join(pasta, "PAINEL.md")
            fm = ficha(ler(arq)) if os.path.exists(arq) else None
            if not fm:
                sem_ficha.append(p)
                continue
            if "duplicada" in (fm.get("motivo_perda") or "").lower():
                continue                                      # a conta em clientes/ é a fonte
            nome = fm.get("prospect") or p
            itens.append(_item(nome, f"30-comercial/assessoria-prospects/{p}", fm, hoje, ultimo_toque_pasta(pasta), "prospect"))
    for nome, fase, fm in contas_fm:
        if fase not in FASE_PARA_ETAPA:
            continue
        fm2 = dict(fm)
        fm2.setdefault("etapa", FASE_PARA_ETAPA[fase])
        if not fm2.get("etapa"):
            fm2["etapa"] = FASE_PARA_ETAPA[fase]
        if not fm2.get("valor") and fm.get("contrato"):
            fm2["valor"] = fm["contrato"]
        fm2.setdefault("proximo_passo", fm.get("proximo_marco", ""))
        if not fm2.get("proximo_prazo"):
            fm2["proximo_prazo"] = fm.get("marco_prazo", "")
        # a pasta pela regra das contas (parceiro e subprojeto de cliente); o toque vem de onde moram os fatos
        try:
            import contas_da_casa
            pc = contas_da_casa.pasta_da_conta(raiz, nome) or os.path.join(raiz, "clientes", nome)
            pf = contas_da_casa.pasta_dos_fatos(raiz, pc)
        except ImportError:
            pc = pf = os.path.join(raiz, "clientes", nome)
        it = _item(nome, os.path.relpath(pc, raiz).replace(os.sep, "/"), fm2, hoje, ultimo_toque_pasta(pf), "conta")
        itens.append(it)
    vivos = [i for i in itens if i["etapa"] not in ("aceite", "perdido")]
    por_etapa = {e: sum(1 for i in itens if i["etapa"] == e) for e in ETAPAS}
    fechados = [i for i in itens if i["etapa"] in ("aceite", "perdido")]
    ganhos = [i for i in fechados if i["etapa"] == "aceite"]
    # METODO-DECISAO-DE-OFERTA §5: a mesma dor sem produto em 3 fichas = necessidade recorrente sem produto
    sem_prod = {}
    for i in itens:
        if i.get("dor_sem_produto") and i.get("dor"):
            sem_prod.setdefault(re.sub(r"\s+", " ", i["dor"].lower()).strip(" ."), []).append(i["nome"])
    recorrentes = [dict(dor=d, fichas=n) for d, n in sem_prod.items() if len(n) >= 3]
    return dict(
        itens=itens, sem_ficha=sem_ficha, necessidades_sem_produto=recorrentes,
        resumo=dict(
            vivos=len(vivos), por_etapa=por_etapa,
            pipeline_bruto=round(sum(i["valor_total"] or 0 for i in vivos), 2),
            pipeline_ponderado=round(sum(i["ponderado"] or 0 for i in vivos), 2),
            propostas_abertas=por_etapa.get("proposta", 0),
            propostas_valor=round(sum(i["valor_total"] or 0 for i in vivos if i["etapa"] == "proposta"), 2),
            sem_valor=sum(1 for i in vivos if i["valor"] is None),
            win_rate=round(100 * len(ganhos) / len(fechados)) if fechados else None, base_win_rate=len(fechados),
            alertas_vermelhos=sum(1 for i in itens for a in i["alertas"] if a["nivel"] == "vermelho"),
            alertas_amarelos=sum(1 for i in itens for a in i["alertas"] if a["nivel"] == "amarelo")))


def receita(contas, recebidas, hoje, casa, lanc=None):
    """Recorrente contratada × recebida no mês, e o que entrou de projeto no mês.
    contas: payload de contas (com recorrencia/mensalidade copiados do frontmatter). recebidas: [{data, contraparte, valor, ref}].
    lanc(conta_payload, lancamento) -> bool (subprojeto de cliente): quem decide de quem é o lançamento;
    sem ele, o casa() pela contraparte. Um lançamento entra numa conta só (o primeiro que casa)."""
    mes = hoje.strftime("%Y-%m")
    do_mes = [r for r in recebidas if (r.get("data") or "").startswith(mes)]
    linhas, rec_contratada, rec_recebida, proj_recebido, nao_casou = [], 0.0, 0.0, 0.0, 0.0
    usados = set()
    for c in contas:
        if not c.get("ativa") or c.get("fase") not in ("fundar", "construir", "operar"):
            continue
        if not (c.get("onboarding") or {}).get("etapa"):      # projeto próprio (onb_fora): não é receita de cliente
            continue
        tipo = c.get("recorrencia")
        mens = c.get("mensalidade") or 0
        entrou = 0.0
        for i, r in enumerate(do_mes):
            if i in usados:
                continue
            if (lanc(c, r) if lanc else casa(c["conta"], r.get("contraparte"))):
                entrou += float(r["valor"]); usados.add(i)
        if tipo == "mensal":
            rec_contratada += mens; rec_recebida += entrou
        else:
            proj_recebido += entrou
        linhas.append(dict(conta=c["conta"], recorrencia=tipo, mensalidade=mens or None, recebido_mes=round(entrou, 2),
                           divergencia=(tipo == "mensal" and hoje.day > 10 and entrou + 0.5 < mens)))
    for i, r in enumerate(do_mes):
        if i not in usados:
            nao_casou += float(r["valor"])
    return dict(mes=mes, recorrente_contratada=round(rec_contratada, 2), recorrente_recebida=round(rec_recebida, 2),
                projeto_recebido=round(proj_recebido, 2), outras_entradas=round(nao_casou, 2),
                sem_tipo=[l["conta"] for l in linhas if not l["recorrencia"]], contas=linhas)
