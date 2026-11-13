#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agenda.py — a agenda do operador (Google Calendar) pelo repo, para rotinas e tasks que
não têm o conector MCP Google Calendar. Fala com a Edge Function `agenda` do Supabase (a mesma que a tela Agenda do
painel do sistema usa); a credencial do Google mora lá, nunca aqui. Criar, editar e excluir eventos vale pela tela e pelo repo.

Configuração: AGENDA_FUNCAO_URL (a URL da Edge Function `agenda`) e AGENDA_CHAVE_PUBLICA (a chave publicável do projeto).

Autenticação: o token da ponte (~/.continuum/decisoes-token.txt, ou AGENDA_TOKEN no ambiente). Hora sempre de Brasília.
Regra da casa (CLAUDE.md §6, "compromisso vai para a agenda"): hora BSB, relógio da contraparte e fonte na descrição,
aviso 30 min antes (a função já põe), e o caminho da folha em PDF da call na descrição.

  agenda.py estado
  agenda.py listar [--de AAAA-MM-DD] [--ate AAAA-MM-DD] [--json]
  agenda.py criar --titulo "Call · Cliente" --dia AAAA-MM-DD --inicio 14:00 --fim 15:00 [--descricao "..."] [--com-meet]
                  [--convidado email ...] [--avisar] [--dia-todo]
  agenda.py editar <id> [--titulo ...] [--dia ... --inicio ... --fim ...] [--descricao ...] [--com-meet] [--avisar]
  agenda.py mover <id> --dia AAAA-MM-DD          # mantém hora e duração
  agenda.py excluir <id> --sim [--avisar]
  agenda.py pdf "<caminho da folha no repo>"     # URL assinada de 10 min

Convidado só recebe e-mail com --avisar (convite é mensagem a terceiro: item 3 da lista fechada, seção de autonomia do CLAUDE.md).
"""
import argparse, json, os, sys, urllib.error, urllib.request
from pathlib import Path

FUNCAO = os.environ.get("AGENDA_FUNCAO_URL", "https://SEU-PROJETO.supabase.co/functions/v1/agenda")
CHAVE_PUBLICA = os.environ.get("AGENDA_CHAVE_PUBLICA", "")   # a chave publicável do projeto (a mesma do config.js), não é segredo
TOKEN_ARQ = Path.home() / ".continuum" / "decisoes-token.txt"


def token():
    t = os.environ.get("AGENDA_TOKEN") or (TOKEN_ARQ.read_text(encoding="utf-8").strip() if TOKEN_ARQ.exists() else "")
    if not t:
        sys.exit(f"sem token da ponte: {TOKEN_ARQ} (ou AGENDA_TOKEN)")
    return t


def chamar(corpo, tok=None):
    req = urllib.request.Request(FUNCAO, data=json.dumps(corpo).encode("utf-8"), method="POST", headers={
        "apikey": CHAVE_PUBLICA, "Content-Type": "application/json", "x-agenda-token": tok or token(),
        "User-Agent": "Continuum-agenda"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode("utf-8")).get("erro") or str(e)
        except Exception:
            msg = str(e)
        raise SystemExit(f"🔴 agenda: {msg}")


def linha(ev):
    hora = "dia todo" if ev["dia_todo"] else f'{ev["inicio"]}–{ev["fim"]}'
    extra = []
    if ev.get("link_call"):
        extra.append(f'{ev.get("tipo_call") or "call"}: {ev["link_call"]}')
    if ev.get("pdfs"):
        extra.append("PDF: " + ", ".join(p["nome"] for p in ev["pdfs"]))
    return f'{ev["dia"]} {hora:<12} {ev["titulo"]}' + (f'  ({" · ".join(extra)})' if extra else "") + f'\n{"":>11}id {ev["id"]}'


def corpo_evento(a):
    c = {}
    for k in ("titulo", "descricao", "local", "dia", "inicio", "fim"):
        v = getattr(a, k, None)
        if v is not None:
            c[k] = v
    if getattr(a, "dia_todo", False):
        c["dia_todo"] = True
    if getattr(a, "com_meet", False):
        c["com_meet"] = True
    if getattr(a, "convidado", None):
        c["convidados"] = a.convidado
    if getattr(a, "avisar", False):
        c["avisar"] = True
    return c


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description="agenda do operador pelo repo (Edge Function agenda)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("estado")
    l = sub.add_parser("listar"); l.add_argument("--de"); l.add_argument("--ate"); l.add_argument("--json", action="store_true")

    def campos(p, novo):
        p.add_argument("--titulo", required=novo); p.add_argument("--dia", required=novo)
        p.add_argument("--inicio"); p.add_argument("--fim"); p.add_argument("--descricao"); p.add_argument("--local")
        p.add_argument("--dia-todo", action="store_true"); p.add_argument("--com-meet", action="store_true")
        p.add_argument("--convidado", action="append"); p.add_argument("--avisar", action="store_true")
    c = sub.add_parser("criar"); campos(c, True)
    e = sub.add_parser("editar"); e.add_argument("id"); campos(e, False)
    m = sub.add_parser("mover"); m.add_argument("id"); m.add_argument("--dia", required=True); m.add_argument("--avisar", action="store_true")
    x = sub.add_parser("excluir"); x.add_argument("id"); x.add_argument("--sim", action="store_true"); x.add_argument("--avisar", action="store_true")
    p = sub.add_parser("pdf"); p.add_argument("caminho")
    a = ap.parse_args()

    if a.cmd == "estado":
        r = chamar({"acao": "estado"})
        print(json.dumps(r, ensure_ascii=False, indent=2)); return 0 if r.get("autorizado") else 1
    if a.cmd == "listar":
        r = chamar({"acao": "listar", "de": a.de, "ate": a.ate})
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2)); return 0
        print(f'agenda de {r.get("conta") or "?"} · {r["de"]} a {r["ate"]} · {len(r["eventos"])} evento(s)')
        for ev in r["eventos"]:
            print(linha(ev))
        return 0
    if a.cmd == "criar":
        if not a.dia_todo and not (a.inicio and a.fim):
            sys.exit("falta --inicio e --fim (HH:MM, Brasília), ou --dia-todo")
        r = chamar({"acao": "criar", **corpo_evento(a)})
    elif a.cmd == "editar":
        if a.dia and not a.dia_todo and not (a.inicio and a.fim):
            sys.exit("mudar o dia por editar pede --inicio e --fim; para só trocar o dia use: mover <id> --dia")
        r = chamar({"acao": "editar", "id": a.id, **corpo_evento(a)})
    elif a.cmd == "mover":
        r = chamar({"acao": "mover", "id": a.id, "dia": a.dia, "avisar": a.avisar})
    elif a.cmd == "excluir":
        if not a.sim:
            sys.exit("excluir pede --sim")
        r = chamar({"acao": "excluir", "id": a.id, "avisar": a.avisar})
        print("✅ excluído", r["excluido"]); return 0
    else:
        r = chamar({"acao": "pdf_url", "caminho": a.caminho})
        print(r["url"]); return 0
    print("✅", linha(r["evento"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
