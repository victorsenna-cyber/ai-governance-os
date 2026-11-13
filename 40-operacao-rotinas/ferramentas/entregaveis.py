# -*- coding: utf-8 -*-
"""
entregaveis.py — a esteira de produção de entregáveis, mecanizada (N0, sem LLM).
Plano: 60-planos/producao-de-entregaveis/PLANO-PRODUCAO-DE-ENTREGAVEIS.md

O item de promessa é uma task comum de tarefas/ com `tipo: entregavel` (plano §1).

  python3 entregaveis.py --nova --conta "Nome da Conta" --o-que "Tabela de preços por escrito" \
      --destinatario Fulano --forma mensagem --prometido-em 2026-01-06 --prometido-para 2026-01-07 \
      --fonte "DESTILACAO-CALL-2026-01-06-1830.md C12-03 [19:41:12]" [--prazo-duro] [--dinheiro] \
      [--nome "tabela de preços"] [--insumos "a.md; b.md"] [--estado-inicial fila|revisao|decisao]
  python3 entregaveis.py --fila [--json]          elegíveis na ordem do §2, com o teto da rodada
  python3 entregaveis.py --verificar              gate do §7 (V-ENT-1 a V-ENT-7); sai 1 se reprovar
  python3 entregaveis.py --triagem --conta "<C>"  proposta para os marcos do PAINEL.md → tarefas/triagem/<conta>.md
  python3 entregaveis.py --gasto --tokens N --resultado "<texto>"   linha em tarefas/log/GASTO.jsonl
  python3 entregaveis.py --painel [--saida x.json]   JSON dos entregáveis para o painel-projetos.py (§6)
  python3 entregaveis.py --pdf-pendentes          gera, nesta máquina, os PDFs que a nuvem marcou pdf: pendente-local

Nunca envia nada, nunca cria conta: a conta tem que existir em clientes/ ou parceiros/.
"""
import argparse, datetime, importlib.util, io, json, os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FER = os.path.dirname(os.path.abspath(__file__))
TAR = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas")
MOLDE = os.path.join(TAR, "modelos", "entregavel.md")
PASTAS = ("fila", "executando", "revisao", "decisao", "entregue", "falhou")
TZ = datetime.timezone(datetime.timedelta(hours=-3))
FORMAS = ("documento", "mensagem", "artefato", "pacote")
TETO_RODADA = 8            # unidades por rodada; documento e pacote valem 2. Várias unidades por conta na mesma rodada; --teto muda na chamada
PESO = {"documento": 2, "pacote": 2}
VERBOS_PRODUCAO = ("mandar", "enviar", "escrever", "montar", "gerar", "pdf", "mensagem", "colar", "corrigir",
                   "redigir", "preparar", "produzir", "entregar", "recado", "texto")
WIN = os.environ.get("GOVERNANCA_WIN", "")   # caminho da raiz no Windows, se a rotina rodar fora dela

_s = importlib.util.spec_from_file_location("despachar", os.path.join(FER, "despachar.py"))
_d = importlib.util.module_from_spec(_s); _s.loader.exec_module(_d)
Task = _d.Task


def hoje():
    return datetime.datetime.now(TZ).date()


def iso(s):
    try:
        return datetime.date.fromisoformat((s or "").strip()[:10])
    except ValueError:
        return None


def nfc(s):
    return unicodedata.normalize("NFC", s)


def pasta_conta(conta):
    """(base, pasta do PAINEL.md da conta). Subprojeto de cliente (contas_da_casa.py) → a subpasta dele."""
    for base in ("clientes", "parceiros"):
        p = os.path.join(RAIZ, base, conta)
        if os.path.isdir(p):
            return base, p
    sys.path.insert(0, FER)
    import contas_da_casa
    p = contas_da_casa.pasta_da_conta(RAIZ, conta)
    if p:
        return os.path.relpath(p, RAIZ).replace(os.sep, "/").split("/")[0], p
    return None, None


def pasta_dos_fatos(conta):
    """(base, pasta onde moram entregaveis/ e o mapa da Evolution): a conta-mãe, se a conta é subprojeto."""
    base, p = pasta_conta(conta)
    if not p:
        return None, None
    sys.path.insert(0, FER)
    import contas_da_casa
    return base, contas_da_casa.pasta_dos_fatos(RAIZ, p)


def slug(s, n=48):
    s = re.sub(r"[\\/:*?\"<>|]+", " ", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s[:n].rstrip(" .-").lower()


def todas():
    out = []
    for p in PASTAS:
        d = os.path.join(TAR, p)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".md") and f.upper().startswith("T-"):
                try:
                    t = Task(os.path.join(d, f))
                except Exception:
                    continue
                t.pasta = p
                out.append(t)
    return out


def entregaveis():
    return [t for t in todas() if t.get("tipo") == "entregavel"]


# ---------- régua do §2 ----------
def prazo_nosso(prometido_em, prometido_para):
    """Quando o entregável deve estar pronto (plano §2)."""
    h = hoje()
    if prometido_para and prometido_para < h:
        return h, True                                 # vencido: próxima rodada
    if not prometido_para:
        return max(h, prometido_em + datetime.timedelta(days=2)), False
    dias = (prometido_para - prometido_em).days
    if dias <= 4:
        alvo = prometido_em + datetime.timedelta(days=2)
    elif dias <= 14:
        alvo = prometido_em + datetime.timedelta(days=dias // 2)
    else:
        alvo = prometido_para - datetime.timedelta(days=7)
    return max(h, min(alvo, prometido_para)), False


def conta_nova(conta):
    _, p = pasta_conta(conta)
    if not p or not os.path.exists(os.path.join(p, "PAINEL.md")):
        return False
    m = re.search(r"(?m)^onb_d0:\s*(\S+)", io.open(os.path.join(p, "PAINEL.md"), encoding="utf-8").read())
    d0 = iso(m.group(1)) if m else None
    return bool(d0 and 0 <= (hoje() - d0).days <= 14)


def chave_ordem(t):
    pp = iso(t.get("prometido_para"))
    vencido = 0 if (pp and pp < hoje()) else 1
    duro = 0 if t.get("prazo_duro") == "sim" else 1
    dinheiro = 0 if t.get("dinheiro") == "sim" else 1
    nova = 0 if conta_nova(t.get("conta")) else 1
    return (vencido, duro, dinheiro, nova, t.get("prazo") or "9999-12-31", t.get("prometido_em") or "9999-12-31", t.id)


# ---------- --nova ----------
def proximo_id():
    pre = "T-%s-" % hoje().isoformat()
    usados = [int(t.id[len(pre):]) for t in todas() if t.id.startswith(pre) and t.id[len(pre):].isdigit()]
    return "%s%03d" % (pre, max(usados + [0]) + 1)


def linha_readme(dir_ent, conta, nome_pasta, o_que, estado):
    """Acrescenta a linha da pasta no entregaveis/README.md da conta (V-ENT-2). Cria o README se faltar;
    não duplica se o nome da pasta já aparece; preserva CRLF/LF do arquivo."""
    rp = os.path.join(dir_ent, "README.md")
    cab = ("<!-- padrão de entregáveis: subpasta AAAA-MM-DD - nome + linha aqui · conferido por verificar-propagacao.py -->\n"
           "# Entregáveis — %s\n\n"
           "> 🔴 **Toda entrega grava aqui: `entregaveis/AAAA-MM-DD - nome/`, com fonte e PDF juntos, e ganha uma linha neste índice.** "
           "\"Enviado\" só se afirma com registro apontável (captura ou registro de conversa).\n\n"
           "| Data | O quê | Pasta | Estado |\n|---|---|---|---|\n") % conta
    if os.path.exists(rp):
        raw = io.open(rp, "r", encoding="utf-8", newline="").read()
    else:
        raw = cab
    if nfc(nome_pasta) in nfc(raw):
        return False
    nl = "\r\n" if "\r\n" in raw else "\n"
    if nl == "\r\n":
        raw = raw.replace("\r\n", "\n").replace("\n", "\r\n")
    if raw and not raw.endswith("\n"):
        raw += nl
    d = hoje()
    raw += "| %s | %s | `%s/` | %s |%s" % (d.strftime("%d/%m/%Y"), o_que, nome_pasta, estado, nl)
    io.open(rp, "w", encoding="utf-8", newline="").write(raw)
    return True


def nova(a):
    if not (a.fonte or "").strip():
        sys.exit("recusado: fonte vazia. Promessa sem fonte é promessa que alguém imaginou (plano §5.3).")
    if a.forma not in FORMAS:
        sys.exit("forma inválida: use " + ", ".join(FORMAS))
    base, pc = pasta_dos_fatos(a.conta)   # subprojeto: o entregável mora no entregaveis/ da conta-mãe
    if not pc:
        sys.exit("recusado: conta '%s' não existe em clientes/ nem parceiros/ (conta só nasce pelo aceite)." % a.conta)
    pem = iso(a.prometido_em) or hoje()
    ppara = iso(a.prometido_para) if a.prometido_para else None
    prazo, vencido = prazo_nosso(pem, ppara)
    nome = slug(a.nome or a.o_que)
    rel_pasta = "%s/entregaveis/%s - %s" % (nfc(os.path.relpath(pc, RAIZ).replace(os.sep, "/")), hoje().isoformat(), nome)
    arquivo = {"mensagem": "mensagem.md", "artefato": "LEIA-ME.md"}.get(a.forma, slug(nome, 40).replace(" ", "-") + ".html")
    saida = rel_pasta + "/" + arquivo
    tid = proximo_id()
    molde = io.open(MOLDE, encoding="utf-8").read()
    molde = re.sub(r"(?s)^<!--.*?-->\s*", "", molde)
    campos = {
        "<ID>": tid, "<TITULO>": a.o_que.replace("\n", " "), "<HOJE>": hoje().isoformat(), "<PRAZO>": prazo.isoformat(),
        "<PRAZO_DURO>": "sim" if a.prazo_duro else "nao", "<CONTA>": nfc(a.conta), "<ARVORE>": a.arvore,
        "<INSUMOS>": a.insumos or "", "<SAIDA>": saida, "<PRIORIDADE>": "1" if vencido else "2",
        "<PROMETIDO_EM>": pem.isoformat(), "<PROMETIDO_PARA>": ppara.isoformat() if ppara else "",
        "<DESTINATARIO>": a.destinatario, "<FORMA>": a.forma, "<FONTE>": a.fonte.replace("\n", " "),
        "<DINHEIRO>": "sim" if a.dinheiro else "nao", "<ATRASADO>": "sim" if vencido else "nao",
        "<ESTADO>": {"fila": "pronta", "revisao": "pronto", "decisao": "aguardando_operador"}[a.estado_inicial],
        "<PRONTO_EM>": hoje().isoformat() if a.estado_inicial == "revisao" else "",
    }
    for k, v in campos.items():
        molde = molde.replace(k, v)
    if a.dry_run:
        print(molde)
        return 0
    os.makedirs(os.path.join(RAIZ, rel_pasta), exist_ok=True)
    gk = os.path.join(RAIZ, rel_pasta, ".gitkeep")
    if not os.listdir(os.path.join(RAIZ, rel_pasta)):
        io.open(gk, "w").close()
    dest = os.path.join(TAR, a.estado_inicial, tid + ".md")
    io.open(dest, "w", encoding="utf-8", newline="\n").write(molde)
    estado_txt = {"fila": "🟡 em fila · prazo nosso %s" % prazo.strftime("%d/%m"),
                  "revisao": "🟡 pronto · em revisão", "decisao": "🟡 aguardando operador"}[a.estado_inicial]
    linha_readme(os.path.join(RAIZ, nfc(os.path.relpath(pc, RAIZ)), "entregaveis"), nfc(a.conta),
                 os.path.basename(rel_pasta), "%s (%s)" % (a.o_que.replace("\n", " ").replace("|", "/"), tid), estado_txt)
    print("✅ %s em %s/ · prazo nosso %s%s · saída %s" % (tid, a.estado_inicial, prazo.strftime("%d/%m"),
          " · VENCIDO para o cliente" if vencido else "", saida))
    return 0


# ---------- --fila ----------
def fila(como_json=False):
    feitas = {t.id for t in todas() if t.pasta == "entregue"}
    cands, bloq = [], []
    for t in entregaveis():
        if t.pasta != "fila":
            continue
        m = []
        if t.get("estado", "pronta") not in ("pronta", "planejada"):
            m.append("estado=" + t.get("estado"))
        if t.get("nivel_minimo") == "N5":
            m.append("N5 só por sessão")
        falta = [d.strip() for d in t.get("depende_de").split(",") if d.strip() and d.strip() not in feitas]
        if falta:
            m.append("depende de " + ",".join(falta))
        (bloq if m else cands).append((t, "; ".join(m)))
    cands.sort(key=lambda x: chave_ordem(x[0]))
    rodada, contas, usado = [], set(), 0
    for t, _ in cands:
        peso = PESO.get(t.get("forma"), 1)
        if usado + peso > TETO_RODADA:   # várias por conta na mesma rodada
            continue
        rodada.append(t); contas.add(t.get("conta")); usado += peso
    if como_json:
        print(json.dumps([dict(id=t.id, conta=t.get("conta"), titulo=t.get("titulo"), forma=t.get("forma"),
                               prometido_para=t.get("prometido_para"), prazo=t.get("prazo"), saida=t.get("saida"),
                               arquivo=os.path.relpath(t.caminho, RAIZ).replace("\\", "/")) for t in rodada],
                         ensure_ascii=False, indent=2))
        return 0
    print("# Fila de produção de entregáveis · %s · teto %d unidades (documento vale 2), várias por conta\n" % (hoje().strftime("%d/%m/%Y"), TETO_RODADA))
    if not rodada:
        print("fila vazia")
    for i, t in enumerate(rodada, 1):
        pp = t.get("prometido_para") or "sem prazo dito"
        print("%d. %s · %s · %s · prometido para %s · prazo nosso %s\n   task: %s\n   saída: %s" % (
            i, t.id, t.get("conta"), t.get("titulo"), pp, t.get("prazo"),
            os.path.relpath(t.caminho, RAIZ).replace("\\", "/"), t.get("saida")))
    resto = [t for t, _ in cands if t not in rodada]
    if resto:
        print("\nficam para a próxima rodada: " + ", ".join("%s (%s)" % (t.id, t.get("conta")) for t in resto))
    if bloq:
        print("\nbloqueadas: " + "; ".join("%s: %s" % (t.id, m) for t, m in bloq))
    return 0


# ---------- --verificar (V-ENT-1..6, plano §7) ----------
def _marcos(texto):
    m = re.match(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    out = []
    if not m:
        return out
    for l in m.group(1).splitlines():
        s = l.strip()
        if s.startswith("- {") and s.endswith("}"):
            d = dict((k, v.strip().strip('"\'')) for k, v in re.findall(
                r"(o_que|prazo|dono|duro|task)\s*:\s*(.*?)(?=,\s*(?:o_que|prazo|dono|duro|task)\s*:|\}$|$)", s[2:]))
            if d.get("o_que"):
                out.append(d)
    return out


def contas_com_painel():
    """(nome, PAINEL.md) de toda conta com painel, pela regra de contas_da_casa.py (inclui subprojeto)."""
    sys.path.insert(0, FER)
    import contas_da_casa
    for nome, pasta, _ in contas_da_casa.contas(RAIZ):
        p = os.path.join(pasta, "PAINEL.md")
        if os.path.exists(p):
            yield nfc(nome), p


def conferir(raiz=RAIZ):
    """(ok, linhas) — chamado pelo verificar-propagacao.py."""
    falhas, linhas = 0, []
    ents = entregaveis()
    fontes = " ".join(t.get("fonte") for t in ents)
    # V-ENT-1: promessa sem fila (eixo 15 das destilações dos últimos 30 dias)
    limite = datetime.datetime.now().timestamp() - 30 * 86400
    sem = []
    for base in ("clientes", "parceiros"):
        for dp, _, fs in os.walk(os.path.join(raiz, base)):
            if "entregaveis" in dp.split(os.sep) or "OpenWA" in dp or "Evolution" in dp:
                continue
            for f in fs:
                if f.startswith("DESTILACAO") and f.endswith(".md") and os.path.getmtime(os.path.join(dp, f)) >= limite:
                    txt = io.open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
                    # só os IDs DENTRO da seção do eixo 15 (P-<conta>-<n> já existe com outros sentidos em destilações antigas)
                    sec = re.search(r"(?im)^(#+)[^\n]*(eixo 15|o que prometemos)[^\n]*\n(.*?)(?=^\1[^#]|\Z)", txt, re.S | re.M)
                    for pid in sorted(set(re.findall(r"\bP-[A-Za-z0-9]+-\d+\b", sec.group(3) if sec else ""))):
                        if not any(pid in t.get("fonte") and f in t.get("fonte") for t in ents):
                            sem.append("%s (%s)" % (pid, f))
    if sem:
        falhas += 1
        linhas.append("🔴 V-ENT-1 promessa sem fila: " + "; ".join(sem[:12]))
    for t in ents:
        saida = t.get("saida")
        rel = os.path.relpath(t.caminho, raiz).replace("\\", "/")
        if t.pasta == "revisao" and t.get("estado") == "pronto":
            # V-ENT-2
            ok_lugar = bool(re.match(r"^(clientes|parceiros)/[^/]+/entregaveis/\d{4}-\d{2}-\d{2} - ", saida or ""))
            existe = bool(saida) and os.path.exists(os.path.join(raiz, saida))
            readme = ""
            if ok_lugar:
                rp = os.path.join(raiz, "/".join(saida.split("/")[:3]), "README.md")
                readme = io.open(rp, encoding="utf-8").read() if os.path.exists(rp) else ""
            pasta_ent = saida.split("/")[3] if ok_lugar else ""
            if not (ok_lugar and existe and pasta_ent in readme):
                falhas += 1
                linhas.append("🔴 V-ENT-2 pronto sem arquivo: %s (%s%s%s)" % (t.id, "fora de entregaveis/; " if not ok_lugar else "",
                              "arquivo não existe; " if not existe else "", "sem linha no README" if ok_lugar and pasta_ent not in readme else ""))
            # V-ENT-7 (mensagem e entregável na mesma pasta; mensagem preferencialmente concisa): documento e pacote têm o arquivo ao lado da mensagem; mensagem longa avisa
            if ok_lugar and t.get("forma") in ("documento", "pacote") and not arquivo_do_entregavel(saida):
                falhas += 1
                linhas.append("🔴 V-ENT-7 mensagem sem o entregável na pasta: %s (a pasta só tem a mensagem; copiar o arquivo para ela)" % t.id)
            arq_m = _arquivo_de_mensagem(saida) if ok_lugar else None
            if ok_lugar and not arq_m and t.get("forma") != "artefato":
                linhas.append("⚠️ V-ENT-7 pronto sem mensagem.md ao lado: %s" % t.id)
            if arq_m:
                longas = [v["rotulo"] for v in mensagens_do_arquivo(arq_m)["versoes"] if len(v["texto"].split()) > 120]
                if longas:
                    linhas.append("⚠️ V-ENT-7 mensagem longa (>120 palavras): %s (%s)" % (t.id, ", ".join(longas)))
        if t.pasta == "entregue" and t.get("estado") != "descartada":   # descartada (painel ou sessão) não foi enviada
            # V-ENT-3
            if not t.get("enviado_em"):
                falhas += 1
                linhas.append("🔴 V-ENT-3 enviado sem prova: %s sem enviado_em" % t.id)
        # V-ENT-5: atraso mudo
        pe, pp = iso(t.get("pronto_em")), iso(t.get("prometido_para"))
        if pe and pp and pe > pp and "## Ajuste de expectativa" not in t.texto and t.get("ajuste") != "dispensado":
            falhas += 1
            linhas.append("🔴 V-ENT-5 atraso mudo: %s pronto %s, prometido %s, sem ## Ajuste de expectativa" % (t.id, pe.strftime("%d/%m"), pp.strftime("%d/%m")))
        # V-ENT-6: envio pela máquina
        if t.get("enviado_em") and t.get("enviado_por") not in ("painel", "sessao-operador"):
            falhas += 1
            linhas.append("🔴 V-ENT-6 envio pela máquina: %s tem enviado_em sem enviado_por painel|sessao-operador" % t.id)
    # V-ENT-4: marco-promessa solto (aviso; o CEO decide na triagem)
    soltos = []
    for conta, p in contas_com_painel():
        for mk in _marcos(io.open(p, encoding="utf-8").read()):
            o = mk["o_que"].lower().lstrip("✅🔴 ")
            if mk.get("task") or not mk.get("dono", "").lower().startswith(("operador", "claude")):
                continue
            if o.startswith(VERBOS_PRODUCAO) or re.match(r"^(pdf|mensagem|recado|texto)\b", o):
                soltos.append(conta)
    if soltos:
        from collections import Counter
        linhas.append("⚠️ V-ENT-4 marco-promessa sem task: " + ", ".join("%s (%d)" % kv for kv in sorted(Counter(soltos).items())) +
                      " → `entregaveis.py --triagem --conta`")
    prontos = sum(1 for t in ents if t.pasta == "revisao" and t.get("estado") == "pronto")
    linhas.insert(0, "%d entregável(is) na esteira · %d pronto(s) esperando envio" % (len(ents), prontos))
    return falhas == 0, linhas


def verificar():
    ok, linhas = conferir()
    print("\n".join("- " + l for l in linhas))
    print("\n**Esteira:**", "✅" if ok else "🔴 reprovada")
    return 0 if ok else 1


# ---------- --triagem ----------
def triagem(conta):
    _, pc = pasta_conta(conta)
    if not pc or not os.path.exists(os.path.join(pc, "PAINEL.md")):
        sys.exit("conta sem PAINEL.md: " + conta)
    linhas = ["# Triagem dos marcos · %s · %s" % (conta, hoje().strftime("%d/%m/%Y")), "",
              "> Proposta do `entregaveis.py --triagem` (heurística, N0). **O CEO decide**; o gabarito do caso 0 está no plano §9.",
              "> Fronteira (plano §1): *quem faz o próximo ato?* Nós produzimos algo que vai para ele → task `tipo: entregavel`. "
              "Cliente age, ou o operador age sem produzir arquivo → fica marco.", "",
              "| # | Marco | Prazo | Dono | Proposta |", "|---|---|---|---|---|"]
    for i, mk in enumerate(_marcos(io.open(os.path.join(pc, "PAINEL.md"), encoding="utf-8").read()), 1):
        o = mk["o_que"]; ol = o.lower().lstrip("✅🔴 ")
        dono = mk.get("dono", "")
        if mk.get("task"):
            prop = "ponteiro para %s: ok" % mk["task"]
        elif o.startswith("✅") and not re.search(r"\b(falta|resta|pendente)\b", ol):
            prop = "**fecha** (feito; sai do marcos: com registro no STATUS)"
        elif not dono.lower().startswith(("operador", "claude")):
            prop = "fica marco (o próximo ato é de %s)" % (dono or "?")
        elif ol.startswith(VERBOS_PRODUCAO) or re.match(r"^(pdf|mensagem|recado|texto)\b", ol) \
                or re.search(r"\be (mandar|enviar|escrever|montar|gerar|colar|redigir)\b", ol):
            prop = "**vira task entregavel** (conferir se já está pronto: aí nasce em revisao/)"
        elif o.startswith("✅"):
            prop = "**parte feita**: o resto vira task entregavel ou marco, conforme o que falta"
        else:
            prop = "fica marco (ato do operador sem arquivo) — conferir"
        linhas.append("| %d | %s | %s | %s | %s |" % (i, o.replace("|", "/")[:160], mk.get("prazo", ""), dono, prop))
    os.makedirs(os.path.join(TAR, "triagem"), exist_ok=True)
    dest = os.path.join(TAR, "triagem", slug(conta).replace(" ", "-") + ".md")
    io.open(dest, "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
    print("\n".join(linhas))
    print("\n→ gravado em", os.path.relpath(dest, RAIZ).replace("\\", "/"))
    return 0


# ---------- --gasto ----------
def gasto(tokens, resultado, modelo):
    _d.registrar_gasto(dict(task="producao-entregaveis", nivel="N4", modelo=modelo, tokens=int(tokens or 0),
                            resultado=resultado or "", origem="rotina-nuvem"))
    print("✅ gasto registrado em tarefas/log/GASTO.jsonl")
    return 0


# ---------- --painel ----------
_VERSAO = re.compile(r"^\s*(?:-{3}\s*(VERS[ÃA]O[^\n]*?)\s*-{3}|#{2,3}\s+(Vers[ãa]o[^\n]*))\s*$", re.I)


def mensagens_do_arquivo(caminho):
    """As mensagens prontas precisam ser fáceis de enviar ou copiar, no sistema.
    Lê um mensagem.md e devolve {canal, nota, versoes: [{rotulo, texto}]}: a 1ª linha é o canal; o que vem antes de
    "TEXTO PARA COLAR" é bastidor (nota, nunca copiado); "--- VERSÃO X ---" ou "## Versão X" abre versão nova; "---" sozinho
    separa; linha que começa com "> " é nota da versão e não entra no texto copiado."""
    s = io.open(caminho, encoding="utf-8").read().replace("\r\n", "\n")
    linhas = s.split("\n")
    canal, corpo = linhas[0].strip(), linhas[1:]
    nota = []
    for i, l in enumerate(corpo):
        if l.strip().upper().startswith("TEXTO PARA COLAR"):
            nota, corpo = corpo[:i], corpo[i + 1:]
            break
    versoes, rotulo, atual, notas_v = [], "Mensagem", [], []

    def fecha():
        texto = "\n".join(atual).strip()
        if texto:
            versoes.append({"rotulo": rotulo, "texto": texto, "nota": " ".join(notas_v).strip() or None})

    for l in corpo:
        m = _VERSAO.match(l)
        if m:
            fecha()
            rotulo, atual, notas_v = re.sub(r"\s*\(.*$", "", (m.group(1) or m.group(2))).strip(" -#") or "Versão", [], []
        elif l.strip() == "---":
            fecha()
            rotulo, atual, notas_v = "Outra versão", [], []
        elif l.startswith("> "):
            notas_v.append(l[2:].strip())
        else:
            atual.append(l)
    fecha()
    return {"canal": canal, "nota": "\n".join(nota).strip() or None, "versoes": versoes}


def _arquivo_de_mensagem(saida):
    """O mensagem.md do entregável: a própria saída, ou o que está ao lado dela (documento com mensagem de envio)."""
    if not saida:
        return None
    p = os.path.join(RAIZ, saida)
    if saida.endswith("mensagem.md") and os.path.exists(p):
        return p
    lado = os.path.join(os.path.dirname(p), "mensagem.md")
    return lado if os.path.exists(lado) else None


_NAO_E_ENTREGA = re.compile(r"(^mensagem\.md$|^readme\.md$|^folha-interna|\.css$|^\.gitkeep$|-capa\.png$)", re.I)


def _arquivos_da_pasta(pasta_rel):
    """Os arquivos da pasta do entregável: o git (o Action baixa só os .md, mas a árvore vem inteira) + o disco (o que
    ainda não foi commitado). Só o 1º nível; subpasta (fontes/) não é entrega."""
    nomes = set()
    try:
        import subprocess
        r = subprocess.run(["git", "-c", "core.quotepath=false", "ls-tree", "--name-only", "HEAD", pasta_rel.rstrip("/") + "/"],
                           cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", timeout=20)
        for l in r.stdout.splitlines():
            nomes.add(l.strip().strip('"').split("/")[-1])
    except Exception:
        pass
    p = os.path.join(RAIZ, pasta_rel)
    if os.path.isdir(p):
        nomes.update(f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f)))
    return sorted(n for n in nomes if n and "." in n)


def arquivo_do_entregavel(saida):
    """O caminho não pode apontar só para o .md da mensagem: a mensagem e o entregável ficam na mesma pasta. O arquivo que vai ao destinatário, na pasta da saída: PDF > HTML > o resto; nunca a
    mensagem, a folha interna, CSS ou capa. None quando a pasta só tem a mensagem."""
    if not saida:
        return None
    pasta = os.path.dirname(saida)
    nomes = [n for n in _arquivos_da_pasta(pasta) if not _NAO_E_ENTREGA.search(n)]
    if not nomes:
        return None
    base = os.path.splitext(os.path.basename(saida))[0]
    peso = lambda n: ({".pdf": 0, ".html": 1}.get(os.path.splitext(n)[1].lower(), 2 if n.upper() != "LEIA-ME.MD" else 3),
                      os.path.splitext(n)[0] != base, n)
    return pasta + "/" + sorted(nomes, key=peso)[0]


MAPA_EVOLUTION = os.path.join(FER, "evolution", "mapa.json")
_MAPA = None


def _sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn").lower()


def destinos(conta, destinatario):
    """O botão WhatsApp chama a Evolution e envia a mensagem por ela: as conversas da conta
    no mapa da Evolution, para o popup escolher a quem vai. Só jid, nome e tipo: telefone que não está no jid não sai daqui
    (a ponte na VPS resolve o @lid pelo mapa do clone). Padrão: a privada cujo nome casa com o destinatário, senão a
    privada da conta, senão o grupo."""
    global _MAPA
    if _MAPA is None:
        try:
            _MAPA = json.load(io.open(MAPA_EVOLUTION, encoding="utf-8")).get("conversas") or []
        except Exception:  # noqa: BLE001
            _MAPA = []
    _, pc = pasta_conta(conta) if conta else (None, None)   # subprojeto conversa pelas conversas da mãe
    sys.path.insert(0, FER)
    import contas_da_casa
    mae =os.path.basename(os.path.dirname(os.path.normpath(pc))) if pc and contas_da_casa.eh_subprojeto(RAIZ, pc) else None
    alvo = _sem_acento(nfc(mae or conta or ""))
    lista = [dict(jid=c["jid"], nome=c.get("nome") or c["jid"], tipo=c.get("tipo") or "privada") for c in _MAPA
             if _sem_acento(c.get("pasta")) == alvo and c.get("relacao") != "ignorar" and c.get("jid")]
    lista.sort(key=lambda c: (c["tipo"] != "privada", c["nome"]))
    quem = _sem_acento(destinatario).split()
    padrao = next((c["jid"] for c in lista if c["tipo"] == "privada" and quem and quem[0] in _sem_acento(c["nome"]).split()), None) \
        or next((c["jid"] for c in lista if c["tipo"] == "privada"), None) or (lista[0]["jid"] if lista else None)
    return lista, padrao


def _win(rel):
    return (WIN + "\\" + rel.replace("/", "\\")) if rel else None


def _etapa(t):
    """Onde o entregável está na esteira, para a barra de progresso da aba Entregáveis:
    0 prometido (fila, ainda não pego) · 1 em produção (executando) · 2 esperando operador (decisao) ·
    3 pronto (revisao) · 4 enviado (entregue). Descartado é -1."""
    if t.get("estado") == "descartada":
        return -1
    return {"fila": 0, "executando": 1, "decisao": 2, "revisao": 3, "entregue": 4, "falhou": 1}.get(t.pasta, 0)


def _rascunhos(saida):
    """Os rascunhos do operador (RASCUNHOS.md, rascunhos_do_painel.py) que já estão no repo: data, id e o começo do texto."""
    if not saida:
        return []
    arq = os.path.join(RAIZ, os.path.dirname(saida), "RASCUNHOS.md")
    if not os.path.isfile(arq):
        return []
    partes = re.split(r"^## ", io.open(arq, encoding="utf-8").read(), flags=re.M)[1:]
    out = []
    for p in partes:
        cab, _, corpo = p.partition("\n")
        m = re.match(r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}) · rascunho (R-\d+)", cab)
        if m:
            out.append(dict(quando=m.group(1), id=m.group(2), texto=corpo.strip()[:600]))
    return out


def painel():
    out = []
    corte = hoje() - datetime.timedelta(days=30)
    for t in entregaveis():
        if t.pasta == "entregue" and (iso(t.get("enviado_em")) or hoje()) < corte:
            continue
        grupo = {"revisao": "prontos" if t.get("estado") == "pronto" else "em_producao", "entregue": "enviados"}.get(t.pasta, "em_producao")
        pp = iso(t.get("prometido_para"))
        saida = t.get("saida")
        texto, msg = None, None
        arq = _arquivo_de_mensagem(saida) if grupo == "prontos" else None
        if arq:
            msg = mensagens_do_arquivo(arq)
            texto = io.open(arq, encoding="utf-8").read()
        arq_ent = arquivo_do_entregavel(saida)   # mensagem que leva anexo (o PDF do Max) também mostra o anexo
        dest, dest_padrao = destinos(t.get("conta"), t.get("destinatario")) if grupo == "prontos" else ([], None)
        out.append(dict(
            id=t.id, grupo=grupo, pasta=t.pasta, titulo=t.get("titulo"), conta=t.get("conta"), destinatario=t.get("destinatario"),
            forma=t.get("forma"), prometido_em=t.get("prometido_em") or None, prometido_para=t.get("prometido_para") or None,
            prazo=t.get("prazo") or None, folga_dias=(pp - hoje()).days if pp else None, pronto_em=t.get("pronto_em") or None,
            enviado_em=t.get("enviado_em") or None, atrasado=t.get("atrasado") == "sim", hipotese=t.get("hipotese") == "sim",
            bloqueio=t.get("bloqueio") or (t.get("estado") if t.pasta == "decisao" else None),
            saida=saida, caminho_windows=_win(saida),
            arquivo=arq_ent, arquivo_windows=_win(arq_ent), pasta_windows=_win(os.path.dirname(saida)) if saida else None,
            anexo=arq_ent if (arq_ent or "").lower().endswith(".pdf") else None,   # HTML não é anexo: sem PDF vai só o texto
            destinos=dest, destino_padrao=dest_padrao,
            fonte=t.get("fonte"), texto=texto, mensagem=msg,
            estado=t.get("estado") or None, etapa=_etapa(t), rascunhos=_rascunhos(saida),
            task=os.path.relpath(t.caminho, RAIZ).replace("\\", "/")))
    ordem = {"prontos": 0, "em_producao": 1, "enviados": 2}
    out.sort(key=lambda e: (ordem[e["grupo"]], e["prometido_para"] or "9999", e["id"]))
    return out


# ---------- --pdf-pendentes (task N0 horária gerar-pdf-pendentes, plano §4.5) ----------
def pdf_pendentes():
    import subprocess
    gerador = os.path.join(RAIZ, "90-templates", "pdf-noturno", "gerar_pdf.py")
    feitos = falhos = 0
    for t in entregaveis():
        if t.get("pdf") != "pendente-local":
            continue
        pasta = os.path.dirname(os.path.join(RAIZ, t.get("saida") or ""))
        htmls = [f for f in os.listdir(pasta) if f.endswith(".html")] if os.path.isdir(pasta) else []
        if not htmls:
            print("! %s: pdf pendente sem .html em %s" % (t.id, pasta)); falhos += 1; continue
        ok = True
        for h in htmls:
            r = subprocess.run([sys.executable, "-X", "utf8", gerador, os.path.join(pasta, h)], capture_output=True, text=True)
            ok = ok and r.returncode == 0
            print(("✅ " if r.returncode == 0 else "🔴 ") + os.path.relpath(os.path.join(pasta, h), RAIZ))
        if ok:
            t.set("pdf", "gerado"); t.log("PDF gerado localmente pelo gerar_pdf.py (gerar-pdf-pendentes)"); t.salvar(); feitos += 1
        else:
            t.log("gerar_pdf.py reprovou o PDF; conferir a fonte"); t.salvar(); falhos += 1
    print("pdf pendentes: %d gerado(s), %d com falha" % (feitos, falhos))
    return 1 if falhos else 0


def main():
    ap = argparse.ArgumentParser(description="Esteira de produção de entregáveis (plano de produção de entregáveis).")
    g = ap.add_mutually_exclusive_group(required=True)
    for f in ("--nova", "--fila", "--verificar", "--triagem", "--gasto", "--painel", "--pdf-pendentes"):
        g.add_argument(f, action="store_true")
    ap.add_argument("--conta"); ap.add_argument("--o-que"); ap.add_argument("--destinatario", default="")
    ap.add_argument("--forma", default="mensagem"); ap.add_argument("--prometido-em"); ap.add_argument("--prometido-para")
    ap.add_argument("--fonte"); ap.add_argument("--nome"); ap.add_argument("--insumos")
    ap.add_argument("--arvore", default="ESCRITA"); ap.add_argument("--prazo-duro", action="store_true")
    ap.add_argument("--dinheiro", action="store_true"); ap.add_argument("--estado-inicial", default="fila", choices=("fila", "revisao", "decisao"))
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--tokens"); ap.add_argument("--resultado"); ap.add_argument("--modelo", default="claude-opus-5-5")
    ap.add_argument("--saida"); ap.add_argument("--teto", type=int)
    a = ap.parse_args()
    if a.nova:
        if not (a.conta and a.o_que):
            sys.exit("--nova precisa de --conta e --o-que")
        return nova(a)
    if a.teto:
        global TETO_RODADA; TETO_RODADA = a.teto
    if a.fila:
        return fila(a.json)
    if a.verificar:
        return verificar()
    if a.triagem:
        if not a.conta:
            sys.exit("--triagem precisa de --conta")
        return triagem(a.conta)
    if a.gasto:
        return gasto(a.tokens, a.resultado, a.modelo)
    if a.pdf_pendentes:
        return pdf_pendentes()
    if a.painel:
        dados = painel()
        j = json.dumps(dados, ensure_ascii=False, indent=2)
        if a.saida:
            io.open(a.saida, "w", encoding="utf-8").write(j)
            print("✅ %d entregáveis → %s" % (len(dados), a.saida))
        else:
            print(j)
        return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
