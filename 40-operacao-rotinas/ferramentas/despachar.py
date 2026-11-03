# -*- coding: utf-8 -*-
"""
despachar.py — despachante das tasks (N0, sem LLM). Lê tarefas/fila/, confere orçamento,
janela e dependências, e lança um worker por task no nível mais barato permitido.

  python3 despachar.py --dry-run          lista e ordena, mostra orçamento, não executa
  python3 despachar.py                    uma rodada (até --max tasks, padrão 3)
  python3 despachar.py --so N0,N2         só esses níveis
  python3 despachar.py --task T-...-001   força uma task (ignora prioridade, respeita orçamento)
  python3 despachar.py --sem-sync         não roda sincronizar.py no fim

WORKER_CLI=<comando> troca o `claude -p` por outro agente (prompt pelo stdin; {modelo} e {nivel} são substituídos).
Agendamento: Windows = Agendador de Tarefas · macOS = LaunchAgent (ferramentas/macos/instalar-mac.sh) · Linux = cron.

Estado = pasta (fila → executando → revisao|entregue|falhou|decisao). Trava: tarefas/.lock.
PAUSA em tarefas/ para tudo. Três falhas seguidas param a rodada.
"""
import argparse, datetime, io, json, os, re, shutil, subprocess, sys, time

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAR = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas")
TOK = os.path.join(RAIZ, "40-operacao-rotinas", "tokens")
FER = os.path.join(RAIZ, "40-operacao-rotinas", "ferramentas")
PASTAS = {k: os.path.join(TAR, k) for k in ("fila", "executando", "revisao", "decisao", "entregue", "falhou", "log")}
TZ = datetime.timezone(datetime.timedelta(hours=-3))
MODELO = {"N2": "claude-haiku-5-5", "N3": "claude-sonnet-5-5", "N4": "claude-opus-5-5", "N5": "claude-fable-5-1"}
NIVEIS = ["N0", "N1", "N2", "N3", "N4", "N5"]
LLM = ("N2", "N3", "N4", "N5")  # níveis que consomem o plano
TOOLS_PADRAO = "Read,Grep,Glob,Edit,Write,Bash(py *),Bash(python *),Bash(python3 *),Bash(curl *),Bash(ls *),Bash(git status*),Bash(git diff*),Bash(git log*)"


def agora():
    return datetime.datetime.now(TZ)


def ler(p):
    return io.open(p, encoding="utf-8", newline="").read()


def escrever(p, t):
    io.open(p, "w", encoding="utf-8", newline="").write(t)


# ---------- task ----------
class Task:
    def __init__(self, caminho):
        self.caminho = caminho
        self.texto = ler(caminho)
        self.nl = "\r\n" if "\r\n" in self.texto else "\n"
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", self.texto, re.S)
        if not m:
            raise ValueError("sem frontmatter")
        self.fm = {}
        for linha in m.group(1).splitlines():
            if ":" in linha and not linha.startswith(" "):
                k, v = linha.split(":", 1)
                v = v.split("  #")[0].strip()
                self.fm[k.strip()] = v
        self.corpo = self.texto[m.end():]
        self.id = self.fm.get("id") or os.path.basename(caminho)[:-3]

    def get(self, k, d=""):
        return self.fm.get(k, d) or d

    @property
    def pronto_quando(self):
        m = re.search(r"## Pronto quando\s*\r?\n(.*?)(?:\r?\n## |\Z)", self.corpo, re.S)
        return (m.group(1).strip() if m else "")

    @property
    def pedido(self):
        m = re.search(r"## Pedido\s*\r?\n(.*?)(?:\r?\n## |\Z)", self.corpo, re.S)
        return (m.group(1).strip() if m else "")

    def set(self, k, v):
        self.fm[k] = v
        self.texto = re.sub(rf"(?m)^{re.escape(k)}:.*$", f"{k}: {v}", self.texto, count=1)
        if not re.search(rf"(?m)^{re.escape(k)}:", self.texto):
            self.texto = self.texto.replace("---" + self.nl, "---" + self.nl + f"{k}: {v}" + self.nl, 1)

    def log(self, msg):
        linha = f"- {agora():%Y-%m-%d %H:%M} · {msg}"
        if "## Log" in self.texto:
            self.texto = self.texto.rstrip("\r\n") + self.nl + linha + self.nl
        else:
            self.texto = self.texto.rstrip("\r\n") + self.nl + "## Log" + self.nl + linha + self.nl

    def salvar(self):
        escrever(self.caminho, self.texto)

    def mover(self, pasta):
        dest = os.path.join(PASTAS[pasta], os.path.basename(self.caminho))
        self.salvar()
        shutil.move(self.caminho, dest)
        self.caminho = dest
        return dest


def tasks_em(pasta):
    out = []
    for f in sorted(os.listdir(PASTAS[pasta])):
        if f.endswith(".md") and f.upper().startswith("T-"):
            try:
                out.append(Task(os.path.join(PASTAS[pasta], f)))
            except Exception as e:
                print(f"  ! {f}: {e}")
    return out


# ---------- orçamento ----------
def orcamento():
    p = os.path.join(TOK, "ORCAMENTO.json")
    base = {"teto_semanal_tokens": None, "operador": 0.40, "agendado": 0.35, "folga": 0.25,
            "rodadas_por_dia": 10, "nota": "teto calibrado por medir-tokens.py --calibrar; sem teto, usa 7x a media diaria medida (input+cache novo+output)"}
    if os.path.exists(p):
        base.update(json.load(io.open(p, encoding="utf-8")))
    if not base["teto_semanal_tokens"]:
        sys.path.insert(0, FER)
        try:
            import importlib
            mt = importlib.import_module("medir-tokens") if False else None
        except Exception:
            mt = None
        # importa por caminho (nome com hífen)
        import importlib.util
        spec = importlib.util.spec_from_file_location("medir_tokens", os.path.join(FER, "medir-tokens.py"))
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        chamadas, _, _ = mod.ler(14)
        por_dia = {}
        for c in chamadas:
            por_dia[c["dia"]] = por_dia.get(c["dia"], 0) + c["uso"]["input_tokens"] + c["uso"]["cache_creation_input_tokens"] + c["uso"]["output_tokens"]
        media = sum(por_dia.values()) / max(1, len(por_dia))
        base["teto_semanal_tokens"] = int(media * 7)
        base["origem_teto"] = f"estimado: 7 x media diaria de {len(por_dia)} dias ({int(media)})"
    return base


def gasto_semana():
    p = os.path.join(PASTAS["log"], "GASTO.jsonl")
    if not os.path.exists(p):
        return 0
    seg = (agora() - datetime.timedelta(days=agora().weekday())).date().isoformat()
    tot = 0
    for l in io.open(p, encoding="utf-8"):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if o.get("dia", "") >= seg and o.get("nivel") in LLM:
            tot += int(o.get("tokens", 0))
    return tot


def registrar_gasto(reg):
    reg["dia"] = agora().date().isoformat()
    reg["hora"] = agora().strftime("%H:%M")
    with io.open(os.path.join(PASTAS["log"], "GASTO.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")


# ---------- seleção ----------
def entregues():
    return {t.id for t in tasks_em("entregue")}


def elegiveis(dry):
    feitas = entregues()
    out = []
    for t in tasks_em("fila"):
        motivos = []
        if t.get("estado", "pronta") not in ("pronta", "planejada"):
            motivos.append(f"estado={t.get('estado')}")
        if not t.pronto_quando:
            motivos.append("sem 'Pronto quando'")
        if t.get("nivel_minimo") not in NIVEIS:
            motivos.append("nivel_minimo inválido")
        if t.get("nivel_minimo") == "N1" and t.get("classe_dado") in ("C", "S"):
            motivos.append("classe C/S não pode em N1")
        dep = [d.strip() for d in t.get("depende_de").split(",") if d.strip()]
        falta = [d for d in dep if d not in feitas]
        if falta:
            motivos.append("depende de " + ",".join(falta))
        ag = t.get("agendada_para")
        if ag:
            try:
                if datetime.datetime.fromisoformat(ag).replace(tzinfo=TZ) > agora():
                    motivos.append(f"agendada para {ag}")
            except ValueError:
                motivos.append("agendada_para inválida")
        t.bloqueio = "; ".join(motivos)
        out.append(t)
    def chave(t):
        return (int(t.get("prioridade", "3") or 3), t.get("prazo") or "9999-12-31", t.id)
    return sorted(out, key=chave)


def escada(t):
    piso = t.get("nivel_minimo")
    lista = [n.strip() for n in t.get("escada", piso).split(",") if n.strip()] or [piso]
    return [n for n in NIVEIS if n in lista and NIVEIS.index(n) >= NIVEIS.index(piso)] or [piso]


# ---------- workers ----------
def worker_n0(t):
    cmd = t.get("comando")
    if not cmd:
        return False, "N0 sem 'comando'", {}
    r = subprocess.run(cmd, shell=True, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    saida = (r.stdout + r.stderr)[-1500:]
    return r.returncode == 0, saida, {}


def worker_n1(t):
    cli = os.path.join(FER, "freellmapi", "n1_cliente.py")
    if not os.path.exists(cli):
        return False, "n1_cliente.py não existe", {}
    prompt = montar_prompt(t, "N1")
    r = subprocess.run([sys.executable, cli, "--classe", t.get("classe_dado"), "--perfil", t.get("perfil", "auto:continuum-rapido"), prompt],
                       cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    if r.returncode != 0:
        return False, (r.stdout + r.stderr)[-1500:], {}
    escrever(os.path.join(RAIZ, t.get("saida")), r.stdout)
    return True, f"saída gravada em {t.get('saida')} ({len(r.stdout)} chars)", {}


def montar_prompt(t, nivel):
    rel = os.path.relpath(t.caminho, RAIZ)
    return (f"Você é um worker de nível {nivel} da {{EMPRESA}}. Execute SOMENTE a task `{rel}` (leia-a inteira primeiro). "
            f"Pedido:\n{t.pedido}\n\nPronto quando:\n{t.pronto_quando}\n\n"
            f"Insumos: {t.get('insumos') or '—'}. Saída: `{t.get('saida')}` (um arquivo só). "
            f"Alçada: {t.get('alcada') or 'nao envia; nao decide preco; nao escreve em DECISOES.md'}. "
            "Regras: não envie nada a ninguém; não altere preço, política, data pactuada nem `00-core/`; não rode git que altere estado; "
            "não leia pastas inteiras — só os insumos; escreva a saída no caminho indicado; ao terminar, acrescente ao `## Log` da task uma linha "
            "começando com `- RESULTADO:` dizendo em 2 linhas o que fez e o que ficou em dúvida. Responda no fim só com `OK` ou `FALHOU: motivo`.")


def worker_ruflo(t):
    """Worker opcional: Ruflo como processo externo para task N4 com `swarm: sim`.
    O comando vem de tokens/ORCAMENTO.json ("ruflo_comando", com {task} no lugar do caminho),
    por exemplo: "npx -y ruflo@3.57.1 swarm run --task {task}". Sem comando configurado,
    cai para o Opus (N4). Nunca entra como MCP da sessão (custo medido: >= 38 mil tokens/sessão)."""
    cmd = orcamento().get("ruflo_comando")
    if not cmd:
        return None
    cmd = cmd.replace("{task}", os.path.relpath(t.caminho, RAIZ))
    try:
        r = subprocess.run(cmd, shell=True, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
    except subprocess.TimeoutExpired:
        return False, "ruflo: timeout 60 min", {}
    return r.returncode == 0, (r.stdout + r.stderr)[-1500:], {}


def worker_claude(t, nivel):
    prompt = montar_prompt(t, nivel)
    tools = t.get("tools", TOOLS_PADRAO)
    cli = os.environ.get("WORKER_CLI")  # outro agente no lugar do Claude Code, ex.: 'codex exec --model {modelo} -' (prompt pelo stdin)
    if cli:
        import shlex
        cmd = shlex.split(cli.format(modelo=MODELO[nivel], nivel=nivel))
    else:
        cmd = ["claude", "-p", "--model", MODELO[nivel], "--output-format", "json", "--allowedTools", tools, "--max-turns", t.get("max_turns", "40")]
    try:
        r = subprocess.run(cmd, input=prompt, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600, shell=(os.name == "nt"))
    except subprocess.TimeoutExpired:
        return False, "timeout 60 min", {}
    uso = {}
    resultado = r.stdout.strip()
    try:
        o = json.loads(resultado)
        resultado = o.get("result", resultado)
        u = o.get("usage") or {}
        uso = {"tokens": int(u.get("input_tokens", 0)) + int(u.get("cache_creation_input_tokens", 0)) + int(u.get("output_tokens", 0)),
               "cache_lido": int(u.get("cache_read_input_tokens", 0)), "custo_usd": o.get("total_cost_usd"), "sessao": o.get("session_id")}
    except ValueError:
        pass
    ok = r.returncode == 0 and not resultado.strip().upper().startswith("FALHOU")
    return ok, (resultado or r.stderr)[-1500:], uso


def verificar(t):
    v = t.get("verificacao")
    if not v:
        return None, ""
    r = subprocess.run(v, shell=True, cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    return r.returncode == 0, (r.stdout + r.stderr)[-800:]


def destino_pos_execucao(t, nivel, verif):
    if verif is False:
        return "falhou"
    if nivel == "N0":
        return "entregue"
    if nivel == "N2" and t.get("carga") == "mecanica" and verif is True:
        return "entregue"
    if t.get("tipo_decisao"):
        return "decisao"
    return "revisao"


def recorrer(t):
    rec = t.get("recorrencia")
    if rec not in ("diaria", "semanal"):
        return
    dias = 1 if rec == "diaria" else 7
    novo = Task(t.caminho)
    prox = (agora() + datetime.timedelta(days=dias)).replace(hour=5, minute=0, second=0, microsecond=0)
    novo.set("agendada_para", prox.strftime("%Y-%m-%dT%H:%M"))
    novo.set("estado", "pronta")
    novo.texto = re.sub(r"## Log.*\Z", "## Log" + novo.nl, novo.texto, flags=re.S)
    novo.caminho = os.path.join(PASTAS["fila"], os.path.basename(t.caminho))
    novo.salvar()


# ---------- rodada ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max", type=int, default=3)
    ap.add_argument("--so", default="", help="níveis, ex. N0,N2")
    ap.add_argument("--task", default="")
    ap.add_argument("--sem-sync", action="store_true")
    a = ap.parse_args()
    so = [s.strip() for s in a.so.split(",") if s.strip()]

    for p in PASTAS.values():
        os.makedirs(p, exist_ok=True)
    if os.path.exists(os.path.join(TAR, "PAUSA")):
        print("PAUSA presente: nada roda."); return 0
    if not a.dry_run and not a.task and 2 <= agora().hour < 6:
        print("fora da janela (02h-06h): nada roda."); return 0
    lock = os.path.join(TAR, ".lock")
    if os.path.exists(lock) and time.time() - os.path.getmtime(lock) < 4 * 3600 and not a.dry_run:
        print("outro despachante em execução (.lock); saindo."); return 0

    orc = orcamento()
    gasto = gasto_semana()
    fatia_semana = int(orc["teto_semanal_tokens"] * orc["agendado"])
    hoje = agora()
    rodadas_restantes = max(1, (7 - hoje.weekday()) * orc["rodadas_por_dia"] - (hoje.hour // max(1, 24 // orc["rodadas_por_dia"])))
    fatia_rodada = max(0, (fatia_semana - gasto) // rodadas_restantes)
    print(f"# Rodada {hoje:%Y-%m-%d %H:%M} · teto semanal {orc['teto_semanal_tokens']:,} ({orc.get('origem_teto','ORCAMENTO.json')}) · "
          f"agendado {fatia_semana:,} · gasto na semana {gasto:,} · fatia desta rodada {fatia_rodada:,} tokens")

    cands = elegiveis(a.dry_run)
    if a.task:
        cands = [t for t in cands if t.id == a.task]
    print(f"\n| # | task | nível | classe | prio | prazo | est. tokens | situação |\n|---|---|---|---|---|---|---:|---|")
    for i, t in enumerate(cands, 1):
        print(f"| {i} | {t.id} · {t.get('titulo')[:50]} | {t.get('nivel_minimo')}→{','.join(escada(t))} | {t.get('classe_dado')} | {t.get('prioridade','3')} | {t.get('prazo') or '—'} | {t.get('estimativa_tokens','?')} | {t.bloqueio or 'elegível'} |")
    if a.dry_run:
        return 0

    escrever(lock, str(os.getpid()))
    rodada = [f"# RODADA {hoje:%Y-%m-%d %H:%M}", "", f"fatia: {fatia_rodada:,} tokens · gasto semana antes: {gasto:,}", ""]
    falhas_seguidas = executadas = 0
    try:
        for t in cands:
            if executadas >= a.max or falhas_seguidas >= 3:
                break
            if t.bloqueio:
                continue
            nivs = [n for n in escada(t) if not so or n in so]
            if not nivs:
                continue
            nivel = nivs[0]
            est = int(t.get("estimativa_tokens", "0") or 0)
            if nivel in LLM and est > fatia_rodada:
                # escada quando o orçamento bate
                if t.get("prazo") and t.get("prazo_duro", "nao") != "sim":
                    prox = (hoje + datetime.timedelta(hours=24 // orc["rodadas_por_dia"] + 1)).strftime("%Y-%m-%dT%H:%M")
                    t.set("agendada_para", prox); t.log(f"adiada: estimativa {est} > fatia {fatia_rodada}; nova janela {prox}"); t.salvar()
                    rodada.append(f"- {t.id}: adiada para {prox} (orçamento)")
                elif "N1" in nivs and t.get("classe_dado") in ("P", "I"):
                    nivel = "N1"
                else:
                    t.set("estado", "aguardando_operador"); t.log(f"orçamento: estimativa {est} > fatia {fatia_rodada}; sem prazo adiável → decisão (usar a reserva ou esperar)")
                    t.mover("decisao"); rodada.append(f"- {t.id}: para decisão (orçamento)")
                continue
            # executa
            t.set("estado", "executando"); t.log(f"início · nível {nivel}"); t.mover("executando")
            ini = time.time()
            if nivel == "N0":
                ok, saida, uso = worker_n0(t)
            elif nivel == "N1":
                ok, saida, uso = worker_n1(t)
            else:
                res = worker_ruflo(t) if (nivel == "N4" and t.get("swarm") == "sim") else None
                ok, saida, uso = res if res else worker_claude(t, nivel)
            dur = int(time.time() - ini)
            t = Task(t.caminho)  # recarrega: o worker pode ter escrito no Log
            verif, vsaida = (verificar(t) if ok else (False, "worker falhou"))
            dest = destino_pos_execucao(t, nivel, verif) if ok else "falhou"
            t.log(f"fim · nível {nivel} · {dur}s · {'ok' if ok else 'FALHOU'} · tokens {uso.get('tokens','—')} · verificação: {verif if verif is not None else 'sem'} → {dest}")
            if saida:
                t.log("saída do worker: " + saida.replace("\r", "").replace("\n", " ⏎ ")[:600])
            if vsaida:
                t.log("verificação: " + vsaida.replace("\r", "").replace("\n", " ⏎ ")[:300])
            t.set("estado", {"entregue": "entregue", "revisao": "em_revisao", "decisao": "aguardando_operador", "falhou": "falhou"}[dest])
            t.mover(dest)
            registrar_gasto({"task": t.id, "nivel": nivel, "modelo": MODELO.get(nivel, nivel), "tokens": uso.get("tokens", 0),
                             "cache_lido": uso.get("cache_lido", 0), "custo_usd": uso.get("custo_usd"), "segundos": dur, "resultado": dest})
            if nivel in LLM:
                fatia_rodada -= uso.get("tokens", est)
            if dest == "entregue":
                recorrer(t)
            executadas += 1
            falhas_seguidas = falhas_seguidas + 1 if dest == "falhou" else 0
            rodada.append(f"- {t.id} · {nivel} · {dur}s · {dest}")
    finally:
        if os.path.exists(lock):
            os.remove(lock)
    rodada.append(f"\nexecutadas: {executadas} · falhas seguidas: {falhas_seguidas}")
    escrever(os.path.join(PASTAS["log"], f"RODADA-{hoje:%Y-%m-%d-%H%M}.md"), "\n".join(rodada) + "\n")
    print("\n".join(rodada))
    if not a.sem_sync and executadas:
        sync = os.path.join(FER, "sincronizar.py")
        if os.path.exists(sync):
            subprocess.run([sys.executable, sync, "--hook"], cwd=RAIZ)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
