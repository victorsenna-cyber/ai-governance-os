#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backup-governanca.py — a rede de segurança da autonomia sobre o kernel.

Tipo: ferramenta (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Motivo: a autonomia do sistema abarca também o kernel (corrigir falhas sozinho). Para isso, um backup fora do repo,
num repo local e no GitHub só para backup da Governança, por segurança.
Regra: CLAUDE.md, seção de autonomia.

Dois destinos, os dois FORA deste repositório e os dois SÓ DE ESCRITA DE BACKUP (nunca fonte):
  local:   <pasta irmã>/<nome da governança>-backup.git            (repositório bare, irmão da Governança)
  GitHub:  <seu usuário>/governanca-backup                         (privado; BACKUP_REMOTO no ambiente)

Só acrescenta, nunca apaga nem reescreve:
  - a main vai sem force. Se a main da Governança tiver sido reescrita (o backup não é ancestral dela),
    o push é recusado e o estado atual entra como ramo `divergiu/<carimbo>`; o histórico antigo fica intacto.
  - `--marco "<motivo>"` grava também a tag `backup/<AAAA-MM-DD-HHMM>` com o motivo. É o que se roda
    ANTES de mexer no kernel (CLAUDE.md, 00-core/, .claude/settings.json, ferramentas de gate).

Uso (de qualquer lugar):
  python3 -X utf8 "<Governança>/40-operacao-rotinas/ferramentas/backup-governanca.py"                 atualiza a main nos dois
  python3 -X utf8 "<Governança>/40-operacao-rotinas/ferramentas/backup-governanca.py" --marco "motivo" idem + tag de marco
  ... --estado     mostra o último backup de cada destino, sem mexer em nada
  ... --restaurar  só IMPRIME os comandos para voltar um arquivo ou o repo a um marco (não executa)

Chamado também no fim do sincronizar.py, em silêncio (falha aqui nunca para a sincronia).
Só roda onde o backup local existe ou pode ser criado (o PC). Na VPS, BACKUP_PULAR=1 ou ausência de pasta → pula.
"""
import os, subprocess, sys, time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL = os.path.join(os.path.dirname(RAIZ), os.path.basename(RAIZ) + "-backup.git")
REMOTO = os.environ.get("BACKUP_REMOTO", "https://github.com/SEU-USUARIO/governanca-backup.git")


def git(*args, cwd=RAIZ, ok=False):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 and not ok:
        raise RuntimeError(f"git {' '.join(args)}: {(r.stderr or r.stdout).strip()[-500:]}")
    return r


def garantir_local():
    if os.path.isdir(LOCAL):
        return
    git("init", "--bare", "-q", LOCAL, cwd=os.path.dirname(RAIZ))
    git("remote", "add", "github", REMOTO, cwd=LOCAL)


def empurrar(destino_git_dir, remoto, refs_tags):
    """Leva main (sem force) e as tags de marco de `origem` para `remoto`. Devolve a linha de resultado."""
    carimbo = time.strftime("%Y-%m-%d-%H%M")
    r = git("push", "-q", remoto, "HEAD:refs/heads/main", *refs_tags, cwd=destino_git_dir, ok=True)
    if r.returncode == 0:
        return "ok"
    if "non-fast-forward" in r.stderr or "rejected" in r.stderr or "fetch first" in r.stderr:
        git("push", "-q", remoto, f"HEAD:refs/heads/divergiu/{carimbo}", *refs_tags, cwd=destino_git_dir, ok=True)
        return f"⚠️ main reescrita: estado atual guardado em divergiu/{carimbo}; o histórico antigo do backup ficou intacto"
    raise RuntimeError(r.stderr.strip()[-300:])


def backup(marco=None):
    if os.environ.get("BACKUP_PULAR"):
        return "pulado (BACKUP_PULAR)"
    if os.name != "nt" and not os.path.isdir(LOCAL):
        return "pulado (sem backup local nesta máquina)"
    garantir_local()
    tags = []
    if marco:
        tag = "backup/" + time.strftime("%Y-%m-%d-%H%M")
        git("tag", "-a", "-f", tag, "-m", marco)
        tags = [f"refs/tags/{tag}:refs/tags/{tag}"]
    # 1. Governança → backup local (bare)
    r_local = empurrar(RAIZ, LOCAL, tags)
    # 2. backup local → GitHub (do bare, para o GitHub receber exatamente o que o local tem)
    # O 1º envio ao GitHub é do operador, à mão; depois disso, segue sozinho.
    if not git("ls-remote", "github", "refs/heads/main", cwd=LOCAL, ok=True).stdout.strip():
        gh = "aguardando o 1º envio do operador: git -C \"" + LOCAL + "\" push github --all; git -C \"" + LOCAL + "\" push github --tags"
    else:
        r_gh = git("push", "-q", "github", "refs/heads/*:refs/heads/*", "refs/tags/backup/*:refs/tags/backup/*", cwd=LOCAL, ok=True)
        gh = "ok" if r_gh.returncode == 0 else "⚠️ " + r_gh.stderr.strip()[-200:]
    head = git("rev-parse", "--short", "HEAD").stdout.strip()
    return f"local {r_local} · GitHub {gh} · {head}" + (f" · marco {tags[0].split(':')[0][10:]}" if tags else "")


def estado():
    if not os.path.isdir(LOCAL):
        print("sem backup local ainda:", LOCAL); return
    for nome, ref in (("local", "main"),):
        r = git("log", "-1", "--format=%h %ci %s", ref, cwd=LOCAL, ok=True)
        print(f"{nome}: {r.stdout.strip() or '—'}")
    marcos = git("tag", "-l", "backup/*", "--sort=-creatordate", "-n1", cwd=LOCAL, ok=True).stdout.strip().splitlines()[:5]
    print("marcos:", *(marcos or ["—"]), sep="\n  ")
    r = git("ls-remote", "github", "refs/heads/main", cwd=LOCAL, ok=True)
    print("GitHub main:", (r.stdout.split() or ["—"])[0][:9])


def restaurar():
    print(f"""Para voltar (comandos, não executados):
  um arquivo a um marco:   git -C "{RAIZ}" checkout backup/<AAAA-MM-DD-HHMM> -- <caminho>
  ver o que o marco mudou:  git -C "{RAIZ}" diff backup/<AAAA-MM-DD-HHMM> -- CLAUDE.md 00-core/
  se a Governança se perder: git clone "{LOCAL}" "<pasta nova>"   (ou {REMOTO})
Depois de restaurar: verificar-propagacao.py e sincronizar.py, como em toda tarefa.""")


def main():
    a = sys.argv[1:]
    if a[:1] in (["-h"], ["--help"]):
        print(__doc__); return
    if a[:1] == ["--estado"]:
        estado(); return
    if a[:1] == ["--restaurar"]:
        restaurar(); return
    marco = a[a.index("--marco") + 1] if "--marco" in a else None
    try:
        print("💾 backup:", backup(marco))
    except RuntimeError as e:
        print(f"⚠️ backup: {e}")
        sys.exit(0 if "--silencioso" in a else 1)


if __name__ == "__main__":
    main()
