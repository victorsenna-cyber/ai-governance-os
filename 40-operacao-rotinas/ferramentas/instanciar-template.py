#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instanciar-template.py — preenche os placeholders {{…}} do template Continuum.

Uso:
  python3 40-operacao-rotinas/ferramentas/instanciar-template.py --listar
      lista cada placeholder com quantidade de ocorrências e os arquivos (caminho:linha)
  python3 40-operacao-rotinas/ferramentas/instanciar-template.py --definir EMPRESA="Minha Empresa" OPERADOR="Nome"
      substitui em todo o repositório (texto: .md .py .json .yml .html .css .js .txt .bat .sql)
  python3 40-operacao-rotinas/ferramentas/instanciar-template.py --arquivo valores.json
      lê um JSON {"EMPRESA": "...", "OPERADOR": "..."} e substitui
  --dry-run   mostra o que mudaria, sem gravar

Nunca altera .git nem pastas _legado. Placeholder não definido fica como está (não vira palpite).
"""
import io, json, os, re, sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEXTO = (".md", ".py", ".json", ".yml", ".yaml", ".html", ".css", ".js", ".txt", ".bat", ".sql", ".sh")
RX = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def arquivos():
    for dp, dns, fns in os.walk(RAIZ):
        dns[:] = [d for d in dns if d not in (".git", "node_modules", "__pycache__", "_legado")]
        for fn in fns:
            if fn.lower().endswith(TEXTO):
                yield os.path.join(dp, fn)


def listar():
    onde = defaultdict(list)
    for p in arquivos():
        try:
            for i, l in enumerate(io.open(p, encoding="utf-8"), 1):
                for m in RX.finditer(l):
                    onde[m.group(1)].append("%s:%d" % (os.path.relpath(p, RAIZ), i))
        except UnicodeDecodeError:
            continue
    for k in sorted(onde, key=lambda k: -len(onde[k])):
        print("{{%s}}  ×%d" % (k, len(onde[k])))
        for o in onde[k][:8]:
            print("    ", o)
        if len(onde[k]) > 8:
            print("     … +%d" % (len(onde[k]) - 8))
    print("\n%d placeholders distintos" % len(onde))


def definir(valores, dry):
    n = 0
    for p in arquivos():
        try:
            t = io.open(p, encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        u = RX.sub(lambda m: valores.get(m.group(1), m.group(0)), t)
        if u != t:
            n += 1
            print(("[dry] " if dry else "") + os.path.relpath(p, RAIZ))
            if not dry:
                io.open(p, "w", encoding="utf-8", newline="").write(u)
    print("%d arquivo(s) %s" % (n, "mudariam" if dry else "alterado(s)"))


def main():
    a = sys.argv[1:]
    dry = "--dry-run" in a
    if "--listar" in a or not a:
        return listar()
    valores = {}
    if "--arquivo" in a:
        valores.update(json.load(io.open(a[a.index("--arquivo") + 1], encoding="utf-8")))
    if "--definir" in a:
        for kv in a[a.index("--definir") + 1:]:
            if kv.startswith("--"):
                break
            k, _, v = kv.partition("=")
            valores[k.strip()] = v
    if not valores:
        print("nada a definir"); return
    definir(valores, dry)


if __name__ == "__main__":
    main()
