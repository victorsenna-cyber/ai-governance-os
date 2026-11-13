#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agenda_pdfs.py — leva as folhas de call em PDF do repo para o bucket privado `calls-pdf` do Supabase, de onde a tela
Agenda do painel as abre por URL assinada de 10 min (abre no celular, sem login no GitHub, nada público).

Roda no Action .github/workflows/agenda-pdfs.yml a cada push que mexe em `clientes/*/00 - roteiros calls/**` ou
`parceiros/*/00 - roteiros calls/**`. Manda o índice inteiro à Edge Function `agenda` (ação pdf_indice), que devolve o
que mudou (sha256 diferente) e tira do bucket o que saiu do repo; depois sobe só esses (pdf_subir).

Token: FINANCAS_SYNC_TOKEN (o mesmo secret do Action do painel). A chave do objeto no bucket é p/<sha1 do caminho>.pdf
(nome sem acento nem espaço); o caminho real fica no índice.

  python3 agenda_pdfs.py            # sincroniza
  python3 agenda_pdfs.py --listar   # só mostra o índice que mandaria
"""
import argparse, base64, hashlib, json, os, re, sys, urllib.error, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FUNCAO = os.environ.get("AGENDA_FUNCAO_URL", "https://SEU-PROJETO.supabase.co/functions/v1/agenda")
CHAVE_PUBLICA = os.environ.get("AGENDA_CHAVE_PUBLICA", "")   # publicável, não é segredo
PASTA = "00 - roteiros calls"


def indice():
    itens = []
    for base in ("clientes", "parceiros"):
        for pdf in sorted((RAIZ / base).glob(f"*/{PASTA}/**/*.pdf")):
            rel = pdf.relative_to(RAIZ).as_posix()
            partes = rel.split("/")
            conta = partes[1]
            pasta = partes[3] if len(partes) > 4 else ""
            m = re.match(r"(\d{4}-\d{2}-\d{2})", pasta)
            itens.append({"caminho": rel, "chave": f"p/{hashlib.sha1(rel.encode('utf-8')).hexdigest()}.pdf", "conta": conta,
                          "data": m.group(1) if m else "", "pasta": pasta, "nome": pdf.name,
                          "sha": hashlib.sha256(pdf.read_bytes()).hexdigest()})
    return itens


def chamar(corpo, tok):
    req = urllib.request.Request(FUNCAO, data=json.dumps(corpo).encode("utf-8"), method="POST", headers={
        "apikey": CHAVE_PUBLICA, "Content-Type": "application/json", "x-agenda-token": tok, "User-Agent": "Continuum-agenda-pdfs"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"🔴 {corpo.get('acao')}: {e.code} {e.read().decode('utf-8', 'replace')[:400]}")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()
    itens = indice()
    if a.listar:
        for i in itens:
            print(i["data"] or "—", i["conta"], "·", i["caminho"])
        print(len(itens), "PDF(s)")
        return 0
    tok = os.environ.get("FINANCAS_SYNC_TOKEN", "").strip()
    if not tok:
        sys.exit("sem FINANCAS_SYNC_TOKEN")
    r = chamar({"acao": "pdf_indice", "itens": itens}, tok)
    subir = r.get("subir", [])
    print(f"{len(itens)} no índice · {len(subir)} para subir · {r.get('removidos', 0)} removido(s) do bucket")
    por_caminho = {i["caminho"]: i for i in itens}
    for c in subir:
        dados = (RAIZ / c).read_bytes()
        chamar({"acao": "pdf_subir", "caminho": c, "sha": por_caminho[c]["sha"], "base64": base64.b64encode(dados).decode("ascii")}, tok)
        print("↑", c, len(dados), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
