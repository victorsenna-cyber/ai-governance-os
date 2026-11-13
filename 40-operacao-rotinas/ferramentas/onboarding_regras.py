"""onboarding_regras.py — a régua do Onboarding Orquestrado, em código.

Método: 100-métodos/METODO-ONBOARDING-ORQUESTRADO.md (as etapas, os prazos e o porquê de cada um).
Quem usa: painel-projetos.py (aba Onboarding do sistema) e, depois, os agentes da VPS (alertas, análise de contexto).
Uma fonte só: se um prazo ou um peso muda, muda aqui e no §5/§6 do método, no mesmo ato.

Entrada: o frontmatter do PAINEL.md da conta (campos onb_*) + o que o painel já calcula (silêncio, a receber, marcos).
Saída: etapa, régua de marcos com estado, saúde (0–100 com os critérios abertos) e alertas com o porquê e o ato mínimo.

Campos no PAINEL.md (todos opcionais, datas AAAA-MM-DD):
  onb_d0                 aceite da proposta / assinatura: o dia em que a janela do remorso abre
  onb_passagem_interna   as 6 perguntas da passagem interna respondidas na conta (D+2)
  onb_promessas_orfas    promessas da venda sem lastro no escopo ainda abertas (número)
  onb_escuta             última conversa de escuta com o cliente (fora de reunião de entrega)
  onb_passagem           passagem de bastão com o cliente realizada
  onb_plano_aprovado     plano de sucesso aprovado por escrito pelo decisor
  onb_kickoff            kickoff realizado
  onb_golive_previsto    data do primeiro "no ar" prometida no plano
  onb_golive             primeiro "no ar" (campanha veiculando com rastreio, site publicado, sistema rodando)
  onb_vitoria_10 / _30 / _60 / _90   vitória rápida do marco reconhecida pelo cliente
  onb_primeiro_valor     a primeira vez que o CLIENTE disse que viu valor (fala dele, nunca métrica nossa)
  onb_primeiro_valor_fala   a fala literal + fonte (arquivo, data, hora)
  onb_revisao            revisão de valor realizada (com o decisor, com dados)
  onb_proxima_revisao    próxima revisão marcada
  onb_renovacao          temperatura de renovação na última leitura: sim | talvez | nao
  onb_fora               sim = projeto próprio ou parceria, fora da régua de cliente
  onb_desde              desde quando a régua vale para esta conta (prazo vencido antes disto não acusa)
"""
import datetime as dt

METODO_DESDE = dt.date(2026, 11, 8)          # dia em que o método entrou na casa
ETAPAS = ("embarque", "passagem", "kickoff", "adocao", "revisao", "expansao")
NOME_ETAPA = dict(embarque="Embarque", passagem="Passagem de bastão", kickoff="Kickoff", adocao="Adoção",
                  revisao="Revisão", expansao="Expansão", sem_d0="Sem D0")
QUEM_E_NOSSO = ("operador", "sessão", "sessao", "casa", "")

# critério de saúde → peso (soma 100). Livro p.205-207: poucos critérios, pesos diferentes, verde/amarelo/vermelho.
PESOS = dict(marcos=25, primeiro_valor=25, cliente_em_dia=15, contato=15, pagamento=15, temperatura=5)


def _d(s):
    if not s:
        return None
    try:
        return dt.date.fromisoformat(str(s).strip()[:10])
    except ValueError:
        return None


def _num(s):
    try:
        return float(str(s).strip()) if s not in (None, "") else None
    except ValueError:
        return None


def _mais(d, n):
    return d + dt.timedelta(days=n) if d else None


def _iso(d):
    return d.isoformat() if d else None


def marco(chave, nome, prazo, feito, hoje, desde, porque, fonte, ato, nivel_vencido="vermelho", aviso_dias=3):
    """Estado de um marco do método: feito · feito_atrasado · aberto · vence_logo · vencido · antes_do_metodo · sem_prazo."""
    if feito:
        estado = "feito_atrasado" if (prazo and feito > prazo) else "feito"
    elif not prazo:
        estado = "sem_prazo"
    elif prazo < desde and prazo < hoje:
        estado = "antes_do_metodo"
    elif prazo < hoje:
        estado = "vencido"
    elif (prazo - hoje).days <= aviso_dias:
        estado = "vence_logo"
    else:
        estado = "aberto"
    return dict(chave=chave, nome=nome, prazo=_iso(prazo), feito=_iso(feito), estado=estado,
                dias=(prazo - hoje).days if prazo else None, porque=porque, fonte=fonte, ato=ato,
                nivel_vencido=nivel_vencido)


def calcular(fm, hoje, fase, ativa, sem_toque_dias=None, a_receber=None, marcos_conta=None):
    """Devolve o bloco 'onboarding' da conta para o payload do painel."""
    a_receber = a_receber or []
    marcos_conta = marcos_conta or []
    g = lambda k: _d(fm.get(k))
    d0, passagem, plano, kickoff = g("onb_d0"), g("onb_passagem"), g("onb_plano_aprovado"), g("onb_kickoff")
    golive_prev, golive, pv = g("onb_golive_previsto"), g("onb_golive"), g("onb_primeiro_valor")
    revisao, prox_rev = g("onb_revisao"), g("onb_proxima_revisao")
    desde = g("onb_desde") or METODO_DESDE
    temp = (fm.get("onb_renovacao") or "").strip().lower().replace("ã", "a") or None
    pos_venda = fase in ("fundar", "construir", "operar")
    if (fm.get("onb_fora") or "").strip().lower() == "sim":      # projeto próprio ou parceria: fora da régua de cliente
        ativa, pos_venda, fase = False, False, None

    # ── etapa ─────────────────────────────────────────────────────────────
    if fase in ("prospecto", "proposta"):
        etapa = "embarque"
    elif not d0:
        etapa = "sem_d0" if pos_venda else None
    elif revisao:
        etapa = "expansao"
    elif kickoff and hoje >= _mais(kickoff, 75):
        etapa = "revisao"
    elif kickoff or golive:
        etapa = "adocao"
    elif passagem:
        etapa = "kickoff"
    else:
        etapa = "passagem"

    regua, alertas = [], []
    if d0:
        base_kick = kickoff or golive
        regua = [
            marco("passagem_interna", "Passagem interna (6 perguntas na conta)", _mais(d0, 2), g("onb_passagem_interna"), hoje, desde,
                  "o cliente não repete o que já disse; quem entrega começa sabendo o que foi prometido", "livro p.95–99",
                  "responder na conta: quem é, o que comprou, por quê, contatos, termos, objetivos", nivel_vencido="amarelo"),
            marco("passagem", "Passagem de bastão com o cliente", _mais(d0, 10), passagem, hoje, desde,
                  "fecha a compra na cabeça do cliente: sem ela, o remorso pós-assinatura segue ruminando", "livro p.44, p.104",
                  "marcar a passagem (30–45 min, com o decisor) e mandar o plano antes"),
            marco("plano", "Plano de sucesso aprovado pelo decisor", _mais(passagem or _mais(d0, 10), 3), plano, hoje, desde,
                  "documento aprovado é o compromisso dele com a parte dele", "livro p.89, p.113",
                  "mandar o plano atualizado e pedir o ok por escrito", nivel_vencido="amarelo"),
            marco("kickoff", "Kickoff (quem faz o quê, até quando)", _mais(passagem or _mais(d0, 10), 14), kickoff, hoje, desde,
                  "sem mapa, o cliente imagina o pior cenário e não cumpre a parte dele", "livro p.119, p.121",
                  "marcar o kickoff (60 min, quem executa do lado dele) e mandar o resumo no mesmo dia"),
            marco("golive", "Primeiro no ar", golive_prev, golive, hoje, desde,
                  "o cliente precisa ver a coisa existir: o vale da desilusão começa na implementação longa", "livro p.177, p.275",
                  "pôr no ar o mínimo que já gera dado e comunicar o dia do lançamento" if golive_prev else "pôr a data do primeiro no ar no plano"),
            marco("vitoria_10", "Vitória rápida · D+10", _mais(d0, 10), g("onb_vitoria_10"), hoje, desde,
                  "vitória rápida corta o remorso e dá ao decisor o que mostrar dentro da empresa", "livro p.188, p.191",
                  "registrar a vitória que ele reconheceu, ou entregar a do plano", nivel_vencido="amarelo"),
            marco("vitoria_30", "Vitória rápida · D+30", _mais(d0, 30), g("onb_vitoria_30"), hoje, desde,
                  "contrato mensal: a segunda fatura chega aqui", "livro p.191 · [inferência: mensal]",
                  "registrar a vitória do mês 1 na fala dele", nivel_vencido="amarelo"),
            marco("vitoria_60", "Vitória rápida · D+60", _mais(d0, 60), g("onb_vitoria_60"), hoje, desde,
                  "cada marco reconhecido é evidência a favor da decisão de compra", "livro p.191",
                  "registrar a vitória do mês 2", nivel_vencido="amarelo"),
            marco("vitoria_90", "Vitória rápida · D+90", _mais(d0, 90), g("onb_vitoria_90"), hoje, desde,
                  "sem resultado em 90 dias, a chance de renovar cai para menos de 10%", "livro p.187, p.191",
                  "registrar a vitória do mês 3", nivel_vencido="amarelo"),
            marco("primeiro_valor", "Primeiro valor (na fala dele)", _mais(d0, 30), pv, hoje, desde,
                  "é o 'aha' que para a prospecção negativa; valor é o que ele percebe, não o nosso KPI", "livro p.180, p.184 · alvo D+30 [inferência: mensal]",
                  "perguntar o que para ele é resultado (as 5 perguntas, p.184) e levar até lá", nivel_vencido="amarelo"),
            marco("revisao", "Revisão de valor (~90 dias do kickoff)", _mais(base_kick, 90) if base_kick else _mais(d0, 100), revisao, hoje, desde,
                  "confirma o valor com dados e mede a renovação cedo; sem venda na pauta", "livro p.143, p.145",
                  "marcar a revisão com o decisor e levar o plano v1 lado a lado com o resultado", aviso_dias=14),
        ]
        # primeiro valor depois de D+90 sem fala: vermelho (livro p.187)
        pvm = next(m for m in regua if m["chave"] == "primeiro_valor")
        if not pv and hoje > _mais(d0, 90) and _mais(d0, 90) >= desde:
            pvm["estado"], pvm["nivel_vencido"] = "vencido", "vermelho"
        for m in regua:
            if m["estado"] == "vencido":
                alertas.append(dict(nivel=m["nivel_vencido"], regra=m["chave"],
                                    texto=f"{m['nome']}: venceu há {-m['dias']} dia(s)", porque=m["porque"], fonte=m["fonte"], ato=m["ato"]))
            elif m["estado"] == "vence_logo":
                alertas.append(dict(nivel="amarelo", regra=m["chave"],
                                    texto=f"{m['nome']}: vence em {m['dias']} dia(s)", porque=m["porque"], fonte=m["fonte"], ato=m["ato"]))
            elif m["estado"] == "sem_prazo" and m["chave"] == "golive" and (kickoff or passagem) and not golive:
                alertas.append(dict(nivel="amarelo", regra="golive", texto="Primeiro no ar sem data no plano",
                                    porque=m["porque"], fonte=m["fonte"], ato=m["ato"]))
        orfas = _num(fm.get("onb_promessas_orfas"))
        if orfas:
            alertas.append(dict(nivel="vermelho", regra="promessas", texto=f"{int(orfas)} promessa(s) da venda sem lastro no escopo",
                                porque="o vendedor 'solista' promete o que o cliente quer ouvir; o pós-venda paga em heroísmo", fonte="livro p.94, p.101",
                                ato="pôr no plano ou corrigir por escrito com o cliente"))
        if revisao and not prox_rev:
            alertas.append(dict(nivel="amarelo", regra="proxima_revisao", texto="Revisão feita sem a próxima marcada",
                                porque="toda revisão termina com a próxima no calendário", fonte="livro p.150",
                                ato="marcar a próxima revisão com o decisor"))
    elif etapa == "sem_d0" and ativa:
        alertas.append(dict(nivel="amarelo", regra="sem_d0", texto="Conta em entrega sem D0: fora da régua",
                            porque="sem a data do aceite não há como medir a janela do remorso nem o primeiro valor",
                            fonte="método §4", ato="pôr onb_d0 no PAINEL.md (data do aceite)"))

    # ── sinais que vêm do resto do sistema ─────────────────────────────────
    em_entrega = ativa and pos_venda
    janela_1 = bool(d0 and hoje <= _mais(d0, 30))
    limite_silencio = 7 if janela_1 else 14
    if em_entrega and sem_toque_dias is not None and sem_toque_dias > limite_silencio:
        alertas.append(dict(nivel="vermelho" if sem_toque_dias > 2 * limite_silencio else "amarelo", regra="silencio",
                            texto=f"Sem contato há {sem_toque_dias} dias",
                            porque="interação inexistente conta como negativa: o viés de confirmação trabalha contra", fonte="livro p.43, p.206",
                            ato="mandar a atualização da semana com um pedido concreto"))
    vencidos = [r for r in a_receber if r.get("dias") is not None and r["dias"] < 0]
    if em_entrega and vencidos:
        alertas.append(dict(nivel="vermelho", regra="pagamento", texto=f"A receber vencido ({len(vencidos)})",
                            porque="adiar pagamento é efeito clássico de onboarding falho", fonte="livro p.28, p.206",
                            ato="entender o porquê antes de cobrar: é sintoma, não causa"))
    do_cliente = [m for m in marcos_conta if (m.get("dono") or "").strip().lower() not in QUEM_E_NOSSO]
    cliente_vencidas = [m for m in do_cliente if m.get("vencido")]
    if em_entrega and cliente_vencidas:
        alertas.append(dict(nivel="vermelho" if len(cliente_vencidas) > 1 else "amarelo", regra="cliente",
                            texto=f"Pendência do cliente vencida ({len(cliente_vencidas)})",
                            porque="o cliente que não faz a parte dele trava a adoção (o elo que mais quebra)", fonte="livro p.120, p.243",
                            ato="relembrar a parte dele com o prazo e o que trava se não vier"))
    if em_entrega and temp in ("nao", "talvez"):
        alertas.append(dict(nivel="vermelho" if temp == "nao" else "amarelo", regra="renovacao",
                            texto="Temperatura de renovação: " + ("não" if temp == "nao" else temp), porque="a renovação se decide no onboarding, não no vencimento",
                            fonte="livro p.45, p.145", ato="revisão de valor antes da próxima fatura"))

    # ── saúde (0–100) ───────────────────────────────────────────────────────
    crit = {}
    if d0:
        pesados = [m for m in regua if m["estado"] in ("feito", "feito_atrasado", "vencido")]
        if pesados:
            crit["marcos"] = round(sum(1 if m["estado"] == "feito" else 0.5 if m["estado"] == "feito_atrasado" else 0 for m in pesados) / len(pesados), 2)
        pvm = next(m for m in regua if m["chave"] == "primeiro_valor")
        if pvm["estado"] in ("feito", "feito_atrasado"):
            crit["primeiro_valor"] = 1
        elif pvm["estado"] in ("aberto", "vence_logo"):
            crit["primeiro_valor"] = 1
        elif pvm["estado"] == "vencido":
            crit["primeiro_valor"] = 0 if pvm["nivel_vencido"] == "vermelho" else 0.5
    if em_entrega:
        crit["cliente_em_dia"] = 1 if not cliente_vencidas else (0.5 if len(cliente_vencidas) == 1 else 0)
        if sem_toque_dias is not None:
            crit["contato"] = 1 if sem_toque_dias <= limite_silencio else (0.5 if sem_toque_dias <= 2 * limite_silencio else 0)
        crit["pagamento"] = 0 if vencidos else 1
        if temp in ("sim", "talvez", "nao"):
            crit["temperatura"] = dict(sim=1, talvez=0.5, nao=0)[temp]
    peso_total = sum(PESOS[k] for k in crit)
    score = round(100 * sum(PESOS[k] * v for k, v in crit.items()) / peso_total) if peso_total else None
    if score is not None and em_entrega and temp == "nao":     # recusa de renovação é fato, não critério: a conta é vermelha
        score = min(score, 40)
    faixa = None if score is None else ("verde" if score >= 70 else "amarelo" if score >= 45 else "vermelho")

    ordem = dict(vermelho=0, amarelo=1)
    alertas.sort(key=lambda a: ordem.get(a["nivel"], 2))
    proximo = next((m for m in regua if m["estado"] in ("vence_logo", "aberto", "vencido", "sem_prazo") and not m["feito"]), None)
    return dict(
        etapa=etapa, etapa_nome=NOME_ETAPA.get(etapa) if etapa else None, d0=_iso(d0), dias_desde_d0=(hoje - d0).days if d0 else None,
        ttfv=(pv - d0).days if (pv and d0) else None, escuta=_iso(g("onb_escuta")), primeiro_valor_fala=fm.get("onb_primeiro_valor_fala", ""),
        proxima_revisao=_iso(prox_rev), renovacao=temp, desde=_iso(desde), regua=regua,
        saude=dict(score=score, faixa=faixa, criterios=crit, pesos=PESOS), alertas=alertas,
        proximo=dict(nome=proximo["nome"], prazo=proximo["prazo"], estado=proximo["estado"]) if proximo else None,
        pendencias_cliente=[dict(o_que=m["o_que"], prazo=m.get("prazo"), dono=m.get("dono"), vencido=m.get("vencido")) for m in do_cliente if not m.get("feito")])


def resumo(contas):
    """KPIs da aba: quantos em onboarding, TTFV mediano, % com primeiro valor, alertas, revisões próximas."""
    obs = [c["onboarding"] for c in contas if c.get("ativa") and c.get("onboarding")]
    pos = [o for o in obs if o["d0"]]
    em_onb = [o for o in pos if o["etapa"] != "expansao"]
    ttfvs = sorted(o["ttfv"] for o in pos if o["ttfv"] is not None)
    maduras = [o for o in pos if (o["dias_desde_d0"] or 0) >= 30]
    com_pv = [o for o in maduras if o["ttfv"] is not None]
    alertas = [a for o in obs for a in o["alertas"]]
    revs = []
    for o in pos:
        for m in o["regua"]:
            if m["chave"] == "revisao" and not m["feito"] and m["dias"] is not None and 0 <= m["dias"] <= 14:
                revs.append(m)
    escutas = [o["escuta"] for o in obs if o.get("escuta")]
    ultima_escuta = max(escutas) if escutas else None
    return dict(
        ultima_escuta=ultima_escuta,
        em_onboarding=len(em_onb), contas_com_d0=len(pos), sem_d0=sum(1 for o in obs if o["etapa"] == "sem_d0"),
        em_embarque=sum(1 for o in obs if o["etapa"] == "embarque"),
        ttfv_mediano=ttfvs[len(ttfvs) // 2] if ttfvs else None,
        pct_primeiro_valor=round(100 * len(com_pv) / len(maduras)) if maduras else None, base_primeiro_valor=len(maduras),
        alertas_vermelhos=sum(1 for a in alertas if a["nivel"] == "vermelho"),
        alertas_amarelos=sum(1 for a in alertas if a["nivel"] == "amarelo"), revisoes_14d=len(revs))
