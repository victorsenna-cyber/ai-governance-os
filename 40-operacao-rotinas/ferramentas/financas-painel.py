#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
financas-painel.py — os .md de finanças viram as tabelas do painel (Supabase).

Fonte única continua sendo o repositório. Este script só LÊ:
  940-operador/FINANCAS.md               §1 caixa conferido · §3 entradas previstas
                                       §4 registro diário · §5 dívidas · §6 a conciliar
  45-financeiro/LANCAMENTOS-EMPRESA.md A receber · Receitas · Despesas
  45-financeiro/extratos/*.csv         extrato {{BANCO}}, linha a linha, classificado por extratos/CLASSIFICACAO.md
  940-operador/cartao-compartilhado/CARTAO-COMPARTILHADO.md  compras num cartão de terceiro, se houver (só as pessoais;
                                       as ferramentas já estão em Despesas da empresa)
e publica uma cópia em Supabase (projeto <projeto-supabase>), que o painel lê.

Uso:
  python3 40-operacao-rotinas/ferramentas/financas-painel.py            # resumo
  python3 40-operacao-rotinas/ferramentas/financas-painel.py --json X   # grava o payload
  python3 40-operacao-rotinas/ferramentas/financas-painel.py --publicar # envia ao Supabase

--publicar lê do ambiente: FINANCAS_SUPABASE_URL, FINANCAS_SUPABASE_KEY (publishable)
e FINANCAS_SYNC_TOKEN. Sem eles, avisa e sai 0 (não quebra a rotina) — menos dentro do
GitHub Action, onde sai 1: Action verde sem atualizar o Supabase esconde o painel parado.
Roda sozinho no GitHub Action .github/workflows/financas-painel.yml a cada push na main
que mexa num dos dois .md.

Regras de leitura (o que o script entende como cada coisa):
  §4  linha com Entrou → entrada; com Saiu → saída. "Em quê" = "<contraparte> — <detalhe> · <categoria> · Pix <id>".
  §5  linha cujo 1º campo começa com ~~ ou cujo estado tem ✅ = quitada, fica de fora.
  §5-bis  multa e juros de mora por credor (vão em meta.encargos; o cálculo é do painel, dia a dia).
      valor "N/dia" = diária (projetada HORIZONTE dias); "N/mês" = mensal entre as duas datas.
  §3  data sem ano recebe o ano corrente. Linha riscada (~~) fica de fora.
  A receber (empresa)  linha riscada ou com ✅ = recebido, fica de fora; o dinheiro está em Receitas.
  conta = "empresa" quando a contraparte bate com o nome inteiro de uma pasta de clientes/.
  meio  "conta" (passou pela conta {{BANCO}}) ou "cartão de terceiro". Só "conta" mexe no caixa; DRE e categorias
      contam tudo. Despesa da empresa cujo id começa com "cartão de terceiro" é meio cartão.
  extrato  movimento igual (dia, sentido, valor) a um lançamento dos .md some: vale a linha do .md, mais rica.
"""
import argparse, csv, datetime as dt, glob, hashlib, io, json, os, re, sys, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PESSOAL = os.path.join(RAIZ, "940-operador", "FINANCAS.md")
EMPRESA = os.path.join(RAIZ, "45-financeiro", "LANCAMENTOS-EMPRESA.md")
EXTRATOS = os.path.join(RAIZ, "45-financeiro", "extratos")
CARTAO_COMPARTILHADO = os.path.join(RAIZ, "940-operador", "cartao-compartilhado", "CARTAO-COMPARTILHADO.md")
CATEGORIA_CARTAO = {"mercado e comida": "alimentação", "cuidado": "cuidado pessoal"}  # tipo do cartão → categoria do extrato
HORIZONTE = 30  # dias de recorrência diária projetados à frente

CATEGORIAS = [  # palavra no texto → categoria, para linhas antigas sem categoria explícita
    (r"aluguel|moradia|condom[ií]nio", "moradia"),
    (r"empr[eé]stimo", "empréstimo"),
    (r"mercado|comida|farm[aá]cia|restaurante", "alimentação"),
    (r"uber|99|[ôo]nibus|transporte", "transporte"),
    (r"meta|facebook|instagram|google ads", "mídia"),
    (r"anthropic|claude|openai|vercel|hostinger|supabase|github|canva|zapsign", "ferramenta"),
    (r"parcelamento|renegocia[cç][aã]o", "dívida"),
]


def hoje():
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=-3))).date()


def limpar(s):
    s = re.sub(r"~~.*?~~", "", s)
    return re.sub(r"\*\*|`", "", s).strip()


def num(s):
    m = re.search(r"\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?|\d+(?:,\d{1,2})?", limpar(s))
    return float(m.group(0).replace(".", "").replace(",", ".")) if m else None


def data(s, ano=None):
    """'24/10 22:22' ou '24/10/2026 22:22' → (date, 'HH:MM' | None)."""
    m = re.search(r"(\d{1,2})/(\d{1,2})(?:/(\d{4}))?(?:\s+(\d{1,2}[:h]\d{2}))?", s)
    if not m:
        return None, None
    d, mth, a, h = m.groups()
    a = int(a) if a else (ano or hoje().year)
    try:
        dia = dt.date(a, int(mth), int(d))
    except ValueError:
        return None, None
    if not m.group(3) and dia > hoje() + dt.timedelta(days=200):
        dia = dia.replace(year=a - 1)
    return dia, (h.replace("h", ":").zfill(5) if h else None)


def datas(s):
    return [dt.date(int(a), int(m), int(d)) for d, m, a in re.findall(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)]


def secao(texto, titulo):
    """Texto de uma seção ## que começa com `titulo` (até a próxima ##)."""
    m = re.search(r"^##\s+" + re.escape(titulo) + r".*?$(.*?)(?=^##\s|\Z)", texto, re.M | re.S)
    return m.group(1) if m else ""


def tabela(trecho):
    linhas = [l.strip() for l in trecho.splitlines() if l.strip().startswith("|")]
    out = []
    for l in linhas[2:]:  # pula cabeçalho e separador
        cel = [c.strip() for c in l.strip("|").split("|")]
        if any(cel):
            out.append(cel)
    return out


def categoria(txt):
    for rx, cat in CATEGORIAS:
        if re.search(rx, txt, re.I):
            return cat
    return "outros"


def ident(*partes):
    return hashlib.sha1("|".join(str(p) for p in partes).encode()).hexdigest()[:16]


def clientes():
    """Nomes das pastas de clientes/ — pelo git (funciona em checkout parcial) ou pelo disco."""
    r = os.popen(f'git -C "{RAIZ}" -c core.quotepath=off ls-tree -d --name-only HEAD clientes/ 2>/dev/null').read()
    nomes = [os.path.basename(l.strip()) for l in r.splitlines() if l.strip()]
    p = os.path.join(RAIZ, "clientes")
    if not nomes and os.path.isdir(p):
        nomes = os.listdir(p)
    return [n for n in nomes if not n.startswith(("_", ".")) and n != "{{OPERADOR}}"]


def conta_de(nome, lista):
    n = nome.lower()
    return "empresa" if any(c.lower() in n for c in lista) else "pessoal"


# ── leitura ────────────────────────────────────────────────────────────────

def ler_registro(texto):
    out = []
    for cel in tabela(secao(texto, "4.")):
        if len(cel) < 4:
            continue
        dia, hora = data(cel[0])
        if not dia:
            continue
        entrou, saiu = num(cel[1]) if cel[1] not in ("—", "-", "") else None, num(cel[2]) if cel[2] not in ("—", "-", "") else None
        partes = [p.strip() for p in limpar(cel[3]).split(" · ")]
        pix = next((p[4:].strip() for p in partes if p.lower().startswith("pix ")), None)
        pix = None if pix in (None, "—", "-") else pix
        resto = [p for p in partes if not p.lower().startswith("pix ")]
        cabeca = resto[0] if resto else ""
        contraparte, _, detalhe = cabeca.partition(" — ")
        cat = resto[1] if len(resto) > 1 else categoria(cabeca)
        for sentido, valor in (("entrada", entrou), ("saida", saiu)):
            if valor:
                out.append(dict(id=pix or ident("p", dia, hora, sentido, valor, cabeca), data=dia.isoformat(), hora=hora,
                                conta="pessoal", sentido=sentido, valor=valor, contraparte=contraparte.strip(),
                                detalhe=detalhe.strip() or None, categoria=cat, ref=pix, origem="940-operador/FINANCAS.md §4", meio="conta"))
    return out


def ler_empresa(texto):
    out = []
    for titulo, sentido in (("Receitas", "entrada"), ("Despesas", "saida")):
        for cel in tabela(secao(texto, titulo)):
            if len(cel) < 5:
                continue
            dia, hora = data(cel[0])
            valor = num(cel[1])
            if not (dia and valor):
                continue
            ref = cel[3] if sentido == "entrada" else None
            cat = "receita de cliente" if sentido == "entrada" else (limpar(cel[3]) or categoria(cel[2]))
            gid = limpar(cel[4]) or None
            out.append(dict(id=gid or ident("e", dia, hora, sentido, valor, cel[2]), data=dia.isoformat(), hora=hora,
                            conta="empresa", sentido=sentido, valor=valor, contraparte=limpar(cel[2]), detalhe=None,
                            categoria=cat, ref=None if ref in (None, "—", "-", "") else limpar(ref),
                            origem="45-financeiro/LANCAMENTOS-EMPRESA.md " + titulo,
                            meio="cartão de terceiro" if (gid or "").startswith("cartão de terceiro") else "conta"))
    return out


def ler_conciliar(texto):
    out = []
    for cel in tabela(secao(texto, "6.")):
        if len(cel) < 6:
            continue
        dia, hora = data(cel[0])
        valor = num(cel[1])
        if not (dia and valor):
            continue
        sentido = "entrada" if "entr" in cel[2].lower() else "saida"
        out.append(dict(id=limpar(cel[5]) or ident("c", dia, hora, valor, cel[3]), data=dia.isoformat(), hora=hora,
                        conta="conciliar", sentido=sentido, valor=valor, contraparte=limpar(cel[3]),
                        detalhe=limpar(cel[4]), categoria="a conciliar", ref=None, origem="940-operador/FINANCAS.md §6", meio="conta"))
    return out


def ler_classificacao():
    """extratos/CLASSIFICACAO.md: padrão (regex) → contraparte, categoria, conta. `\\|` é alternância, não coluna."""
    p = os.path.join(EXTRATOS, "CLASSIFICACAO.md")
    out = []
    if not os.path.exists(p):
        return out
    for l in io.open(p, encoding="utf-8"):
        if not l.startswith("|"):
            continue
        cel = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l.strip().strip("|"))]
        if len(cel) < 4 or cel[0] in ("Padrão", "") or set(cel[0]) <= set("-: "):
            continue
        out.append((re.compile(cel[0], re.I), cel[1], cel[2], cel[3]))
    return out


def ler_extratos():
    """45-financeiro/extratos/*.csv (Data,Valor,Identificador,Descrição) → lançamentos meio conta."""
    regras, out = ler_classificacao(), []
    for f in sorted(glob.glob(os.path.join(EXTRATOS, "*.csv"))):
        for r in csv.DictReader(io.open(f, encoding="utf-8")):
            d, m, a = r["Data"].split("/")
            v = float(r["Valor"])
            desc = r["Descrição"].strip()
            tipo, _, resto = desc.partition(" - ")
            nome = resto.split(" - ")[0].strip() or tipo
            cp, cat, conta = nome, "a classificar", "pessoal"
            for rx, c, k, ct in regras:
                if rx.search(desc):
                    cp, cat, conta = (nome if c in ("—", "-", "") else c), k, ct
                    break
            # Pix no crédito: a entrada do crédito e o Pix enviado dividem o Identificador
            out.append(dict(id="ext-" + r["Identificador"] + ("-e" if v > 0 else "-s"), data=f"{a}-{m}-{d}", hora=None, conta=conta,
                            sentido="entrada" if v > 0 else "saida", valor=round(abs(v), 2), contraparte=cp,
                            detalhe=desc, categoria=cat, ref=None, origem="45-financeiro/extratos/" + os.path.basename(f),
                            meio="conta"))
    return out


def ler_cartao_compartilhado():
    """CARTAO-COMPARTILHADO.md, LANÇAMENTOS: só as compras pessoais (as ferramentas estão em Despesas da empresa)."""
    if not os.path.exists(CARTAO_COMPARTILHADO):
        return []
    texto = io.open(CARTAO_COMPARTILHADO, encoding="utf-8").read()
    trecho = texto.split("## LANÇAMENTOS", 1)[-1] if "## LANÇAMENTOS" in texto else ""
    out = []
    for bloco in trecho.split("### ")[1:]:
        for cel in tabela(bloco):
            if len(cel) < 5:
                continue
            dia, _ = data(cel[0] + "/2026")
            valor = num(cel[3])
            tipo = limpar(cel[4])
            if not (dia and valor) or not tipo.startswith("pessoal"):
                continue
            sub = tipo.partition("·")[2].strip()
            out.append(dict(id=ident("cv", dia, cel[1], valor, cel[2]), data=dia.isoformat(), hora=cel[1] or None,
                            conta="pessoal", sentido="saida", valor=valor, contraparte=limpar(cel[2]),
                            detalhe="cartão de terceiro · " + limpar(cel[5] if len(cel) > 5 else ""),
                            categoria=CATEGORIA_CARTAO.get(sub, sub or "outros"), ref=None,
                            origem="940-operador/cartao-compartilhado/CARTAO-COMPARTILHADO.md", meio="cartão de terceiro"))
    return out


def sem_duplicata(extrato, md):
    """Tira do extrato o que já está nos .md (mesmo dia, sentido e valor, um para um)."""
    vistos = {}
    for l in md:
        if l.get("meio") == "conta":
            k = (l["data"], l["sentido"], round(l["valor"], 2))
            vistos[k] = vistos.get(k, 0) + 1
    out, iguais = [], 0
    for l in extrato:
        k = (l["data"], l["sentido"], l["valor"])
        if vistos.get(k):
            vistos[k] -= 1
            iguais += 1
        else:
            out.append(l)
    return out, iguais


def ler_dividas(texto, lista):
    out, h = [], hoje()
    for cel in tabela(secao(texto, "5.").split("### ")[0]):  # só a tabela de dívidas, antes da §5-bis
        if len(cel) < 5 or cel[0].startswith("~~") or "✅" in cel[4]:
            continue
        nome = limpar(cel[0])
        contraparte, _, desc = nome.partition(" — ")
        valor = num(cel[1])
        if not valor:
            continue
        bruto = limpar(cel[1]).lower()
        recorr = "diaria" if "/dia" in bruto else "mensal" if "/m" in bruto else None
        ds = datas(cel[2])
        estado = limpar(cel[4])
        limite = None
        m = re.search(r"(?:prazo(?: real| pedido)?|até)\s+(\d{1,2}/\d{1,2}(?:/\d{4})?)", limpar(cel[3]) + " " + estado)
        if m:
            limite = data(m.group(1))[0]
        base = dict(tipo="pagar", conta=conta_de(contraparte, lista), contraparte=contraparte.strip(),
                    estado=estado, certeza=None, nota=limpar(cel[3]), origem="940-operador/FINANCAS.md §5")
        if recorr == "diaria" and ds:
            ini = max(ds[0], h)
            for i in range(HORIZONTE):
                d = ini + dt.timedelta(days=i)
                out.append(dict(base, id=ident("d", nome, d), descricao=f"diária · dia {d:%d/%m}",
                                valor=valor, vencimento=d.isoformat(), recorrencia="diaria", limite=None))
        elif recorr == "mensal" and ds:
            fim = ds[1] if len(ds) > 1 else ds[0]
            n0 = re.search(r"parcelas?\s+(\d+)", desc)
            n = int(n0.group(1)) if n0 else 1
            d = ds[0]
            while d <= fim:
                out.append(dict(base, id=ident("m", nome, d), descricao=f"{re.sub(r',?\s*parcelas?\s+\d+\s+a\s+\d+', '', desc).strip() or 'parcela'} · parcela {n}",
                                valor=valor, vencimento=d.isoformat(), recorrencia="mensal", limite=None))
                n += 1
                d = (d.replace(day=1) + dt.timedelta(days=32)).replace(day=d.day)
        else:
            venc = ds[0] if ds and "venc" in cel[2].lower() else None
            out.append(dict(base, id=ident("u", nome), descricao=desc or None, valor=valor,
                            vencimento=venc.isoformat() if venc else None, recorrencia=None,
                            limite=limite.isoformat() if limite else None))
    return out


def ler_a_receber(texto):
    """LANCAMENTOS-EMPRESA.md, A receber: o combinado com cliente. Linha riscada ou com ✅ = recebido, fica de fora
    (o dinheiro já está em Receitas)."""
    out = []
    for cel in tabela(secao(texto, "A receber")):
        if len(cel) < 5 or cel[0].startswith("~~") or "✅" in cel[4]:
            continue
        valor = num(cel[1])
        if not valor:
            continue
        quando = limpar(cel[0])
        dia = data(quando)[0] if re.search(r"\d/\d", quando) else None
        contraparte, desc = limpar(cel[2]), limpar(cel[3])
        out.append(dict(id=ident("r", contraparte, desc), tipo="receber", conta="empresa", contraparte=contraparte,
                        descricao=desc or None, valor=valor, vencimento=dia.isoformat() if dia else None,
                        recorrencia="mensal" if "mensal" in quando.lower() else None, limite=None, estado=quando,
                        certeza=limpar(cel[4]), nota=None, origem="45-financeiro/LANCAMENTOS-EMPRESA.md A receber"))
    return out


def ler_previstas(texto, lista):
    out = []
    for cel in tabela(secao(texto, "3.")):
        if len(cel) < 4 or cel[0].startswith("~~"):
            continue
        valor = num(cel[2])
        if not valor:
            continue
        nome = limpar(cel[1])
        contraparte, _, desc = nome.partition(" — ")
        quando = limpar(cel[0])
        dia = data(quando)[0] if re.search(r"\d/\d", quando) else None
        recorr = "mensal" if "mensal" in quando.lower() else None
        out.append(dict(id=ident("r", nome), tipo="receber", conta=conta_de(contraparte, lista),
                        contraparte=contraparte.strip(), descricao=desc or None, valor=valor,
                        vencimento=dia.isoformat() if dia else None, recorrencia=recorr, limite=None,
                        estado=quando, certeza=limpar(cel[3]), nota=None, origem="940-operador/FINANCAS.md §3"))
    return out


def ler_encargos(texto):
    """§5-bis: multa e juros de mora por credor; o painel aplica sobre o que está vencido."""
    m = re.search(r"^###\s+5-bis.*?$(.*?)(?=^##|\Z)", texto, re.M | re.S)
    out = []
    for cel in tabela(m.group(1) if m else ""):
        if len(cel) >= 3 and num(cel[1]) is not None:
            out.append(dict(contraparte=limpar(cel[0]), multa=num(cel[1]) / 100, juros_am=(num(cel[2]) or 0) / 100))
    return out


def ler_caixa(texto):
    for cel in tabela(secao(texto, "1.")):
        if "caixa" in cel[0].lower() and len(cel) > 1:
            v = num(cel[1])
            ds = re.findall(r"\d{1,2}/\d{1,2}(?:/\d{4})?", limpar(cel[1]))
            dia = data(ds[-1])[0] if ds else None
            return dict(valor=v, data=dia.isoformat() if dia else None, texto=limpar(cel[1]))
    return dict(valor=None, data=None, texto=None)


def montar():
    tp = io.open(PESSOAL, encoding="utf-8").read()
    te = io.open(EMPRESA, encoding="utf-8").read() if os.path.exists(EMPRESA) else ""
    lista = clientes()
    md = ler_registro(tp) + ler_empresa(te)
    extrato, iguais = sem_duplicata(ler_extratos(), md)
    lanc = md + extrato + ler_cartao_compartilhado() + ler_conciliar(tp)
    contas = ler_dividas(tp, lista) + ler_previstas(tp, lista) + ler_a_receber(te)
    agora = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    commit = os.environ.get("GITHUB_SHA") or os.popen(f'git -C "{RAIZ}" rev-parse --short HEAD 2>/dev/null').read().strip()
    fim_extrato = max((l["data"] for l in extrato), default=None)
    meta = dict(caixa_conferido=ler_caixa(tp), encargos=ler_encargos(tp), gerado_em=agora, commit=commit or None, horizonte_diarias=HORIZONTE,
                extrato=dict(linhas=len(extrato), iguais_aos_md=iguais, ate=fim_extrato))
    return dict(lancamentos=lanc, contas=contas, meta=meta)


def publicar(payload):
    url, key, tok = (os.environ.get(k) for k in ("FINANCAS_SUPABASE_URL", "FINANCAS_SUPABASE_KEY", "FINANCAS_SYNC_TOKEN"))
    if not (url and key and tok):
        print("⚠️ financas-painel: FINANCAS_SUPABASE_URL / _KEY / FINANCAS_SYNC_TOKEN ausentes — Supabase não atualizado")
        return 1 if os.environ.get("GITHUB_ACTIONS") else 0
    req = urllib.request.Request(url.rstrip("/") + "/rest/v1/rpc/sincronizar_financas", method="POST",
                                 data=json.dumps(dict(token=tok, payload=payload)).encode(),
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("✅ financas-painel: Supabase atualizado —", r.read().decode()[:200])
            return 0
    except urllib.error.HTTPError as e:
        print("🔴 financas-painel:", e.code, e.read().decode()[:400])
        return 1
    except (urllib.error.URLError, OSError) as e:
        print("🔴 financas-painel: sem conexão com o Supabase —", getattr(e, "reason", e))
        return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    ap.add_argument("--publicar", action="store_true")
    a = ap.parse_args()
    p = montar()
    if a.json:
        io.open(a.json, "w", encoding="utf-8").write(json.dumps(p, ensure_ascii=False, indent=1))
    if a.publicar:
        sys.exit(publicar(p))
    print(f"lançamentos: {len(p['lancamentos'])} · contas: {len(p['contas'])} · caixa conferido: {p['meta']['caixa_conferido']}")


if __name__ == "__main__":
    main()
