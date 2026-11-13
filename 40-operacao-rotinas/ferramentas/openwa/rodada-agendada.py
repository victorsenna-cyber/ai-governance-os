# -*- coding: utf-8 -*-
"""
rodada-agendada.py — o comando da task diária de captura (T-2026-10-28-012) pelo despachante.

Garante o Docker Desktop de pé (abre e espera até 4 min se estiver fechado), sobe o contêiner
do OpenWA e roda a rodada.py com o mesmo Python, nunca o `py` da Store.
Caso que instituiu (11/11/2026): a rodada das 12h falhou em 0 s porque o Docker estava fechado.

  python rodada-agendada.py [--espaco 30]   (os argumentos seguem para a rodada.py)
"""
import os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
COMPOSE = os.path.normpath(os.path.join(RAIZ, "..", "..", "42 - repo iso", "OpenWA", "docker-compose.dev.yml"))
DOCKER_DESKTOP = r"C:\Program Files\Docker\Docker\Docker Desktop.exe"


def docker_ok():
    r = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"], capture_output=True, text=True)
    return r.returncode == 0


def main():
    if not docker_ok():
        if not os.path.exists(DOCKER_DESKTOP):
            print("Docker fechado e Docker Desktop não encontrado em " + DOCKER_DESKTOP); return 1
        print("Docker fechado: abrindo o Docker Desktop…", flush=True)
        subprocess.Popen([DOCKER_DESKTOP], creationflags=getattr(subprocess, "DETACHED_PROCESS", 0))
        for _ in range(48):  # até 4 min
            time.sleep(5)
            if docker_ok():
                break
        else:
            print("Docker não subiu em 4 min."); return 1
        print("Docker de pé.", flush=True)
    r = subprocess.run(["docker", "compose", "-f", COMPOSE, "up", "-d"])
    if r.returncode != 0:
        print("docker compose up falhou."); return r.returncode
    time.sleep(10)  # o OpenWA reconecta a sessão do WhatsApp
    return subprocess.run([sys.executable, "-X", "utf8", os.path.join(AQUI, "rodada.py")] + sys.argv[1:], cwd=RAIZ).returncode


if __name__ == "__main__":
    sys.exit(main())
