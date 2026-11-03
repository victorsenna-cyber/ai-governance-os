#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_prancha.py — monta a prancha de escolha (método: 100-métodos/METODO-PRANCHA-DE-ESCOLHA.md).

Uso:  python3 gerar_prancha.py manifesto.json [--png]
Manifesto:
  {"titulo": "Prancha de", "titulo_italico": "teste", "subtitulo": "…",
   "saida": "prancha-teste.html",                       # relativo ao manifesto
   "secoes": [{"codigo": "1", "nome": "Escolha a tipografia", "colunas": 4,
               "itens": [{"img": "teste/saida/x.png", "rotulo": "A", "legenda": "…", "mudar": "…"}]}]}
Caminhos de imagem são relativos à página gerada.
--png  também salva <saida>.png para enviar ao cliente ("altura_png" no manifesto, padrão 3600).
"""
import html, io, json, os, subprocess, sys, tempfile

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), '40-operacao-rotinas', 'ferramentas'))
from navegador import chrome_path  # noqa: E402  Chrome em Windows, macOS e Linux (ou CHROME=<caminho>)
CHROME = chrome_path()
e = html.escape
CSS = """:root{--noite:#0A0907;--carvao:#16130F;--borda:#2A251E;--pedra:#8A8378;--osso:#EFE9DD;--luz:#E9A23B}
*{box-sizing:border-box}body{margin:0;background:var(--noite);color:var(--osso);font:15px/1.45 'Instrument Sans',sans-serif;padding:32px 16px 64px}
main{max-width:1320px;margin:0 auto}h1{font:400 clamp(34px,6vw,60px)/1 'Instrument Serif',serif;margin:0 0 10px}h1 i{color:var(--luz)}
p.sub{color:var(--pedra);font:13px/1.55 'JetBrains Mono',monospace;max-width:820px}
h2{font:400 30px 'Instrument Serif',serif;border-top:1px solid var(--borda);padding-top:18px;margin:44px 0 14px}
h2 em{font:500 12px 'JetBrains Mono',monospace;color:var(--luz);font-style:normal;margin-right:10px;letter-spacing:.1em}
.g{display:grid;gap:16px}figure{margin:0}img{width:100%;display:block;border:1px solid var(--borda);border-radius:4px}
figcaption{font:12px/1.4 'JetBrains Mono',monospace;color:var(--pedra);margin-top:8px}figcaption b{color:var(--luz);font-weight:500;margin-right:6px}
figcaption span{display:block;margin-top:4px;opacity:.85}
@media(max-width:700px){.g{grid-template-columns:repeat(2,1fr)!important}}"""
FONTES = ("https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1"
          "&family=JetBrains+Mono:wght@400;500&family=Instrument+Sans:wght@400;600&display=swap")

def gerar(m):
    h = [f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         f'<title>{e(m.get("titulo", "Prancha") + " " + m.get("titulo_italico", ""))}</title>'
         f'<link href="{FONTES}" rel="stylesheet"><style>{CSS}</style></head><body><main>',
         f'<h1>{e(m.get("titulo", "Prancha de"))} <i>{e(m.get("titulo_italico", "escolha"))}</i></h1>',
         f'<p class="sub">{e(m.get("subtitulo", ""))}</p>']
    for s in m["secoes"]:
        cols = s.get("colunas", 4)
        h.append(f'<h2><em>{e(str(s.get("codigo", "")))}</em> {e(s["nome"])}</h2>'
                 f'<div class="g" style="grid-template-columns:repeat({cols},1fr)">')
        for it in s["itens"]:
            mudar = f'<span>mudar: {e(it["mudar"])}</span>' if it.get("mudar") else ""
            h.append(f'<figure><img loading="lazy" src="{e(it["img"])}" alt="{e(it.get("rotulo", ""))}">'
                     f'<figcaption><b>{e(it.get("rotulo", ""))}</b>{e(it.get("legenda", ""))}{mudar}</figcaption></figure>')
        h.append("</div>")
    h.append("</main></body></html>\n")
    return "".join(h)

if __name__ == "__main__":
    arq = os.path.abspath(sys.argv[1])
    m = json.load(io.open(arq, encoding="utf-8"))
    saida = os.path.join(os.path.dirname(arq), m.get("saida", "prancha.html"))
    io.open(saida, "w", encoding="utf-8", newline="\n").write(gerar(m))
    print("ok", saida)
    if "--png" in sys.argv:
        png = os.path.splitext(saida)[0] + ".png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size=1360,{m.get('altura_png', 3600)}",
                        "--virtual-time-budget=9000", f"--user-data-dir={tempfile.mkdtemp(prefix='prancha-')}",
                        f"--screenshot={png}", "file:///" + saida.replace("\\", "/")], capture_output=True, timeout=180)
        print(("ok " if os.path.exists(png) else "ERRO ") + png)
