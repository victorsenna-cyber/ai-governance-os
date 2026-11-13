#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backup.py — a cópia de segurança deste repositório no próprio computador, fora da pasta dele.

🔴 Não editar aqui. A fonte é a Governança, `90-templates/repo-cliente/ferramentas/`,
e o sincronizar da Governança copia a versão nova para cá a cada rodada.

Regra: todo repositório vivo guarda backup local, para o caso de uma alteração que não dê para reverter rápido. Molde: o backup da própria Governança (40-operacao-rotinas/ferramentas/backup-governanca.py).

Onde fica, em qualquer computador (Windows ou Mac): <pasta do usuário>/Backups-repositorios/<nome-do-repo>.git
— um repositório "bare", fora da pasta do repo, que SÓ RECEBE. Nunca é fonte e não se edita.

O que guarda, a cada sincronia (o sincronizar.py chama sozinho, em silêncio; falha aqui nunca para a sincronia):
  - `main`   : o estado deste computador, antes de juntar com o GitHub
  - `github` : a main do GitHub como chegou, antes de juntar com a daqui
  - `github-<branch>` : as outras branches do GitHub (ex.: uma branch de frontend), cada uma como chegou
  - `dia/AAAA-MM-DD` : uma etiqueta por dia, com o primeiro estado do dia (o "como estava hoje de manhã")
Nada se perde: se alguém reescrever a história (push --force, reset), a versão anterior do backup fica guardada no
ramo `reescrito/<carimbo>-<main|github>` antes de o backup seguir o estado novo; o aviso sai uma vez só. Na nuvem e na VPS (Linux sem a pasta), pula.

Uso:
  python backup.py              guarda agora
  python backup.py --marco "x"  guarda e marca (etiqueta marco/<carimbo>) — antes de uma mudança grande
  python backup.py --estado     mostra o que o backup tem
  python backup.py --voltar     só IMPRIME os comandos para voltar um arquivo ou o repo inteiro (não executa)
"""
import os, re, subprocess, sys, time

for fluxo in (sys.stdout, sys.stderr):
    if hasattr(fluxo, "reconfigure"):
        fluxo.reconfigure(encoding="utf-8")

AQUI = os.path.dirname(os.path.abspath(__file__))
AMBIENTE = dict(os.environ, GIT_TERMINAL_PROMPT="0")
BASE = os.path.join(os.path.expanduser("~"), "Backups-repositorios")


def git(*args, cwd=None, ok=False):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=AMBIENTE)
    if r.returncode != 0 and not ok:
        raise RuntimeError(f"git {' '.join(args)}: {(r.stderr or r.stdout).strip()[-400:]}")
    return r


def raiz():
    return git("rev-parse", "--show-toplevel", cwd=AQUI, ok=True).stdout.strip()


def destino(rz):
    """Nome do repo no GitHub (ex.: meu-repo); sem remoto, o nome da pasta."""
    url = git("remote", "get-url", "origin", cwd=rz, ok=True).stdout.strip()
    nome = re.sub(r"\.git$", "", url.rstrip("/").split("/")[-1]) if url else os.path.basename(rz)
    nome = re.sub(r"[^\w.-]+", "-", nome).strip("-") or "repositorio"
    return os.path.join(BASE, nome + ".git")


def pular(dst):
    if os.environ.get("BACKUP_PULAR"):
        return "pulado (BACKUP_PULAR)"
    if sys.platform.startswith("linux") and not os.path.isdir(dst):
        return "pulado (nuvem ou servidor: o backup local é do computador de quem escreve)"
    return ""


def guardar_ref(rz, dst, origem, ref, carimbo):
    """origem → refs/heads/<ref> no backup, sem force. Reescrito: a versão anterior vai para reescrito/<carimbo>-<ref>
    (dentro do backup) e só então o ref segue o estado novo."""
    if git("rev-parse", "-q", "--verify", origem, cwd=rz, ok=True).returncode != 0:
        return ""
    r = git("push", "-q", dst, f"{origem}:refs/heads/{ref}", cwd=rz, ok=True)
    if r.returncode == 0:
        return ""
    if re.search(r"non-fast-forward|rejected|fetch first", r.stderr):
        guarda = f"reescrito/{carimbo}-{ref}"
        git("branch", "-f", guarda, ref, cwd=dst)
        git("push", "-q", "-f", dst, f"{origem}:refs/heads/{ref}", cwd=rz)
        return f"⚠️ {ref} foi reescrita (push --force ou reset): a versão anterior ficou no backup em {guarda}"
    raise RuntimeError(r.stderr.strip()[-300:])


def guardar(marco=None, rz=None):
    rz = rz or raiz()
    if not rz:
        return "pulado (não é repositório git)"
    dst = destino(rz)
    p = pular(dst)
    if p:
        return p
    if not os.path.isdir(dst):
        os.makedirs(BASE, exist_ok=True)
        git("init", "--bare", "-q", dst, cwd=BASE)
    carimbo = time.strftime("%Y-%m-%d-%H%M")
    avisos = [a for a in (guardar_ref(rz, dst, "HEAD", "main", carimbo),
                          guardar_ref(rz, dst, "refs/remotes/origin/main", "github", carimbo)) if a]
    # as outras branches do GitHub também (a branch de outra pessoa que também escreve no repositório), como github-<nome>
    git("fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*", cwd=rz, ok=True)
    for ref in git("for-each-ref", "--format=%(refname:strip=3)", "refs/remotes/origin/", cwd=rz, ok=True).stdout.split():
        if ref not in ("main", "HEAD"):
            a = guardar_ref(rz, dst, f"refs/remotes/origin/{ref}", "github-" + ref, carimbo)
            if a:
                avisos.append(a)
    dia = "dia/" + time.strftime("%Y-%m-%d")
    if git("rev-parse", "-q", "--verify", f"refs/tags/{dia}", cwd=dst, ok=True).returncode != 0:
        git("push", "-q", dst, f"HEAD:refs/tags/{dia}", cwd=rz, ok=True)
    if marco:
        tag = "marco/" + carimbo
        quem = [] if git("config", "user.email", cwd=rz, ok=True).stdout.strip() else             ["-c", "user.name=backup", "-c", "user.email=backup@example.com"]
        git(*quem, "tag", "-a", "-f", tag, "-m", marco, cwd=rz)
        git("push", "-q", dst, f"refs/tags/{tag}:refs/tags/{tag}", cwd=rz, ok=True)
    head = git("rev-parse", "--short", "HEAD", cwd=rz).stdout.strip()
    return " · ".join(["ok", head, dst] + avisos + ([f"marco/{carimbo}"] if marco else []))


def estado():
    rz = raiz(); dst = destino(rz)
    if not os.path.isdir(dst):
        print("sem backup ainda neste computador:", dst); return
    print("backup:", dst)
    outros = [b for b in git("for-each-ref", "--format=%(refname:short)", "refs/heads/github-*", cwd=dst, ok=True).stdout.split()]
    for ref in ("main", "github", *outros):
        r = git("log", "-1", "--format=%h %ci %s", ref, cwd=dst, ok=True)
        print(f"  {ref:18}: {r.stdout.strip() or '—'}")
    dias = git("tag", "-l", "dia/*", "--sort=-refname", cwd=dst, ok=True).stdout.split()[:7]
    marcos = git("tag", "-l", "marco/*", "--sort=-refname", cwd=dst, ok=True).stdout.split()[:5]
    div = [b for b in git("branch", "--list", "reescrito/*", cwd=dst, ok=True).stdout.split() if b != "*"]
    print("  dias   :", ", ".join(d[4:] for d in dias) or "—")
    print("  marcos :", ", ".join(m[6:] for m in marcos) or "—")
    if div:
        print("  ⚠️ reescrito (versões anteriores guardadas):", ", ".join(div))


def voltar():
    rz = raiz(); dst = destino(rz)
    print(f"""Para voltar (comandos, NÃO executados; ou peça ao Claude: "volta o arquivo X para como estava ontem"):
  trazer o backup para consulta:     git -C "{rz}" fetch "{dst}" "refs/tags/*:refs/tags/backup-*"
  um arquivo como estava num dia:    git -C "{rz}" checkout backup-dia/AAAA-MM-DD -- "<caminho do arquivo>"
  ver o que mudou desde aquele dia:  git -C "{rz}" diff backup-dia/AAAA-MM-DD --stat
  uma versão reescrita por push --force: git -C "{rz}" fetch "{dst}" "refs/heads/reescrito/*:refs/remotes/backup/reescrito/*"
  o repo inteiro, se a pasta se perder: git clone "{dst}" "<pasta nova>"
Depois de voltar: o sincronizar.py publica a volta como uma mudança nova (nada se apaga do histórico).""")


def main():
    a = sys.argv[1:]
    if a[:1] in (["-h"], ["--help"]):
        print(__doc__); return
    if a[:1] == ["--estado"]:
        estado(); return
    if a[:1] == ["--voltar"]:
        voltar(); return
    marco = a[a.index("--marco") + 1] if "--marco" in a else None
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=os.path.dirname(os.path.abspath(__file__)),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    raiz = r.stdout.strip() if r.returncode == 0 else ""
    if raiz and os.path.exists(os.path.join(raiz, "40-operacao-rotinas", "ferramentas", "verificar-propagacao.py")):
        # pasta ainda versionada dentro da Governança (sem git próprio): o backup é o da casa.
        print("⏸ backup: esta pasta ainda mora dentro da Governança; o backup é o da casa. Nada feito."); return
    try:
        print("💾 backup:", guardar(marco))
    except RuntimeError as e:
        print(f"⚠️ backup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
