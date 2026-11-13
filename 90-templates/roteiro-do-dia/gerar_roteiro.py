"""
gerar_roteiro.py · MODELO 10 do CATALOGO-PDF: o roteiro do dia do operador, com o dia em BPMN

    python3 gerar_roteiro.py roteiro.json           -> HTML + PDF na pasta do JSON
    python3 gerar_roteiro.py roteiro.json --so-html -> só o HTML (para olhar no navegador)

Lê um JSON (molde: exemplo/roteiro.json) e escreve:
  · capa no modelo elétrico A4, cinza, sem fita;
  · página 01: o dia em BPMN vertical, duas raias ("Você" × "A casa"), calculado dos passos;
  · página 02: o laço de cada envio (fixo) + a tabela "agora";
  · página 03: a tabela "tarde", o destaque e a lista de fechamento.
Copia noturno.css, eletrico.css e fontes/ de ../pdf-noturno/ para a pasta de saída e imprime pelo
../pdf-noturno/gerar_pdf.py, que reprova Type3 e página em branco. Defeito de desenho se corrige AQUI.

Tipos de passo: "tarefa" · "fixo" (compromisso de hora marcada, borda branca) · "decisao" (losango; "sim" vira
tarefa abaixo, "não" contorna pela esquerda e as duas se juntam num losango de junção).
Eventos da casa: {"hora", "linhas": [...], "passo": índice (ou "fim"), "aviso": true = seta tracejada até o passo}.
Lugar e hora: passo com "icone" (banho · lavanderia · trabalho · casa · cafe · caminho) e "hora" ganha o
ícone e a hora à esquerda da caixa. O lugar não se escreve por extenso: o ícone é a referência.
"""
import html, io, json, os, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
NOTURNO = AQUI.parent / "pdf-noturno"
E = html.escape

ESTILO = """
  :root { --fundo:#0A0A0A; --painel:#151515; --borda:#2A2A2A; --azul:#8F8F8F; --azul-claro:#C4C4C4; --branco:#FFFFFF; --texto:#E6E6E6; --fraco:#8A8A8A; }
  @page { background:#0A0A0A;
    @bottom-left  { content:"Continuum AI Systems"; font-family:"Montserrat"; font-size:6pt; letter-spacing:1pt; color:#555555; }
    @bottom-right { content:counter(page); font-family:"Montserrat"; font-size:6pt; color:#555555; } }
  td { border-bottom-color:#1C1C1C; }
  em, i { color:#CFCFCF; }
  .capa .botao { background:#E6E6E6; color:#0A0A0A; }
  td, th { font-size:7.5pt; line-height:1.32; padding-top:1.3mm; padding-bottom:1.3mm; }
  .destaque { padding:2.4mm 3.2mm; margin:2.6mm 0; }
  .destaque .lead { font-size:10.5pt; }
  .destaque p { font-size:8.2pt; margin-bottom:0; }
  p { font-size:8.6pt; }
  .num5 { font-family:"Anton", sans-serif; font-size:11pt; color:#FFFFFF; text-align:center; }
  .bpmn { display:block; width:100%; height:auto; margin:1mm 0 2mm 0; }
  .bpmn text { font-family:"Inter", sans-serif; fill:#E6E6E6; }
  .bpmn .t { font-size:12px; font-weight:600; }
  .bpmn .s { font-size:9.5px; fill:#9A9A9A; font-weight:400; }
  .bpmn .h { font-family:"Montserrat"; font-size:9px; letter-spacing:2px; fill:#8F8F8F; font-weight:700; }
  .bpmn .g { font-size:9.5px; fill:#C4C4C4; font-weight:600; }
  .caixa { list-style:none; padding:0; margin:0; }
  .caixa li { font-size:7.6pt; line-height:1.4; padding-left:5mm; position:relative; margin-bottom:0.8mm; }
  .caixa li::before { content:""; position:absolute; left:0; top:0.9mm; width:2.6mm; height:2.6mm; border:1px solid #8F8F8F; border-radius:0.6mm; }
  .cam { font-family:"DejaVu Sans Mono", monospace; font-size:6.4pt; color:#9A9A9A; }
"""

SETA = '<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#seta)"/>'


def caixa(y, titulo, linhas, fixo=False, x0=80, larg=340):
    h = 38 + 14 * max(1, len(linhas))
    borda = 'stroke="#E6E6E6" stroke-width="1.6"' if fixo else 'stroke="#8F8F8F"'
    fundo = "#1C1C1C" if fixo else "#151515"
    out = [f'<rect x="{x0}" y="{y}" width="{larg}" height="{h}" rx="8" fill="{fundo}" {borda}/>',
           f'<text class="t" x="{x0 + 16}" y="{y + 22}">{E(titulo)}</text>']
    for i, l in enumerate(linhas):
        out.append(f'<text class="s" x="{x0 + 16}" y="{y + 40 + 13 * i}">{E(l)}</text>')
    return out, h


# Lugar e hora ao lado do passo, sem citar o lugar: o ícone é só uma referência ilustrada, com o horário. O passo leva "icone" (nome abaixo) e "hora" ("12:20–13:10");
# o ícone fica à esquerda da caixa, a hora embaixo dele. Lugar nunca vai por extenso no texto: o ícone é o lugar.
_TR = 'fill="none" stroke="#C4C4C4" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"'


def icone(nome, cx, cy):
    if nome == "banho":        # chuveiro: cano, crivo e gotas
        return [f'<path d="M{cx - 10},{cy - 13} L{cx + 3},{cy - 13} L{cx + 3},{cy - 8}" {_TR}/>',
                f'<path d="M{cx - 6},{cy - 2} Q{cx + 3},{cy - 12} {cx + 12},{cy - 2} Z" {_TR}/>',
                *[f'<line x1="{cx + d}" y1="{cy + 3}" x2="{cx + d - 1}" y2="{cy + 9}" {_TR}/>' for d in (-3, 3, 9)],
                *[f'<line x1="{cx + d}" y1="{cy + 11}" x2="{cx + d - 1}" y2="{cy + 15}" {_TR}/>' for d in (0, 6)]]
    if nome == "lavanderia":   # máquina de lavar
        return [f'<rect x="{cx - 11}" y="{cy - 14}" width="22" height="28" rx="3" {_TR}/>',
                f'<line x1="{cx - 11}" y1="{cy - 7}" x2="{cx + 11}" y2="{cy - 7}" {_TR}/>',
                f'<circle cx="{cx + 6}" cy="{cy - 10.5}" r="1.2" fill="#C4C4C4"/>',
                f'<circle cx="{cx}" cy="{cy + 3}" r="7" {_TR}/>',
                f'<path d="M{cx - 4},{cy + 4} Q{cx},{cy + 1} {cx + 4},{cy + 4}" {_TR}/>']
    if nome == "trabalho":     # notebook
        return [f'<rect x="{cx - 11}" y="{cy - 11}" width="22" height="15" rx="2" {_TR}/>',
                f'<path d="M{cx - 15},{cy + 9} L{cx - 11},{cy + 4} L{cx + 11},{cy + 4} L{cx + 15},{cy + 9} Z" {_TR}/>']
    if nome == "casa":
        return [f'<path d="M{cx - 13},{cy - 1} L{cx},{cy - 13} L{cx + 13},{cy - 1}" {_TR}/>',
                f'<path d="M{cx - 9},{cy - 4} L{cx - 9},{cy + 12} L{cx + 9},{cy + 12} L{cx + 9},{cy - 4}" {_TR}/>',
                f'<rect x="{cx - 3}" y="{cy + 4}" width="6" height="8" {_TR}/>']
    if nome == "cafe":         # xícara (pausa)
        return [f'<path d="M{cx - 10},{cy - 3} L{cx - 8},{cy + 10} L{cx + 6},{cy + 10} L{cx + 8},{cy - 3} Z" {_TR}/>',
                f'<path d="M{cx + 8},{cy} Q{cx + 14},{cy + 1} {cx + 7},{cy + 6}" {_TR}/>',
                *[f'<path d="M{cx + d},{cy - 7} Q{cx + d + 3},{cy - 10} {cx + d},{cy - 14}" {_TR}/>' for d in (-5, 1)]]
    if nome == "caminho":      # deslocamento: seta em curva
        return [f'<path d="M{cx - 12},{cy + 10} Q{cx - 12},{cy - 8} {cx + 8},{cy - 8}" {_TR}/>',
                f'<path d="M{cx + 3},{cy - 13} L{cx + 9},{cy - 8} L{cx + 3},{cy - 3}" {_TR}/>']
    return []


def marca_lugar(p, y, h):
    """Ícone + hora à esquerda da caixa do passo (x 0–78, fora da caixa, que começa em 80)."""
    if not (p.get("icone") or p.get("hora")):
        return []
    cy = y + h / 2 - (7 if p.get("hora") else 0)
    out = icone(p.get("icone", ""), 40, cy)
    if p.get("hora"):
        out.append(f'<text class="s" x="40" y="{cy + 29}" text-anchor="middle" style="font-size:8.5px;fill:#C4C4C4">{E(p["hora"])}</text>')
    return out


def losango(cx, cy):
    return [f'<polygon points="{cx},{cy - 28} {cx + 28},{cy} {cx},{cy + 28} {cx - 28},{cy}" fill="#151515" stroke="#C4C4C4"/>',
            f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" style="font-size:15px;fill:#C4C4C4;font-weight:700">×</text>']


def relogio(cx, cy):
    return [f'<circle cx="{cx}" cy="{cy}" r="15" fill="#151515" stroke="#8F8F8F"/>',
            f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="#8F8F8F"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 8}" stroke="#C4C4C4" stroke-width="1.2"/>',
            f'<line x1="{cx}" y1="{cy}" x2="{cx + 6}" y2="{cy + 3}" stroke="#C4C4C4" stroke-width="1.2"/>']


def svg_dia(r):
    cx, el, ancora = 250, [], {}
    y = 47
    el += [f'<circle cx="{cx}" cy="{y + 15}" r="15" fill="#151515" stroke="#C4C4C4" stroke-width="1.5"/>',
           f'<text class="g" x="{cx + 25}" y="{y + 19}">{E(r["inicio"])}</text>']
    y += 30
    for i, p in enumerate(r["passos"]):
        el.append(SETA.format(x=cx, y1=y, y2=y + 21)); y += 23
        if p["tipo"] == "decisao":
            gy = y + 28
            el += losango(cx, gy)
            perg = p["pergunta"] if isinstance(p["pergunta"], list) else [p["pergunta"]]
            for k, l in enumerate(perg):
                el.append(f'<text class="g" x="{cx + 36}" y="{gy - 4 + 13 * k}">{E(l)}</text>')
            ancora[i] = gy
            y = gy + 28
            el.append(SETA.format(x=cx, y1=y, y2=y + 24))
            el.append(f'<text class="s" x="{cx + 6}" y="{y + 16}">sim</text>')
            y += 26
            c, h = caixa(y, p["sim"]["titulo"], p["sim"].get("linhas", []), p["sim"].get("fixo", False))
            el += c; y += h
            el.append(SETA.format(x=cx, y1=y, y2=y + 24)); y += 26
            my = y + 28
            el += losango(cx, my)
            el.append(f'<polyline points="{cx - 28},{gy} 40,{gy} 40,{my} {cx - 30},{my}" fill="none" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#seta)"/>')
            el.append(f'<text class="s" x="48" y="{gy - 6}">{E(p.get("nao", "não"))}</text>')
            y = my + 28
        else:
            c, h = caixa(y, p["titulo"], p.get("linhas", []), p["tipo"] == "fixo")
            el += c + marca_lugar(p, y, h)
            ancora[i] = y + h / 2
            y += h
    el.append(SETA.format(x=cx, y1=y, y2=y + 18)); y += 20
    fy = y + 15
    el += [f'<circle cx="{cx}" cy="{fy}" r="15" fill="#151515" stroke="#E6E6E6" stroke-width="4"/>',
           f'<text class="g" x="{cx + 25}" y="{fy + 4}">{E(r.get("fim", "dia fechado"))}</text>']
    ancora["fim"] = fy
    H = fy + 28
    for ev in r.get("casa", []):
        ey = ancora[ev["passo"]]
        el += relogio(590, ey)
        linhas = [ev["hora"]] + ev.get("linhas", [])
        acima = ev["passo"] == "fim"
        for k, l in enumerate(linhas):
            cls = "g" if k == 0 else "s"
            ty = (ey - 30 - 13 * (len(linhas) - 1 - k)) if acima else (ey + 32 + 13 * k)
            el.append(f'<text class="{cls}" x="590" y="{ty}" text-anchor="middle">{E(l)}</text>')
        if ev.get("aviso"):
            el.append(f'<line x1="575" y1="{ey}" x2="424" y2="{ey}" stroke="#5A5A5A" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#seta2)"/>')
    cab = [f'<rect x="1" y="1" width="678" height="{H - 2}" rx="6" fill="none" stroke="#2A2A2A"/>',
           f'<line x1="500" y1="1" x2="500" y2="{H - 1}" stroke="#2A2A2A"/>',
           '<line x1="1" y1="30" x2="679" y2="30" stroke="#2A2A2A"/>',
           '<text class="h" x="250" y="20" text-anchor="middle">V O C Ê</text>',
           '<text class="h" x="590" y="20" text-anchor="middle">A&#160;&#160;C A S A</text>']
    defs = ('<defs><marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8F8F8F"/></marker>'
            '<marker id="seta2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5A5A5A"/></marker></defs>')
    alt_mm = min(226, 194 * H / 680)   # cabe na página do título; acima disso, encolhe por inteiro
    return (f'<svg class="bpmn" style="width:auto;height:{alt_mm:.1f}mm;margin:0 auto" viewBox="0 0 680 {H:.0f}" xmlns="http://www.w3.org/2000/svg">'
            + defs + "".join(cab + el) + "</svg>")


SVG_LACO = """<svg class="bpmn" viewBox="0 0 680 250" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="s3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#8F8F8F"/></marker></defs>
  <rect x="1" y="1" width="678" height="248" rx="6" fill="none" stroke="#2A2A2A"/>
  <circle cx="34" cy="70" r="14" fill="#151515" stroke="#C4C4C4" stroke-width="1.5"/>
  <line x1="48" y1="70" x2="70" y2="70" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <rect x="72" y="44" width="150" height="52" rx="8" fill="#151515" stroke="#8F8F8F"/>
  <text class="t" x="84" y="66">Abrir o entregável</text><text class="s" x="84" y="83">aba Entregáveis · Prontos</text>
  <line x1="222" y1="70" x2="246" y2="70" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <rect x="248" y="44" width="150" height="52" rx="8" fill="#151515" stroke="#8F8F8F"/>
  <text class="t" x="260" y="66">Ler o resumo</text><text class="s" x="260" y="83">o que é · o que pede de você</text>
  <line x1="398" y1="70" x2="440" y2="70" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <polygon points="470,42 498,70 470,98 442,70" fill="#151515" stroke="#C4C4C4"/>
  <text x="470" y="75" text-anchor="middle" style="font-size:15px;fill:#C4C4C4;font-weight:700">×</text>
  <text class="g" x="508" y="64">Pede algo</text><text class="g" x="508" y="77">seu?</text>
  <line x1="470" y1="98" x2="470" y2="128" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <text class="s" x="476" y="118">sim</text>
  <rect x="400" y="130" width="140" height="48" rx="8" fill="#151515" stroke="#8F8F8F"/>
  <text class="t" x="412" y="151">Decidir ou preencher</text><text class="s" x="412" y="167">só o campo apontado</text>
  <polyline points="400,154 300,154 300,188" fill="none" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <polyline points="498,70 620,70 620,214 380,214" fill="none" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <text class="s" x="580" y="86">não</text>
  <rect x="230" y="190" width="150" height="48" rx="8" fill="#151515" stroke="#8F8F8F"/>
  <text class="t" x="242" y="211">Colar e enviar</text><text class="s" x="242" y="227">no canal da linha 1 do arquivo</text>
  <line x1="230" y1="214" x2="196" y2="214" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <rect x="44" y="190" width="150" height="48" rx="8" fill="#151515" stroke="#8F8F8F"/>
  <text class="t" x="56" y="211">Clicar "Enviado"</text><text class="s" x="56" y="227">a casa para de cobrar</text>
  <line x1="44" y1="214" x2="26" y2="214" stroke="#8F8F8F" stroke-width="1.4" marker-end="url(#s3)"/>
  <circle cx="14" cy="214" r="10" fill="#151515" stroke="#E6E6E6" stroke-width="3.5"/>
</svg>"""


def tabela(linhas, col3="O que é seu"):
    out = [f'<table>\n  <tr><th style="width:5%"></th><th style="width:30%">O quê</th><th>{E(col3)}</th></tr>']
    for l in linhas:   # texto e título aceitam HTML curto (<strong>, <em>): o JSON é nosso
        cam = f'<br><span class="cam">{E(l["caminho"])}</span>' if l.get("caminho") else ""
        out.append(f'  <tr><td class="num5">{E(str(l.get("n", "·")))}</td><td><strong>{l["titulo"]}</strong>{cam}</td><td>{l["texto"]}</td></tr>')
    return "\n".join(out) + "\n</table>"


# Símbolo fora das fontes do modelo (✓, emoji) cai numa fonte do sistema e sai Type3 no PDF (reprovado).
TROCA = {"✓": "OK", "✔": "OK", "⚠️ ": "Atenção: ", "⚠️": "Atenção:", "⚠ ": "Atenção: ", "🔴 ": "", "🟡 ": "", "🟢 ": "", "🚀": ""}


def limpar(o):
    if isinstance(o, str):
        for k, v in TROCA.items():
            o = o.replace(k, v)
        return o
    if isinstance(o, list):
        return [limpar(x) for x in o]
    if isinstance(o, dict):
        return {k: limpar(v) for k, v in o.items()}
    return o


def laco(r):
    """Página do laço de envio. Dia de imersão, sem envios de colar, leva "laco": false e a página sai."""
    if not r.get("laco", True):
        return ""
    return f"""<div class="page-break"></div>
<div class="rotulo">02 · como cada envio anda</div>
<h1>O mesmo laço, <span>para todos</span></h1>
<p class="sub">{E(r.get('laco_sub', 'Se a resposta do entregável disser "precisa de você", é só aquilo: uma decisão ou um campo. O resto está escrito.'))}</p>
{SVG_LACO}
<div class="destaque"><span class="lead">Um envio só "existe" quando o botão é clicado</span>
<p>O sistema não lê o seu WhatsApp para saber o que saiu. Sem o clique, a rodada seguinte continua tratando o entregável como pendente, e o painel da conta continua mostrando o atraso.</p></div>
"""


def montar(r):
    r = limpar(r)
    c = r["capa"]
    partes = [f"""<!DOCTYPE html>
<!-- Roteiro do dia · {E(r['data'])} · MODELO 10 (90-templates/roteiro-do-dia/gerar_roteiro.py). Gerado: não editar à mão; edita-se o JSON. -->
<html lang="pt-BR"><head><meta charset="utf-8"><title>Roteiro do dia</title>
<link rel="stylesheet" href="noturno.css"><link rel="stylesheet" href="eletrico.css"><style>{ESTILO}</style></head><body>
<div class="capa"><div class="miolo">
  <div class="kicker">{' '.join(E(c['kicker']))}</div>
  <h1>{E(c['titulo'])} <span>{E(c['span'])}</span></h1>
  <p class="lead">{c['lead']}</p>
  <div class="botao">ROTEIRO INTERNO · USO DO OPERADOR</div>
</div><div class="rodape">CONTINUUM AI SYSTEMS · ROTEIRO DO DIA · {E(r['data_extenso']).upper()}</div></div>

<div class="rotulo">01 · o dia, em um fluxo</div>
<h1>Siga de cima <span>para baixo</span></h1>
<p class="sub">À esquerda, o que é seu. À direita, o que a casa faz sozinha e quando ela te chama. Losango é decisão; tracejado é aviso; borda branca é hora marcada.</p>
{svg_dia(r)}

{laco(r)}
<div class="page-break"></div>
<div class="rotulo">{'03' if r.get('laco', True) else '02'} · o que tem em cada passo</div>
<h1>Peça por peça, <span>com o que é seu</span></h1>
<p class="sub">Caminho de cada arquivo embaixo, para achar rápido no sistema ou na pasta.</p>
{tabela(r['agora'])}
"""]
    if r.get("tarde"):
        partes.append(f"""<div class="page-break"></div>
<div class="rotulo">{'03' if r.get('laco', True) else '02'} · continuação</div>
<h1>{E(r['tarde_titulo'][0])} <span>{E(r['tarde_titulo'][1])}</span></h1>
<p class="sub">{E(r.get('tarde_sub', ''))}</p>
{tabela(r['tarde'], 'O que é seu · prazo')}
""")
    if r.get("destaque"):
        partes.append(f'<div class="destaque"><span class="lead">{E(r["destaque"][0])}</span><p>{r["destaque"][1]}</p></div>\n')
    if r.get("fechar"):
        partes.append('<h2>Antes de fechar o dia</h2>\n<ul class="caixa">\n' + "\n".join(f"  <li>{l}</li>" for l in r["fechar"]) + "\n</ul>\n")
    partes.append("</body></html>\n")
    return "".join(partes)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    js = Path(sys.argv[1]).resolve()
    r = json.loads(io.open(js, encoding="utf-8").read())
    pasta = js.parent
    for f in ("noturno.css", "eletrico.css"):
        shutil.copy2(NOTURNO / f, pasta / f)
    if not (pasta / "fontes").exists():
        shutil.copytree(NOTURNO / "fontes", pasta / "fontes")
    nome = r.get("arquivo", "roteiro-do-dia")
    h = pasta / f"{nome}.html"
    io.open(h, "w", encoding="utf-8", newline="\n").write(montar(r))
    print("HTML:", h)
    if "--so-html" in sys.argv:
        return
    rc = subprocess.run([sys.executable, "-X", "utf8", str(NOTURNO / "gerar_pdf.py"), str(h), str(pasta / f"{r.get('pdf', nome)}.pdf")]).returncode
    sys.exit(rc)


if __name__ == "__main__":
    main()
