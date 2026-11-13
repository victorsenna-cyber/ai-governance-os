# -*- coding: utf-8 -*-
"""
despachante_painel.py — o estado do despachante, lido do repo, para a tela Despachante do Continuum-Analytics.

Leitor, nunca fonte (mesma régua do painel-projetos.py, que o importa e põe o resultado em payload["despachante"]).
As regras NÃO se repetem aqui: a elegibilidade, a escada, o orçamento e o gasto da semana vêm do próprio
despachar.py (Task, tasks_em, elegiveis, escada, orcamento, gasto_semana, MODELO). Este módulo só traduz.

  tarefas/PAUSA                      pausa ligada ou não
  tarefas/<estado>/T-*.md            as tasks, por pasta (fila · executando · revisao · decisao · falhou · entregue)
  tarefas/log/RODADA-*.md            as rodadas (o que cada uma executou)
  tarefas/log/GASTO.jsonl            tokens, segundos e custo de cada execução
  tokens/ORCAMENTO.json              teto semanal e a parte do agendado (pelo orcamento() do despachar.py)

  python3 despachante_painel.py           resumo na tela
  python3 despachante_painel.py --json X  grava só o bloco do despachante

O despachante aparece no sistema numa tela à parte.
"""
import datetime as dt, glob, importlib.util, io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location("despachar", os.path.join(AQUI, "despachar.py"))
desp = importlib.util.module_from_spec(_s)
_s.loader.exec_module(desp)

ROT_NIVEL = {"N0": "script, sem modelo", "N1": "modelo gratuito", "N2": "Haiku", "N3": "Sonnet", "N4": "Opus", "N5": "Fable"}
ROT_ESTADO = {"pronta": "pronta", "planejada": "planejada", "executando": "executando", "em_revisao": "em revisão",
              "aguardando_operador": "aguardando sua decisão", "entregue": "entregue", "descartada": "descartada",
              "falhou": "falhou", "bloqueada": "bloqueada", "pronto": "pronto"}
JANELA_SEM = (2, 6)          # o despachar.py não roda das 02h às 06h (as rodadas das 02h e 04h do Agendador)
RITMO_H = 24 // 10           # Agendador: a cada 2 h a partir de 00h (10 rodadas por dia, tokens/ORCAMENTO.json)
ENTREGUES_DIAS = 7
RODADAS_N = 10
LOG_LINHA = re.compile(r"^- (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) · (.*)$")


def agora():
    return desp.agora()


def quando_br(iso):
    """AAAA-MM-DDTHH:MM → DD/MM HH:MM"""
    try:
        d = dt.datetime.fromisoformat(iso)
        return d.strftime("%d/%m %H:%M")
    except (TypeError, ValueError):
        return iso or ""


def log_da_task(t):
    """(última linha do ## Log, data-hora da última entrada com data, linha RESULTADO do worker)."""
    corpo = t.corpo.split("## Log", 1)[1] if "## Log" in t.corpo else ""
    linhas = [l.strip() for l in corpo.splitlines() if l.strip().startswith("- ")]
    ultima = linhas[-1][2:] if linhas else ""
    quando = None
    for l in reversed(linhas):
        m = LOG_LINHA.match(l)
        if m:
            quando = f"{m.group(1)} {m.group(2)}"
            break
    resultado = next((l[2:].split(":", 1)[1].strip() for l in reversed(linhas) if l.startswith("- RESULTADO:")), "")
    m = LOG_LINHA.match("- " + ultima) if ultima else None
    if m:
        ultima = m.group(3)
    ultima = ultima.replace(" ⏎ ", " · ")
    return (ultima[:280] + "…" if len(ultima) > 280 else ultima), quando, (resultado[:280] + "…" if len(resultado) > 280 else resultado)


def traduzir(motivo, titulos):
    """O motivo exatamente como o elegiveis() calcula, em português de gente."""
    m = motivo.strip()
    if m.startswith("tipo entregavel"):
        return "é da rotina na nuvem, não do despachante"
    if m.startswith("estado="):
        e = m.split("=", 1)[1]
        return {"aguardando_operador": "aguardando sua decisão", "bloqueada": "bloqueada"}.get(e, "estado no arquivo: " + ROT_ESTADO.get(e, e))
    if m == "sem 'Pronto quando'":
        return "falta dizer quando fica pronta (seção “Pronto quando”)"
    if m == "nivel_minimo inválido":
        return "nível inválido no arquivo"
    if m.startswith("classe C/S"):
        return "dado sensível não pode ir ao modelo gratuito"
    if m.startswith("depende de "):
        ids = [x.strip() for x in m[len("depende de "):].split(",") if x.strip()]
        return "espera " + ", ".join(f"{i} ({titulos[i]})" if titulos.get(i) else i for i in ids) + " ficar pronta"
    if m.startswith("agendada para "):
        return "agendada para " + quando_br(m[len("agendada para "):])
    if m == "agendada_para inválida":
        return "data de agendamento inválida no arquivo"
    return m


def task_dict(t, pasta, titulos, hoje):
    ultima, quando, resultado = log_da_task(t)
    nivel = t.get("nivel_minimo")
    prazo = t.get("prazo") or None
    dias = None
    if prazo:
        try:
            dias = (dt.date.fromisoformat(prazo[:10]) - hoje).days
        except ValueError:
            prazo = None
    d = dict(id=t.id, titulo=t.get("titulo"), conta=t.get("conta", "casa") or "casa", pasta=pasta,
             estado=t.get("estado"), estado_rot=ROT_ESTADO.get(t.get("estado"), t.get("estado")),
             nivel=nivel, nivel_rot=ROT_NIVEL.get(nivel, nivel), modelo=desp.MODELO.get(nivel),
             escada=desp.escada(t) if nivel in desp.NIVEIS else [nivel],
             prioridade=int(t.get("prioridade", "3") or 3), prazo=prazo, prazo_duro=t.get("prazo_duro", "nao") == "sim",
             dias=dias, vencido=dias is not None and dias < 0, tipo=t.get("tipo") or None,
             recorrencia=t.get("recorrencia") or None, agendada_para=t.get("agendada_para") or None,
             estimativa_tokens=int(t.get("estimativa_tokens", "0") or 0) if str(t.get("estimativa_tokens", "0")).isdigit() else None,
             depende_de=[x.strip() for x in t.get("depende_de").split(",") if x.strip()],
             ultimo_log=ultima, ultimo_log_em=quando, resultado=resultado,
             da_nuvem=t.get("tipo") == "entregavel")
    return d


def rodadas(gasto):
    """As últimas RODADA-*.md, com tokens, segundos e custo de cada execução casados no GASTO.jsonl."""
    arqs = sorted(glob.glob(os.path.join(desp.PASTAS["log"], "RODADA-*.md")))[-RODADAS_N:]
    out = []
    for a in reversed(arqs):
        try:
            txt = desp.ler(a)
        except OSError:
            continue
        m = re.search(r"# RODADA (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})", txt)
        if not m:
            continue
        dia, hora = m.group(1), m.group(2)
        f = re.search(r"fatia: ([\d,.]+) tokens · gasto semana antes: ([\d,.]+)", txt)
        ex = re.search(r"executadas: (\d+) · falhas seguidas: (\d+)", txt)
        itens = []
        for l in txt.splitlines():
            mi = re.match(r"^- (T-[\w-]+) · (N\d) · (\d+)s · (\w+)", l)
            if mi:
                tid, niv, seg, dest = mi.groups()
                g = next((x for x in gasto if x.get("task") == tid and x.get("dia") == dia and x.get("hora", "") >= hora), None)
                itens.append(dict(task=tid, nivel=niv, segundos=int(seg), destino=dest,
                                  tokens=(g or {}).get("tokens"), custo_usd=(g or {}).get("custo_usd")))
                continue
            mi = re.match(r"^- (T-[\w-]+): (.*)$", l)
            if mi:
                itens.append(dict(task=mi.group(1), nivel=None, segundos=None, destino=mi.group(2), tokens=None, custo_usd=None))
        num = lambda s: int(re.sub(r"\D", "", s)) if s else None  # noqa: E731
        out.append(dict(quando=f"{dia} {hora}", arquivo=os.path.relpath(a, desp.RAIZ).replace(os.sep, "/"),
                        fatia=num(f.group(1)) if f else None, gasto_antes=num(f.group(2)) if f else None,
                        executadas=int(ex.group(1)) if ex else len([i for i in itens if i["nivel"]]),
                        falhas_seguidas=int(ex.group(2)) if ex else None, itens=itens,
                        tokens=sum(int(i["tokens"] or 0) for i in itens), segundos=sum(int(i["segundos"] or 0) for i in itens)))
    return out


def ler_gasto():
    p = os.path.join(desp.PASTAS["log"], "GASTO.jsonl")
    out = []
    if not os.path.exists(p):
        return out
    for l in io.open(p, encoding="utf-8"):
        try:
            out.append(json.loads(l))
        except ValueError:
            continue   # linha que não é JSON (marca de conflito de mescla, linha quebrada) não conta, como no despachar.py
    return out


def origem_gasto(o):
    t = str(o.get("task", ""))
    if o.get("origem") == "rotina-nuvem":
        return "nuvem"
    if t.startswith("contexto:"):
        return "contexto"
    return "despachante" if t.startswith("T-") else "outro"


def orcamento_bloco(gasto):
    try:
        orc = desp.orcamento()
    except Exception as e:  # noqa: BLE001  (sem ORCAMENTO.json o despachar.py tentaria medir os transcritos locais)
        return dict(erro=f"orçamento não lido: {e}")
    teto = int(orc.get("teto_semanal_tokens") or 0)
    gasto_sem = desp.gasto_semana()
    fatia_sem = int(teto * float(orc["agendado"]))
    h = agora()
    rpd = int(orc.get("rodadas_por_dia", 10))
    restantes = max(1, (7 - h.weekday()) * rpd - (h.hour // max(1, 24 // rpd)))
    seg = (h - dt.timedelta(days=h.weekday())).date().isoformat()
    por_origem = {}
    for o in gasto:
        if o.get("dia", "") >= seg and o.get("nivel") in desp.LLM:
            k = origem_gasto(o)
            por_origem[k] = por_origem.get(k, 0) + int(o.get("tokens", 0) or 0)
    return dict(teto_semanal=teto, agendado_pct=float(orc["agendado"]), fatia_semana=fatia_sem, gasto_semana=gasto_sem,
                pct=round(100 * gasto_sem / fatia_sem, 1) if fatia_sem else None, por_origem=por_origem,
                fatia_rodada=max(0, (fatia_sem - gasto_sem) // restantes), rodadas_restantes=restantes, semana_desde=seg,
                origem_teto=orc.get("origem_teto", ""))


def montar():
    hoje = agora().date()
    # como o main() do despachar.py: pasta vazia não existe no checkout do Action (o git não guarda pasta vazia),
    # e o tasks_em()/elegiveis() quebram sem ela (na 1ª publicação, com executando/ vazia)
    for p in desp.PASTAS.values():
        os.makedirs(p, exist_ok=True)
    pausa =os.path.exists(os.path.join(desp.TAR, "PAUSA"))
    gasto = ler_gasto()
    por_pasta = {p: desp.tasks_em(p) for p in ("fila", "executando", "revisao", "decisao", "falhou", "entregue")}
    titulos = {t.id: t.get("titulo") for ts in por_pasta.values() for t in ts}
    orc = orcamento_bloco(gasto)
    fatia = orc.get("fatia_rodada")
    fila = desp.elegiveis(True)               # a mesma ordem e os mesmos motivos da rodada
    tasks = []
    vez = 0
    for t in fila:
        d = task_dict(t, "fila", titulos, hoje)
        motivos = [x for x in (t.bloqueio or "").split("; ") if x]
        d["motivos"] = [traduzir(x, titulos) for x in motivos]
        d["motivos_brutos"] = motivos
        d["elegivel"] = not motivos
        # quem a próxima rodada pega (até 3, o --max padrão): elegível, e o orçamento cabe ou não conta
        if d["elegivel"]:
            vez += 1
            d["vez"] = vez
            # a mesma conta da rodada: nível que gasta modelo, estimativa acima da fatia e sem `orcamento: isento` → adiada ou decisão
            nivel = (desp.escada(t) or [d["nivel"]])[0]
            d["cabe_na_fatia"] = not (nivel in desp.LLM and fatia is not None and (d["estimativa_tokens"] or 0) > fatia
                                      and t.get("orcamento") != "isento")
        tasks.append(d)
    for pasta in ("executando", "revisao", "decisao", "falhou"):
        for t in por_pasta[pasta]:
            tasks.append(task_dict(t, pasta, titulos, hoje))
    limite = (hoje - dt.timedelta(days=ENTREGUES_DIAS)).isoformat()
    for t in por_pasta["entregue"]:
        d = task_dict(t, "entregue", titulos, hoje)
        if (d["ultimo_log_em"] or "")[:10] >= limite:
            tasks.append(d)
    rods = rodadas(gasto)
    return dict(pausa=pausa, gerado_em=agora().strftime("%Y-%m-%d %H:%M"),
                agendador=dict(ritmo_horas=RITMO_H, primeira="00:00", pula=list(range(JANELA_SEM[0], JANELA_SEM[1], RITMO_H)),
                               nome="Continuum - despachante", max_por_rodada=3),
                orcamento=orc, ultima_rodada=rods[0] if rods else None, rodadas=rods, tasks=tasks,
                contagem={p: len(por_pasta[p]) for p in por_pasta}, entregues_dias=ENTREGUES_DIAS)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    p = montar()
    if a.json:
        io.open(a.json, "w", encoding="utf-8").write(json.dumps(p, ensure_ascii=False, indent=1))
        print("gravado", a.json)
    o = p["orcamento"]
    print(f"pausa: {'LIGADA' if p['pausa'] else 'não'} · semana: {o.get('gasto_semana', 0):,} de {o.get('fatia_semana', 0):,} ({o.get('pct')}%)")
    u = p["ultima_rodada"]
    if u:
        print(f"última rodada {u['quando']}: {u['executadas']} executada(s) · " + ", ".join(f"{i['task']}→{i['destino']}" for i in u["itens"]))
    for t in p["tasks"]:
        if t["pasta"] == "fila":
            print(f"  fila  {t['id']} {t['nivel']:<3} p{t['prioridade']} {('#' + str(t['vez'])) if t.get('vez') else '  '} "
                  f"{(t['titulo'] or '')[:50]:<50} {'elegível' if t['elegivel'] else ' · '.join(t['motivos'])}")
    print("contagem:", p["contagem"])


if __name__ == "__main__":
    main()
