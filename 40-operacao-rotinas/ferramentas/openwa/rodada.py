#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rodada.py — a rotina de captura do WhatsApp: UMA conversa por vez, com intervalo entre elas.

Tipo: ferramenta (00-core/TAXONOMIA-DE-ARTEFATOS.md) · alçada {{OPERADOR}}
Regra: capturar tudo e todas as conversas de uma vez corre o risco de o WhatsApp interromper pelo grande fluxo,
e numa rotina o operador pode não ver as próprias notificações. A rotina captura conversas específicas, uma de
cada vez, com espaçamento breve (N segundos) entre uma e outra captura.

O que faz: lê o mapa `conversas.json`, e para cada conversa ativa roda um processo separado
`capturar.py --chat <chatId>` (só aquela conversa; transcrição dos áudios dela no fim do processo, local,
sem tocar o WhatsApp), espera `--espaco` segundos e vai para a próxima. Nunca chama o `capturar.py` sem
`--chat`. Para no `--max` ou em `--falhas` falhas seguidas (conexão caindo), e grava um relatório em
`tarefas/log/CAPTURA-<data-hora>.md`.

Uso (da raiz da Governança):
  python3 40-operacao-rotinas/ferramentas/openwa/rodada.py                    todas as conversas do mapa, 30 s entre elas
  py ... rodada.py --espaco 60 --max 8                                    60 s de intervalo, no máximo 8 conversas
  py ... rodada.py --so "<Pasta 1>" --so "<Pasta 2>"               só as pastas citadas
  py ... rodada.py --lista 40-operacao-rotinas/ferramentas/openwa/rodada.json   só os chatIds do arquivo
  py ... rodada.py --dry-run                                               mostra a ordem, não captura

Ordem: a conversa com atividade mais antiga no último cursor vai primeiro? Não: a ordem é a do mapa, estável,
para que uma rodada interrompida continue de onde parou na próxima (`--max` + `.rodada-cursor`).
"""
import io, json, os, subprocess, sys, time
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
GOV = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CAPTURAR = os.path.join(AQUI, "capturar.py")
MAPA = os.path.join(AQUI, "conversas.json")
CURSOR = os.path.join(AQUI, ".rodada-cursor")
LOGDIR = os.path.join(GOV, "40-operacao-rotinas", "tarefas", "log")


def tirar(args, flag, valor=False, varios=False):
    out, vals, i = [], [], 0
    achou = False
    while i < len(args):
        if args[i] == flag:
            achou = True
            if valor:
                if i + 1 >= len(args): sys.exit(f"{flag} precisa de valor")
                vals.append(args[i + 1]); i += 2; continue
            i += 1; continue
        out.append(args[i]); i += 1
    if valor: return (vals if varios else (vals[-1] if vals else None)), out
    return achou, out


def main(argv):
    espaco, argv = tirar(argv, "--espaco", True)
    maximo, argv = tirar(argv, "--max", True)
    falhas_max, argv = tirar(argv, "--falhas", True)
    so, argv = tirar(argv, "--so", True, varios=True)
    lista, argv = tirar(argv, "--lista", True)
    dry, argv = tirar(argv, "--dry-run")
    if argv: sys.exit(f"argumento desconhecido: {' '.join(argv)} — nada foi lido. Uso: python3 rodada.py --help")
    espaco = int(espaco or 30); maximo = int(maximo or 0); falhas_max = int(falhas_max or 2)

    mapa = json.load(io.open(MAPA, encoding="utf-8"))
    conversas = [c for c in mapa.get("conversas", []) if c.get("ativa") and c.get("chatId") and c.get("pasta")]
    if so: conversas = [c for c in conversas if c["pasta"] in so]
    if lista:
        ids = json.load(io.open(lista, encoding="utf-8"))
        ids = ids.get("chatIds", ids) if isinstance(ids, dict) else ids
        conversas = [c for c in conversas if c["chatId"] in set(ids)]
    if not conversas: sys.exit("nenhuma conversa ativa no mapa para capturar")

    # continua de onde a rodada anterior parou (quando houve --max)
    inicio = 0
    if os.path.exists(CURSOR) and not so and not lista:
        try:
            ult = io.open(CURSOR, encoding="utf-8").read().strip()
            ids = [c["chatId"] for c in conversas]
            if ult in ids: inicio = (ids.index(ult) + 1) % len(ids)
        except OSError: pass
    ordem = conversas[inicio:] + conversas[:inicio]
    if maximo: ordem = ordem[:maximo]

    print(f"rodada: {len(ordem)} conversa(s), {espaco} s entre elas" + (" (dry-run)" if dry else ""))
    for c in ordem: print(f"  - {c['relacao']}/{c['pasta']} · {c.get('nome') or c['chatId']}")
    if dry: return 0

    os.makedirs(LOGDIR, exist_ok=True)
    rel, falhas, novas, ok = [], 0, 0, 0
    t0 = datetime.now()
    for i, c in enumerate(ordem):
        nome = f"{c['relacao']}/{c['pasta']} · {c.get('nome') or c['chatId']}"
        r = subprocess.run([sys.executable, CAPTURAR, "--chat", c["chatId"]], cwd=GOV,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
        saida = (r.stdout or "") + (r.stderr or "")
        fim = next((l for l in saida.splitlines() if l.startswith("fim:")), "").strip()
        falhou = r.returncode != 0 or "falhou (" in saida or "falhas de conexão" in saida
        if falhou:
            falhas += 1
            rel.append(f"- 🔴 {nome}: falhou (código {r.returncode}) · {saida.strip().splitlines()[-1][:200] if saida.strip() else ''}")
        else:
            falhas = 0; ok += 1
            try: novas += int(fim.split("fim:")[1].split("mensagem")[0])
            except (IndexError, ValueError): pass
            rel.append(f"- ✅ {nome}: {fim or 'ok'}")
        print(rel[-1])
        io.open(CURSOR, "w", encoding="utf-8").write(c["chatId"])
        if falhas >= falhas_max:
            rel.append(f"- 🔴 {falhas} falhas seguidas: rodada parada para não derrubar o WhatsApp; o resto fica para a próxima.")
            print(rel[-1]); break
        if i < len(ordem) - 1: time.sleep(espaco)

    texto = (f"# Captura de WhatsApp — rodada {t0:%d/%m/%Y %H:%M}\n\n"
             f"{ok} conversa(s) lida(s) · {novas} mensagem(ns) nova(s) · intervalo {espaco} s · duração {(datetime.now()-t0).seconds//60} min\n\n"
             + "\n".join(rel) + "\n")
    io.open(os.path.join(LOGDIR, f"CAPTURA-{t0:%Y-%m-%d-%H%M}.md"), "w", encoding="utf-8", newline="\n").write(texto)
    print(f"fim da rodada: {ok} lida(s), {novas} nova(s)")
    return 1 if (ok == 0 and falhas) else 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try: s.reconfigure(encoding="utf-8")
        except Exception: pass
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__); sys.exit(0)
    sys.exit(main(sys.argv[1:]))
