#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render.py — renderiza as peças do sistema visual da marca.

Tipo: blueprint (ferramenta do sistema) · Regra: ../IDENTIDADE-VISUAL.md
Uso:   python3 render.py pecas.json [pasta_de_saida]
       pecas.json pode ser uma lista de peças (a casa) ou um kit de conta:
       {"tokens": "tokens.css", "fontes_url": "<Google Fonts>", "combos": {"A": {"--f-display": ..., "--t": "110px"}},
        "assinatura": "@conta", "fundo": "claro", "pecas": [...]}   (caminhos relativos ao JSON)
       Kit de conta: 90-templates/kit-de-marca/ (gerar_kit.py chama este motor).
       cada item do JSON: {"id", "tipo": N1|N2|N3|P1|P2|B1|C1|D1|F1 (retrato, "foto"), "formato": feed|story,
                            "combo": A|B|C|D, ...campos do tipo}
Saída: <id>.html e <id>.png (1080×1350 feed, 1080×1920 story), pelo Chrome sem interface.
Os PNG não entram no git: se regeneram daqui.
"""
import html, io, json, os, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, "..", "..", "..", "40-operacao-rotinas", "ferramentas")))
from navegador import chrome_path  # noqa: E402  Chrome em Windows, macOS e Linux (ou CHROME=<caminho>)
CHROME = chrome_path()
FONTES = ("https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1"
          "&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400"
          "&family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400"
          "&family=JetBrains+Mono:wght@400;500&family=IBM+Plex+Mono:wght@400;500"
          "&family=Instrument+Sans:wght@400;500;600&family=Anton&family=Figtree:wght@700;800&display=block")

# combinações tipográficas da prancha de teste (a vencedora vira o padrão do tokens.css)
COMBOS = {
    "A": {"--f-display": "'Instrument Serif',serif", "--f-mono": "'JetBrains Mono',monospace", "--t": "116px"},
    "B": {"--f-display": "'Newsreader',serif", "--f-mono": "'IBM Plex Mono',monospace", "--t": "100px"},
    "C": {"--f-display": "'Bodoni Moda',serif", "--f-mono": "'JetBrains Mono',monospace", "--t": "94px"},
    "D": {"--f-display": "'Instrument Serif',serif", "--f-mono": "'JetBrains Mono',monospace", "--t": "116px", "grito": True},
}
e = html.escape

def titulo(p, c):
    a, b = e(p.get("titulo_a", "")), e(p.get("titulo_b", ""))
    luz = " luz" if p.get("vira_luz", True) else ""
    if c.get("grito"):
        return f'<h1 class="titulo"><span class="grito">{a}</span><span class="vira{luz}">{b}</span></h1>'
    return f'<h1 class="titulo">{a}<span class="vira{luz}">{b}</span></h1>'

def assinatura(p):
    return f'<div class="assinatura"><span>{e(p.get("assinatura") or p.get("_assinatura_kit") or "@suamarca")}</span><span>{e(p.get("data", ""))}</span></div>'

def lei(p):
    return f'<p class="lei">{e(p["lei"])}</p>' if p.get("lei") else ""

POS_CAOS = [(4, 6, -9), (40, 20, 7), (10, 40, 5), (46, 56, -6), (2, 74, 8), (36, 86, -4)]

def n1_eixo(p, c):
    (re, ie), (rd, idd) = p["colunas"]
    esq = "".join(f'<div class="eixo-linha"><b>{e(t)}</b><i>{k+1:02d}</i></div>' for k, t in enumerate(ie))
    dir_ = "".join(f'<div class="eixo-linha"><i>{k+1:02d}</i><b>{e(t)}</b></div>' for k, t in enumerate(idd))
    pontos = "".join('<div class="eixo-ponto"><u></u></div>' for _ in ie)
    corpo = f'<p class="corpo">{e(p["corpo"])}</p><div style="height:34px"></div>' if p.get("corpo") else ""
    return (f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:34px"></div>{titulo(p, c)}'
            f'<div class="eixo-palco"><div class="eixo-col esq"><p class="rotulo">{e(re)}</p>{esq}</div>'
            f'<div class="eixo-centro">{pontos}</div>'
            f'<div class="eixo-col"><p class="rotulo">{e(rd)}</p>{dir_}</div></div>'
            f'{corpo}{lei(p)}<div class="mola" style="flex:1"></div><div style="height:30px"></div>{assinatura(p)}')

def n1(p, c):
    if p.get("colunas"): return n1_eixo(p, c)
    caos = "".join(f'<span style="left:{x}%;top:{y}%;transform:rotate({r}deg)">{e(t)}</span>'
                   for t, (x, y, r) in zip(p["caos"], POS_CAOS))
    ordem = "".join(f'<div class="n1-no"><i>{i+1:02d}</i><b>{e(t)}</b></div>' for i, t in enumerate(p["ordem"]))
    return (f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:34px"></div>{titulo(p, c)}'
            f'<div class="n1-palco"><div><p class="rotulo n1-colrot">{e(p["rot_caos"])}</p><div class="n1-caos">{caos}</div></div>'
            f'<div><p class="rotulo n1-colrot" style="color:var(--luz)">{e(p["rot_ordem"])}</p><div class="n1-ordem">{ordem}</div></div></div>'
            f'{lei(p)}<div style="height:36px"></div>{assinatura(p)}')

def bloco_print(p):
    linhas = "".join(f'<div class="l on">{e(l[1:])}</div>' if l.startswith("!") else f'<div class="l">{e(l)}</div>'
                     for l in p["print_linhas"])
    return (f'<div class="print"><div class="barra"><u></u><u></u><u></u><em>{e(p.get("print_titulo", ""))}</em></div>'
            f'<div class="linhas">{linhas}</div></div>')

def n2(p, c):
    return (f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:34px"></div>{titulo(p, c)}'
            f'<div style="height:40px"></div><p class="corpo">{e(p["corpo"])}</p>'
            f'<div style="height:54px"></div>{bloco_print(p)}<div style="height:48px"></div>'
            f'<span class="chamada">{e(p["chamada"])}</span><div style="height:40px"></div>{assinatura(p)}')

def n3(p, c):
    return (f'<div class="n3-chao"></div><div class="n3-porta"></div>'
            f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:34px"></div>{titulo(p, c)}'
            f'<div style="height:36px"></div>{lei(p)}<div style="height:760px"></div>{assinatura(p)}')

def p1(p, c):
    a, g, b = e(p["titulo_a"]), e(p["grifo"]), e(p.get("titulo_b", ""))
    if c.get("grito"):
        t = f'<h1 class="titulo"><span class="grito" style="--tg:104px">{a}</span><span class="vira"><span class="grifo">{g}</span>{b}</span></h1>'
    else:
        t = f'<h1 class="titulo">{a} <span class="vira"><span class="grifo">{g}</span>{b}</span></h1>'
    return (f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:40px"></div>{t}'
            f'<div class="mola" style="flex:1"></div><div style="height:48px"></div><p class="corpo">{e(p["corpo"])}</p>'
            f'<div style="height:44px"></div>{lei(p)}<div style="height:56px"></div>{assinatura(p)}')

def p2(p, c):
    g = lambda t: e(t).replace("[[", '<span class="grifo">').replace("]]", "</span>")
    paras = "".join(f'<p class="{"parenteses" if t.startswith("(") else ""}">{g(t)}</p>' for t in p["paragrafos"])
    return (f'<span class="etiqueta">{e(p["etiqueta"])}</span>{paras}'
            f'<div class="lei-nativa">{e(p["lei"])}</div>')

def b1(p, c):
    return (f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:34px"></div>{titulo(p, c)}'
            f'<div style="height:56px"></div>{bloco_print(p)}<div style="height:48px"></div>'
            f'<p class="corpo">{e(p["corpo"])}</p><div class="mola" style="flex:1"></div>{assinatura(p)}')

def c1(p, c):
    total, n = p["total"], p["n"]
    corpo = f'<p class="corpo">{e(p["corpo"])}</p>' if p.get("corpo") else ""
    meio = ""
    if p.get("ordem"):
        meio = '<div class="n1-ordem" style="margin:30px 0">' + "".join(
            f'<div class="n1-no"><i>{i+1:02d}</i><b>{e(t)}</b></div>' for i, t in enumerate(p["ordem"])) + "</div>"
    return (f'<p class="paginacao"><b>{n:02d}</b> / {total:02d} · {e(p["rotulo"])}</p><div style="height:44px"></div>'
            f'{titulo(p, c)}<div style="height:44px"></div>{corpo}{meio}<div style="height:30px"></div>{lei(p)}'
            f'<div class="mola" style="flex:1"></div>{assinatura(p)}')

CIRCULO = ('<svg viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M58,5 C88,6 99,30 98,55 '
           'C96,88 55,98 26,93 C5,89 1,62 3,42 C6,14 38,3 70,8" fill="none" stroke-width="1.1" '
           'vector-effect="non-scaling-stroke" style="stroke:var(--luz);stroke-width:3px" stroke-linecap="round"/></svg>')

def d1(p, c):
    ops = ""
    for i, t in enumerate(p["opcoes"]):
        marc = i == p.get("marcada", -1)
        ops += (f'<div class="opcao{" marcada" if marc else ""}">{CIRCULO if marc else ""}'
                f'<i>{chr(65+i)}</i><span>{e(t)}</span></div>')
    anot = f'<p class="anotacao">{e(p["anotacao"])}</p>' if p.get("anotacao") else ""
    return (f'<p class="rotulo">{e(p["rotulo"])}</p><div style="height:34px"></div>{titulo(p, c)}'
            f'<div class="opcoes">{ops}</div>{anot}<div style="height:30px"></div>{lei(p)}<div class="mola" style="flex:1"></div>{assinatura(p)}')

def f1(p, c):
    corpo = f'<div style="height:30px"></div><p class="corpo">{e(p["corpo"])}</p>' if p.get("corpo") else ""
    return (f'<div class="f1-mola" style="flex:1"></div><p class="rotulo">{e(p["rotulo"])}</p><div style="height:28px"></div>{titulo(p, c)}{corpo}'
            f'<div style="height:30px"></div>{lei(p)}<div style="height:40px"></div>{assinatura(p)}')

TIPOS = {"N1": n1, "N2": n2, "N3": n3, "P1": p1, "P2": p2, "B1": b1, "C1": c1, "D1": d1, "F1": f1}
PAPEL = {"P1", "P2"}

def montar(p):
    c = (p.get("_combos_kit") or COMBOS)[p.get("combo", "A")]
    vars_ = ";".join(f"{k}:{v}" for k, v in c.items() if k.startswith("--"))
    extra = p.get("estilo", "")
    classes = ["tela", p.get("formato", "feed")]
    if p["tipo"] in PAPEL: classes.append("papel")
    if p["tipo"] == "P2": classes.append("nativa")
    if (p.get("fundo") or p.get("_fundo_kit")) == "claro": classes.append("claro")
    if p["tipo"] == "F1": classes.append("f1")
    foto = ""
    if p.get("_foto_abs"):   # F1, ou qualquer tipo com "foto": a foto real por baixo, o véu por cima
        foto = (f'<img class="foto" src="file:///{p["_foto_abs"].replace(chr(92), "/")}" style="--foco:{e(p.get("foco", "50% 22%"))}">'
                '<div class="veu"></div>')
    tokens = p.get("_tokens_abs") or os.path.join(AQUI, "tokens.css")   # conta de cliente: "tokens" no JSON
    css = io.open(tokens, encoding="utf-8").read() + io.open(os.path.join(AQUI, "componentes.css"), encoding="utf-8").read()
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<link href="{p.get("_fontes_kit") or FONTES}" rel="stylesheet"><style>{css}</style></head>'
            f'<body><div class="{" ".join(classes)}" style="{vars_};{extra}">{foto}{TIPOS[p["tipo"]](p, c)}</div></body></html>')

def carregar(spec):
    """Lê a lista de peças da casa ou o kit de uma conta e devolve as peças prontas para montar."""
    dado = json.load(io.open(spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec))
    kit = dado if isinstance(dado, dict) else {}
    pecas = dado["pecas"] if isinstance(dado, dict) else dado
    for p in pecas:
        tk = p.get("tokens") or kit.get("tokens")
        if tk: p["_tokens_abs"] = os.path.join(base, tk)
        if kit.get("combos"): p["_combos_kit"] = kit["combos"]
        if kit.get("fontes_url"): p["_fontes_kit"] = kit["fontes_url"]
        if kit.get("assinatura"): p["_assinatura_kit"] = kit["assinatura"]
        if kit.get("fundo"): p["_fundo_kit"] = kit["fundo"]
        if p.get("foto"): p["_foto_abs"] = os.path.normpath(os.path.join(base, p["foto"]))
    return pecas

def renderizar(pecas, saida):
    os.makedirs(saida, exist_ok=True)
    perfil = tempfile.mkdtemp(prefix="render-chrome-")
    for p in pecas:
        h = 1920 if p.get("formato") == "story" else 1350
        arq_html = os.path.join(saida, p["id"] + ".html")
        arq_png = os.path.join(saida, p["id"] + ".png")
        io.open(arq_html, "w", encoding="utf-8").write(montar(p))
        url = "file:///" + arq_html.replace("\\", "/")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size=1080,{h}",
                        "--virtual-time-budget=9000", f"--user-data-dir={perfil}", f"--screenshot={arq_png}", url],
                       capture_output=True, timeout=180)
        print(("ok  " if os.path.exists(arq_png) else "ERRO") + " " + p["id"])

if __name__ == "__main__":
    spec = sys.argv[1]
    saida = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(AQUI, "saida")
    renderizar(carregar(spec), saida)
