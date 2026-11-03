#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar.py — o gate deste repositório: o equivalente, para o repo do cliente, do
verificar-propagacao.py da Governança.

🔴 Não editar aqui. A fonte é a Governança, `90-templates/repo-cliente/ferramentas/`.

  python verificar.py           tudo: vetos + estrutura + avisos
  python verificar.py --vetos   só os vetos (é o que o sincronizar.py roda antes de publicar)

VETOS (bloqueiam a publicação): CPF · senha com valor · chave ou token de serviço · chave privada ·
  salário com valor · agência e conta · arquivo que nunca vai ao GitHub (.env, .ofx, .pem, chave SSH).
ESTRUTURA (❌, não bloqueia a sincronia, mas a tarefa não está fechada):
  · todo .md das pastas numeradas é citado no CLAUDE.md (pelo nome, ou a pasta inteira com "/")
  · toda pasta da raiz aparece no README.md
  · todo caminho citado entre crases existe
AVISO: arquivo mudou e o STATUS.md não.

Linha que precisa mostrar um desses padrões de propósito leva o marcador `verificar:ok`.
Ajuste por repositório, opcional: `verificar.json` ao lado deste arquivo
  {"isentas_roteador": ["70-sistema"]}
"""
import json, os, re, subprocess, sys

for fluxo in (sys.stdout, sys.stderr):
    if hasattr(fluxo, "reconfigure"):
        fluxo.reconfigure(encoding="utf-8")

AQUI = os.path.dirname(os.path.abspath(__file__))
TEXTO = {".md", ".txt", ".json", ".py", ".sh", ".sql", ".yml", ".yaml", ".csv", ".html", ".css",
         ".js", ".ts", ".example", ".cfg", ".ini", ".toml", ""}
OK = "verificar:ok"

PADROES = [
    ("CPF", re.compile(r"(?<![\d.])\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)")),
    ("CPF", re.compile(r"(?i)\bcpf\b\D{0,6}\d{11}(?!\d)")),
    ("token do GitHub", re.compile(r"\b(ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}")),
    ("chave de API", re.compile(r"\bsk-(ant-)?[A-Za-z0-9_-]{20,}")),
    ("chave de API do Google", re.compile(r"\bAIza[0-9A-Za-z_-]{35}")),
    ("chave da AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token JWT (chave de banco ou de serviço)", re.compile(r"\beyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}")),
    ("chave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("agência e conta", re.compile(r"(?i)\bag(ência|encia|\.)?\s*:?\s*\d{3,5}(-\d)?\b.{0,30}\b(c/c|conta|cc)\s*:?\s*\d{4,}")),
]
SENHA = re.compile(r"(?i)\b(senha|password|passwd|pwd)\b\s*[:=]\s*(?P<q>[\"']?)(?P<v>[^\s<`\"'*|,)]{4,})")
CODIGO = {".py", ".js", ".ts", ".sh"}
SALARIO = re.compile(r"(?i)sal[aá]rio")
VALOR = re.compile(r"R\$\s?\d")
PROIBIDOS = re.compile(r"(^|/)(\.env|id_rsa|id_ed25519|id_ecdsa)$|\.(ofx|pem|key|p12|pfx|pyc)$", re.I)


def senha_escrita(linha, ext):
    """Senha com valor. No código, `password=senha` (nome de variável, sem aspas) não é senha;
    `password="abc123"` (entre aspas) é. Marcadores como ${VAR}, xxx e ... não são senha."""
    for m in SENHA.finditer(linha):
        v = m.group("v")
        if re.fullmatch(r"\$\{?\w+\}?|x{3,}|\.{3,}", v, re.I):
            continue
        if not m.group("q") and ext in CODIGO and re.fullmatch(r"[A-Za-z_][\w.\[\]()]*", v):   # variável ou chamada
            continue
        return True
    return False


def _git(raiz, *args):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=raiz, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def arquivos(raiz):
    """O que iria para o GitHub: rastreado + novo não ignorado."""
    saida = _git(raiz, "ls-files", "-co", "--exclude-standard")
    return [l for l in saida.splitlines() if l and os.path.exists(os.path.join(raiz, l))]


def vetos(raiz):
    achados = []
    for rel in arquivos(raiz):
        if PROIBIDOS.search(rel):
            achados.append(f"{rel}: arquivo que nunca vai ao GitHub")
            continue
        if os.path.basename(rel) == "verificar.py":
            continue
        ext = os.path.splitext(rel)[1].lower()
        caminho = os.path.join(raiz, rel)
        if ext not in TEXTO or os.path.getsize(caminho) > 2_000_000:
            continue
        try:
            linhas = open(caminho, encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            continue
        for n, linha in enumerate(linhas, 1):
            if OK in linha:
                continue
            for nome, rx in PADROES:
                if rx.search(linha):
                    achados.append(f"{rel}:{n}: {nome}")
                    break
            else:
                if senha_escrita(linha, ext):
                    achados.append(f"{rel}:{n}: senha com valor")
                elif SALARIO.search(linha) and VALOR.search(linha):
                    achados.append(f"{rel}:{n}: salário com valor")
    return achados


def _config():
    p = os.path.join(AQUI, "verificar.json")
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    except Exception:
        return {}


def estrutura(raiz):
    cfg = _config()
    isentas = set(cfg.get("isentas_roteador", ["70-sistema"]))
    estritas = set(cfg.get("estritas", []))   # pastas em que cada arquivo precisa ser citado pelo nome
    falhas = []
    ler = lambda n: open(os.path.join(raiz, n), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(raiz, n)) else ""
    kernel, readme = ler("CLAUDE.md"), ler("README.md")
    raiz_dirs = sorted(d for d in os.listdir(raiz) if os.path.isdir(os.path.join(raiz, d)) and not d.startswith("."))
    numeradas = [d for d in raiz_dirs if re.match(r"^\d\d-", d)]

    # 1. roteador: todo .md de pasta numerada citado no CLAUDE.md
    for d in numeradas:
        if d in isentas:
            continue
        for base, _, fs in os.walk(os.path.join(raiz, d)):
            for f in fs:
                if not f.endswith(".md") or f == "README.md":
                    continue
                rel = os.path.relpath(os.path.join(base, f), raiz).replace("\\", "/")
                pasta_citada = d not in estritas and (os.path.dirname(rel) + "/") in kernel
                if f not in kernel and rel not in kernel and not pasta_citada:
                    falhas.append(f"roteador: {rel} não é citado no CLAUDE.md (ninguém chega até ele)")

    # 2. índice: toda pasta da raiz no README.md
    for d in raiz_dirs:
        if d not in readme:
            falhas.append(f"índice: a pasta {d}/ não aparece no README.md")

    # 3. referências: todo caminho entre crases existe
    prefixos = set(raiz_dirs)
    raiz_arqs = {f for f in os.listdir(raiz) if os.path.isfile(os.path.join(raiz, f))}
    ferr = os.path.relpath(AQUI, raiz).replace("\\", "/") + "/"
    for rel in arquivos(raiz):
        if not rel.endswith(".md") or rel.startswith(ferr):   # o README das ferramentas é genérico
            continue
        texto = open(os.path.join(raiz, rel), encoding="utf-8", errors="replace").read()
        for trecho in re.findall(r"`([^`\n]+)`", texto):
            for cand in trecho.split():
                cand = cand.strip(".,;:()[]\"'").split("#")[0]
                if (not cand or any(c in cand for c in "<>{}*$|") or cand.startswith(("http", "~", "/"))
                        or re.search(r"AAAA|MM-DD|\bNN\b|\.\.\.", cand)):   # caminho-modelo, não arquivo
                    continue
                primeiro = cand.split("/")[0]
                if "/" in cand and primeiro in prefixos or ("/" not in cand and cand in raiz_arqs | {"STATUS.md", "DECISOES.md", "CLAUDE.md", "README.md"}):
                    if not os.path.exists(os.path.join(raiz, cand.rstrip("/"))):
                        falhas.append(f"referência: {rel} cita `{cand}`, que não existe")
    return sorted(set(falhas))


def avisos(raiz):
    if not os.path.exists(os.path.join(raiz, "STATUS.md")):
        return []
    mudou = [l[3:].strip('"') for l in _git(raiz, "status", "--porcelain").splitlines() if l.strip()]
    outros = [m for m in mudou if not m.startswith(("STATUS.md", "DECISOES.md", "registros/", ".claude/"))
              and "/ferramentas/" not in f"/{m}"]
    if outros and not any(m.startswith("STATUS.md") for m in mudou):
        return [f"registro: {len(outros)} arquivo(s) mudaram e o STATUS.md não (o que mudou no estado vai para lá)"]
    return []


def main():
    raiz = _git(AQUI, "rev-parse", "--show-toplevel").strip() or os.path.dirname(os.path.dirname(AQUI))
    v = vetos(raiz)
    if "--vetos" in sys.argv:
        print("\n".join(f"🔴 {a}" for a in v) or "✅ nenhum dado sensível")
        sys.exit(1 if v else 0)
    e, a = estrutura(raiz), avisos(raiz)
    for x in v:
        print(f"🔴 veto · {x}")
    for x in e:
        print(f"❌ {x}")
    for x in a:
        print(f"⚠️ {x}")
    if v or e:
        print(f"\n**Resultado:** {'🔴' if v else '❌'} {len(v)} veto(s) · {len(e)} falha(s) de estrutura · {len(a)} aviso(s)")
        sys.exit(1)
    print(f"**Resultado:** ✅ nada a corrigir{' · ' + str(len(a)) + ' aviso(s)' if a else ''}")


if __name__ == "__main__":
    main()
