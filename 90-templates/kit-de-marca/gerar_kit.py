#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_kit.py — monta o kit de marca de uma conta a partir de um kit.json.

Tipo: blueprint (ferramenta) · Método: 100-métodos/METODO-KIT-DE-MARCA.md
Uso:  python3 gerar_kit.py <pasta-da-conta>/branding/01 - identidade visual/kit.json [--sem-png]

Gera, na pasta do kit.json:
  tokens.css         cor e fonte da conta (gerado: mude o kit.json, nunca este arquivo)
  saida/             as peças renderizadas pelo motor da casa (945-branding/.../sistema/render.py)
  prancha-teste.html (+ .png)  as opções lado a lado, uma variável por linha (METODO-PRANCHA-DE-ESCOLHA)
  kit.html (+ .png)  a página do kit: arquétipos, direção, paleta, tipografia, tipos, gravação, veto
Formato do kit.json: kit-modelo.json, nesta pasta.
"""
import copy, html, io, json, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
MOTOR = os.path.join(RAIZ, "945-branding", "01 - identidade visual", "sistema")
sys.path.insert(0, MOTOR)
sys.path.insert(0, os.path.join(RAIZ, "90-templates", "prancha-de-escolha"))
import render            # noqa: E402  o motor da casa
import gerar_prancha     # noqa: E402

CHROME = render.CHROME
e = html.escape
RGB = ("--luz", "--halo", "--osso", "--tinta", "--carvao", "--noite", "--papel")
OBRIGATORIOS = ["--noite", "--carvao", "--borda", "--pedra", "--osso", "--papel", "--tinta", "--luz", "--halo"]

def rgb(h):
    h = h.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))

def tokens_css(k):
    cores = {c["token"]: c["hex"] for c in k["cores"]}
    falta = [t for t in OBRIGATORIOS if t not in cores]
    assert not falta, "kit.json sem os tokens: %s" % falta
    a = k["combos"]["A"]
    linhas = ["/* tokens.css — %s · GERADO por 90-templates/kit-de-marca/gerar_kit.py a partir do kit.json." % k["conta"],
              "   Não editar à mão: mude o kit.json e gere de novo. */", ":root {"]
    for t, v in cores.items():
        linhas.append("  %s: %s;" % (t, v))
    for t in RGB:
        linhas.append("  %s-rgb: %s;" % (t, rgb(cores[t])))
    if "--papel-2" in cores:
        linhas.append("  --papel-2-rgb: %s;" % rgb(cores["--papel-2"]))
    for t in ("--f-display", "--f-mono", "--f-corpo", "--f-grito", "--f-nativa"):
        v = a.get(t) or k.get("fontes_padrao", {}).get(t)
        if v: linhas.append("  %s: %s;" % (t, v))
    linhas += ["  --raio: %s;" % k.get("raio", "4px"), "  --margem: 84px;", "}", ""]
    return "\n".join(linhas)

def pecas_da_prancha(k):
    """Linha 1: tipografia (a mesma peça em cada combo). Linha 2: paleta (mesma peça, combo A, cada paleta).
    Linha 3: os tipos de criativo, cada peça no combo dela."""
    por_id = {p["id"]: p for p in k["pecas"]}
    pr = k.get("prancha", {})
    base = por_id[pr.get("peca_teste", k["pecas"][0]["id"])]
    tipo, pal, tipos = [], [], []
    for c in k["combos"]:
        p = copy.deepcopy(base); p["id"] = "tipografia-%s" % c; p["combo"] = c; tipo.append(p)
    for nome, alt in k.get("paletas", {}).items():
        p = copy.deepcopy(base); p["id"] = "paleta-%s" % nome; p["combo"] = "A"
        p["estilo"] = ";".join("%s:%s;%s-rgb:%s" % (t, v, t, rgb(v)) if t in RGB
                               else "%s:%s" % (t, v) for t, v in alt.get("cores", {}).items())
        pal.append(p)
    for p in k["pecas"]:
        tipos.append(copy.deepcopy(p))
    return tipo, pal, tipos

def secao_imgs(nome, cod, itens, cols=4):
    return {"codigo": cod, "nome": nome, "colunas": cols, "itens": itens}

def pagina_kit(k, pasta):
    cores = k["cores"]; a = k["combos"]["A"]
    arq = "".join(f'<div class="arq"><p class="rot">{e(x["papel"])}</p><h3>{e(x["nome"])}</h3><p>{e(x["leitura"])}</p></div>'
                  for x in k["arquetipos"])
    pal = "".join(f'<div class="cor"><div class="am" style="background:{c["hex"]}"></div><b>{e(c.get("nome", c["token"]))}</b>'
                  f'<span>{e(c["hex"])} · {e(c["token"])}</span><em>{e(c.get("uso", ""))}</em></div>' for c in cores)
    tip = ""
    for cod, c in k["combos"].items():
        grito = (f'<p style="font-family:{c["--f-grito"]};font-size:64px;line-height:1;text-transform:uppercase">{e(k.get("frase_grito", "A frase crua."))}</p>'
                 f'<p style="font-family:{c["--f-display"]};font-style:italic;font-size:56px;line-height:1;color:var(--luz)">e a virada em itálico.</p>') if c.get("grito") else ""
        tip += (f'<div class="tipo"><p class="rot">combinação {e(cod)} · {e(c.get("legenda", ""))}</p>{grito}'
                f'<p style="font-family:{c["--f-display"]};font-size:64px;line-height:1.05">{e(k.get("frase_amostra", k["conta"]))}</p>'
                f'<p style="font-family:{c.get("--f-mono", a["--f-mono"])};font-size:18px;letter-spacing:.12em;text-transform:uppercase">rótulo · a lei da peça</p>'
                f'<p style="font-family:{c.get("--f-corpo", a.get("--f-corpo", "sans-serif"))};font-size:20px">Texto de leitura, no corpo da combinação.</p></div>')
    tps = "".join(f'<figure><img src="saida/{e(p["id"])}.png"><figcaption><b>{e(p["tipo"])}</b> {e(p.get("_nome_tipo", ""))}'
                  f'<span>{e(p.get("_quando", ""))}</span></figcaption></figure>' for p in k["pecas"])
    veto = "".join(f"<li>{e(v)}</li>" for v in k["veto"])
    d = k["direcao"]
    claro = k.get("fundo") == "claro"
    fundo, texto = ("var(--papel)", "var(--tinta)") if claro else ("var(--noite)", "var(--osso)")
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kit de marca · {e(k["conta"])}</title><link href="{k["fontes_url"]}" rel="stylesheet"><link rel="stylesheet" href="tokens.css">
<style>*{{box-sizing:border-box;margin:0}}body{{background:{fundo};color:{texto};font:17px/1.55 var(--f-corpo);padding:56px 48px 80px}}
main{{max-width:1140px;margin:0 auto}}h1{{font:400 76px/1 var(--f-display)}}h1 i{{color:var(--luz)}}
h2{{font:400 38px var(--f-display);margin:64px 0 20px;padding-top:18px;border-top:1px solid var(--borda)}}
.rot{{font:500 13px var(--f-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--pedra);margin-bottom:8px}}
.estado{{font:400 14px var(--f-mono);color:var(--pedra);margin-top:14px}}.g{{display:grid;gap:18px}}
.arqs{{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}.arq{{border:1px solid var(--borda);padding:20px;border-radius:var(--raio)}}
.arq h3{{font:400 34px var(--f-display);margin-bottom:8px}}.arq:first-child{{border-color:var(--luz)}}
.lei{{font:400 22px/1.45 var(--f-display);font-style:italic;border-left:3px solid var(--luz);padding-left:20px;margin-top:22px}}
.dir{{grid-template-columns:repeat(3,1fr)}}.dir p:last-child{{font-size:18px}}
.cores{{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}}.cor .am{{height:96px;border-radius:var(--raio);border:1px solid var(--borda)}}
.cor b{{display:block;margin-top:8px}}.cor span{{display:block;font:400 13px var(--f-mono);color:var(--pedra)}}.cor em{{display:block;font-size:14px;font-style:normal;opacity:.8}}
.tipo{{border-bottom:1px solid var(--borda);padding:18px 0}}.tipo p{{margin:6px 0}}
.tps{{grid-template-columns:repeat(4,1fr)}}figure img{{width:100%;display:block;border:1px solid var(--borda);border-radius:var(--raio)}}
figcaption{{font:400 13px/1.4 var(--f-mono);color:var(--pedra);margin-top:8px}}figcaption b{{color:var(--luz);margin-right:6px}}figcaption span{{display:block}}
ul{{padding-left:20px}}li{{margin:4px 0}}@media(max-width:760px){{.dir,.tps{{grid-template-columns:1fr 1fr}}h1{{font-size:52px}}}}</style></head>
<body><main><p class="rot">kit de marca · {e(k["data"])}</p><h1>{e(k["conta"])} <i>{e(k.get("titulo_italico", "kit de marca"))}</i></h1>
<p class="estado">{e(k["estado"])}</p>
<h2>Arquétipos</h2><div class="g arqs">{arq}</div><p class="lei">Teste de toda peça: {e(k["teste_da_peca"])}</p>
<h2>Direção</h2><div class="g dir"><div><p class="rot">sensação que a marca compra</p><p>{e(d["sensacao"])}</p></div>
<div><p class="rot">o extremo</p><p>{e(d["extremo"])}</p></div><div><p class="rot">elemento memorável</p><p>{e(d["memoravel"])}</p></div></div>
<h2>Paleta</h2><div class="g cores">{pal}</div><p class="estado">{e(k.get("regra_cor", ""))}</p>
<h2>Tipografia</h2>{tip}
<h2>Tipos de criativo</h2><div class="g tps">{tps}</div>
<h2>Ambiente de gravação</h2><p>{e(k["gravacao"])}</p>
<h2>O que esta marca nunca faz</h2><ul>{veto}</ul>
</main></body></html>
"""

def png_pagina(arq_html, largura=1240, altura=6000):
    png = os.path.splitext(arq_html)[0] + ".png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={largura},{altura}",
                    "--virtual-time-budget=9000", f"--user-data-dir={tempfile.mkdtemp(prefix='kit-')}",
                    f"--screenshot={png}", "file:///" + arq_html.replace("\\", "/")], capture_output=True, timeout=180)
    try:   # corta o fundo vazio do fim
        from PIL import Image, ImageChops
        im = Image.open(png).convert("RGB")
        bg = Image.new("RGB", im.size, im.getpixel((im.width - 2, im.height - 2)))
        caixa = ImageChops.difference(im, bg).getbbox()
        if caixa: im.crop((0, 0, im.width, min(im.height, caixa[3] + 60))).save(png)
    except Exception as erro:
        print("aviso: sem corte do PNG (%s)" % erro)
    return png

def main():
    arq = os.path.abspath(sys.argv[1]); pasta = os.path.dirname(arq)
    k = json.load(io.open(arq, encoding="utf-8"))
    io.open(os.path.join(pasta, "tokens.css"), "w", encoding="utf-8", newline="\n").write(tokens_css(k))
    print("ok tokens.css")
    for p in k["pecas"]:
        assert p.get("_procedencia"), "peça %s sem _procedencia (METODO-PRANCHA-DE-ESCOLHA §4.2)" % p["id"]
    tipo, pal, tipos = pecas_da_prancha(k)
    for p in tipo + pal + tipos:
        p["_tokens_abs"] = os.path.join(pasta, "tokens.css"); p["_combos_kit"] = k["combos"]
        p["_fontes_kit"] = k["fontes_url"]; p["_assinatura_kit"] = k.get("assinatura")
        if k.get("fundo"): p["_fundo_kit"] = k["fundo"]
        if p.get("foto"): p["_foto_abs"] = os.path.normpath(os.path.join(pasta, p["foto"]))
    saida = os.path.join(pasta, "saida")
    if "--sem-png" not in sys.argv:
        render.renderizar(tipo + pal + tipos, saida)
    nomes = {t["codigo"]: t for t in k.get("tipos", [])}
    for p in k["pecas"]:
        t = nomes.get(p["tipo"], {}); p["_nome_tipo"] = t.get("nome", ""); p["_quando"] = t.get("quando", "")
    secoes = [secao_imgs("Tipografia · a mesma peça em cada combinação", "1",
                         [{"img": "saida/%s.png" % p["id"], "rotulo": p["combo"], "legenda": k["combos"][p["combo"]].get("legenda", "")} for p in tipo])]
    if pal:
        secoes.append(secao_imgs("Paleta · a mesma peça, combinação A", "2",
                                 [{"img": "saida/%s.png" % p["id"], "rotulo": p["id"].split("-", 1)[1],
                                   "legenda": k["paletas"][p["id"].split("-", 1)[1]].get("legenda", "")} for p in pal]))
    secoes.append(secao_imgs("Tipos de criativo", str(len(secoes) + 1),
                             [{"img": "saida/%s.png" % p["id"], "rotulo": p["tipo"], "legenda": p["_nome_tipo"]} for p in k["pecas"]]))
    man = {"titulo": "Prancha de", "titulo_italico": "escolha · " + k["conta"], "saida": "prancha-teste.html",
           "subtitulo": "%s · %s · textos com procedência (kit.json). Nada aqui foi publicado." % (k["data"], k["estado"]),
           "secoes": secoes}
    io.open(os.path.join(pasta, "prancha-teste.html"), "w", encoding="utf-8", newline="\n").write(gerar_prancha.gerar(man))
    print("ok prancha-teste.html")
    kh = os.path.join(pasta, "kit.html")
    io.open(kh, "w", encoding="utf-8", newline="\n").write(pagina_kit(k, pasta))
    print("ok kit.html")
    if "--sem-png" not in sys.argv:
        print("ok", png_pagina(kh))
        print("ok", png_pagina(os.path.join(pasta, "prancha-teste.html"), 1360, 7000))

if __name__ == "__main__":
    main()
