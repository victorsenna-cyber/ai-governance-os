#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
publicar.py — sobe o site do painel de projetos para a Hostinger, na pasta /projetos/ do domínio do
painel financeiro (financeiro.{{DOMINIO}}/projetos/): mesmo login, mesma sessão do navegador.

Token da API da Hostinger em ~/.continuum/hostinger-token.txt (ou HOSTINGER_API_TOKEN), nunca no repo.
Mesmo envio TUS do painel de resultado (40-operacao-rotinas/ferramentas/painel-resultado/servir.py).

  python3 publicar.py            # envia index.html, config.js e .htaccess
  python3 publicar.py --conferir # baixa cada arquivo publicado e compara byte a byte
"""
import argparse, hashlib, io, json, os, sys, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SITE = json.loads((AQUI / ".hostinger" / "site.json").read_text(encoding="utf-8"))
API = "https://developers.hostinger.com/api/hosting/v1/files/upload-urls"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Continuum-painel-projetos"
TOKEN_ARQ = Path.home() / ".continuum" / "hostinger-token.txt"
ARQUIVOS = ("index.html", "config.js", ".htaccess")


def token():
    t = os.environ.get("HOSTINGER_API_TOKEN") or (TOKEN_ARQ.read_text(encoding="utf-8").strip() if TOKEN_ARQ.exists() else "")
    if not t:
        sys.exit(f"sem token da Hostinger: {TOKEN_ARQ}")
    return t


def pedir_upload_url():
    req = urllib.request.Request(API, data=json.dumps({"username": SITE["username"], "domain": SITE["domain"]}).encode(),
                                 method="POST", headers={"Authorization": f"Bearer {token()}", "Content-Type": "application/json",
                                                         "User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def subir(caminho, dados):
    j = pedir_upload_url()
    base = {"X-Auth": j["auth_key"], "X-Auth-Rest": j["rest_auth_key"], "Tus-Resumable": "1.0.0", "User-Agent": UA}
    alvo = f"{j['url']}/{caminho}"
    for metodo, extra, corpo, esperado in (
            ("POST", {"Upload-Length": str(len(dados)), "Upload-Offset": "0"}, b"", 201),
            ("PATCH", {"Upload-Offset": "0", "Content-Type": "application/offset+octet-stream"}, dados, 204)):
        req = urllib.request.Request(alvo + ("?override=true" if metodo == "POST" else ""), data=corpo, method=metodo,
                                     headers={**base, **extra})
        with urllib.request.urlopen(req, timeout=60) as r:
            if r.status != esperado:
                raise RuntimeError(f"envio falhou ({metodo} {r.status})")


def conferir():
    ok = True
    for a in ARQUIVOS:
        if a == ".htaccess":
            continue
        url = f"https://{SITE['domain']}/{SITE['pasta']}/{a}"
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=30) as r:
            remoto = r.read()
        local = (AQUI / a).read_bytes()
        igual = hashlib.sha256(remoto).hexdigest() == hashlib.sha256(local).hexdigest()
        ok &= igual
        print(("✅" if igual else "🔴"), url, f"{len(remoto)} bytes")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conferir", action="store_true")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    if a.conferir:
        return conferir()
    for arq in ARQUIVOS:
        dados = (AQUI / arq).read_bytes()
        subir(f"{SITE['pasta']}/{arq}", dados)
        print("↑", f"{SITE['pasta']}/{arq}", len(dados), "bytes")
    print(f"publicado em https://{SITE['domain']}/{SITE['pasta']}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
