#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF CONTINUUM — gerador padrão de PDF a partir de Markdown.

Uso mínimo:
    python3 build-pdf.py --in doc.md --out doc.pdf

Com capa:
    python3 build-pdf.py --in doc.md --out doc.pdf --capa capa.json

Dependências (sandbox):
    pip install weasyprint markdown --break-system-packages

Fontes esperadas: Lora e Poppins em /usr/share/fonts/truetype/google-fonts/
Se faltarem, o gerador cai para serif/sans do sistema e avisa.

NÃO editar estilo.css por documento. Variação vai em --paleta.
"""
import argparse, html, json, os, re, sys, unicodedata
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

AQUI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- paletas
PALETAS = {
    # padrão institucional: dourado + rubi/vinho
    "ouro-rubi": """:root{
  --papel:#FBF8F3; --tinta:#241B20; --escuro:#3A2E33; --medio:#5C5049;
  --suave:#8A7C72; --fraco:#A9906A;
  --realce:#6B1E36;
  --ouro:#C9A24B; --ouro-medio:#D9C59A; --ouro-claro:#EADCC0; --ouro-escuro:#8A6A2F;
  --zebra:#F6F1E8; --bloco:#F4EEE3; --chip:#F3E9D4;
}""",
    # documento interno / técnico
    "grafite": """:root{
  --papel:#FAFAF9; --tinta:#1C1C1B; --escuro:#33322F; --medio:#55534E;
  --suave:#807D76; --fraco:#9A968D;
  --realce:#2E3A45;
  --ouro:#8C8577; --ouro-medio:#C8C3B8; --ouro-claro:#E4E1DA; --ouro-escuro:#5F594D;
  --zebra:#F2F1ED; --bloco:#EFEEE9; --chip:#E8E6DF;
}""",
    # jurídico / contraparte
    "vinho-sobrio": """:root{
  --papel:#FCFAF7; --tinta:#1F1A1A; --escuro:#332B2B; --medio:#574E4E;
  --suave:#867B7B; --fraco:#A08A8A;
  --realce:#5A1A22;
  --ouro:#A8853F; --ouro-medio:#CFBE97; --ouro-claro:#E6DCC6; --ouro-escuro:#7A5F2A;
  --zebra:#F5F1EA; --bloco:#F1ECE3; --chip:#EFE5D2;
}""",
}

# marca geométrica da capa (círculos concêntricos + vesica) — neutra de propósito
MARCA = """<svg width="112" height="112" viewBox="0 0 112 112" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="56" cy="56" r="53" stroke="%(medio)s" stroke-width=".7"/>
  <circle cx="56" cy="56" r="40" stroke="%(ouro)s" stroke-width=".7"/>
  <circle cx="56" cy="56" r="22" stroke="%(ouro)s" stroke-width=".55" opacity=".85"/>
  <circle cx="56" cy="56" r="7" stroke="%(realce)s" stroke-width=".9"/>
  <circle cx="56" cy="56" r="1.7" fill="%(ouro)s"/>
</svg>"""

EMOJIS = [
    ("\u26a0\ufe0f", '<span class="mk mk-alert">!</span>'),
    ("\u26a0",       '<span class="mk mk-alert">!</span>'),
    ("\u2b50",       '<span class="mk mk-star">&#9670;</span>'),
    ("\U0001f4b0",   '<span class="mk mk-star">&#9670;</span>'),
    ("\U0001f534",   '<span class="mk mk-alert">!</span>'),
    ("\U0001f7e1",   '<span class="mk mk-amber">&#9679;</span>'),
    ("\u2705",       '<span class="mk mk-star">&#10003;</span>'),
]

def css_escape(s):
    """Escapa texto para uso em content: '...' do CSS.

    O cabecalho corrido entra por CSS, e CSS nao decodifica entidade HTML.
    Sem este unescape, um '&middot;' no JSON da capa sai literal no topo de
    toda pagina. As entidades sao decodificadas ANTES do escape numerico.
    """
    s = html.unescape(s)
    out = []
    for ch in s:
        if ch in ("'", "\\"):
            out.append("\\" + ch)
        elif ord(ch) > 126:
            out.append("\\%04X " % ord(ch))
        else:
            out.append(ch)
    return "".join(out)

def cor(paleta, nome, padrao):
    m = re.search(r"--%s:\s*([^;]+);" % nome, PALETAS[paleta])
    return m.group(1).strip() if m else padrao

def monta_capa(c, paleta):
    if not c:
        return ""
    marca = MARCA % {
        "ouro":   cor(paleta, "ouro", "#C9A24B"),
        "medio":  cor(paleta, "ouro-medio", "#D9C59A"),
        "realce": cor(paleta, "realce", "#6B1E36"),
    }
    subs = "<br>".join(c.get("subtitulo", []))
    metas = "".join(
        "<div><b>%s</b> %s</div>" % (k, v) for k, v in c.get("meta", {}).items()
    )
    rodape = ""
    if c.get("rodape"):
        r = c["rodape"]
        rodape = ("<div class='foot'><div class='l'>%s</div>"
                  "<div class='n'>%s</div><div class='d'>%s</div></div>") % (
            r.get("rotulo", ""), r.get("frase", ""), r.get("nota", ""))
    return ("<div class='cover'><div class='frame'></div><div class='inner'>"
            "<div class='mark'>%s</div>"
            "<div class='eyebrow'>%s</div>"
            "<h1>%s%s</h1>"
            "<div class='sub'>%s</div>"
            "<div class='rule'></div>"
            "<div class='meta'>%s</div>"
            "%s</div></div>") % (
        marca,
        c.get("sobretitulo", "{{EMPRESA}}"),
        c.get("titulo", ""),
        ("<br><em>%s</em>" % c["titulo_italico"]) if c.get("titulo_italico") else "",
        subs, metas, rodape)

def main():
    ap = argparse.ArgumentParser(description="Gera PDF padrão Continuum a partir de Markdown.")
    ap.add_argument("--in", dest="entrada", required=True, help="arquivo .md de origem")
    ap.add_argument("--out", dest="saida", required=True, help="arquivo .pdf de destino")
    ap.add_argument("--capa", help="JSON com os dados da capa (ver capa.exemplo.json)")
    ap.add_argument("--paleta", default="ouro-rubi", choices=sorted(PALETAS),
                    help="paleta de cores (padrão: ouro-rubi)")
    ap.add_argument("--cabecalho", default="", help="texto do cabeçalho corrido")
    ap.add_argument("--manter-titulo", action="store_true",
                    help="não cortar o bloco de título/metadados do .md (padrão: corta quando há capa)")
    args = ap.parse_args()

    md_txt = open(args.entrada, encoding="utf-8").read()
    capa = json.load(open(args.capa, encoding="utf-8")) if args.capa else None
    cabecalho = args.cabecalho or (capa or {}).get("cabecalho", "")

    # corta o cabeçalho do .md (H1 + bloco de citação de metadados) quando há capa
    if capa and not args.manter_titulo:
        linhas = md_txt.split("\n")
        i = 0
        while i < len(linhas) and not re.match(r"^##\s", linhas[i]):
            i += 1
        if i < len(linhas):
            md_txt = "\n".join(linhas[i:])

    for a, b in EMOJIS:
        md_txt = md_txt.replace(a, b)

    html_corpo = markdown.Markdown(
        extensions=["tables", "attr_list", "sane_lists", "fenced_code"]
    ).convert(md_txt)

    # IDs curtos (C-01, F-12...) viram etiquetas
    html_corpo = re.sub(r"<strong>([A-Z]{1,3}-\d{2,3})</strong>",
                        r'<span class="cid">\1</span>', html_corpo)
    html_corpo = re.sub(r"(?<![\w>-])([A-Z]{1,3}-\d{2,3})(?![\w-])",
                        r'<span class="cid cid-inline">\1</span>', html_corpo)
    html_corpo = html_corpo.replace(
        "<hr />", '<div class="orn"><span></span><i>&#10022;</i><span></span></div>')

    css_txt = open(os.path.join(AQUI, "estilo.css"), encoding="utf-8").read()
    css_txt = css_txt.replace("__PALETA__", PALETAS[args.paleta])
    css_txt = css_txt.replace("__CABECALHO__", css_escape(cabecalho))
    if not cabecalho:
        css_txt = css_txt.replace('content:"";', "content:none;")

    doc = ("<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'>"
           "<title>%s</title></head><body>%s<div class='doc'>%s</div></body></html>") % (
        (capa or {}).get("titulo", "Documento Continuum"),
        monta_capa(capa, args.paleta), html_corpo)

    fc = FontConfiguration()
    HTML(string=doc, base_url=AQUI).write_pdf(
        args.saida, stylesheets=[CSS(string=css_txt, font_config=fc)], font_config=fc)
    print("PDF gerado:", args.saida)

if __name__ == "__main__":
    main()
