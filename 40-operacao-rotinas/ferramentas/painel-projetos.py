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
  40-operacao-rotinas/tarefas/*/T-*.md    frontmatter das tasks (conta, prazo, prazo_duro, prioridade, estado)
  40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md   os cartões em "## Abertas"
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
            for k, v in re.findall(r"(o_que|prazo|dono|duro)\s*:\s*(.*?)(?=,\s*(?:o_que|prazo|dono|duro)\s*:|$)", corpo):
                d[k] = v.strip().strip('"').strip("'")
            if not d.get("o_que"):
                erros.append(f"marco sem o_que: {item[:60]}")
                continue
            prazo = iso(d.get("prazo"))
            if d.get("prazo") and not prazo:
                erros.append(f"prazo inválido no marco '{d['o_que'][:40]}': {d.get('prazo')}")
            marcos.append(dict(o_que=d["o_que"], prazo=prazo.isoformat() if prazo else None,
                               dono=d.get("dono") or "", duro=(d.get("duro", "").lower() == "sim")))
            continue
        em_marcos = False
        mm = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", linha)
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
    for k in ("marco_prazo", "atualizado"):
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
    if not os.path.isdir(CLIENTES):
        return []
    return sorted(n for n in os.listdir(CLIENTES)
                  if os.path.isdir(os.path.join(CLIENTES, n)) and not n.startswith(("_", ".")))


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
    t = ler(PENDENTES)
    if "## Abertas" not in t:
        return []
    abertas = t.split("## Abertas", 1)[1].split("## Decididas", 1)[0]
    out = []
    for m in re.finditer(r"^### (D-[\d-]+) · (.*?)$\n((?:(?!^### ).*\n?)*)", abertas, re.M):
        did, cab, corpo = m.group(1), m.group(2), m.group(3)
        partes = [p.strip() for p in cab.split(" · ")]
        conta_titulo = partes[0]
        conta, titulo = (conta_titulo.split(" — ", 1) + [""])[:2]
        tipo = re.search(r"tipo `([^`]+)`", cab)
        auton = re.search(r"autonomia (A\d)", cab)
        prazo = None
        mp = re.search(r"prazo\s*:?\s*(\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", cab)
        if mp:
            prazo = iso(mp.group(1))
        opcoes = [dict(letra=l, texto=x.strip()) for l, x in re.findall(r"^- \*\*([A-C])\)\*\*\s*(.*?)$", corpo, re.M)]
        rec = re.search(r"\*\*Recomendação:\*\*\s*([A-C])", corpo)
        ctx = re.search(r"\*\*Contexto:\*\*\s*(.*?)(?=\n- \*\*[A-C]\)|\n\*\*Recomendação|\Z)", corpo, re.S)
        out.append(dict(id=did, conta=conta.replace("Casa", "casa").strip(), titulo=titulo.strip(), tipo=tipo.group(1) if tipo else None,
                        autonomia=auton.group(1) if auton else None, prazo=prazo.isoformat() if prazo else None,
                        contexto=(ctx.group(1).strip() if ctx else "")[:600], opcoes=opcoes,
                        recomendado=rec.group(1) if rec else None))
    return out


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
    return dict(a_receber=a_receber, recebido=recebido)


def casa(nome, contraparte):
    a, b = nome.lower(), (contraparte or "").lower()
    return a in b or b in a or a.split()[0] in b.split()


# ── montagem ───────────────────────────────────────────────────────────────

def montar():
    h = hoje()
    fin = financeiro()
    todas_tasks = tasks()
    todas_dec = decisoes()
    saida = []
    for nome in contas():
        pasta = os.path.join(CLIENTES, nome)
        painel = os.path.join(pasta, "PAINEL.md")
        status = os.path.join(pasta, "STATUS.md")
        tem_painel, tem_status = os.path.exists(painel), os.path.exists(status)
        fm, erros = (frontmatter(ler(painel)) if tem_painel else (None, ["sem PAINEL.md"]))
        fm = fm or {}
        ult_status = ultima_data_no_texto(ler(status)) if tem_status else None
        toque_wa = ultimo_toque_openwa(pasta)
        atualizado = iso(fm.get("atualizado"))
        toques = [d for d in (ult_status, toque_wa) if d]
        ultimo_toque = max(toques) if toques else None
        fase = fm.get("fase") if fm.get("fase") in FASES else ("arquivada" if not tem_status else None)
        ativa = fase in ATIVAS
        marcos = []
        for mk in fm.get("marcos", []):
            d = dias(iso(mk["prazo"])) if mk["prazo"] else None
            marcos.append(dict(mk, dias=d, vencido=(d is not None and d < 0)))
        minhas_tasks = [t for t in todas_tasks if t["conta"].lower() == nome.lower()]
        for t in minhas_tasks:
            d = dias(iso(t["prazo"])) if t["prazo"] else None
            t.update(dias=d, vencido=(d is not None and d < 0))
        minhas_dec = [d for d in todas_dec if d["conta"].lower() == nome.lower()]
        a_receber = [dict(r, dias=dias(iso(r["vencimento"])) if r.get("vencimento") else None)
                     for r in fin["a_receber"] if casa(nome, r.get("contraparte"))]
        recebido_fin = sum(v for k, v in fin["recebido"].items() if casa(nome, k))
        defasagem = (ult_status - atualizado).days if (ult_status and atualizado and ult_status > atualizado) else 0
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
            if any(0 <= (m["dias"] if m["dias"] is not None else 99) <= 7 for m in marcos) or (prox is not None and 0 <= prox <= 7):
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
            risco=fm.get("risco", ""), atualizado=atualizado.isoformat() if atualizado else None,
            ultimo_registro=ult_status.isoformat() if ult_status else None, ultimo_whatsapp=toque_wa.isoformat() if toque_wa else None,
            sem_toque_dias=sem_toque, defasagem_dias=defasagem, marcos=marcos, tasks=minhas_tasks, decisoes=minhas_dec,
            a_receber=a_receber, saude=saude, motivos=[m for _, m in motivos], erros=erros,
            tem_painel=tem_painel, tem_status=tem_status,
            arquivos=dict(painel="clientes/%s/PAINEL.md" % nome, status="clientes/%s/STATUS.md" % nome,
                          decisoes="clientes/%s/DECISOES.md" % nome)))
    casa_tasks = [t for t in todas_tasks if t["conta"].lower() == "casa"]
    for t in casa_tasks:
        d = dias(iso(t["prazo"])) if t["prazo"] else None
        t.update(dias=d, vencido=(d is not None and d < 0))
    return dict(
        gerado_em=dt.datetime.now(FUSO).strftime("%Y-%m-%d %H:%M"), hoje=h.isoformat(),
        contas=saida, decisoes=todas_dec, tasks_casa=casa_tasks,
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
