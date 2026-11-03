# -*- coding: utf-8 -*-
"""
medir-tokens.py — consumo de tokens do Claude Code, lido dos transcritos locais.

Fonte: ~/.claude/projects/**/*.jsonl (cada mensagem do assistente traz modelo e `usage`).
Nada externo: não chama API, não lê o plano. O plano mostra % em `/usage`; o teto em
tokens se calibra cruzando o % anotado com o que este script mede (T3 §5, F0).

Uso:
  python3 medir-tokens.py                 → últimos 14 dias, relatório em
                                       40-operacao-rotinas/tokens/SEMANA-<ano>-S<nn>.md
  python3 medir-tokens.py --dias 30       → janela maior
  python3 medir-tokens.py --so-tela       → imprime e não grava
  python3 medir-tokens.py --calibrar 37   → anota o % do /usage de hoje e estima tokens por 1 %

O que separa: dia · modelo · projeto · sessão principal × subagente (isSidechain).
Métrica extra: **carga fixa por sessão** = cache_creation da 1ª chamada de cada sessão,
que é o que o CLAUDE.md + 00-core + STATUS.md custam antes do primeiro pedido.
Duplicata (mesmo message.id + requestId) conta uma vez.
"""
import argparse, datetime, glob, io, json, os, sys
from collections import defaultdict

TZ = datetime.timezone(datetime.timedelta(hours=-3))  # America/Sao_Paulo, sem DST em 2026
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA_SAIDA = os.path.join(RAIZ, "40-operacao-rotinas", "tokens")
CAMPOS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def ler(dias):
    base = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    ini = datetime.datetime.now(TZ) - datetime.timedelta(days=dias)
    vistos = set()
    chamadas = []  # dicts: dia, modelo, projeto, sessao, sidechain, uso
    primeira = {}  # sessao -> (timestamp, cache_creation) da 1ª chamada
    for arq in glob.glob(os.path.join(base, "*", "**", "*.jsonl"), recursive=True):
        projeto = os.path.relpath(arq, base).split(os.sep)[0]
        try:
            f = io.open(arq, encoding="utf-8", errors="replace")
        except OSError:
            continue
        with f:
            for linha in f:
                if '"usage"' not in linha:
                    continue
                try:
                    o = json.loads(linha)
                except ValueError:
                    continue
                msg = o.get("message") or {}
                uso = msg.get("usage")
                if not isinstance(uso, dict):
                    continue
                ts = o.get("timestamp")
                if not ts:
                    continue
                try:
                    t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(TZ)
                except ValueError:
                    continue
                chave = (msg.get("id"), o.get("requestId"))
                if chave in vistos:
                    continue
                vistos.add(chave)
                sessao = o.get("sessionId") or os.path.basename(arq)
                cc = int(uso.get("cache_creation_input_tokens") or 0)
                if sessao not in primeira or t < primeira[sessao][0]:
                    primeira[sessao] = (t, cc)
                if t < ini:
                    continue
                chamadas.append({
                    "dia": t.date(), "modelo": msg.get("model") or "?", "projeto": projeto,
                    "sessao": sessao, "sidechain": bool(o.get("isSidechain")),
                    "uso": {k: int(uso.get(k) or 0) for k in CAMPOS},
                })
    return chamadas, primeira, ini


def soma(chamadas, chave):
    d = defaultdict(lambda: defaultdict(int))
    for c in chamadas:
        k = chave(c)
        for f in CAMPOS:
            d[k][f] += c["uso"][f]
        d[k]["chamadas"] += 1
    return d


def fmt(n):
    return f"{n:,}".replace(",", ".")


def tabela(titulo, d, rotulo, ordem=None):
    linhas = [f"### {titulo}", "", f"| {rotulo} | chamadas | input | cache novo | cache lido | output | total |", "|---|---:|---:|---:|---:|---:|---:|"]
    chaves = ordem or sorted(d, key=lambda k: -sum(d[k][f] for f in CAMPOS))
    tot = defaultdict(int)
    for k in chaves:
        v = d[k]
        t = sum(v[f] for f in CAMPOS)
        linhas.append(f"| {k} | {fmt(v['chamadas'])} | {fmt(v['input_tokens'])} | {fmt(v['cache_creation_input_tokens'])} | {fmt(v['cache_read_input_tokens'])} | {fmt(v['output_tokens'])} | {fmt(t)} |")
        for f in CAMPOS:
            tot[f] += v[f]
        tot["chamadas"] += v["chamadas"]
    t = sum(tot[f] for f in CAMPOS)
    linhas.append(f"| **total** | {fmt(tot['chamadas'])} | {fmt(tot['input_tokens'])} | {fmt(tot['cache_creation_input_tokens'])} | {fmt(tot['cache_read_input_tokens'])} | {fmt(tot['output_tokens'])} | **{fmt(t)}** |")
    return linhas + [""], tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=14)
    ap.add_argument("--so-tela", action="store_true")
    ap.add_argument("--calibrar", type=float, help="%% mostrado no /usage hoje (semana corrente)")
    a = ap.parse_args()

    chamadas, primeira, ini = ler(a.dias)
    hoje = datetime.datetime.now(TZ)
    ano, semana, _ = hoje.isocalendar()
    out = [f"# TOKENS — {a.dias} dias até {hoje:%d/%m/%Y %H:%M} (semana ISO {ano}-S{semana:02d})", "",
           f"> Gerado por `40-operacao-rotinas/ferramentas/medir-tokens.py` a partir de `~/.claude/projects/**/*.jsonl`. "
           f"Janela: {ini:%d/%m/%Y} a {hoje:%d/%m/%Y}. Só sessões desta máquina: rotinas na nuvem não entram.", ""]
    if not chamadas:
        out.append("Nenhuma chamada na janela.")
    else:
        por_dia = soma(chamadas, lambda c: c["dia"].strftime("%d/%m"))
        t1, tot = tabela("Por dia", por_dia, "dia", ordem=sorted(por_dia, key=lambda s: (s[3:], s[:2])))
        out += t1
        t2, _ = tabela("Por modelo", soma(chamadas, lambda c: c["modelo"]), "modelo")
        out += t2
        t3, _ = tabela("Sessão principal × subagente", soma(chamadas, lambda c: "subagente" if c["sidechain"] else "principal"), "tipo")
        out += t3
        t4, _ = tabela("Por projeto (pasta aberta)", soma(chamadas, lambda c: c["projeto"][-60:]), "projeto")
        out += t4
        # carga fixa por sessão
        sess = {s for s in {c["sessao"] for c in chamadas} if s in primeira}
        cargas = sorted(primeira[s][1] for s in sess if primeira[s][0] >= ini and primeira[s][1] > 0)
        if cargas:
            med = cargas[len(cargas) // 2]
            out += ["### Carga fixa por sessão (cache novo da 1ª chamada)", "",
                    f"- sessões na janela: {len(cargas)} · mediana: **{fmt(med)} tokens** · máximo: {fmt(cargas[-1])} · mínimo: {fmt(cargas[0])}",
                    f"- soma das cargas de abertura na janela: {fmt(sum(cargas))} tokens "
                    f"({100 * sum(cargas) / max(1, sum(tot[f] for f in CAMPOS)):.1f}% de tudo o que foi lido ou gerado)",
                    "- é o custo do `CLAUDE.md` + `00-core/` + `STATUS.md` + árvore antes do primeiro pedido; o gate de contexto fixo da T2/T4 se mede aqui.", ""]
        dias_com_uso = len(por_dia)
        total = sum(tot[f] for f in CAMPOS)
        out += ["### Semana", "", f"- média por dia com uso: **{fmt(total // max(1, dias_com_uso))} tokens** · projeção de 7 dias: {fmt(7 * total // max(1, dias_com_uso))}"]
        if a.calibrar:
            # consumo desde a segunda-feira da semana ISO corrente
            seg = (hoje - datetime.timedelta(days=hoje.weekday())).date()
            sem = [c for c in chamadas if c["dia"] >= seg]
            tsem = sum(c["uso"][f] for c in sem for f in CAMPOS)
            por1 = tsem / a.calibrar if a.calibrar else 0
            out += [f"- calibração: {fmt(tsem)} tokens desde segunda {seg:%d/%m} = {a.calibrar:.0f}% do /usage → **{fmt(int(por1))} tokens por 1%** → teto estimado da semana: {fmt(int(por1 * 100))}"]
        out.append("")
    texto = "\n".join(out)
    if a.so_tela:
        sys.stdout.write(texto + "\n")
        return
    os.makedirs(PASTA_SAIDA, exist_ok=True)
    arq = os.path.join(PASTA_SAIDA, f"SEMANA-{ano}-S{semana:02d}.md")
    io.open(arq, "w", encoding="utf-8").write(texto + "\n")
    sys.stdout.write(texto + f"\n\n→ gravado em {os.path.relpath(arq, RAIZ)}\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
