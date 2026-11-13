#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mensagens_do_painel.py — a aba Mensagens do sistema: o clique do operador envia a mensagem que espera ✅ na fila do mensageiro.

A aba reúne as decisões de envio: no momento em que o operador opta, a mensagem é enviada (com um campo para ele
acrescentar alterações ou a mensagem literal, que o Claude identifica e envia pela Evolution, pelo número pessoal para
prospects ou pelo outro número para clientes).

  python3 mensagens_do_painel.py             # uma rodada: espelha a fila, aplica os cliques, espelha de novo
  python3 mensagens_do_painel.py --estado    # o que está aguardando na fila e os cliques ainda não aplicados
  python3 mensagens_do_painel.py --dry-run   # mostra o que faria (inclusive o texto que o Claude devolveria), sem aprovar nada

Caminho: fila do mensageiro (VPS) → mensagens_sincronizar(token) → public.mensagens_fila → aba Mensagens
→ escolher_mensagem() → public.mensagens_escolhas → AQUI: mensagens_pendentes(token) → campo vazio: aprova como está ·
campo com texto: o Claude lê se é a mensagem literal ou um ajuste, e devolve o texto final → /fila/<id>/editar →
/fila/<id>/aprovar (por "operador:painel") → mensagens_marcar(token). O envio sai no ritmo da fila (janela, tetos, intervalo).

Quem roda: a VPS, chamada pelo decisoes-do-painel.py a cada passada do contexto.service. O clique é o ✅ do operador (ele leu
o texto na aba): é a mesma alçada do botão do Telegram. Texto que o Claude reescreveu sai sem segundo ✅ porque o operador
mandou assim; o texto final fica no registro e na aba, ao lado do original.

Registro literal do que foi aprovado: 40-operacao-rotinas/tarefas/log/MENSAGENS-DO-PAINEL.md (camada 4 do §11.1).
"""
import argparse, datetime, io, json, os, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(AQUI / "evolution"))
import _comum  # noqa: E402

SUPABASE_URL = os.environ.get("FINANCAS_SUPABASE_URL", "https://<projeto>.supabase.co")   # o projeto Supabase do painel; no ambiente
SUPABASE_KEY = os.environ.get("FINANCAS_SUPABASE_KEY", "")   # chave publicável do painel (config.js do painel-financeiro)
REGISTRO = RAIZ / "40-operacao-rotinas" / "tarefas" / "log" / "MENSAGENS-DO-PAINEL.md"
BRT = datetime.timezone(datetime.timedelta(hours=-3))
DIAS_ESPELHO = 7
CLAUDE_DIR = (Path("/srv/ordens") if _comum.NA_VPS else AQUI / "evolution" / ".cache") / "mensagens-claude"

SISTEMA = """Você aplica, numa mensagem de WhatsApp que o operador vai mandar a um cliente ou prospect, o que ele
escreveu no campo de ajuste. Você recebe: a MENSAGEM ORIGINAL e o CAMPO.

Decida o que é o CAMPO:
- "literal": o campo é ele mesmo a mensagem a enviar (texto completo, endereçado à pessoa, que substitui a original).
  Devolva o campo exatamente como está, sem mudar uma vírgula.
- "ajuste": o campo é uma instrução sobre a original ("tira a segunda frase", "fala que é amanhã às 15h", "mais curto",
  "acrescenta o link X"). Aplique só o que ele pediu. Mantenha todo o resto: a voz dele, o tratamento, o tamanho, a ordem,
  os fatos. Não invente fato, número, data, preço ou promessa que não esteja na original ou no campo.

Regras de saída da mensagem: português do Brasil, texto puro de WhatsApp, sem aspas em volta, sem ">" de citação, sem
markdown além do *negrito* do próprio WhatsApp se já existir, sem assinatura nova, sem "com calma".

Responda SÓ com um JSON numa linha: {"tipo": "literal" | "ajuste", "texto": "<a mensagem final>"}"""


def token():
    t = os.environ.get("DECISOES_TOKEN", "").strip()
    env_vps = Path("/srv/ordens/.env")
    if not t and env_vps.exists():
        for l in env_vps.read_text(encoding="utf-8").splitlines():
            if l.strip().startswith("DECISOES_TOKEN="):
                t = l.split("=", 1)[1].strip()
    arq = Path.home() / ".continuum" / "decisoes-token.txt"
    if not t and arq.exists():
        t = arq.read_text(encoding="utf-8").strip()
    return t


def rpc(nome, corpo):
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/rpc/{nome}", method="POST", data=json.dumps(corpo).encode("utf-8"),
                                 headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8") or "null")


def agora_brt():
    return datetime.datetime.now(BRT)


def espelho(fila):
    """O que vai para a aba: o que espera ✅ e o histórico dos últimos dias. Pedido de ✅ ao comandante fica de fora."""
    corte = (agora_brt() - datetime.timedelta(days=DIAS_ESPELHO)).isoformat()
    itens = []
    for it in fila or []:
        if it.get("comandante") or it.get("origem") == "mensageiro":
            continue
        if it.get("estado") != "aguardando" and (it.get("criado") or "") < corte:
            continue
        x = {k: it.get(k) for k in ("id", "para", "nome", "conta", "instancia", "texto", "texto_original", "origem",
                                    "estado", "criado", "enviado_em", "erro")}
        if it.get("midia"):   # o entregável vai com o PDF; a aba mostra o anexo junto do texto
            x["texto"] = (x["texto"] or "") + f"\n\n📎 {it['midia'].get('fileName')}"
        itens.append(x)
    return itens


def chamar_claude(original, campo, modelo="opus"):
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)
    sistema = CLAUDE_DIR / "sistema.txt"
    if not sistema.exists() or sistema.read_text(encoding="utf-8") != SISTEMA:
        io.open(sistema, "w", encoding="utf-8", newline="\n").write(SISTEMA)
    entrada = f"MENSAGEM ORIGINAL:\n{original}\n\nCAMPO:\n{campo}\n"
    # sem --bare: ele desliga o login OAuth do Max. Fora do repo: sem CLAUDE.md nem hook.
    cmd = ["claude", "-p", "--model", modelo, "--tools", "", "--max-turns", "1", "--output-format", "json", "--strict-mcp-config",
           "--no-session-persistence", "--system-prompt-file", str(sistema)]
    try:
        r = subprocess.run(cmd, input=entrada, cwd=str(CLAUDE_DIR), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=180, shell=(os.name == "nt"))
    except subprocess.TimeoutExpired:
        return None, None, "Claude passou de 180 s"
    except FileNotFoundError:
        return None, None, "claude não está no PATH"
    try:
        res = (json.loads(r.stdout.strip()).get("result") or "").strip()
        ini, fim = res.find("{"), res.rfind("}")
        o = json.loads(res[ini:fim + 1])
        tipo, texto = o.get("tipo"), (o.get("texto") or "").strip()
        if tipo not in ("literal", "ajuste") or not texto:
            return None, None, f"resposta do Claude fora do formato: {res[:200]}"
        if tipo == "literal":
            texto = campo.strip()   # literal é literal: o campo, não a cópia dele
        return tipo, texto, None
    except Exception as e:  # noqa: BLE001
        return None, None, f"não li a resposta do Claude ({type(e).__name__}): {(r.stdout or r.stderr)[:200]}"


def registrar(linhas):
    novo = not REGISTRO.exists()
    REGISTRO.parent.mkdir(parents=True, exist_ok=True)
    with io.open(REGISTRO, "a", encoding="utf-8", newline="\n") as f:
        if novo:
            f.write("# MENSAGENS DO PAINEL — o que o operador aprovou ou descartou na aba Mensagens do sistema\n\n"
                    "> Registro vivo, escrito por `40-operacao-rotinas/ferramentas/mensagens_do_painel.py`. Texto literal do que "
                    "foi para a fila de envio, com o original quando o campo mudou algo. O envio em si sai no ritmo da fila "
                    "do mensageiro; a confirmação de entrega fica na aba e no `envios.jsonl` da VPS.\n")
        for l in linhas:
            f.write("\n" + l + "\n")


def citar(t):
    return "\n".join("    " + l for l in (t or "").splitlines()) or "    (vazio)"


def rodar(tk, dry=False, so_estado=False):
    """Uma rodada. Devolve (n de cliques aplicados, mudou_o_repo)."""
    env = _comum.ler_env()
    if not env.get("MENSAGEIRO_CHAVE"):
        print("mensagens-do-painel: sem MENSAGEIRO_CHAVE; nada a fazer")
        return 0, False
    with _comum.Tunel():
        st, fila = _comum.mensageiro(env, "GET", "/fila")
        if st != 200:
            print(f"mensagens-do-painel: fila HTTP {st}")
            return 0, False
        try:
            if not so_estado:
                rpc("mensagens_sincronizar", {"token": tk, "itens": espelho(fila)})
            pend = rpc("mensagens_pendentes", {"token": tk}) or []
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print("mensagens-do-painel: as funções não existem no Supabase (rodar o 011-mensagens.sql)")
                return 0, False
            raise
        if so_estado:
            for it in espelho(fila):
                if it["estado"] == "aguardando":
                    print(f"{it['id']}  {it.get('instancia') or 'continuum':10}  {it.get('nome') or it['para']}  {it['texto'][:70]!r}")
            for p in pend:
                print(f"clique #{p['id']}: {p['acao']} {p['fila_id']}{' · campo' if p.get('campo') else ''}{' · ' + p['instancia'] if p.get('instancia') else ''}")
            return 0, False
        por_id = {it["id"]: it for it in fila or []}
        linhas, n = [], 0
        for p in pend:
            it = por_id.get(p["fila_id"])
            tipo, final, erro = "vazio", None, None
            quando = agora_brt().strftime("%Y-%m-%d %H:%M")
            if not it or it.get("estado") != "aguardando":
                erro = f"a mensagem não estava aguardando ({(it or {}).get('estado', 'não existe')})"
            elif p["acao"] == "descartar":
                if not dry:
                    s, r = _comum.mensageiro(env, "POST", f"/fila/{it['id']}/recusar", {"por": "operador:painel", "motivo": p.get("campo") or "descartada no sistema"})
                    erro = None if s == 200 else f"recusar HTTP {s}: {r}"
                if not erro:
                    linhas.append(f"## {quando} · descartada · {it.get('nome') or it['para']} · `{it['id']}`\n\n{citar(it['texto'])}")
            else:
                final = it["texto"]
                if p.get("campo"):
                    tipo, final, erro = chamar_claude(it["texto"], p["campo"])
                if not erro:
                    mudou_inst = p.get("instancia") and p["instancia"] != (it.get("instancia") or "continuum")
                    if dry:
                        print(f"[dry-run] {it['id']}: {tipo} → {final[:200]!r}{' · número ' + p['instancia'] if mudou_inst else ''}")
                    else:
                        if final != it["texto"] or mudou_inst:
                            corpo = {"por": "operador:painel"}
                            if final != it["texto"]:
                                corpo["texto"] = final
                            if mudou_inst:
                                corpo["instancia"] = p["instancia"]
                            s, r = _comum.mensageiro(env, "POST", f"/fila/{it['id']}/editar", corpo)
                            if s != 200:
                                erro = f"editar HTTP {s}: {r}"
                        if not erro:
                            s, r = _comum.mensageiro(env, "POST", f"/fila/{it['id']}/aprovar", {"por": "operador:painel"})
                            erro = None if s == 200 else f"aprovar HTTP {s}: {r}"
                    if not erro:
                        inst = p.get("instancia") or it.get("instancia") or "continuum"
                        bloco = f"## {quando} · aprovada ({'como estava' if tipo == 'vazio' else tipo}) · pelo número {inst} · {it.get('nome') or it['para']} · `{it['id']}`\n\n"
                        if tipo != "vazio":
                            bloco += f"Campo do operador:\n\n{citar(p['campo'])}\n\nOriginal:\n\n{citar(it['texto'])}\n\nFinal:\n\n"
                        linhas.append(bloco + citar(final))
            if dry:
                if erro:
                    print(f"[dry-run] clique #{p['id']}: {erro}")
                continue
            rpc("mensagens_marcar", {"token": tk, "p_id": p["id"], "p_tipo": tipo, "p_texto_final": final, "p_erro": erro})
            print(("🔴 " if erro else "✅ ") + f"mensagem {p['fila_id']}: " + (erro or (p["acao"] if p["acao"] == "descartar" else f"aprovada ({tipo})")))
            n += 1
        if n and not dry:
            st, fila = _comum.mensageiro(env, "GET", "/fila")
            if st == 200:
                rpc("mensagens_sincronizar", {"token": tk, "itens": espelho(fila)})
        if linhas and not dry:
            registrar(linhas)
        return n, bool(linhas) and not dry


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
    tk = token()
    if not tk:
        print("mensagens-do-painel: sem DECISOES_TOKEN; nada a fazer")
        return 0
    rodar(tk, dry=a.dry_run, so_estado=a.estado)
    return 0


if __name__ == "__main__":
    sys.exit(main())
