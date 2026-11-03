"""Dashboard fixo de dados em PDF (A4 deitado, uma página), no visual do painel de resultado.

Uso:  python3 gerar_dashboard.py <dados.json>
Gera <nome>.html, <nome>.pdf e <nome>.png (prévia) na pasta do JSON (ou em "saida", se o JSON disser).

Dois modos, escolhidos pelo JSON:
  · campanha (o original, 27/10/2026): "campanhas" + "serie". Molde: exemplo.json.
    Os seis números, os dois gráficos e a tabela de tráfego se calculam dos dados.
  · genérico (01/11/2026): "kpis" + "graficos" + "tabela". Molde: exemplo/EXEMPLO-DASHBOARD.json.
    Rótulos e números vêm prontos do JSON; o visual é o mesmo.

01/11/2026: as fontes são arquivos estáticos de fontes/, embutidos no HTML. A Plus Jakarta Sans
pelo link do Google é fonte variável e entrava no PDF do Chrome como Type3 (um PDF real
saiu com 13). O gerador agora reprova, com código 1, PDF com fonte Type3 ou com mais de uma página.
"""
import base64, json, pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
GOV = AQUI.parents[1]
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), '40-operacao-rotinas', 'ferramentas'))
from navegador import chrome_path  # noqa: E402  Chrome em Windows, macOS e Linux (ou CHROME=<caminho>)
CHROME = chrome_path()
# Logo opcional: sem o arquivo, o topo mostra o nome da empresa.
LOGO = GOV / "40-operacao-rotinas/ferramentas/painel-resultado/logo-continuum.png"
EMPRESA = "{{EMPRESA}}"


def brl(v, d=2):
    s = f"{v:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def topo_escala(v, passos=4):
    """Teto do eixo: múltiplo 'redondo' acima do maior valor."""
    import math
    bruto = v * 1.05 / passos
    mag = 10 ** math.floor(math.log10(bruto)) if bruto > 0 else 1
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= bruto:
            return m * mag * passos
    return 10 * mag * passos


W, H = 486, 222
PL, PR, PT, PB = 30, 6, 18, 26
pw, ph = W - PL - PR, H - PT - PB


def grid(maxv, passos, fmt):
    g = ""
    for i in range(passos + 1):
        v = maxv * i / passos
        y = PT + ph - ph * v / maxv
        g += f'<line x1="{PL}" x2="{W-PR}" y1="{y:.1f}" y2="{y:.1f}" class="gl"/>'
        g += f'<text x="{PL-8}" y="{y+4:.1f}" text-anchor="end">{fmt(v)}</text>'
    return g


def barras_pts(pts, fmt_val, fmt_grid):
    """pts = [(rótulo, valor)]; a última barra sai em destaque."""
    maxv = topo_escala(max(v for _, v in pts))
    s = grid(maxv, 4, fmt_grid)
    slot = pw / len(pts); bw = min(34, slot * .6)
    for i, (d, c) in enumerate(pts):
        x = PL + slot * i + (slot - bw) / 2
        h = ph * c / maxv; y = PT + ph - h; r = min(4, h / 2)
        s += (f'<path d="M{x:.1f},{PT+ph:.1f} V{y+r:.1f} Q{x:.1f},{y:.1f} {x+r:.1f},{y:.1f} '
              f'H{x+bw-r:.1f} Q{x+bw:.1f},{y:.1f} {x+bw:.1f},{y+r:.1f} V{PT+ph:.1f} Z" '
              f'class="bar{" fim" if i == len(pts)-1 else ""}"/>')
        s += f'<text x="{x+bw/2:.1f}" y="{y-6:.1f}" text-anchor="middle" class="val">{fmt_val(c)}</text>'
        s += f'<text x="{x+bw/2:.1f}" y="{H-8}" text-anchor="middle">{d}</text>'
    return s


def linha_pts(pts, fmt_val, fmt_grid):
    """pts = [(rótulo, valor)], em ordem de tempo."""
    maxv = topo_escala(max(v for _, v in pts))
    s = grid(maxv, 4, fmt_grid)
    slot = pw / len(pts)
    xy = [(PL + slot * i + slot / 2, PT + ph - ph * v / maxv, v, d) for i, (d, v) in enumerate(pts)]
    s += '<polyline class="ln" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y, *_ in xy) + '"/>'
    for x, y, v, d in xy:
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" class="pt"/>'
        s += f'<text x="{x:.1f}" y="{y-11:.1f}" text-anchor="middle" class="val">{fmt_val(v)}</text>'
        s += f'<text x="{x:.1f}" y="{H-8}" text-anchor="middle">{d}</text>'
    return s


# modo campanha: os mesmos números de antes, agora pelas funções genéricas
def barras(serie):
    return barras_pts([(d, c) for d, _, c in serie], str, lambda v: f"{v:.0f}")


def linha(serie):
    return linha_pts([(d, g / c) for d, g, c in serie], brl,
                     lambda v: brl(v, 0) if v == int(v) else brl(v, 1))


def kpi(rot, val, sub="", dest=False):
    return (f'<div class="kpi{" dest" if dest else ""}"><div class="kr">{rot}</div>'
            f'<div class="kv">{val}</div><div class="ks">{sub}</div></div>')


def card_grafico(titulo, sub, svg):
    return (f'<div class="card"><div class="ct">{titulo}<span>{sub}</span></div>'
            f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{svg}</svg></div>')


def linha_tab(c, cls=""):
    seg = "—" if c.get("seguidores") is None else c["seguidores"]
    vis = "—" if c.get("visitas") is None else c["visitas"]
    return (f'<tr class="{cls}"><td class="nm">{c["nome"]}<span>{c.get("detalhe","")}</span></td>'
            f'<td>R$ {brl(c["gasto"])}</td><td class="hl">{c["conversas"]}</td>'
            f'<td class="hl">R$ {brl(c["gasto"]/c["conversas"])}</td>'
            f'<td>R$ {brl(c["gasto"]/c["impressoes"]*1000)}</td><td>{brl(c["impressoes"],0)}</td>'
            f'<td>{brl(c["alcance"],0)}</td><td>{brl(c["impressoes"]/c["alcance"])}</td>'
            f'<td>{vis}</td><td>{seg}</td><td>{brl(c["conversas"]/c["impressoes"]*1000, 1)}</td></tr>')


def corpo_campanha(D):
    camps = D["campanhas"]
    soma = lambda k: sum(c.get(k) or 0 for c in camps)
    T = dict(nome="Total", detalhe=D["periodo"], gasto=soma("gasto"), conversas=soma("conversas"),
             impressoes=soma("impressoes"), alcance=soma("alcance"),
             visitas=soma("visitas"), seguidores=soma("seguidores"))
    serie = [(p["data"], p["gasto"], p["conversas"]) for p in D["serie"]]
    kpis = "".join([
        kpi("Investido", "R$ " + brl(T["gasto"]), f'de R$ {brl(D["verba"])} de verba' if D.get("verba") else ""),
        kpi("Conversas", T["conversas"], "iniciadas no WhatsApp", True),
        kpi("Custo por conversa", "R$ " + brl(T["gasto"] / T["conversas"]), "média do período", True),
        kpi("Impressões", brl(T["impressoes"], 0), "CPM R$ " + brl(T["gasto"] / T["impressoes"] * 1000)),
        kpi("Visitas ao perfil", T["visitas"], "R$ " + brl(T["gasto"] / T["visitas"]) + " por visita" if T["visitas"] else ""),
        kpi("Seguidores", "+" + str(T["seguidores"]), "Instagram"),
    ])
    graficos = (card_grafico("Conversas acumuladas", "por dia de leitura", barras(serie))
                + card_grafico("Custo por conversa acumulado (R$)", "por dia de leitura", linha(serie)))
    linhas = "".join(linha_tab(c) for c in camps) + (linha_tab(T, "tot") if len(camps) > 1 else "")
    tabela = ('<div class="card" style="padding-bottom:4px"><div class="ct">Por campanha</div>'
              '<table><thead><tr><th>Campanha</th><th>Investido</th><th>Conversas</th><th>Custo/conversa</th>'
              '<th>CPM</th><th>Impressões</th><th>Alcance</th><th>Frequência</th><th>Visitas perfil</th>'
              '<th>Seguidores</th><th>Conv./mil impr.</th></tr></thead>'
              f'<tbody>{linhas}</tbody></table><div class="nota">{D.get("nota","")}</div></div>')
    return kpis, graficos, tabela


def corpo_generico(D):
    kpis = "".join(kpi(k["rotulo"], k["valor"], k.get("sub", ""), k.get("destaque", False)) for k in D["kpis"])
    graficos = ""
    for g in D["graficos"]:
        casas = g.get("casas", 0)
        fmt = (lambda v, c=casas: brl(v, c)) if casas else (lambda v: f"{v:.0f}")
        pts = [(p[0], p[1]) for p in g["pontos"]]
        desenho = linha_pts if g.get("tipo") == "linha" else barras_pts
        graficos += card_grafico(g["titulo"], g.get("sub", ""), desenho(pts, fmt, lambda v: f"{v:.0f}"))
    t = D["tabela"]
    hl = set(t.get("destaque", []))

    def tr(cel, cls=""):
        tds = ""
        for i, v in enumerate(cel):
            if i == 0:
                tds += f'<td class="nm">{v}</td>'
            else:
                tds += f'<td class="{"hl" if i in hl else ""}">{v}</td>'
        return f'<tr class="{cls}">{tds}</tr>'

    cab = "".join(f"<th>{c}</th>" for c in t["colunas"])
    linhas = "".join(tr(l) for l in t["linhas"]) + (tr(t["total"], "tot") if t.get("total") else "")
    tabela = (f'<div class="card" style="padding-bottom:4px"><div class="ct">{t.get("titulo","")}</div>'
              f'<table><thead><tr>{cab}</tr></thead><tbody>{linhas}</tbody></table>'
              f'<div class="nota">{D.get("nota","")}</div></div>')
    return kpis, graficos, tabela


def fontes_embutidas():
    faces = ""
    for peso in (400, 500, 600, 700):
        b64 = base64.b64encode((AQUI / "fontes" / f"plus-jakarta-sans-{peso}.woff2").read_bytes()).decode()
        faces += ("@font-face{font-family:'Plus Jakarta Sans';font-weight:%d;font-style:normal;"
                  "src:url(data:font/woff2;base64,%s) format('woff2')}" % (peso, b64))
    return faces


def gerar(dados_path):
    dp = pathlib.Path(dados_path).resolve()
    D = json.loads(dp.read_text(encoding="utf-8"))
    kpis, graficos, tabela = corpo_generico(D) if "kpis" in D else corpo_campanha(D)
    empresa = D.get("empresa") or EMPRESA
    logo = (f'<img src="data:image/png;base64,{base64.b64encode(LOGO.read_bytes()).decode()}" alt="{empresa}">'
            if LOGO.exists() else f'<div class="marca">{empresa}</div>')
    css = (AQUI / "estilo.css").read_text(encoding="utf-8")
    chips = "".join(f'<div class="chip">{c}</div>' for c in D["chips"])
    html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>{fontes_embutidas()}</style>
<style>{css}</style></head><body><div class="pg">
<div class="top">{logo}<div class="meta">{chips}</div></div>
<div class="kpis">{kpis}</div>
<div class="row">{graficos}</div>
{tabela}
</div></body></html>"""
    saida = (dp.parent / D["saida"]) if D.get("saida") else dp.parent
    saida.mkdir(parents=True, exist_ok=True)
    hp = saida / f'{D["arquivo"]}.html'
    hp.write_text(html, encoding="utf-8")
    pdf = saida / f'{D["arquivo"]}.pdf'
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", hp.as_uri()], check=True, capture_output=True)
    try:
        import fitz
    except ImportError:
        print(pdf, "\n(sem PyMuPDF: a prévia e a conferência de fonte não rodaram)")
        return
    doc = fitz.open(pdf)
    prev = saida / f'{D["arquivo"]}.png'
    doc[0].get_pixmap(dpi=110).save(str(prev))
    print(f"{pdf}\n{len(doc)} página(s) · prévia: {prev}")
    t3 = sum(1 for p in doc for f in p.get_fonts() if f[2] == "Type3")
    if t3 or len(doc) != 1:
        print(f"REPROVADO, não entregar: {t3} fonte(s) Type3 · {len(doc)} página(s); o dashboard tem uma só")
        sys.exit(1)
    print("aprovado: uma página, sem Type3")


if __name__ == "__main__":
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    gerar(sys.argv[1])
