#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
painel-projetos.py — o andamento das contas, lido do repo, vira o painel de projetos.

O painel é LEITOR, nunca fonte (mesma régua do financeiro). Este script só lê:
  clientes/<Conta>/PAINEL.md              frontmatter YAML (a camada de máquina da conta: fase, próximo marco,
                                          prazo, dono, contrato, recebido, risco, atualizado, marcos abertos)
  clientes/<Conta>/STATUS.md              a data mais recente escrita no arquivo (último registro) — para medir
                                          a defasagem do painel; nunca o conteúdo
  clientes/<Conta>/01 - contexto/OpenWA/  a data mais nova no nome dos arquivos (último toque por WhatsApp);
                                          em checkout parcial, pelos nomes no git (ls-tree), sem baixar os arquivos
  clientes/<Conta>/<subpasta>/PAINEL.md   subprojeto (11/11/2026, contas_da_casa.py): cartão próprio com `conta:` próprio;
                                          STATUS e OpenWA vêm da conta-mãe; lançamento do financeiro vai a ele pelo
                                          `financeiro_ref:` (o resto fica na mãe, nada conta duas vezes); defasagem não
                                          se mede nele. Marco que abre com ✅ está feito: não vence nem é pendência
  40-operacao-rotinas/tarefas/*/T-*.md    frontmatter das tasks (conta, prazo, prazo_duro, prioridade, estado)
  40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md   os cartões em "## Abertas"
  40-operacao-rotinas/tarefas/ (PAUSA, log/RODADA-*.md, log/GASTO.jsonl) e tokens/ORCAMENTO.json → payload["despachante"],
                                          pelo despachante_painel.py (11/11/2026: tela Despachante)
  45-financeiro/LANCAMENTOS-EMPRESA.md    A receber e Receitas, pelas funções de financas-painel.py (importado)
e publica UM documento JSON no Supabase (projeto <projeto-supabase>, tabela projetos_estado), que o site lê.

Uso:
  python3 40-operacao-rotinas/ferramentas/painel-projetos.py               # resumo na tela
  python3 40-operacao-rotinas/ferramentas/painel-projetos.py --json X.json # grava o payload (serve ao brief diário)
  python3 40-operacao-rotinas/ferramentas/painel-projetos.py --verificar   # lista contas com painel inválido ou
                                                                      # defasado; sai 1 se houver (gate N0)
  python3 40-operacao-rotinas/ferramentas/painel-projetos.py --publicar    # envia ao Supabase

--publicar lê do ambiente FINANCAS_SUPABASE_URL, FINANCAS_SUPABASE_KEY e FINANCAS_SYNC_TOKEN (os mesmos do
financeiro). Sem eles avisa e sai 0 — menos no GitHub Action, onde sai 1.

Saúde (calculada, nunca declarada):
  🔴 marco ou task dura vencida · a receber vencido · decisão com prazo vencido · sem toque > 14 dias em
     conta construir/operar · frontmatter inválido
  🟡 prazo em até 7 dias · sem toque > 7 dias · painel defasado > 3 dias em relação ao STATUS · contrato vazio
     em conta além de proposta
  🟢 o resto
Frontmatter: só `chave: valor` e a lista `marcos:` com itens inline `- { o_que: …, prazo: …, dono: …, duro: … }`.
Sem PyYAML de propósito: o Action roda com o Python puro do runner.
"""
import argparse, datetime as dt, importlib.util, io, json, os, re, subprocess, sys, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLIENTES = os.path.join(RAIZ, "clientes")
TAREFAS = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas")
PENDENTES = os.path.join(TAREFAS, "DECISOES-PENDENTES.md")
EMPRESA = os.path.join(RAIZ, "45-financeiro", "LANCAMENTOS-EMPRESA.md")
FINANCAS_PY = os.path.join(RAIZ, "40-operacao-rotinas", "ferramentas", "financas-painel.py")
FASES = ("prospecto", "proposta", "fundar", "construir", "operar", "pausada", "encerrada", "arquivada")
ATIVAS = ("prospecto", "proposta", "fundar", "construir", "operar")
PASTAS_TASK = ("fila", "executando", "revisao", "decisao", "falhou")
FUSO = dt.timezone(dt.timedelta(hours=-3))
# 08/11/2026: a régua do Onboarding Orquestrado (aba Onboarding; 100-métodos/METODO-ONBOARDING-ORQUESTRADO.md)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import onboarding_regras as onb  # noqa: E402
import comercial_regras as com  # noqa: E402  (08/11/2026: áreas Comercial e Operação)
import contas_da_casa  # noqa: E402  (08/11/2026: conta em clientes/ ou em parceiros/<P>/PAINEL.md)


def hoje():
    return dt.datetime.now(FUSO).date()


def ler(p):
    try:
        return io.open(p, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return ""


def iso(s):
    s = (s or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", s)
    if m:
        try:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        try:
            return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None
    return None


def num(s):
    s = re.sub(r"[^\d,.\-]", "", s or "")
    if not s:
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def dias(d):
    return (d - hoje()).days if d else None


# ── frontmatter ────────────────────────────────────────────────────────────

def frontmatter(texto):
    """Devolve (dict, erros). Só o subconjunto que o esquema usa."""
    erros = []
    m = re.match(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    if not m:
        return None, ["sem frontmatter"]
    fm, marcos = {}, []
    em_marcos = False
    for linha in m.group(1).splitlines():
        if not linha.strip():
            continue
        if em_marcos and linha.lstrip().startswith("-"):
            item = linha.strip()[1:].strip()
            if not (item.startswith("{") and item.endswith("}")):
                erros.append(f"marco fora do formato inline: {item[:60]}")
                continue
            corpo = item[1:-1]
            d = {}
            for k, v in re.findall(r"(o_que|prazo|dono|duro|task)\s*:\s*(.*?)(?=,\s*(?:o_que|prazo|dono|duro|task)\s*:|$)", corpo):
                d[k] = v.strip().strip('"').strip("'")
            if not d.get("o_que"):
                erros.append(f"marco sem o_que: {item[:60]}")
                continue
            prazo = iso(d.get("prazo"))
            if d.get("prazo") and not prazo:
                erros.append(f"prazo inválido no marco '{d['o_que'][:40]}': {d.get('prazo')}")
            marcos.append(dict(o_que=d["o_que"], prazo=prazo.isoformat() if prazo else None,
                               dono=d.get("dono") or "", duro=(d.get("duro", "").lower() == "sim"), task=d.get("task") or None))
            continue
        em_marcos = False
        mm = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", linha)
        if not mm:
            erros.append(f"linha fora do esquema: {linha[:60]}")
            continue
        k, v = mm.group(1), mm.group(2).strip()
        if k == "marcos":
            em_marcos = True
            if v and v != "[]":
                erros.append("marcos: precisa ser lista (uma linha por marco) ou []")
            continue
        fm[k] = v.strip('"').strip("'")
    fm["marcos"] = marcos
    if fm.get("fase") not in FASES:
        erros.append(f"fase inválida: {fm.get('fase')!r}")
    datas_onb = [k for k in fm if k.startswith("onb_") and k not in ("onb_primeiro_valor_fala", "onb_renovacao", "onb_fora", "onb_promessas_orfas")]
    for k in ["marco_prazo", "atualizado"] + datas_onb:
        if fm.get(k) and not iso(fm[k]):
            erros.append(f"{k} inválido: {fm[k]}")
    if not fm.get("atualizado"):
        erros.append("sem atualizado:")
    for k in ("contrato", "recebido"):
        if fm.get(k) and num(fm[k]) is None:
            erros.append(f"{k} não é número: {fm[k]}")
    return fm, erros


# ── fontes ─────────────────────────────────────────────────────────────────

def contas():
    """[(nome, pasta, rel)]: clientes/<Conta>/ e parceiros/<Parceiro>/ com PAINEL.md (contas_da_casa.py)."""
    return contas_da_casa.contas(RAIZ)


DATA_BR = re.compile(r"\b(\d{1,2})/(\d{1,2})/(20\d{2})\b")
DATA_ISO = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")


def ultima_data_no_texto(texto, teto=None):
    teto = teto or hoje()
    out = None
    for d, m, a in DATA_BR.findall(texto):
        try:
            x = dt.date(int(a), int(m), int(d))
        except ValueError:
            continue
        if x <= teto and (out is None or x > out):
            out = x
    for a, m, d in DATA_ISO.findall(texto):
        try:
            x = dt.date(int(a), int(m), int(d))
        except ValueError:
            continue
        if x <= teto and (out is None or x > out):
            out = x
    return out


def nomes_openwa(pasta):
    """Nomes dos arquivos de OpenWA da conta: do disco, ou do git quando o checkout é parcial (Action, blob:none)."""
    base = os.path.join(pasta, "01 - contexto", "OpenWA")
    if os.path.isdir(base):
        return [a for _, _, arqs in os.walk(base) for a in arqs]
    rel = os.path.relpath(base, RAIZ).replace(os.sep, "/")
    try:
        r = subprocess.run(["git", "-C", RAIZ, "-c", "core.quotepath=off", "ls-tree", "-r", "--name-only", "HEAD", rel],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        return [os.path.basename(l) for l in r.stdout.splitlines() if l.strip()] if r.returncode == 0 else []
    except (OSError, subprocess.SubprocessError):
        return []


def ultimo_toque_openwa(pasta):
    out = None
    for a in nomes_openwa(pasta):
        if True:
            m = DATA_ISO.search(a)
            if not m:
                continue
            try:
                x = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                continue
            if x <= hoje() and (out is None or x > out):
                out = x
    return out


def tasks():
    out = []
    for pasta in PASTAS_TASK:
        p = os.path.join(TAREFAS, pasta)
        if not os.path.isdir(p):
            continue
        for a in sorted(os.listdir(p)):
            if not (a.startswith("T-") and a.endswith(".md")):
                continue
            t = ler(os.path.join(p, a))
            m = re.match(r"^\ufeff?---\r?\n(.*?)\r?\n---", t, re.S)
            if not m:
                continue
            fm = {}
            for linha in m.group(1).splitlines():
                mm = re.match(r"^([a-z_]+)\s*:\s*(.*?)\s*(?:#.*)?$", linha)
                if mm:
                    fm[mm.group(1)] = mm.group(2).strip()
            prazo = iso(fm.get("prazo"))
            out.append(dict(id=fm.get("id") or a[:-3], titulo=fm.get("titulo", ""), conta=fm.get("conta", "casa"),
                            pasta=pasta, estado=fm.get("estado", ""), prazo=prazo.isoformat() if prazo else None,
                            duro=(fm.get("prazo_duro", "").lower() == "sim"), prioridade=int(fm.get("prioridade") or 3),
                            recorrencia=fm.get("recorrencia") or None, arvore=fm.get("arvore", "")))
    return out


def decisoes():
    # 12/11/2026 (PLANO-DECISOES-NO-PAINEL §4.2): o leitor é o decisoes_cartao.py, a fonte única do formato; sem corte
    # de 600. Cartão = face (titulo, em_jogo, numeros, opcoes[letra, rotulo, efeito], porque, supondo) + lastro inteiro.
    # Os nomes antigos ficam (id, conta, titulo, tipo, autonomia, prazo, recomendado: avisar-prazos e foto-da-operacao) e
    # os apelidos opcoes[].texto = rótulo e contexto = "Em jogo" seguram a aba antiga aberta num navegador.
    _sc = importlib.util.spec_from_file_location("decisoes_cartao", os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisoes_cartao.py"))
    _dc = importlib.util.module_from_spec(_sc); _sc.loader.exec_module(_dc)
    return _dc.ler(ler(PENDENTES))


def financeiro():
    """A receber aberto e receitas por contraparte, pelas funções do leitor financeiro."""
    vazio = dict(a_receber=[], recebido={})
    if not os.path.exists(FINANCAS_PY) or not os.path.exists(EMPRESA):
        return vazio
    try:
        spec = importlib.util.spec_from_file_location("financas_painel", FINANCAS_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        texto = ler(EMPRESA)
        a_receber = mod.ler_a_receber(texto)
        receitas = [l for l in mod.ler_empresa(texto) if l["sentido"] == "entrada"]
    except Exception as e:  # noqa: BLE001
        print("⚠️ painel-projetos: leitor financeiro falhou —", e, file=sys.stderr)
        return vazio
    recebido = {}
    for r in receitas:
        recebido[r["contraparte"]] = recebido.get(r["contraparte"], 0) + float(r["valor"])
    entradas = [dict(data=r.get("data"), contraparte=r.get("contraparte"), valor=float(r["valor"]), ref=r.get("ref") or "")
                for r in receitas]
    return dict(a_receber=a_receber, recebido=recebido, entradas=entradas)


def casa(nome, contraparte):
    a, b = nome.lower(), (contraparte or "").lower()
    return a in b or b in a or a.split()[0] in b.split()


def casador(contas_info):
    """11/11/2026 (subprojeto de cliente, contas_da_casa.py): de quem é um lançamento do financeiro.
    contas_info: [dict(nome, pasta, fatos, sub, fm)]. Devolve f(info, contraparte, texto) -> bool.
    Subprojeto: contraparte da mãe e o `financeiro_ref:` dele no texto do lançamento. Mãe: o casa() de sempre, menos o que
    um subprojeto dela reclamou. Subprojeto sem `financeiro_ref:` não pega nada: um lançamento nunca conta duas vezes."""
    refs = {}
    for x in contas_info:
        r = (x["fm"].get("financeiro_ref") or "").strip().lower()
        if x["sub"] and r:
            refs.setdefault(os.path.normcase(x["fatos"]), []).append(r)

    def f(x, contraparte, texto):
        t = (texto or "").lower()
        if x["sub"]:
            r = (x["fm"].get("financeiro_ref") or "").strip().lower()
            return bool(r) and casa(os.path.basename(x["fatos"]), contraparte) and r in t
        if not casa(x["nome"], contraparte):
            return False
        return not any(r in t for r in refs.get(os.path.normcase(x["pasta"]), []))
    return f


# ── montagem ───────────────────────────────────────────────────────────────

def montar():
    h = hoje()
    fin = financeiro()
    todas_tasks = tasks()
    todas_dec = decisoes()
    saida, contas_fm = [], []
    # 11/11/2026: subprojeto de cliente (clientes/<Conta>/<subpasta>/PAINEL.md com conta: próprio). O cartão é dele;
    # STATUS, DECISOES, 01 - contexto/ (toque e silêncio) vêm da mãe (contas_da_casa.pasta_dos_fatos)
    info = []
    for nome, pasta, rel in contas():
        painel = os.path.join(pasta, "PAINEL.md")
        tem_painel = os.path.exists(painel)
        fm, erros = (frontmatter(ler(painel)) if tem_painel else (None, ["sem PAINEL.md"]))
        fatos = contas_da_casa.pasta_dos_fatos(RAIZ, pasta)
        sub = os.path.normcase(os.path.normpath(fatos)) != os.path.normcase(os.path.normpath(pasta))
        rel_fatos = os.path.relpath(fatos, RAIZ).replace(os.sep, "/") if sub else rel
        info.append(dict(nome=nome, pasta=pasta, rel=rel, fatos=fatos, rel_fatos=rel_fatos, sub=sub, fm=fm or {},
                         erros=erros, tem_painel=tem_painel))
    do_lanc = casador(info)
    por_nome = {x["nome"].lower(): x for x in info}
    for x in info:
        nome, pasta, rel, fm, erros, tem_painel = x["nome"], x["pasta"], x["rel"], x["fm"], x["erros"], x["tem_painel"]
        status = os.path.join(x["fatos"], "STATUS.md")
        tem_status = os.path.exists(status)
        contas_fm.append((nome, fm.get("fase"), fm))
        ult_status = ultima_data_no_texto(ler(status)) if tem_status else None
        toque_wa = ultimo_toque_openwa(x["fatos"])
        atualizado = iso(fm.get("atualizado"))
        toques = [d for d in (ult_status, toque_wa) if d]
        ultimo_toque = max(toques) if toques else None
        fase = fm.get("fase") if fm.get("fase") in FASES else ("arquivada" if not tem_status else None)
        ativa = fase in ATIVAS
        marcos = []
        for mk in fm.get("marcos", []):
            d = dias(iso(mk["prazo"])) if mk["prazo"] else None
            # 11/11/2026: marco que abre com ✅ está feito (convenção dos PAINEL.md); não vence nem conta como pendência
            feito = mk["o_que"].lstrip().startswith("✅")
            marcos.append(dict(mk, dias=d, feito=feito, vencido=(not feito and d is not None and d < 0)))
        minhas_tasks = [t for t in todas_tasks if t["conta"].lower() == nome.lower()]
        for t in minhas_tasks:
            d = dias(iso(t["prazo"])) if t["prazo"] else None
            t.update(dias=d, vencido=(d is not None and d < 0))
        minhas_dec = [d for d in todas_dec if d["conta"].lower() == nome.lower()]
        a_receber = [dict(r, dias=dias(iso(r["vencimento"])) if r.get("vencimento") else None)
                     for r in fin["a_receber"] if do_lanc(x, r.get("contraparte"), r.get("descricao"))]
        recebido_fin = sum(e["valor"] for e in fin.get("entradas", []) if do_lanc(x, e.get("contraparte"), e.get("ref")))
        # subprojeto: o STATUS é da mãe e anda com a outra frente; a defasagem não se mede nele (o silêncio, sim)
        defasagem = (ult_status - atualizado).days if (not x["sub"] and ult_status and atualizado and ult_status > atualizado) else 0
        sem_toque = (h - ultimo_toque).days if ultimo_toque else None
        marco_prazo = iso(fm.get("marco_prazo"))
        prox = dias(marco_prazo) if marco_prazo else None

        motivos = []
        if erros:
            motivos.append(("vermelho", "painel inválido: " + "; ".join(erros[:3])))
        if ativa:
            if any(m["vencido"] for m in marcos) or (prox is not None and prox < 0):
                motivos.append(("vermelho", "marco vencido"))
            if any(t["vencido"] and t["duro"] for t in minhas_tasks):
                motivos.append(("vermelho", "task com prazo duro vencida"))
            if any(r.get("dias") is not None and r["dias"] < 0 for r in a_receber):
                motivos.append(("vermelho", "a receber vencido"))
            if any(d["prazo"] and dias(iso(d["prazo"])) < 0 for d in minhas_dec):
                motivos.append(("vermelho", "decisão com prazo vencido"))
            if sem_toque is not None and sem_toque > 14 and fase in ("construir", "operar"):
                motivos.append(("vermelho", f"sem toque há {sem_toque} dias"))
            if any(not m["feito"] and 0 <= (m["dias"] if m["dias"] is not None else 99) <= 7 for m in marcos) or (prox is not None and 0 <= prox <= 7):
                motivos.append(("amarelo", "prazo em até 7 dias"))
            if sem_toque is not None and 7 < sem_toque <= 14:
                motivos.append(("amarelo", f"sem toque há {sem_toque} dias"))
            if defasagem > 3:
                motivos.append(("amarelo", f"STATUS mais novo que o painel há {defasagem} dias"))
            if not fm.get("contrato") and fase not in ("prospecto", "proposta"):
                motivos.append(("amarelo", "contrato sem número (n=0)"))
        saude = "vermelho" if any(c == "vermelho" for c, _ in motivos) else ("amarelo" if motivos else "verde")
        saida.append(dict(
            conta=nome, fase=fase, ativa=ativa, projeto=fm.get("projeto", ""), proximo_marco=fm.get("proximo_marco", ""),
            marco_prazo=marco_prazo.isoformat() if marco_prazo else None, marco_dias=prox, marco_dono=fm.get("marco_dono", ""),
            contrato=num(fm.get("contrato")), recebido=num(fm.get("recebido")), recebido_financeiro=round(recebido_fin, 2),
            recorrencia=(fm.get("recorrencia") or "").strip().lower() or None, mensalidade=num(fm.get("mensalidade")),
            risco=fm.get("risco", ""), atualizado=atualizado.isoformat() if atualizado else None,
            ultimo_registro=ult_status.isoformat() if ult_status else None, ultimo_whatsapp=toque_wa.isoformat() if toque_wa else None,
            sem_toque_dias=sem_toque, defasagem_dias=defasagem, marcos=marcos, tasks=minhas_tasks, decisoes=minhas_dec,
            a_receber=a_receber, saude=saude, motivos=[m for _, m in motivos], erros=erros,
            onboarding=onb.calcular(fm, h, fase, ativa, sem_toque, a_receber, marcos),
            tem_painel=tem_painel, tem_status=tem_status,
            conta_mae=os.path.basename(x["fatos"]) if x["sub"] else None,
            arquivos=dict(painel="%s/PAINEL.md" % rel, status="%s/STATUS.md" % x["rel_fatos"],
                          decisoes="%s/DECISOES.md" % x["rel_fatos"])))
    # 12/11/2026 (T-2026-11-11-061): "espera resposta nossa há 3+ dias" — régua do retorno atrasado (ARVORE-ESCRITA §7)
    try:
        import sem_resposta
        espera = sem_resposta.calcular(RAIZ, dt.datetime.now(FUSO).replace(tzinfo=None))
    except Exception as e:  # noqa: BLE001  (o alerta some, o painel não cai)
        print("! sem_resposta:", e)
        espera = []
    espera_conta = {}
    for x in espera:
        espera_conta.setdefault(x["conta"].lower(), x)
    for c in saida:
        x = espera_conta.get(c["conta"].lower())
        c["sem_resposta"] = x
        if x and c["ativa"]:
            c["motivos"].append(x["texto"])
            if x["dias"] >= 7 and c["saude"] != "vermelho":
                c["saude"] = "vermelho"
            elif c["saude"] == "verde":
                c["saude"] = "amarelo"
    casa_tasks = [t for t in todas_tasks if t["conta"].lower() == "casa"]
    for t in casa_tasks:
        d = dias(iso(t["prazo"])) if t["prazo"] else None
        t.update(dias=d, vencido=(d is not None and d < 0))
    # 09/11/2026: aba Entregáveis (PLANO-PRODUCAO-DE-ENTREGAVEIS §6); a fonte é a task tipo: entregavel
    try:
        _se = importlib.util.spec_from_file_location("entregaveis", os.path.join(os.path.dirname(os.path.abspath(__file__)), "entregaveis.py"))
        _ent = importlib.util.module_from_spec(_se); _se.loader.exec_module(_ent)
        entregaveis = _ent.painel()
    except Exception as e:  # noqa: BLE001  (a aba some, o resto do painel não cai)
        print("! entregaveis:", e)
        entregaveis = []
    # 11/11/2026: tela Despachante (despachante_painel.py, que importa as regras do despachar.py)
    try:
        import despachante_painel
        despachante = despachante_painel.montar()
    except Exception as e:  # noqa: BLE001  (a tela avisa que não leu; o resto do painel não cai)
        print("! despachante:", e)
        despachante = dict(erro=str(e))
    comercial = com.montar(RAIZ, contas_fm, h, ler, ultimo_toque_openwa)
    for it in comercial["itens"]:                      # prospect (e conta em proposta) com mensagem sem resposta nossa
        x = espera_conta.get(str(it["nome"]).lower())
        if x and it["etapa"] not in ("aceite", "perdido"):
            it["alertas"].append(dict(nivel=sem_resposta.nivel(x["dias"]), texto=x["texto"], ato=x["ato"]))
    comercial["resumo"]["alertas_vermelhos"] = sum(1 for i in comercial["itens"] for a in i["alertas"] if a["nivel"] == "vermelho")
    comercial["resumo"]["alertas_amarelos"] = sum(1 for i in comercial["itens"] for a in i["alertas"] if a["nivel"] == "amarelo")
    return dict(
        gerado_em=dt.datetime.now(FUSO).strftime("%Y-%m-%d %H:%M"), hoje=h.isoformat(),
        contas=saida, decisoes=todas_dec, tasks_casa=casa_tasks, onboarding=onb.resumo(saida), entregaveis=entregaveis,
        despachante=despachante, sem_resposta=espera,
        comercial=comercial,
        receita=com.receita(saida, fin.get("entradas", []), h, casa,
                            lanc=lambda c, r: do_lanc(por_nome[c["conta"].lower()], r.get("contraparte"), r.get("ref"))
                            if c["conta"].lower() in por_nome else casa(c["conta"], r.get("contraparte"))),
        resumo=dict(contas=len(saida), ativas=sum(1 for c in saida if c["ativa"]),
                    vermelhas=sum(1 for c in saida if c["ativa"] and c["saude"] == "vermelho"),
                    decisoes_abertas=len(todas_dec), sem_painel=[c["conta"] for c in saida if not c["tem_painel"]],
                    invalidas=[c["conta"] for c in saida if c["erros"] and c["tem_painel"]]))


def publicar(payload):
    url, key, tok = (os.environ.get(k) for k in ("FINANCAS_SUPABASE_URL", "FINANCAS_SUPABASE_KEY", "FINANCAS_SYNC_TOKEN"))
    if not (url and key and tok):
        print("⚠️ painel-projetos: FINANCAS_SUPABASE_URL / _KEY / FINANCAS_SYNC_TOKEN ausentes — Supabase não atualizado")
        return 1 if os.environ.get("GITHUB_ACTIONS") else 0
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/rpc/sincronizar_projetos", method="POST",
                                 data=json.dumps(dict(token=tok, payload=payload), ensure_ascii=False).encode("utf-8"),
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("✅ painel-projetos: Supabase atualizado —", r.read().decode()[:200])
            return 0
    except urllib.error.HTTPError as e:
        print("🔴 painel-projetos:", e.code, e.read().decode()[:400])
        return 1
    except (urllib.error.URLError, OSError) as e:
        print("🔴 painel-projetos: sem conexão com o Supabase —", getattr(e, "reason", e))
        return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--verificar", action="store_true")
    ap.add_argument("--publicar", action="store_true")
    ap.add_argument("--teto-defasagem", type=int, default=3)
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    p = montar()
    if a.json:
        io.open(a.json, "w", encoding="utf-8").write(json.dumps(p, ensure_ascii=False, indent=1))
        print("gravado", a.json)
    cor = {"vermelho": "🔴", "amarelo": "🟡", "verde": "🟢", None: "⚪"}
    for c in p["contas"]:
        if not (c["ativa"] or c["erros"] or a.verificar):
            continue
        print(f"{cor.get(c['saude'], '⚪')} {c['conta']:<22} {c['fase'] or '?':<10} marco: {c['proximo_marco'][:48]:<48} "
              f"{('em ' + str(c['marco_dias']) + 'd') if c['marco_dias'] is not None else '':<8} "
              f"{'· ' + ' · '.join(c['motivos']) if c['motivos'] else ''}")
    r = p["resumo"]
    print(f"\n{r['ativas']} ativas de {r['contas']} · {r['vermelhas']} vermelhas · {r['decisoes_abertas']} decisões abertas"
          + (f" · sem PAINEL.md: {', '.join(r['sem_painel'])}" if r["sem_painel"] else "")
          + (f" · inválidas: {', '.join(r['invalidas'])}" if r["invalidas"] else ""))
    rc = 0
    if a.verificar:
        problemas = [c for c in p["contas"] if c["erros"] or (c["ativa"] and c["defasagem_dias"] > a.teto_defasagem)]
        for c in problemas:
            print(f"✗ {c['conta']}: " + "; ".join(c["erros"] or [f"STATUS mais novo que o painel há {c['defasagem_dias']} dias"]))
        print("✅ painéis íntegros" if not problemas else f"🔴 {len(problemas)} conta(s) a corrigir")
        rc = 1 if problemas else 0
    if a.publicar:
        rc = publicar(p) or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
