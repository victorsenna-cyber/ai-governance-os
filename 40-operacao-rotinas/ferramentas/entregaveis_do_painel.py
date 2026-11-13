#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entregaveis_do_painel.py — o botão WhatsApp da aba Entregáveis do sistema envia o entregável pela Evolution.

O botão WhatsApp chama a Evolution e envia a mensagem por ela, com popup de confirmação antes de enviar.

  python3 entregaveis_do_painel.py             # uma rodada: põe na fila o que foi confirmado e acompanha o que já está nela
  python3 entregaveis_do_painel.py --estado    # os pedidos em aberto, sem mexer em nada
  python3 entregaveis_do_painel.py --dry-run   # mostra o que faria (destino, anexo, tamanho), sem pôr nada na fila

Caminho: popup confirmado no sistema → pedir_envio_entregavel() → public.entregaveis_envios (012-envio-entregavel.sql) →
AQUI, na VPS, a cada passada do contexto.service (chamado pelo decisoes-do-painel.py): entregaveis_envios_pendentes(token)
→ confere a task no clone (revisao/, tipo entregavel, estado pronto) → lê o PDF do clone (só sob <conta>/entregaveis/,
≤ 15 MB) → POST /fila no mensageiro, já aprovado por "operador:painel" (o clique confirmado é o ✅ dele sobre aquele texto)
→ /fila/<id>/agora (ordem dele fura a janela, nunca os tetos nem o intervalo) → marca 'na_fila'. Nas passadas seguintes:
o mensageiro enviou → a task vai para entregue/ pelo mesmo caminho do "Enviado" (acoes_do_painel.py: enviado_em,
enviado_por: painel) e o pedido fica 'enviado'; falhou ou foi recusado → 'falhou' com o erro, que a aba mostra.

O @lid do WhatsApp se resolve aqui pelo mapa da Evolution do clone (o telefone não vai ao Supabase).
Registro literal: 40-operacao-rotinas/tarefas/log/MENSAGENS-DO-PAINEL.md (o mesmo do módulo irmão mensagens_do_painel.py).
"""
import argparse, base64, datetime, importlib.util, io, json, os, re, sys, urllib.error
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
TAR = RAIZ / "40-operacao-rotinas" / "tarefas"
MAPA = AQUI / "evolution" / "mapa.json"
ANEXO_MAX = 15 * 1024 * 1024
BRT = datetime.timezone(datetime.timedelta(hours=-3))
ANEXO_OK = re.compile(r"^(clientes|parceiros)/[^/]+/(?:[^/]+/)*entregaveis/[^/]+/[^/]+\.pdf$", re.I)


def _mod(nome, arquivo):
    spec = importlib.util.spec_from_file_location(nome, AQUI / arquivo)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mdp = _mod("mensagens_do_painel", "mensagens_do_painel.py")   # rpc, token, registrar, citar e o _comum da Evolution
_comum = mdp._comum


def task_pronta(tid):
    f = TAR / "revisao" / f"{tid}.md"
    if not f.exists():
        onde = next((p for p in ("entregue", "fila", "executando", "decisao", "falhou") if (TAR / p / f"{tid}.md").exists()), None)
        return None, f"a task {tid} não está pronta em revisao/" + (f" (está em {onde}/)" if onde else " (não existe)")
    t = f.read_text(encoding="utf-8")
    if not re.search(r"^tipo:\s*entregavel\s*$", t, re.M):
        return None, f"a task {tid} não é entregável"
    if not re.search(r"^estado:\s*pronto\s*$", t, re.M):
        return None, f"a task {tid} não está com estado: pronto"
    return f, None


def resolver_destino(para):
    """@lid → telefone pelo mapa da Evolution (quando o mapa tem); o resto passa como está."""
    if not para.endswith("@lid"):
        return para
    try:
        for c in json.loads(MAPA.read_text(encoding="utf-8")).get("conversas") or []:
            if c.get("jid") == para and re.sub(r"\D", "", c.get("telefone") or ""):
                return re.sub(r"\D", "", c["telefone"])
    except Exception:  # noqa: BLE001
        pass
    return para


def ler_anexo(rel):
    rel = (rel or "").replace("\\", "/").strip()
    if not rel:
        return None, None
    if ".." in rel.split("/") or not ANEXO_OK.match(rel):
        return None, f"anexo fora de <conta>/entregaveis/ ou não é PDF: {rel}"
    p = RAIZ / rel
    if not p.exists():
        return None, f"anexo não existe no clone: {rel}"
    if p.stat().st_size > ANEXO_MAX:
        return None, f"anexo acima de 15 MB: {rel}"
    return {"base64": base64.b64encode(p.read_bytes()).decode("ascii"), "fileName": p.name, "mimetype": "application/pdf"}, None


def marcar(tk, pid, fila_id, estado, erro):
    mdp.rpc("entregaveis_envios_marcar", {"token": tk, "p_id": pid, "p_fila_id": fila_id, "p_estado": estado, "p_erro": erro})


def rodar(tk, dry=False, so_estado=False):
    """Uma rodada. Devolve (n de pedidos tratados, mudou_o_repo)."""
    env = _comum.ler_env()
    if not env.get("MENSAGEIRO_CHAVE"):
        print("entregaveis-do-painel: sem MENSAGEIRO_CHAVE; nada a fazer")
        return 0, False
    try:
        pend = mdp.rpc("entregaveis_envios_pendentes", {"token": tk}) or []
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("entregaveis-do-painel: as funções não existem no Supabase (rodar o 012-envio-entregavel.sql)")
            return 0, False
        raise
    if so_estado or not pend:
        for p in pend:
            print(f"pedido #{p['id']} · {p['estado']} · {p['task_id']} · {p.get('nome') or p['para']} · {p.get('anexo') or 'sem anexo'}")
        if not pend:
            print("entregaveis-do-painel: nenhum pedido")
        return 0, False
    n, linhas, mudou = 0, [], False
    agora = datetime.datetime.now(BRT)
    quando = agora.strftime("%Y-%m-%d %H:%M")
    with _comum.Tunel():
        for p in pend:
            pid, tid = p["id"], p["task_id"]
            if p["estado"] == "pedido":
                f, erro = task_pronta(tid)
                midia, fila_id = None, None
                if not erro:
                    midia, erro = ler_anexo(p.get("anexo"))
                para = resolver_destino(p["para"])
                if dry:
                    print(f"[dry-run] #{pid} {tid} → {p.get('nome') or para} ({p['instancia']}) · anexo "
                          f"{(midia or {}).get('fileName') or '—'} · {erro or 'ok'}")
                    continue
                if not erro:
                    corpo = {"para": para, "texto": p["texto"], "origem": "entregavel-painel", "por": "operador:painel",
                             "aprovado": True, "instancia": p["instancia"], "nome": p.get("nome"), "conta": p.get("conta")}
                    if midia:
                        corpo["midia"] = midia
                    s, r = _comum.mensageiro(env, "POST", "/fila", corpo, tempo=120)
                    if s != 201:
                        erro = f"fila HTTP {s}: {str(r)[:200]}"
                    else:
                        fila_id = r["id"]
                        s, r = _comum.mensageiro(env, "POST", f"/fila/{fila_id}/agora", {"por": "operador:painel"})
                        if s != 200:
                            erro = f"na fila ({fila_id}), mas /agora HTTP {s}: {str(r)[:160]}; sai na janela"
                marcar(tk, pid, fila_id, "na_fila" if fila_id else "falhou", erro)
                print(("🔴 " if erro else "✅ ") + f"entregável {tid}: " + (erro or f"na fila {fila_id}"))
                if fila_id:
                    linhas.append(f"## {quando} · entregável {tid} posto na fila (botão WhatsApp, confirmado no popup) · "
                                  f"pelo número {p['instancia']} · {p.get('nome') or p['para']} · `{fila_id}`"
                                  f"{' · 📎 ' + midia['fileName'] if midia else ''}\n\n{mdp.citar(p['texto'])}")
                n += 1
            elif p["estado"] == "na_fila" and p.get("fila_id"):
                s, it = _comum.mensageiro(env, "GET", f"/fila/{p['fila_id']}")
                est = (it or {}).get("estado") if s == 200 else None
                if dry:
                    print(f"[dry-run] #{pid} {tid}: fila {p['fila_id']} em {est}")
                    continue
                if est == "enviado":
                    acoes = _mod("acoes_do_painel", "acoes_do_painel.py")
                    feitos, erros = acoes.aplicar([{"id": f"envio-{pid}", "alvo": "task", "acao": "feito", "ref": tid,
                                                    "conta": p.get("conta"), "valor": None, "criado_em": p["criado_em"],
                                                    "nota": f"enviado pela Evolution, botão WhatsApp do sistema (fila {p['fila_id']})"}])
                    erro = erros.get(f"envio-{pid}")
                    marcar(tk, pid, p["fila_id"], "enviado", erro)
                    mudou = mudou or bool(feitos)
                    print(f"✅ entregável {tid} enviado ({p['fila_id']})" + (f"; task: {erro}" if erro else ""))
                    linhas.append(f"## {quando} · entregável {tid} enviado · `{p['fila_id']}` em {it.get('enviado_em')}")
                    n += 1
                elif est in ("falhou", "recusado") or s == 404:
                    erro = (it or {}).get("erro") or (f"item {est}" if est else "item sumiu da fila")
                    marcar(tk, pid, p["fila_id"], "falhou", erro)
                    print(f"🔴 entregável {tid}: {erro}")
                    n += 1
    if linhas and not dry:
        mdp.registrar(linhas)
        mudou = True
    return n, mudou


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--estado", action="store_true")
    a = ap.parse_args()
    tk = mdp.token()
    if not tk:
        print("entregaveis-do-painel: sem DECISOES_TOKEN; nada a fazer")
        return 0
    rodar(tk, dry=a.dry_run, so_estado=a.estado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
