#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
navegador.py — acha o Chrome (ou equivalente) em Windows, macOS e Linux.

Uso nos scripts da casa:
    from navegador import chrome_path
    CHROME = chrome_path()          # str, ou levanta RuntimeError com instrução

Ordem: variável de ambiente CHROME → caminhos conhecidos do sistema → `which`.
Rodar direto (`python3 navegador.py`) imprime o caminho encontrado.
"""
import os, shutil, sys

CANDIDATOS = {
    "win32": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ],
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ],
    "linux": [
        "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium",
        "/usr/bin/chromium-browser", "/snap/bin/chromium", "/usr/bin/microsoft-edge",
    ],
}
NOMES = ["google-chrome", "google-chrome-stable", "chrome", "chromium", "chromium-browser", "msedge", "brave"]


def chrome_path(obrigatorio=True):
    env = os.environ.get("CHROME")
    if env and os.path.exists(env):
        return env
    chave = "win32" if sys.platform.startswith("win") else ("darwin" if sys.platform == "darwin" else "linux")
    for c in CANDIDATOS[chave]:
        if os.path.exists(c):
            return c
    for n in NOMES:
        w = shutil.which(n)
        if w:
            return w
    if obrigatorio:
        raise RuntimeError("Chrome não encontrado. Instale o Google Chrome ou defina a variável de ambiente CHROME "
                           "com o caminho do executável (macOS: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome').")
    return None


if __name__ == "__main__":
    print(chrome_path())
