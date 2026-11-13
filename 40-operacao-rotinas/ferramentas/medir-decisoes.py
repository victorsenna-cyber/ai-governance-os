# -*- coding: utf-8 -*-
"""
medir-decisoes.py — a medição do cartão de decisão em duas camadas (PLANO-DECISOES-NO-PAINEL.md §5.2).

Tipo: ferramenta · medição (N0, sem LLM).
Pergunta que responde: com a face e o lastro, o operador decide mais rápido e dentro das letras?

Lê:
  40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md   o "aberta:" de cada cartão e a linha da resposta
                                                       (`- **AAAA-MM-DD HH:MM** · escolha literal: **X**` ou `resposta livre`)
  40-operacao-rotinas/tarefas/log/DECISOES-DO-PAINEL.md as letras clicadas no sistema (hora do clique)
  o git do DECISOES-PENDENTES.md                       E4: a face mudou com o cartão aberto?
Calcula, só para cartões NASCIDOS no molde novo depois da publicação (INICIO), E1 a E4 e o monitor, e grava
40-operacao-rotinas/tarefas/log/MEDICAO-DECISOES.md com a linha de base congelada no topo.

  python3 -X utf8 medir-decisoes.py            imprime
  python3 -X utf8 medir-decisoes.py --gravar   imprime e grava o relatório

Janela (plano §5.2): os próximos 10 cartões nascidos no molde novo e respondidos, ou 21 dias depois da publicação.
Sentada = momento em que ele responde pelo menos um cartão; respostas a menos de 30 min uma da outra são a mesma sentada.
"""
import argparse, datetime as dt, io, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAR = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas")
PEND = os.path.join(TAR, "DECISOES-PENDENTES.md")
CLIQUES = os.path.join(TAR, "log", "DECISOES-DO-PAINEL.md")
SAIDA = os.path.join(TAR, "log", "MEDICAO-DECISOES.md")
INICIO = dt.datetime.fromisoformat(os.environ.get("MEDIR_DECISOES_INICIO", "2000-01-01T00:00"))   # publicação da tela nova (ISO, no ambiente); cartões abertos antes não entram na janela
JANELA_DIAS, JANELA_N, SENTADA_MIN = 21, 10, 30

BASE = """## Linha de base (a medir na instalação, antes do molde novo; PLANO-DECISOES-NO-PAINEL §5.2)

| | Métrica | Linha de base (formato antigo) | Passa com (10 cartões no molde novo) |
|---|---|---|---|
| **E1** | Respondido na primeira sentada depois de nascer | {{BASE_E1}} | **9 de 10** |
| **E2** | Respondido em até 24 h da abertura | {{BASE_E2}} | **8 de 10**, e nenhum com data acima de 72 h |
| **E3** | Coube na letra (letra, com ou sem ajuste) | {{BASE_E3}} | **9 de 10** |
| **E4** | Face reescrita com o cartão aberto (adendo de fato novo não conta) | {{BASE_E4}} | **no máximo 1 em 10** |
| monitor | Seguiu a recomendação | {{BASE_MONITOR}} | não é meta |

Leitura (plano §5.2): E1 e E3 passam e E2 não piora → o formato fica · E1 passa e E2 não → o atraso é o intervalo entre sentadas
(alavanca seguinte: aviso quando nasce cartão com data) · E3 não passa → ler cada resposta livre contra a linha "Supondo" e corrigir a
regra de escrita · E1 não passa → a task reabre com os 10 cartões como dado.
"""


def _hora(txt):
    txt = (txt or "").strip()
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(txt[:len(f) + 2 if "H" in f else 10], f)
        except ValueError:
            pass
    return None


def cartoes(texto):
    """Todos os cartões do arquivo (abertos e decididos), com aberta, formato, recomendação e a resposta."""
    texto = texto.replace("\r\n", "\n")
    out = []
    for m in re.finditer(r"^### (?:✅[^\n]*?· )?(D-\d{4}-\d{2}-\d{2}-\d{3}) · (.*?)$\n((?:(?!^### |^## ).*\n?)*)", texto, re.M):
        did, cab, corpo = m.groups()
        frente = re.split(r"^\*\*Lastro:\*\*", corpo, maxsplit=1, flags=re.M)[0]
        rec = re.search(r"\*\*Recomendação:\*\*\s*([A-C])", frente)
        ma = re.search(r"aberta\s*:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", cab)
        resp = re.search(r"^- \*\*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\*\* · (escolha literal: \*\*([A-C]|veto|adiar)\*\*|resposta livre)", corpo, re.M)
        out.append(dict(id=did, formato="novo" if re.search(r"^\*\*Em jogo:\*\*", frente, re.M) else "antigo",
                        aberta=_hora(ma.group(1)) if ma else None, recomendado=rec.group(1) if rec else None,
                        respondido=_hora(resp.group(1)) if resp else None,
                        escolha=(resp.group(3) or "LIVRE") if resp else None, face=frente.strip()))
    return out


def cliques():
    if not os.path.exists(CLIQUES):
        return {}
    out = {}
    for l in io.open(CLIQUES, encoding="utf-8").read().split("\n"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 6 and re.match(r"D-\d{4}", c[1]):
            h = _hora(c[5])
            if h:
                out[c[1]] = h
    return out


def sentadas(horas):
    """Agrupa as horas de resposta em sentadas (menos de 30 min entre uma e outra)."""
    hs, grupos = sorted(set(horas)), []
    for h in hs:
        if grupos and (h - grupos[-1][-1]).total_seconds() <= SENTADA_MIN * 60:
            grupos[-1].append(h)
        else:
            grupos.append([h])
    return [(g[0], g[-1]) for g in grupos]


def faces_no_git(ids):
    """E4: quantas versões diferentes da face cada cartão teve enquanto estava em Abertas (só commits desde INICIO)."""
    try:
        hs = subprocess.run(["git", "log", "--format=%H", "--since", INICIO.strftime("%Y-%m-%d %H:%M"), "--",
                             os.path.relpath(PEND, RAIZ)], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8").stdout.split()
    except Exception:
        return {}
    versoes = {i: set() for i in ids}
    for h in hs[:400]:
        t = subprocess.run(["git", "show", "%s:%s" % (h, os.path.relpath(PEND, RAIZ).replace(os.sep, "/"))], cwd=RAIZ,
                           capture_output=True, text=True, encoding="utf-8").stdout
        abertas = t.replace("\r\n", "\n").split("## Decididas", 1)[0]
        for c in cartoes(abertas):
            if c["id"] in versoes:
                versoes[c["id"]].add(re.sub(r"\s+", " ", c["face"]))
    return {i: len(v) for i, v in versoes.items()}


def medir(agora=None):
    agora = agora or dt.datetime.now()
    texto = io.open(PEND, encoding="utf-8").read()
    cs = cartoes(texto)
    clq = cliques()
    for c in cs:   # a hora do clique, quando houver, é mais fiel que a da linha gravada pela VPS
        if c["id"] in clq and c["respondido"]:
            c["respondido"] = clq[c["id"]]
    todas = [c["respondido"] for c in cs if c["respondido"]] + list(clq.values())
    st = sentadas(todas)
    novos = [c for c in cs if c["formato"] == "novo" and c["aberta"] and c["aberta"] >= INICIO]
    resp = sorted([c for c in novos if c["respondido"]], key=lambda c: c["respondido"])
    janela = resp[:JANELA_N]
    fim_janela = INICIO + dt.timedelta(days=JANELA_DIAS)
    e4 = faces_no_git([c["id"] for c in novos])
    linhas = []
    for c in janela:
        primeira = next((s for s in st if s[1] >= c["aberta"]), None)
        c["e1"] = bool(primeira and primeira[0] <= c["respondido"] <= primeira[1] + dt.timedelta(minutes=SENTADA_MIN))
        c["horas"] = (c["respondido"] - c["aberta"]).total_seconds() / 3600
        c["e3"] = c["escolha"] in ("A", "B", "C")
        c["e4"] = e4.get(c["id"], 1) > 1
        c["seguiu"] = c["escolha"] == c["recomendado"]
        linhas.append(c)
    n = len(linhas)
    abertos_72 = [c for c in novos if not c["respondido"] and (agora - c["aberta"]).total_seconds() > 72 * 3600]
    r = dict(n=n, novos=len(novos), pendentes=len(novos) - len(resp), agora=agora, fim_janela=fim_janela,
             fechou=(n >= JANELA_N or agora >= fim_janela),
             e1=sum(c["e1"] for c in linhas), e2=sum(c["horas"] <= 24 for c in linhas), e2_72=sum(c["horas"] > 72 for c in linhas) + len(abertos_72),
             e3=sum(c["e3"] for c in linhas), e4=sum(c["e4"] for c in linhas), seguiu=sum(c["seguiu"] for c in linhas),
             mediana=(sorted(c["horas"] for c in linhas)[n // 2] if n else None), linhas=linhas, sentadas=len(st))
    return r


def relatorio(r):
    f = lambda a, b: "%d de %d" % (a, b) if b else "—"
    out = ["# MEDIÇÃO — o cartão de decisão em duas camadas", "",
           "> Escrito por `40-operacao-rotinas/ferramentas/medir-decisoes.py` (task N0 semanal). Plano: `60-planos/decisoes-no-painel-2026-11-11/PLANO-DECISOES-NO-PAINEL.md` §5.2. "
           "Só entram cartões nascidos no molde novo depois de %s." % INICIO.strftime("%d/%m/%Y %H:%M"), "", BASE,
           "## Leitura de %s" % r["agora"].strftime("%d/%m/%Y %H:%M"), "",
           "- Cartões nascidos no molde novo: **%d** · respondidos na janela: **%d** · ainda abertos: %d · sentadas no registro inteiro: %d"
           % (r["novos"], r["n"], r["pendentes"], r["sentadas"]),
           "- Janela: fecha com %d respondidos ou em %s · **%s**" % (JANELA_N, r["fim_janela"].strftime("%d/%m/%Y"), "fechada: ler o resultado" if r["fechou"] else "aberta"), "",
           "| | Métrica | Agora | Passa com |", "|---|---|---|---|",
           "| E1 | primeira sentada | %s | 9 de 10 |" % f(r["e1"], r["n"]),
           "| E2 | até 24 h | %s%s · acima de 72 h: %d | 8 de 10, nenhum acima de 72 h |" % (f(r["e2"], r["n"]), (" · mediana %.1f h" % r["mediana"]) if r["mediana"] is not None else "", r["e2_72"]),
           "| E3 | coube na letra | %s | 9 de 10 |" % f(r["e3"], r["n"]),
           "| E4 | face reescrita aberta | %s | no máximo 1 em 10 |" % f(r["e4"], r["n"]),
           "| monitor | seguiu a recomendação | %s | não é meta |" % f(r["seguiu"], r["n"]), ""]
    if r["linhas"]:
        out += ["| Cartão | aberta | respondida | horas | escolha | rec. | E1 | E3 | E4 |", "|---|---|---|---:|---|---|---|---|---|"]
        for c in r["linhas"]:
            out.append("| %s | %s | %s | %.1f | %s | %s | %s | %s | %s |" % (c["id"], c["aberta"].strftime("%d/%m %H:%M"), c["respondido"].strftime("%d/%m %H:%M"),
                       c["horas"], c["escolha"], c["recomendado"] or "—", "✅" if c["e1"] else "—", "✅" if c["e3"] else "fora", "reescrita" if c["e4"] else "—"))
    else:
        out.append("*(nenhum cartão nascido no molde novo foi respondido ainda)*")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gravar", action="store_true")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = medir()
    txt = relatorio(r)
    print(txt)
    if a.gravar:
        os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
        io.open(SAIDA, "w", encoding="utf-8", newline="").write(txt)
        print("gravado", os.path.relpath(SAIDA, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
