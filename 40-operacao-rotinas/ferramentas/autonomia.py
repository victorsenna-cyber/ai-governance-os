# -*- coding: utf-8 -*-
"""
autonomia.py — escada de autonomia por tipo de decisão (A0–A3), a partir do histórico
recomendação × escolha do {{OPERADOR}} (T3 §12.1).

Histórico: 40-operacao-rotinas/tarefas/log/DECISOES.jsonl, uma linha por decisão:
  {"id": "D-...", "tipo": "preco", "recomendado": "A", "escolhido": "A",
   "data": "AAAA-MM-DD", "hora": "HH:MM", "veto": false}

Regras (fixas até o {{OPERADOR}} mudar):
  A0  tipo novo, sem histórico (o {{OPERADOR}} decide sem recomendação)
  A1  o sistema recomenda e o {{OPERADOR}} escolhe (padrão de entrada)
  A2  o sistema decide e avisa, janela de veto de 24 h: acerto >= 90% em >= 10 decisões do tipo
  A3  o sistema decide e registra: acerto >= 95% em >= 20 decisões em A2, sem veto
  Veto ou reversão num tipo em A2/A3 devolve o tipo a A1 até refazer a contagem.
  Teto proposto: dinheiro, contrato e mensagem a cliente começam em A1 e só sobem com
  "aprovado" literal, tipo a tipo (lista TETO abaixo).

  python3 autonomia.py                 → tabela por tipo
  python3 autonomia.py --tipo X        → nível de um tipo (imprime A0..A3)
  python3 autonomia.py --registrar D-001 tipo A B [--veto]
"""
import argparse, datetime, io, json, os, sys
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HIST = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas", "log", "DECISOES.jsonl")
TETO = {"dinheiro", "preco", "desconto", "cobranca", "contrato", "clausula", "mensagem_cliente", "publicacao", "remuneracao"}


def ler():
    if not os.path.exists(HIST):
        return []
    out = []
    for l in io.open(HIST, encoding="utf-8"):
        try:
            out.append(json.loads(l))
        except ValueError:
            pass
    return out


def nivel(tipo, hist=None):
    hist = [h for h in (hist if hist is not None else ler()) if h.get("tipo") == tipo]
    if not hist:
        return "A0", 0, 0.0
    # reinicia a contagem depois do último veto/reversão
    ult_veto = max((i for i, h in enumerate(hist) if h.get("veto")), default=-1)
    janela = hist[ult_veto + 1:]
    n = len(janela)
    acertos = sum(1 for h in janela if h.get("recomendado") and h.get("recomendado") == h.get("escolhido"))
    taxa = acertos / n if n else 0.0
    if tipo in TETO and not any(h.get("liberado_pelo_operador") for h in hist):
        return ("A1" if n else "A0"), n, taxa
    if n >= 20 and taxa >= 0.95:
        return "A3", n, taxa
    if n >= 10 and taxa >= 0.90:
        return "A2", n, taxa
    return ("A1" if n else "A0"), n, taxa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tipo")
    ap.add_argument("--registrar", nargs=4, metavar=("ID", "TIPO", "RECOMENDADO", "ESCOLHIDO"))
    ap.add_argument("--veto", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.registrar:
        os.makedirs(os.path.dirname(HIST), exist_ok=True)
        i, t, r, e = a.registrar
        reg = {"id": i, "tipo": t, "recomendado": r, "escolhido": e, "veto": a.veto,
               "data": datetime.date.today().isoformat(), "hora": datetime.datetime.now().strftime("%H:%M")}
        io.open(HIST, "a", encoding="utf-8").write(json.dumps(reg, ensure_ascii=False) + "\n")
        print("registrado:", reg); return
    hist = ler()
    if a.tipo:
        print(nivel(a.tipo, hist)[0]); return
    tipos = sorted({h.get("tipo") for h in hist})
    print("| tipo | nível | decisões na janela | acerto |\n|---|---|---:|---:|")
    for t in tipos:
        n, c, taxa = nivel(t, hist)
        print(f"| {t} | {n} | {c} | {taxa:.0%} |")
    if not tipos:
        print("| (sem histórico) | A0 | 0 | — |")


if __name__ == "__main__":
    main()
