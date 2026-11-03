"""
gerar_pdf.py · imprime um documento do pdf-noturno/elétrico e CONFERE o PDF (01/11/2026)

    python3 gerar_pdf.py documento.html                 -> documento.pdf ao lado do HTML
    python3 gerar_pdf.py documento.html saida.pdf
    python3 gerar_pdf.py documento.html --png pasta/    -> também grava a capa em PNG, para olhar
    python3 gerar_pdf.py --conferir arquivo.pdf [--html documento.html]   -> só confere um PDF pronto

Imprime pelo Chrome sem interface (o WeasyPrint costuma não carregar no Windows) e reprova,
com código de saída 1, o PDF que tiver:
  1. fonte Type3 (fonte variável do Google Fonts: o PDF abre quebrado)
  2. fita da capa que não chega às DUAS bordas da página com texto dentro
  3. página sem texto nenhum (capa que vazou e empurrou uma página em branco)

Por que existe: defeito corrigido só no documento volta
no PDF seguinte, porque o conserto não chegou ao modelo. Conferir a olho depende de
alguém lembrar; este script não depende.
Precisa de PyMuPDF (fitz). Reprovado = não entregar.
"""
import os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

try:
    import fitz
except ImportError:
    sys.exit("falta o PyMuPDF: python3 -m pip install pymupdf")

CANDIDATOS_CHROME = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or "",
]


def achar_chrome():
    for c in CANDIDATOS_CHROME:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome não encontrado. Defina a variável CHROME com o caminho do executável.")


def imprimir(html: Path, pdf: Path):
    # imprime num caminho temporário sem acento nem espaço e move depois:
    # o Chrome falha com caminho acentuado vindo do Git Bash (27/10)
    with tempfile.TemporaryDirectory() as tmp:
        saida_tmp = Path(tmp) / "saida.pdf"
        cmd = [achar_chrome(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
               "--virtual-time-budget=10000", f"--print-to-pdf={saida_tmp}", html.resolve().as_uri()]
        r = subprocess.run(cmd, capture_output=True, timeout=180)
        if not saida_tmp.exists():
            sys.exit("o Chrome não gerou o PDF:\n" + r.stderr.decode("utf-8", "ignore")[-1500:])
        shutil.move(str(saida_tmp), str(pdf))


def conferir_fontes(doc):
    erros = []
    for i, pagina in enumerate(doc, 1):
        t3 = [f for f in pagina.get_fonts() if f[2] == "Type3"]
        if t3:
            erros.append(f"página {i}: {len(t3)} fonte(s) Type3. Carregar as fontes de fontes/ "
                         "pelo eletrico.css, nunca pelo link do Google Fonts.")
            break
    return erros


def conferir_paginas_vazias(doc):
    return [f"página {i}: sem texto nenhum (página em branco?)"
            for i, pagina in enumerate(doc, 1) if not pagina.get_text().strip()]


def conferir_fita(doc, n_fitas):
    """Na capa, nas faixas de 6 mm das duas bordas, procura as fitas (pixels claros) e,
    no meio de cada uma, o texto (pixels escuros). Fita que não chega à borda, ou que
    chega vazia, reprova."""
    if n_fitas == 0:
        return []
    pagina = doc[0]
    dpi = 100
    pix = pagina.get_pixmap(dpi=dpi)
    w, h, n = pix.width, pix.height, pix.n
    amostra = pix.samples
    mm = dpi / 25.4
    tira = max(4, int(6 * mm))
    y0, y1 = int(h * 0.04), int(h * 0.35)  # zona das fitas: acima do miolo da capa

    def px(x, y):
        k = (y * w + x) * n
        return amostra[k], amostra[k + 1], amostra[k + 2]

    erros = []
    for lado, xs in (("esquerda", range(0, tira)), ("direita", range(w - tira, w))):
        linhas_fita = []
        for y in range(y0, y1):
            claros = sum(1 for x in xs if max(px(x, y)) > 150)
            linhas_fita.append(claros >= 0.3 * len(xs))
        # agrupa linhas consecutivas: cada grupo é uma fita cruzando a borda
        grupos, ini = [], None
        for i, sim in enumerate(linhas_fita + [False]):
            if sim and ini is None:
                ini = i
            elif not sim and ini is not None:
                if i - ini >= int(2 * mm):
                    grupos.append((y0 + ini, y0 + i))
                ini = None
        if len(grupos) < n_fitas:
            erros.append(f"capa: só {len(grupos)} de {n_fitas} fita(s) chegam à borda {lado}. "
                         "A fita não pode ter largura em mm: usar o eletrico.css do modelo sem sobrescrever.")
            continue
        for a, b in grupos:
            meio = range(a + (b - a) * 35 // 100, a + (b - a) * 65 // 100 + 1)
            total = escuros = 0
            for y in meio:
                for x in xs:
                    total += 1
                    escuros += max(px(x, y)) < 100
            if total and escuros / total < 0.01:
                erros.append(f"capa: uma fita chega à borda {lado} sem texto. "
                             "A frase acabou antes da borda: pôr a frase no data-texto da fita.")
    return erros


def conferir(pdf: Path, html: Path | None):
    n_fitas = 0
    if html and html.exists():
        n_fitas = len(re.findall(r'class="fita\b', html.read_text(encoding="utf-8", errors="ignore")))
    doc = fitz.open(pdf)
    erros = conferir_fontes(doc) + conferir_paginas_vazias(doc) + conferir_fita(doc, n_fitas)
    p = doc[0].rect
    print(f"{pdf.name}: {len(doc)} página(s), {p.width / 72 * 25.4:.0f} x {p.height / 72 * 25.4:.0f} mm, "
          f"{n_fitas} fita(s) na capa")
    return doc, erros


def main():
    for fluxo in (sys.stdout, sys.stderr):
        try: fluxo.reconfigure(encoding="utf-8")
        except Exception: pass
    args = sys.argv[1:]
    png = None
    if "--png" in args:
        i = args.index("--png"); png = Path(args[i + 1]); del args[i:i + 2]
    if args and args[0] == "--conferir":
        pdf = Path(args[1])
        html = Path(args[args.index("--html") + 1]) if "--html" in args else None
    elif args:
        html = Path(args[0])
        pdf = Path(args[1]) if len(args) > 1 else html.with_suffix(".pdf")
        imprimir(html, pdf)
    else:
        sys.exit(__doc__)
    doc, erros = conferir(pdf, html)
    if png:
        png.mkdir(parents=True, exist_ok=True)
        destino = png / (pdf.stem + "-capa.png")
        doc[0].get_pixmap(dpi=60).save(destino)
        print("capa em", destino)
    if erros:
        print("REPROVADO, não entregar:")
        for e in erros:
            print("  -", e)
        sys.exit(1)
    print("aprovado: sem Type3, sem página em branco, fita de borda a borda")


if __name__ == "__main__":
    main()
