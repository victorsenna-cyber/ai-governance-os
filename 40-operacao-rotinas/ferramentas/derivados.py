# -*- coding: utf-8 -*-
"""
derivados.py — a propagação da casa para os repositórios derivados (CLAUDE.md §11.7), N0, sem LLM.
Registro: 40-operacao-rotinas/derivados/DERIVADOS.json (tipos, bases, quarentena, exceções).

  python3 -X utf8 derivados.py --estado                 uma linha por derivado: base, dias, o que está pendente
  python3 -X utf8 derivados.py --delta [--repo NOME]    o que mudou na casa desde a base de cada um, filtrado
                                                   pelo tipo, sem quarentena; grava derivados/DELTA-AAAA-MM-DD.md
  python3 -X utf8 derivados.py --abrir-task             --delta + abre a task de porte (molde portar-derivados.md)
                                                   se houver pendente e nenhuma task de porte aberta
  python3 -X utf8 derivados.py --registrar NOME --base HASH [--base-derivado HASH]
                                                   depois de um porte fechado: anda a base (só assim ela anda)

O meio automático é este: a casa muda → o delta sai sozinho (task semanal) → a task de porte abre sozinha →
o modelo porta, respeitando a quarentena e o EXCECOES-DA-CASA.md do derivado → gates → --registrar.
Nunca porta nada sozinho, nunca faz push: quem porta é o modelo; quem publica é o sincronizar.py
(cliente, parceiro) ou o git push depois do varrer-publico.py ✅ (template).
"""
import argparse, datetime, io, json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(RAIZ, "40-operacao-rotinas", "derivados")
REG = os.path.join(DIR, "DERIVADOS.json")
TAR = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas")
MOLDE = os.path.join(TAR, "modelos", "portar-derivados.md")
TZ = datetime.timezone(datetime.timedelta(hours=-3))

# O que cada tipo recebe da casa e o que é só da casa moram no DERIVADOS.json ("recebe", "so_da_casa") desde 11/11/2026
# (D1 do PLANO-ITERACAO-DERIVADOS-2026-11-11.md: o mapa é política, não código). Preenchidos por carregar().
PORTAVEL = {}
SO_DA_CASA = []
CAMADA = [("Kernel", ("CLAUDE.md", "00-core/POL", "00-core/COMP", "00-core/TAX", "00-core/PRO", "00-core/MOD", "00-core/CRI", "00-core/")),
          ("Roteador", ("00-core/roteador/",)), ("Métodos", ("100-métodos/",)), ("Skills e agentes", ("10-skills/", ".claude/skills/", ".claude/agents/")),
          ("Hooks", (".claude/settings",)), ("Ferramentas", ("40-operacao-rotinas/",)), ("Moldes", ("90-templates/",)),
          ("Resto", ("",))]
SYNC = re.compile(r"^(sync \(|AGENTS\.md regenerado|Merge )")


def git(*a, cwd=RAIZ):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *a], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def carregar():
    with io.open(REG, encoding="utf-8") as h:
        reg = json.load(h)
    if not reg.get("recebe"):
        raise ValueError("DERIVADOS.json sem o mapa 'recebe' (o que cada tipo recebe da casa)")
    PORTAVEL.clear(); PORTAVEL.update(reg["recebe"])
    SO_DA_CASA[:] = reg.get("so_da_casa", [])
    return reg


def gravar_reg(reg):
    with io.open(REG, "w", encoding="utf-8", newline="\n") as h:
        json.dump(reg, h, ensure_ascii=False, indent=2); h.write("\n")


def base_de(r):
    b = r.get("base_governanca", "")
    if b and git("cat-file", "-e", b + "^{commit}") is not None and git("rev-parse", "--verify", "-q", b + "^{commit}").strip():
        return b
    return git("rev-list", "-1", "--before=%s 23:59 -0300" % r.get("base_data", "2026-01-01"), "HEAD").strip()


def provisorios():
    out = set()
    pm = os.path.join(RAIZ, "100-métodos")
    for x in os.listdir(pm):
        if x.endswith(".md"):
            try:
                with io.open(os.path.join(pm, x), encoding="utf-8") as h: cab = h.read(1500)
            except Exception: continue
            if "🟡" in cab and "provis" in cab.lower(): out.add("100-métodos/" + x)
    return out


def quarentena_de(reg, tipo, cam, prov):
    for q in reg.get("quarentena", []):
        if tipo in q.get("vale_para", []) and cam.startswith(q["caminho"]):
            return q["motivo"]
    if tipo != "template-publico" and cam in prov:
        return "método 🟡 provisório (sai quando virar ✅)"
    return None


def historico(base):
    """arquivo → (data, assunto) do commit nomeado mais recente desde a base; ('sync', data) se só houve sync."""
    out = git("log", "%s..HEAD" % base, "--no-merges", "--date=short", "--format=@@%ad|%s", "--name-only", "-z")
    mapa, atual = {}, None
    for bloco in out.replace("\x00", "\n").split("\n"):
        if bloco.startswith("@@"):
            d, _, s = bloco[2:].partition("|"); atual = (d, s.strip()); continue
        cam = bloco.strip()
        if not cam or atual is None: continue
        ant = mapa.get(cam)
        nomeado = not SYNC.match(atual[1])
        if ant is None or (ant[2] is False and nomeado):
            mapa[cam] = (atual[0], atual[1] if nomeado else "sync", nomeado)
    return mapa


def delta(reg, r, prov):
    tipo = r["tipo"]
    if tipo == "demo":
        return {"nota": "segue o template; portar depois que o template estiver na base nova"}
    base = base_de(r)
    if not base:
        return {"erro": "base não encontrada"}
    hist = historico(base)
    ns = git("diff", "--name-status", "-M", base, "HEAD")
    itens, fora, quar, casa = [], 0, [], 0
    for ln in ns.splitlines():
        p = ln.split("\t")
        if len(p) < 2: continue
        st, cam = p[0][0], p[-1]
        if not any(cam == x or cam.startswith(x) for x in PORTAVEL.get(tipo, [])):
            fora += 1; continue
        if any(x in cam for x in SO_DA_CASA):
            casa += 1; continue
        m = quarentena_de(reg, tipo, cam, prov)
        if m:
            quar.append((cam, m)); continue
        d, s, _ = hist.get(cam, ("", "", False))
        itens.append((st, cam, d, s))
    nomeados = [l for l in git("log", "%s..HEAD" % base, "--no-merges", "--date=short", "--format=%ad %h %s").splitlines()
                if not SYNC.match(l.split(" ", 2)[2] if l.count(" ") >= 2 else l)]
    exc = r.get("excecoes", "")
    pasta = os.path.normpath(os.path.join(RAIZ, r["pasta"]))
    exc_ok = bool(exc) and os.path.exists(os.path.join(pasta, exc))
    return {"base": base, "itens": itens, "fora": fora, "quar": quar, "casa": casa, "nomeados": nomeados,
            "excecoes": exc, "excecoes_existe": exc_ok, "pasta_existe": os.path.isdir(pasta)}


ATIVO = re.compile(r"(/exemplos/|/fontes/|\.(pdf|woff2?|ttf|png|jpe?g|webp|svg)$)", re.I)


def secoes_tocadas(base, cam):
    """Os títulos (#, ##, ###) sob os quais caem as linhas mudadas desde a base, na versão de hoje."""
    try:
        with io.open(os.path.join(RAIZ, cam), encoding="utf-8") as h: linhas = h.read().splitlines()
    except Exception:
        return []
    tit = [(i + 1, l.lstrip("#").strip()[:70]) for i, l in enumerate(linhas) if re.match(r"^#{1,3} ", l)]
    out = []
    for m in re.finditer(r"^@@ -\S+ \+(\d+)", git("diff", "-U0", base, "HEAD", "--", cam), re.M):
        n = int(m.group(1)); t = [x for x in tit if x[0] <= n]
        nome = t[-1][1] if t else "(topo)"
        if nome not in out: out.append(nome)
    return out


def camada(cam):
    for nome, pref in CAMADA:
        if any(cam.startswith(p) for p in pref): return nome
    return "Resto"


def relatorio(reg, so=None):
    prov = provisorios()
    hoje = datetime.datetime.now(TZ)
    L = ["# DELTA DA CASA PARA OS DERIVADOS — %s" % hoje.strftime("%d/%m/%Y %H:%M"), "",
         "> Gerado por `40-operacao-rotinas/ferramentas/derivados.py --delta` (CLAUDE.md §11.7). Lista o que mudou na Governança desde a base de cada derivado, "
         "**filtrado pelo tipo** (o que ele recebe), **sem quarentena** e sem o que é só da casa. Não porta nada: é o insumo da task de porte.", ""]
    total = 0
    for r in reg["repos"]:
        if so and r["nome"] != so: continue
        if not r.get("ativo", True) and not so:
            L += ["## %s (%s) · inativo" % (r["nome"], r["tipo"]), "", "- " + r.get("nota_base", ""), ""]; continue
        d = delta(reg, r, prov)
        L += ["## %s · `%s`" % (r["nome"], r["tipo"]), ""]
        if "nota" in d or "erro" in d:
            L += ["- " + d.get("nota", d.get("erro", "")), ""]; continue
        total += len(d["itens"])
        L += ["- **Pasta:** `%s` %s · **remoto:** %s%s" % (r["pasta"], "" if d["pasta_existe"] else "🔴 não existe nesta máquina", r["remoto"], " · 🔴 **PÚBLICO**" if r.get("publico") else ""),
              "- **Base na casa:** `%s` (%s) · %s" % (d["base"][:8], r.get("base_data", ""), r.get("nota_base", "")),
              "- **Exceções do derivado:** %s" % (("`%s` ✅ (ler antes de portar; prevalece sobre a casa)" % d["excecoes"]) if d["excecoes_existe"]
                                                  else "`%s` não existe: sem exceção declarada; ler o `CLAUDE.md` dele antes de portar" % (d["excecoes"] or "—")),
              "- **A portar:** %d arquivo(s) · **em quarentena:** %d · só da casa: %d · fora do tipo: %d" % (len(d["itens"]), len(d["quar"]), d["casa"], d["fora"]), ""]
        por, ativos = {}, {}
        for it in d["itens"]:
            if ATIVO.search(it[1]):
                k = os.path.dirname(it[1]); ativos[k] = ativos.get(k, 0) + 1
            else:
                por.setdefault(camada(it[1]), []).append(it)
        for nome, _ in CAMADA:
            if nome not in por: continue
            L += ["### %s (%d)" % (nome, len(por[nome])), "", "| | arquivo | último commit nomeado |", "|---|---|---|"]
            for st, cam, dt, s in sorted(por[nome], key=lambda x: x[1]):
                L.append("| %s | `%s` | %s %s |" % (st, cam, dt, s.replace("|", "/")[:110]))
            L.append("")
            if nome == "Kernel":
                for st, cam, dt, s in sorted(por[nome], key=lambda x: x[1]):
                    if cam.endswith(".md") and st == "M":
                        sec = secoes_tocadas(d["base"], cam)
                        if sec: L += ["**Seções de `%s` tocadas desde a base (%d):** " % (cam, len(sec)) + " · ".join(sec[:40]), ""]
        if ativos:
            L += ["### Ativos binários e exemplos (%d, por pasta)" % sum(ativos.values()), ""] + ["- `%s/`: %d" % kv for kv in sorted(ativos.items())] + [""]
        if d["quar"]:
            grp = {}
            for cam, mot in d["quar"]: grp.setdefault(mot, []).append(cam)
            L += ["### Em quarentena (não porta agora)", ""] + ["- **%s** (%d): %s" % (mot, len(cs), ", ".join("`%s`" % c for c in sorted(cs)[:6]) + (" +%d" % (len(cs) - 6) if len(cs) > 6 else "")) for mot, cs in grp.items()] + [""]
        if r["tipo"] == "template-publico":
            L += ["### Commits nomeados desde a base (%d; os temas para o plano)" % len(d["nomeados"]), ""] + ["- " + n[:160] for n in d["nomeados"][:150]] + [""]
    return "\n".join(L), total


def task_aberta():
    for p in ("fila", "executando", "revisao", "decisao"):
        pd = os.path.join(TAR, p)
        if not os.path.isdir(pd): continue
        for x in os.listdir(pd):
            try:
                with io.open(os.path.join(pd, x), encoding="utf-8") as h:
                    if "tipo: porte-derivados" in h.read(3000): return x
            except Exception: pass
    return None


def proximo_id():
    # 13/11/2026 (T-2026-11-12-022): o gerador único, com faixa por origem (PC, VPS e nuvem não repetem número)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import tarefa_id
    return tarefa_id.proximo(dia=datetime.datetime.now(TZ).date().isoformat(), tarefas=TAR)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--estado", action="store_true"); ap.add_argument("--delta", action="store_true")
    ap.add_argument("--abrir-task", action="store_true"); ap.add_argument("--repo")
    ap.add_argument("--registrar"); ap.add_argument("--base"); ap.add_argument("--base-derivado")
    a = ap.parse_args()
    reg = carregar()
    if a.registrar:
        r = next((x for x in reg["repos"] if x["nome"] == a.registrar), None)
        if not r or not a.base: sys.exit("uso: --registrar NOME --base HASH")
        if not git("rev-parse", "--verify", "-q", a.base + "^{commit}").strip(): sys.exit("base %s não existe na Governança" % a.base)
        r["base_governanca"] = a.base[:8]; r["base_data"] = git("log", "-1", "--date=short", "--format=%ad", a.base).strip()
        if a.base_derivado: r["base_derivado"] = a.base_derivado
        gravar_reg(reg); print("✅ %s: base %s (%s)" % (r["nome"], r["base_governanca"], r["base_data"])); return
    if a.estado:
        prov = provisorios()
        for r in reg["repos"]:
            d = delta(reg, r, prov) if r.get("ativo", True) else {"nota": "inativo"}
            if "itens" in d:
                print("%-26s %-19s base %s (%s) · a portar %3d · quarentena %2d · exceções %s" % (
                    r["nome"], r["tipo"], d["base"][:8], r.get("base_data", ""), len(d["itens"]), len(d["quar"]), "✅" if d["excecoes_existe"] else "—"))
            else:
                print("%-26s %-19s %s" % (r["nome"], r["tipo"], d.get("nota", d.get("erro", ""))))
        return
    if a.delta or a.abrir_task:
        # 11/11/2026: clone raso (nuvem) não tem a base; sem base não se grava delta (um delta vazio apagava o do dia)
        sem = [r["nome"] for r in reg["repos"] if r.get("ativo", True) and r["tipo"] != "demo" and not base_de(r)]
        if sem:
            print("⚠️ base não encontrada neste clone para: %s. Nada gravado: rode onde o histórico é inteiro (PC) ou aprofunde o clone." % ", ".join(sem))
            return
        txt, total = relatorio(reg, a.repo)
        os.makedirs(DIR, exist_ok=True)
        arq = os.path.join(DIR, "DELTA-%s.md" % datetime.datetime.now(TZ).strftime("%Y-%m-%d"))
        with io.open(arq, "w", encoding="utf-8", newline="\n") as h: h.write(txt + "\n")
        print("📄 %s · %d arquivo(s) a portar" % (os.path.relpath(arq, RAIZ), total))
        if a.abrir_task:
            ab = task_aberta()
            if ab: print("· task de porte já aberta: %s" % ab); return
            if total == 0: print("· nada a portar, nenhuma task"); return
            with io.open(MOLDE, encoding="utf-8") as h: m = h.read()
            tid = proximo_id(); hoje = datetime.datetime.now(TZ).date().isoformat()
            m = m.replace("T-AAAA-MM-DD-nnn", tid).replace("AAAA-MM-DD", hoje).replace("<DELTA>", os.path.relpath(arq, RAIZ).replace("\\", "/")).replace("<N>", str(total))
            with io.open(os.path.join(TAR, "fila", tid + ".md"), "w", encoding="utf-8", newline="\n") as h: h.write(m)
            print("✅ task de porte aberta: %s" % tid)
        return
    ap.print_help()


def conferir(raiz=RAIZ):
    """Para o verificar-propagacao.py: aviso, nunca reprova (o porte é semanal, não por tarefa). Reprova só registro quebrado."""
    try:
        reg = carregar()
    except Exception as e:
        return False, ["🔴 DERIVADOS.json ilegível: %s" % e]
    linhas = []
    for r in reg["repos"]:
        if not r.get("ativo", True): continue
        base = r.get("base_data", "")
        try:
            dias = (datetime.date.today() - datetime.date.fromisoformat(base)).days
        except Exception:
            return False, ["🔴 %s sem base_data válida" % r["nome"]]
        extra = " — porte atrasado, rodar `derivados.py --abrir-task`" if dias > 14 else ""
        # D6 (11/11/2026): o molde do repo de cliente mudou depois da base → porte na hora, sem esperar a semanal
        if r["tipo"] != "template-publico" and r.get("base_governanca"):
            try:
                mud = git("log", "--oneline", "%s..HEAD" % r["base_governanca"], "--", "90-templates/repo-cliente/")
            except Exception:
                mud = ""
            if mud.strip():
                extra += " — ⚠️ o molde `90-templates/repo-cliente/` mudou depois da base (%d commit(s)): porte na hora" % len(mud.strip().splitlines())
        if r.get("espera"):
            extra += " — espera: " + r["espera"]
        linhas.append("%s %s: base %s (%d dia(s))%s" % ("⚠️" if dias > 14 else "·", r["nome"], base, dias, extra))
    return True, linhas


if __name__ == "__main__":
    main()
