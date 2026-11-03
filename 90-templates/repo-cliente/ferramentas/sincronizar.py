#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sincronizar.py — a sincronia deste repositório com o GitHub, igual à da Governança.

🔴 Não editar aqui. A fonte é a Governança, `90-templates/repo-cliente/ferramentas/`,
e o sincronizar da Governança copia a versão nova para cá a cada rodada.

Uma operação, igual em qualquer computador:
  1. confere dado sensível (verificar.py, vetos): achou → não publica nada e diz onde está
  2. commita tudo o que mudou na pasta (git add -A)
  3. traz a main do GitHub e mescla no ponto atual (merge, nunca rebase)
  4. publica: HEAD → main

Conflito: a mescla é desfeita, nada se perde, e o aviso diz o que fazer.

Roda sozinho pelos hooks de `.claude/settings.json` (ao abrir e ao fechar a conversa no Claude) e à mão:
  python <este arquivo> [-m "mensagem"] [--hook] [--sem-push]
"""
import json, os, socket, subprocess, sys, time

for fluxo in (sys.stdout, sys.stderr):
    if hasattr(fluxo, "reconfigure"):
        fluxo.reconfigure(encoding="utf-8")

sys.dont_write_bytecode = True   # o import do verificar não deixa __pycache__ para trás (subiu ao GitHub em 30/10/2026)
AQUI = os.path.dirname(os.path.abspath(__file__))
AMBIENTE = dict(os.environ, GIT_TERMINAL_PROMPT="0")   # hook nunca fica parado esperando senha
IGNORAR = ["__pycache__/", "*.pyc"]                    # nunca vai ao GitHub, diga o .gitignore o que disser


def _raiz():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=AQUI, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=AMBIENTE)
    return r.stdout.strip() if r.returncode == 0 else ""


RAIZ = _raiz()


def git(*args, ok=False):
    r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=AMBIENTE)
    if r.returncode != 0 and not ok:
        raise RuntimeError(f"git {' '.join(args)}: {(r.stderr or r.stdout).strip()[-600:]}")
    return r


def identidade():
    """Computador sem nome e e-mail no git: o commit sai com o nome da máquina, em vez de falhar."""
    extra = []
    if not git("config", "user.name", ok=True).stdout.strip():
        extra += ["-c", f"user.name={socket.gethostname()}"]
    if not git("config", "user.email", ok=True).stdout.strip():
        extra += ["-c", "user.email=sistema@repositorio.local"]
    return extra


def vetos():
    sys.path.insert(0, AQUI)
    try:
        import verificar
        return verificar.vetos(RAIZ), ""
    except Exception as e:   # sem o gate, publica, mas avisa
        return [], f"⚠️ verificar.py não rodou ({e}); publicado sem conferir dado sensível"


def garantir_ignorados():
    p = os.path.join(RAIZ, ".gitignore")
    t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    falta = [l for l in IGNORAR if l not in t.splitlines()]
    if falta:
        with open(p, "a", encoding="utf-8", newline="\n") as f:
            f.write(("\n" if t and not t.endswith("\n") else "") + "\n".join(falta) + "\n")
    git("rm", "-r", "-q", "--cached", "--ignore-unmatch", "*__pycache__*", ok=True)


def commitar(msg):
    git("add", "-A")
    if git("diff", "--cached", "--quiet", ok=True).returncode != 0:
        git(*identidade(), "commit", "-q", "-m", msg)
        return True
    return False


def mesclar_main():
    """Mescla origin/main no HEAD. Devolve os arquivos em conflito (vazio = ok)."""
    git("fetch", "-q", "origin", "main")
    if git("merge-base", "--is-ancestor", "origin/main", "HEAD", ok=True).returncode == 0:
        return []
    if git(*identidade(), "merge", "--no-edit", "-q", "origin/main", ok=True).returncode == 0:
        return []
    conflitos = [l for l in git("-c", "core.quotepath=false", "diff", "--name-only",
                                "--diff-filter=U").stdout.splitlines() if l]
    git("merge", "--abort", ok=True)
    return conflitos or ["(mescla recusada sem arquivo em conflito)"]


def main():
    hook = "--hook" in sys.argv
    sem_push = "--sem-push" in sys.argv
    msg = sys.argv[sys.argv.index("-m") + 1] if "-m" in sys.argv else None
    evento = {}
    if hook:
        try:
            evento = json.load(sys.stdin)
        except Exception:
            evento = {}
    no_stop = hook and evento.get("hook_event_name") == "Stop" and not evento.get("stop_hook_active")

    def falhar(txt):
        print(txt, file=sys.stderr)
        sys.exit(2 if no_stop else (0 if hook else 1))

    if not RAIZ:
        falhar("🔴 sincronizar: esta pasta não é um repositório git.")
    if os.name == "nt":
        git("config", "core.fileMode", "false", ok=True)

    onde = socket.gethostname()
    carimbo = time.strftime("%d/%m/%Y %H:%M")
    try:
        if git("rev-parse", "-q", "--verify", "MERGE_HEAD", ok=True).returncode == 0:
            raise RuntimeError("há uma mescla em andamento: resolva os conflitos e rode de novo")
        garantir_ignorados()
        achados, aviso = vetos()
        if achados:
            falhar("🔴 sincronizar: nada foi publicado. Há dado sensível que não pode ir para o GitHub:\n"
                   + "\n".join(f"   · {a}" for a in achados[:15])
                   + "\n   Tire o dado do arquivo (ele mora no banco de dados ou com o contador) e rode de novo.")
        if aviso:
            print(aviso)
        commitar(msg or f"sync ({onde}): {carimbo}")
        duros = mesclar_main()
        if duros:
            falhar("🔴 sincronizar: o GitHub tem mudança que conflita com a daqui em " + ", ".join(duros)
                   + ". A mescla foi desfeita e nada se perdeu. Resolver: `git merge origin/main`, editar os "
                   "arquivos mantendo as duas versões quando ambas valem (em STATUS e DECISOES, as entradas "
                   "das duas pontas, em ordem de data), `git add -A`, `git commit`, e rodar de novo.")
        if not sem_push:
            for _ in range(3):
                r = git("push", "-q", "origin", "HEAD:main", ok=True)
                if r.returncode == 0:
                    break
                if mesclar_main():
                    raise RuntimeError("o GitHub mudou durante a publicação e gerou conflito")
            else:
                raise RuntimeError("publicação recusada: " + (r.stderr or "").strip()[-300:])
        print(f"✅ sincronizado ({onde}) {carimbo}")
    except RuntimeError as e:
        print(f"🔴 sincronizar: {e}", file=sys.stderr)
        sys.exit(0 if hook else 1)


if __name__ == "__main__":
    main()
