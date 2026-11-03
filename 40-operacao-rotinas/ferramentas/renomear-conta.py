#!/usr/bin/env python3
"""
renomear-conta.py — renomeia a pasta de uma conta (clientes/, parceiros/, assessoria-prospects/) e, no mesmo
ato, reescreve todo caminho que aponta para ela. Assim nenhum arquivo do repo fica apontando para uma pasta que não existe.

Roteado em
`00-core/roteador/ARVORE-CASA.md`, linha "onde guardo esta peça … mover arquivo de área … renomear conta".

O que faz, em ordem (para no primeiro erro, sem estado pela metade):
  1. confere: a origem existe, o destino não existe;
  2. `.gitignore`: para cada linha com o caminho antigo, garante a linha equivalente com o novo ANTES de mover.
     Mantém a antiga, porque o espelho ignorado não pode cair no commit em nenhum instante;
  3. move a pasta (os.rename). Se o Windows negar, é porque há sessão, terminal ou janela com o diretório
     dentro dela: sai com código 2 e não toca em mais nada;
  4. reescreve `<raiz>/<antigo>/` → `<raiz>/<novo>/` (barra normal e invertida) em todo arquivo de texto
     versionado ou novo não ignorado. Fora: `_legado/`, fotos e logs datados (`operacao-hoje/`, `tarefas/log/`,
     `sessoes-claude/`) e o próprio `.gitignore`. Trabalha em bytes, então preserva CRLF e LF;
  5. confere: nenhum caminho antigo sobrou fora das exceções. Se sobrou, lista e sai com código 1.

O nome antigo SEM o prefixo da raiz (ex.: "ex-`Nome Antigo/`") não é tocado. É assim que se escreve a
menção histórica que deve sobreviver.

Uso (cwd = raiz do repo):
  python3 -X utf8 40-operacao-rotinas/ferramentas/renomear-conta.py --de "Nome Antigo" --para "Nome Novo" --dry-run
  python3 -X utf8 40-operacao-rotinas/ferramentas/renomear-conta.py --de "Nome Antigo" --para "Nome Novo"
  (--raiz clientes | parceiros | 30-comercial/assessoria-prospects; padrão: clientes)
"""
import argparse, os, subprocess, sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FORA = ("_legado/", "40-operacao-rotinas/operacao-hoje/", "40-operacao-rotinas/tarefas/log/",
        "40-operacao-rotinas/sessoes-claude/", ".gitignore")
TEXTO = (".md", ".txt", ".json", ".jsonl", ".py", ".yml", ".yaml", ".csv", ".html", ".css", ".js", ".ps1", ".bat", ".toml", ".sh")


def arquivos():
    r = subprocess.run(["git", "ls-files", "-z", "-co", "--exclude-standard"], cwd=RAIZ, capture_output=True)
    if r.returncode != 0:
        sys.exit("git ls-files falhou: " + r.stderr.decode("utf-8", "replace"))
    for p in r.stdout.decode("utf-8").split("\0"):
        if p and p.lower().endswith(TEXTO) and not any(f in p for f in FORA):
            yield p


def formas(raiz, nome):
    return [f"{raiz}/{nome}/", f"{raiz}\\{nome}\\".replace("/", "\\")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--de", required=True)
    ap.add_argument("--para", required=True)
    ap.add_argument("--raiz", default="clientes")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    origem = os.path.join(RAIZ, a.raiz, a.de)
    destino = os.path.join(RAIZ, a.raiz, a.para)
    if not os.path.isdir(origem):
        sys.exit(f"origem não existe: {a.raiz}/{a.de}/")
    if os.path.exists(destino):
        sys.exit(f"destino já existe: {a.raiz}/{a.para}/")

    antigos = [s.encode("utf-8") for s in formas(a.raiz, a.de)]
    novos = [s.encode("utf-8") for s in formas(a.raiz, a.para)]

    # 1. inventário (antes de mover, com os caminhos ainda antigos)
    alvos = []
    for p in arquivos():
        try:
            b = open(os.path.join(RAIZ, p), "rb").read()
        except OSError:
            continue
        n = sum(b.count(x) for x in antigos)
        if n:
            alvos.append((p, n))

    # 2. .gitignore
    gi = os.path.join(RAIZ, ".gitignore")
    gi_b = open(gi, "rb").read()
    nl = b"\r\n" if b"\r\n" in gi_b else b"\n"
    linhas = gi_b.split(nl)
    acrescentar = []
    for ln in linhas:
        if antigos[0] in ln:
            nova = ln.replace(antigos[0], novos[0])
            if nova not in linhas and nova not in acrescentar:
                acrescentar.append(nova)

    print(f"{a.raiz}/{a.de}/ → {a.raiz}/{a.para}/")
    print(f".gitignore: {len(acrescentar)} linha(s) nova(s) para o caminho novo (as antigas ficam)")
    for p, n in alvos:
        print(f"  {n:>3}× {p}")
    print(f"{len(alvos)} arquivo(s), {sum(n for _, n in alvos)} ocorrência(s)")
    if a.dry_run:
        print("dry-run: nada alterado")
        return 0

    if acrescentar:
        saida = []
        for ln in linhas:
            saida.append(ln)
            if antigos[0] in ln:
                saida += [x for x in acrescentar if x.replace(novos[0], antigos[0]) == ln]
        open(gi, "wb").write(nl.join(saida))

    # 3. mover
    try:
        os.rename(origem, destino)
    except PermissionError as e:
        print(f"🔴 pasta em uso, nada movido ({e.strerror}). Feche a sessão, terminal ou janela que está dentro dela e rode de novo.")
        return 2

    # 4. reescrever (os caminhos dentro da pasta movida mudaram junto)
    for p, _ in alvos:
        if p.startswith(f"{a.raiz}/{a.de}/"):
            p = f"{a.raiz}/{a.para}/" + p[len(f"{a.raiz}/{a.de}/"):]
        f = os.path.join(RAIZ, p)
        b = open(f, "rb").read()
        for x, y in zip(antigos, novos):
            b = b.replace(x, y)
        open(f, "wb").write(b)

    # 5. conferir
    sobra = []
    for p in arquivos():
        try:
            b = open(os.path.join(RAIZ, p), "rb").read()
        except OSError:
            continue
        if any(x in b for x in antigos):
            sobra.append(p)
    if sobra:
        print("🔴 caminho antigo ainda apontado em:")
        for p in sobra:
            print("  " + p)
        return 1
    print(f"✅ renomeada; {len(alvos)} arquivo(s) reescrito(s); nenhum caminho antigo fora das exceções")
    return 0


if __name__ == "__main__":
    sys.exit(main())
