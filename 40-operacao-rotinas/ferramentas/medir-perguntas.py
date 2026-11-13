#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
medir-perguntas.py — a medição semanal da autonomia (PLANO-AUTONOMIA-2026-11-09 §7).

Tipo: ferramenta (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Origem: script de medição da autonomia (plano de autonomia, F0)

Lê os transcritos locais do Claude Code deste projeto e conta, para cada resposta nossa que precede um turno
HUMANO do operador (notificação de task, mensagem entre sessões e resultado de ferramenta não contam):
  - quantas terminam em pergunta (? no fim)
  - quantas terminam OFERECENDO ato sem citar item da lista fechada (o mesmo critério do gate-fecho.py)
  - quantas vezes o operador cobrou autonomia ("por que parou", "não resolveu", "autonomia"...)
E soma os bloqueios do gate (40-operacao-rotinas/tokens/GATE-FECHO.jsonl).

Uso:
  python3 -X utf8 40-operacao-rotinas/ferramentas/medir-perguntas.py               últimos 7 dias, imprime
  python3 -X utf8 40-operacao-rotinas/ferramentas/medir-perguntas.py --dias 30
  python3 -X utf8 40-operacao-rotinas/ferramentas/medir-perguntas.py --gravar      e acrescenta a semana em tokens/AUTONOMIA.md
Metas (4 semanas a partir da instalação): ofertas de ato reversível 0 · perguntas <= 5% · cobranças 0.
"""
import glob, importlib.util, io, json, os, re, sys, time
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJ = os.path.join(os.path.expanduser("~"), ".claude", "projects",
                    "<pasta-do-projeto-no-claude>")
REL = os.path.join(RAIZ, "40-operacao-rotinas", "tokens", "AUTONOMIA.md")
LOG = os.path.join(RAIZ, "40-operacao-rotinas", "tokens", "GATE-FECHO.jsonl")
_s = importlib.util.spec_from_file_location("gate", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate-fecho.py"))
gate = importlib.util.module_from_spec(_s); _s.loader.exec_module(gate)

COBRANCA = re.compile(r"por qual raz[ãa]o (voc[êe] )?parou|por que (voc[êe] )?parou|n[ãa]o resolveu|(dar|ter|tem|precisa de|abarcar) (essa |sua |mais )?autonomia|"
                      r"j[áa] (podia|devia) ter feito|j[áa] (est[áa]|t[áa]) (pronto|rodando|no ar|ligado|funcionando)|j[áa] (fez|ligou|subiu|publicou)\b|"
                      r"precis(o|a) ficar (pedindo|lembrando)|por que (voc[êe] )?(me )?pergunt", re.I)
NAO_HUMANO = ("<task-notification", "<cross-session", "[SYSTEM", "<system-reminder", "<local-command", "<command-")


def texto(content):
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in (content or []) if isinstance(b, dict) and b.get("type") == "text")


def medir(dias):
    desde = datetime.now().astimezone() - timedelta(days=dias)
    n = perg = oferta = cobr = 0
    exemplos = []
    for f in glob.glob(os.path.join(PROJ, "*.jsonl")):
        if os.path.getmtime(f) < desde.timestamp():
            continue
        ult = None
        for linha in io.open(f, encoding="utf-8", errors="replace"):
            try:
                o = json.loads(linha)
            except ValueError:
                continue
            if o.get("isSidechain"):
                continue
            ts = o.get("timestamp")
            if ts:
                try:
                    if datetime.fromisoformat(ts.replace("Z", "+00:00")) < desde:
                        continue
                except ValueError:
                    pass
            msg = o.get("message") or {}
            if o.get("type") == "assistant":
                t = texto(msg.get("content"))
                if t.strip():
                    ult = t
            elif o.get("type") == "user":
                t = texto(msg.get("content")).strip()
                if not t or t.startswith(NAO_HUMANO):
                    continue
                if COBRANCA.search(t):
                    cobr += 1
                if ult:
                    n += 1
                    if ult.rstrip().endswith("?"):
                        perg += 1
                    r = gate.julgar_fecho(ult)
                    if r:
                        oferta += 1
                        exemplos.append(f"{os.path.basename(f)[:8]} · \"{r}\"")
                ult = None
    bloq = {"Stop": 0, "SubagentStop": 0}
    if os.path.exists(LOG):
        for l in io.open(LOG, encoding="utf-8"):
            try:
                e = json.loads(l)
            except ValueError:
                continue
            if e.get("data", "") >= desde.strftime("%Y-%m-%d"):
                bloq[e.get("evento", "Stop")] = bloq.get(e.get("evento", "Stop"), 0) + 1
    return {"turnos": n, "perguntas": perg, "ofertas": oferta, "cobrancas": cobr, "bloqueios": bloq, "exemplos": exemplos}


def relatorio(m, dias):
    pct = lambda x: f"{(x / m['turnos'] * 100):.0f}%" if m["turnos"] else "—"
    linhas = [f"## Semana até {time.strftime('%d/%m/%Y')} (últimos {dias} dias)", "",
              "| Indicador | Valor | Meta |", "|---|---:|---|",
              f"| respostas antes de turno humano | {m['turnos']} | — |",
              f"| terminando em pergunta | {m['perguntas']} ({pct(m['perguntas'])}) | ≤ 5% |",
              f"| terminando em oferta de ato sem item da lista | {m['ofertas']} | 0 |",
              f"| cobranças do operador por autonomia | {m['cobrancas']} | 0 |",
              f"| bloqueios do gate · Stop / SubagentStop | {m['bloqueios'].get('Stop', 0)} / {m['bloqueios'].get('SubagentStop', 0)} | cai semana a semana |", ""]
    if m["exemplos"]:
        linhas += ["Ofertas encontradas:", *[f"- {e}" for e in m["exemplos"][:10]], ""]
    return "\n".join(linhas)


def main():
    a = sys.argv[1:]
    if a[:1] in (["-h"], ["--help"]):
        print(__doc__); return
    dias = int(a[a.index("--dias") + 1]) if "--dias" in a else 7
    txt = relatorio(medir(dias), dias)
    print(txt)
    if "--gravar" in a:
        novo = not os.path.exists(REL)
        with io.open(REL, "a", encoding="utf-8") as f:
            if novo:
                f.write("# AUTONOMIA — medição semanal\n\n> Escrito por `40-operacao-rotinas/ferramentas/medir-perguntas.py`. "
                        "Plano: `40-operacao-rotinas/PLANO-AUTONOMIA.md` §7. Duas reversões do operador no mesmo "
                        "tipo de ato em 4 semanas devolvem o tipo à lista fechada.\n\n")
            f.write(txt + "\n")
        print("gravado em", os.path.relpath(REL, RAIZ))


if __name__ == "__main__":
    main()
