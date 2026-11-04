#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
varrer-publico.py — o gate da régua "público SEMPRE anonimizado" (00-core/POLITICAS-DE-DECISAO.md §8).

Reprova o que identifica cliente, prospect, parceiro ou contraparte em tudo o que alguém alcança sem login.
O dicionário sai das próprias pastas de conta (clientes/, parceiros/, 30-comercial/assessoria-prospects/), mais
o arquivo varrer-publico.txt, ao lado deste script (modelo em varrer-publico.exemplo.txt; o real é privado e
não se versiona em repositório público). Lista de nomes de memória não é gate.

O que olha num repositório: o conteúdo de hoje E o histórico inteiro, nomes de arquivo, autor e mensagem de
commit, branches e tags, texto e metadados de PDF, bytes de binários (caminho local, e-mail), segredos.

Uso (da raiz do repo):
  python3 40-operacao-rotinas/ferramentas/varrer-publico.py --repo <pasta>            # repositório, com histórico
  python3 40-operacao-rotinas/ferramentas/varrer-publico.py --pasta <pasta>           # peças antes de subir
  python3 40-operacao-rotinas/ferramentas/varrer-publico.py --url <endereço>          # página no ar (pode repetir)
  python3 40-operacao-rotinas/ferramentas/varrer-publico.py --todos                   # os repositórios públicos da conta e as páginas listadas
  python3 40-operacao-rotinas/ferramentas/varrer-publico.py --instalar-hook <pasta>   # pre-push que bloqueia publicação reprovada
  --relatorio <arquivo.md> grava os achados. --permite-operador aceita o nome do operador (site dele, marca dele).

Saída: 0 limpo · 1 achou ou não conseguiu ler (não publique) · 2 erro de uso.
Só leitura, exceto --instalar-hook e --relatorio. Os achados têm nome: nunca colar relatório em lugar público.
"""
import argparse, io, json, os, re, shutil, ssl, subprocess, sys, tempfile, unicodedata, urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CONFIG = os.path.join(AQUI, "varrer-publico.txt")
RAIZES = (("clientes", "cliente"), ("parceiros", "parceiro"), (os.path.join("30-comercial", "assessoria-prospects"), "prospect"))
PALAVRA_COMUM = set("de da do das dos e o a the and ka cor ivs dias junior jr rosa grupo sistema instituto repo projeto casa".split())
TEXTO = (".md", ".txt", ".py", ".json", ".html", ".htm", ".css", ".js", ".sql", ".yml", ".yaml", ".sh", ".bat", ".cmd", ".csv", ".toml", ".ps1", ".cs", ".plist", ".xml", ".svg", ".env", ".ini", ".cfg")
SEM_EXTENSAO = (".gitignore", ".gitattributes", ".htaccess", "dockerfile", "makefile", "license", "readme")
BASE64 = re.compile(r"data:[a-z/+\-0-9.]+;base64,[A-Za-z0-9+/=]+")
SEGREDO = re.compile(r"ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|github[_]pat_|sk[-]ant-|sk-[A-Za-z0-9]{32,}|EAA[A-Za-z0-9]{40,}|eyJhbG[c]iOi|sb[_]secret_|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|(?<![\d.])\d{3}\.\d{3}\.\d{3}-\d{2}(?![\d.])|(?<!\d)\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}(?!\d)|\d@lid\b|\d@c\.us\b|\d@g\.us\b")
MODELO_SEGREDO = {"000.000.000-00", "00.000.000/0000-00"}
LOCAL = re.compile(rb"[A-Za-z]:\\Users\\[A-Za-z0-9._-]{2,}|/home/[a-z0-9._-]{2,}/|/Users/[A-Za-z0-9._-]{2,}/", re.I)
LOCAL_OK = re.compile(r"/home/(?:user|usuario|runner|voce|you|me|<[^>]*>)/|/Users/(?:Shared|you|voce|<[^>]*>)/|\\Users\\(?:Public|Default|voce|<[^>]*>)", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


class Dicionario:
    def __init__(self, permite_operador=False):
        self.termos, self.permitidos, self.autores_ok, self.urls, self.sitemaps, self.urls_ok = {}, [], set(), [], [], set()
        self.operador = set()
        self.ignorar = set(PALAVRA_COMUM)
        linhas = []
        if os.path.exists(CONFIG):
            linhas = open(CONFIG, encoding="utf-8").read().split("\n")
        for l in linhas:
            l = l.strip()
            if not l or l.startswith("#") or ":" not in l:
                continue
            k, v = (x.strip() for x in l.split(":", 1))
            if k == "ignorar":
                self.ignorar.add(norm(v))
        for raiz, tipo in RAIZES:
            d = os.path.join(RAIZ, raiz)
            if not os.path.isdir(d):
                continue
            for n in sorted(os.listdir(d)):
                if not os.path.isdir(os.path.join(d, n)) or n.startswith((".", "_")):
                    continue
                ws = re.findall(r"[a-z0-9]+", norm(n))
                if len(ws) >= 2:
                    self.termos.setdefault(" ".join(ws), f"{tipo}: {n}")
                for w in ws:
                    if w not in self.ignorar and len(w) >= 3:
                        self.termos.setdefault(w, f"{tipo}: {n}")
        for l in linhas:
            l = l.strip()
            if not l or l.startswith("#") or ":" not in l:
                continue
            k, v = (x.strip() for x in l.split(":", 1))
            if k == "termo":
                t, _, q = v.partition("|")
                self.termos[norm(t.strip())] = q.strip() or "lista da casa"
            elif k == "operador":
                self.operador.add(norm(v))
                self.termos[norm(v)] = "operador"
            elif k == "permitido":
                self.permitidos.append(norm(v))
            elif k == "autor-ok":
                self.autores_ok.add(v.lower())
            elif k == "url":
                self.urls.append(v)
            elif k == "sitemap":
                self.sitemaps.append(v)
            elif k == "url-ok":
                self.urls_ok.add(v.rstrip("/"))
        if permite_operador:
            for t in self.operador:
                self.termos.pop(t, None)
            for t in [t for t, q in self.termos.items() if norm(q).endswith(tuple(self.operador))]:
                self.termos.pop(t, None)
        self.permitidos.sort(key=len, reverse=True)
        chaves = sorted(map(re.escape, self.termos), key=len, reverse=True)
        self.rx = re.compile(r"(?<![a-z0-9])(" + "|".join(chaves) + r")(?![a-z0-9])") if chaves else None

    def achar(self, texto):
        """Devolve [(termo, quem, trecho)] de uma linha ou nome."""
        if not self.rx:
            return []
        n = norm(texto)
        for p in self.permitidos:
            if p in n:
                n = n.replace(p, " " * len(p))
        return [(m.group(1), self.termos[m.group(1)], n[max(0, m.start() - 55):m.end() + 55].strip()) for m in self.rx.finditer(n)]


class Laudo:
    def __init__(self):
        self.itens, self.nao_lidos = [], []

    def add(self, onde, termo, quem, ctx):
        self.itens.append((onde, termo, quem, ctx))


def ler_texto(d, laudo, onde, t):
    t = BASE64.sub("data:…", t)
    for i, l in enumerate(t.split("\n"), 1):
        for termo, quem, ctx in d.achar(l):
            laudo.add(f"{onde}:{i}", termo, quem, ctx)
        for m in SEGREDO.finditer(l):
            if m.group(0) not in MODELO_SEGREDO:
                laudo.add(f"{onde}:{i}", "segredo ou documento", "dado sensível", l[max(0, m.start() - 20):m.start() + 12] + "…")


def e_texto(nome):
    b = os.path.basename(nome).lower()
    return b.endswith(TEXTO) or b in SEM_EXTENSAO or "." not in b


def ler_bytes(d, laudo, onde, b, nome):
    baixo = nome.lower()
    if baixo.endswith(".pdf"):
        try:
            import fitz
        except ImportError:
            laudo.nao_lidos.append(f"{onde}: PDF sem PyMuPDF (python3 -m pip install pymupdf)")
            return
        try:
            doc = fitz.open(stream=b, filetype="pdf")
        except Exception as e:
            laudo.nao_lidos.append(f"{onde}: PDF ilegível ({e})")
            return
        for i, pg in enumerate(doc, 1):
            ler_texto(d, laudo, f"{onde}#p{i}", pg.get_text())
        ler_texto(d, laudo, f"{onde}#metadados", " | ".join(str(v) for v in (doc.metadata or {}).values() if v))
        return
    if e_texto(nome):
        ler_texto(d, laudo, onde, b.decode("utf-8", "replace"))
        return
    for m in LOCAL.finditer(b):
        trecho = m.group(0).decode("latin-1")
        if not LOCAL_OK.search(trecho):
            laudo.add(onde, "caminho local", "máquina", trecho[:60])
    for email in re.findall(rb"[a-z0-9._%+\-]{3,}@[a-z0-9\-]+\.[a-z.]{2,}", b, re.I):
        e = email.decode("latin-1").lower()
        if e.split("@", 1)[0] in {norm(t).replace(" ", "") for t in d.operador} or norm(e) in d.termos:
            laudo.add(onde, "e-mail", "pessoa", e)


def git(repo, *a):
    return subprocess.run(["git", "-c", "core.quotepath=false", *a], cwd=repo, capture_output=True)


def varrer_repo(d, repo, laudo):
    if git(repo, "rev-parse", "--git-dir").returncode != 0:
        print(f"não é repositório git: {repo}")
        sys.exit(2)
    commits = git(repo, "rev-list", "--all").stdout.decode().split()
    fmt = "%h%x00%an%x00%ae%x00%cn%x00%ce%x00%B%x01"
    for bloco in git(repo, "log", "--all", f"--format={fmt}").stdout.decode("utf-8", "replace").split("\x01"):
        p = bloco.strip("\n").split("\x00")
        if len(p) < 6:
            continue
        h, an, ae, cn, ce, msg = p[0], p[1], p[2].lower(), p[3], p[4].lower(), p[5]
        for email in {ae, ce}:
            if d.autores_ok and email not in d.autores_ok and email != "noreply@github.com":
                laudo.add(f"commit {h}", email, "autor fora da lista", f"autor de commit público: {email}")
        for quem in (an, cn):
            for termo, q, ctx in d.achar(quem):
                laudo.add(f"commit {h} (autor)", termo, q, ctx)
        ler_texto(d, laudo, f"commit {h} (mensagem)", msg)
    for ref in git(repo, "for-each-ref", "--format=%(refname:short)").stdout.decode("utf-8", "replace").split("\n"):
        for termo, q, ctx in d.achar(ref):
            laudo.add(f"ref {ref}", termo, q, ctx)
    blobs = {}
    for c in commits:
        for l in git(repo, "ls-tree", "-r", c).stdout.decode("utf-8", "replace").split("\n"):
            if not l:
                continue
            meta, path = l.split("\t", 1)
            _, tipo, sha = meta.split()
            if tipo == "blob":
                blobs.setdefault(sha, set()).add(path)
                for termo, q, ctx in d.achar(path):
                    laudo.add(f"caminho {path} [{c[:7]}]", termo, q, ctx)
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    entrada = ("\n".join(blobs) + "\n").encode() if blobs else b""
    saida, _ = proc.communicate(entrada)
    buf, pos = io.BytesIO(saida), 0
    for sha in blobs:
        cab = buf.readline().decode().split()
        if len(cab) < 3 or cab[1] != "blob":
            continue
        dado = buf.read(int(cab[2]))
        buf.read(1)
        nomes = sorted(blobs[sha])
        ler_bytes(d, laudo, nomes[0], dado, nomes[0])
    return len(commits), len(blobs)


def varrer_pasta(d, pasta, laudo):
    n = 0
    for dp, dn, fs in os.walk(pasta):
        dn[:] = [x for x in dn if x not in (".git", "node_modules", "__pycache__", ".next")]
        for f in fs:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, pasta).replace(os.sep, "/")
            for termo, q, ctx in d.achar(rel):
                laudo.add(f"caminho {rel}", termo, q, ctx)
            try:
                if os.path.getsize(p) > 25_000_000:
                    continue
                ler_bytes(d, laudo, rel, open(p, "rb").read(), f)
                n += 1
            except OSError as e:
                laudo.nao_lidos.append(f"{rel}: {e}")
    return n


def baixar(u):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 varrer-publico"})
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return r.read(6_000_000).decode("utf-8", "replace"), r.status


def varrer_url(d, u, laudo):
    try:
        t, _ = baixar(u)
    except Exception as e:
        if getattr(e, "code", None) in (403, 404, 410):
            return
        laudo.nao_lidos.append(f"{u}: {e}")
        return
    if u.rstrip("/") in d.urls_ok:
        return
    ler_texto(d, laudo, u, t)


def paginas_do_sitemap(u, vistos=None):
    vistos = vistos if vistos is not None else set()
    if u in vistos:
        return []
    vistos.add(u)
    try:
        t, _ = baixar(u)
    except Exception:
        return []
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t)
    saida = []
    for l in locs:
        saida += paginas_do_sitemap(l, vistos) if l.endswith(".xml") else [l]
    return saida


def instalar_hook(repo):
    gd = git(repo, "rev-parse", "--git-dir").stdout.decode().strip()
    if not gd:
        print(f"não é repositório git: {repo}")
        return 2
    gd = gd if os.path.isabs(gd) else os.path.join(repo, gd)
    os.makedirs(os.path.join(gd, "hooks"), exist_ok=True)
    alvo = os.path.join(gd, "hooks", "pre-push")
    script = os.path.abspath(__file__).replace("\\", "/")
    with open(alvo, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"""#!/bin/sh
# Gate da régua "público SEMPRE anonimizado". Reprovou, o push não sai.
P=; for c in python3 python py; do $c -c '' 2>/dev/null && P=$c && break; done
if [ -z "$P" ]; then echo "sem Python: push bloqueado, o gate não pôde rodar"; exit 1; fi
PYTHONUTF8=1 $P "{script}" --repo "$(git rev-parse --show-toplevel)" || {{ echo "🔴 push bloqueado pelo varrer-publico.py"; exit 1; }}
""")
    try:
        os.chmod(alvo, 0o755)
    except OSError:
        pass
    print(f"✅ hook instalado: {alvo}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Gate da régua público SEMPRE anonimizado.")
    ap.add_argument("--repo", action="append", default=[])
    ap.add_argument("--pasta", action="append", default=[])
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--instalar-hook")
    ap.add_argument("--permite-operador", action="store_true")
    ap.add_argument("--relatorio")
    a = ap.parse_args()
    if a.instalar_hook:
        return instalar_hook(a.instalar_hook)
    if not (a.repo or a.pasta or a.url or a.todos):
        ap.print_help()
        return 2
    d = Dicionario(permite_operador=a.permite_operador)
    laudo = Laudo()
    print(f"dicionário: {len(d.termos)} termos, das pastas de conta e de {os.path.basename(CONFIG)}")
    if not d.termos:
        print(f"🔴 dicionário vazio: crie {os.path.basename(CONFIG)} a partir de varrer-publico.exemplo.txt (ao lado deste script) antes de publicar. Gate recusado.")
        return 2
    for r in a.repo:
        c, b = varrer_repo(d, r, laudo)
        print(f"repositório {os.path.basename(os.path.abspath(r))}: {c} commit(s), {b} arquivo(s) distinto(s) no histórico")
    for p in a.pasta:
        print(f"pasta {p}: {varrer_pasta(d, p, laudo)} arquivo(s)")
    for u in a.url:
        varrer_url(d, u, laudo)
    if a.todos:
        r = subprocess.run(["gh", "repo", "list", "--visibility", "public", "--limit", "200", "--json", "nameWithOwner,url"], capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            laudo.nao_lidos.append("gh repo list falhou: " + r.stderr.strip()[:160])
            repos = []
        else:
            repos = json.loads(r.stdout or "[]")
        for repo in repos:
            tmp = tempfile.mkdtemp(prefix="varrer-publico-")
            try:
                c = subprocess.run(["git", "clone", "-q", "--mirror", repo["url"] + ".git", tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
                if c.returncode != 0:
                    laudo.nao_lidos.append(f"{repo['nameWithOwner']}: clone falhou")
                    continue
                antes = len(laudo.itens)
                nc, nb = varrer_repo(d, tmp, laudo)
                for i in range(antes, len(laudo.itens)):
                    o, t, q, x = laudo.itens[i]
                    laudo.itens[i] = (f"{repo['nameWithOwner']} · {o}", t, q, x)
                print(f"público {repo['nameWithOwner']}: {nc} commit(s), {nb} arquivo(s)")
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        dsite = Dicionario(permite_operador=True)
        paginas = list(d.urls)
        for s in d.sitemaps:
            paginas += paginas_do_sitemap(s)
        paginas = sorted(set(paginas))
        for u in paginas:
            varrer_url(dsite, u, laudo)
        print(f"páginas no ar: {len(paginas)}")
    achados = sorted(set(laudo.itens))
    linhas = [f"- `{o}` «{t}» ({q}) …{c}…" for o, t, q, c in achados] + [f"- não lido: {n}" for n in laudo.nao_lidos]
    if a.relatorio:
        with open(a.relatorio, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Varredura do que é público\n\n> Tem nome: não colar em lugar público.\n\n" + ("\n".join(linhas) or "Nada achado.") + "\n")
    if achados or laudo.nao_lidos:
        print(f"🔴 {len(achados)} achado(s), {len(laudo.nao_lidos)} não lido(s). Não publique.")
        for l in linhas[:120]:
            print(l[:240])
        if len(linhas) > 120:
            print(f"… mais {len(linhas) - 120}; use --relatorio")
        return 1
    print("✅ nada de conta, nenhum segredo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
