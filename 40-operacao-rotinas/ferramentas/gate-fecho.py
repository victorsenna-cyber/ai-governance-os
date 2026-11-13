#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate-fecho.py — o passe P5 do COMPLIANCE-DE-OUTPUT ("fecho sem oferta"), mecanizado.

Tipo: ferramenta · gate (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Plano: 40-operacao-rotinas/PLANO-AUTONOMIA.md · regra: CLAUDE.md §5.2

Dois hooks do Claude Code (.claude/settings.json), mesmo script:
  Stop          a última resposta da sessão termina OFERECENDO um ato ("faço agora?", "quer que eu…?")
                sem citar item da lista fechada → bloqueia o fecho UMA vez, com a razão. O Claude faz o ato
                (ou diz qual item da lista o segura) e fecha de novo.
  SubagentStop  o relatório do subagente endereça o operador ("decisão para o operador", "cabe ao operador")
                → devolve ao subagente para reclassificar como achado + recomendação + classe (R ou L1–L7).

  Stop          a resposta ADIA, segura ou desvia um ato ("sai às 06h", "fora da janela", "fica na fila", "contraria a
                sua regra") sem citar item 1–4 da lista fechada → bloqueia UMA vez: é o nível 1 das decisões do operador
                (CLAUDE.md §5.2, três níveis): o pedido literal dele que esbarra numa regra já é a decisão de iterá-la.
Uma vez só: com stop_hook_active, passa sempre (sem laço). Quando passa, não escreve nada (custo de contexto zero).
Cada bloqueio vira uma linha em 40-operacao-rotinas/tokens/GATE-FECHO.jsonl, lida pela medição semanal.

Teste sem hook:
  python3 -X utf8 gate-fecho.py --testar "texto da resposta"        → diz se bloquearia no Stop
  python3 -X utf8 gate-fecho.py --testar-sub "texto do relatório"   → idem no SubagentStop
  python3 -X utf8 gate-fecho.py --testar-adiou "texto"              → diz se o Stop-N1 bloquearia
  python3 -X utf8 gate-fecho.py --testar-pediu-tempo "fala dele"    → diz se a fala pede o adiamento (P3)
"""
import io, json, os, re, sys, time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(RAIZ, "40-operacao-rotinas", "tokens", "GATE-FECHO.jsonl")

OFERTA = re.compile(
    r"(fa[çc]o (agora|isso|j[áa]|eu)\b[^.\n]{0,40}\?|quer que eu\b|querem que eu\b|deseja que eu\b|posso (fazer|corrigir|seguir|aplicar|criar|mover|rodar|ajustar|levar|incluir|atualizar|consertar)\b[^.\n]{0,80}\?"
    r"|prossigo\?|sigo\?|sigo com\b[^.\n]{0,60}\?|aplico\?|corrijo\?|fa[çc]o\?|manda(r)? ver\?|bora\?|topa\?|se quiser,? (eu )?(fa[çc]o|corrijo|sigo|aplico|levo|crio)"
    r"|me (avisa|diz|fala) se (quer|quiser|devo)|(uma |a |essa )?decis[ãa]o [ée] (sua|tua|do operador)\b|devo (seguir|fazer|aplicar|corrigir)\b[^.\n]{0,60}\?|quer[^.\n]{0,30}que (eu )?(fa[çc]a|corrija|siga|aplique)|fa[çc]o agora\b)",
    re.I)
LISTA = re.compile(
    r"\bL[1-7]\b|lista fechada|item [1-7]\b|dinheiro|pre[çc]o|desconto|cobran|pagamento|contrato|cl[áa]usula|enviar|envio|mensagem (a|ao|à|para)|publica|"
    r"apagar de vez|tirar do ar|\bVPS\b|deploy|infraestrutura|agendador|plugin|\bMCP\b|componente externo|regra escrita|diverg", re.I)
ADIOU = re.compile(
    r"fora da janela|esperando a janela|sai(r[áa])? (às|as) \d|fica(r[áa]|m)? na fila|fica(m)? para amanh[ãa]|"
    r"contraria (a )?(sua )?regra|contra a (sua )?regra|"
    # "ficou registrado, mas não foi feito nesta tarefa" (caso medido nos transcritos,
    # pedido "investiga e corrige a falha na vps") adiava o ato sem trava nenhuma
    r"n[ãa]o (foi )?feito nesta (tarefa|sess[ãa]o)|fica(r[áa])? para (outra|a pr[óo]xima) (tarefa|sess[ãa]o|rodada)", re.I)
TRAVA_LEGITIMA = re.compile(r"\bL[1-4]\b|item [1-4]\b|dinheiro|pre[çc]o|pagamento|cobran|contrato|cl[áa]usula|apagar de vez|tirar do ar", re.I)
# P3: o adiamento que o operador PEDIU não é trava nossa. Se a última fala humana
# pede tempo ("na quarta", "amanhã", "às 04h02", "de madrugada", "assim que ele tiver fôlego"), o Stop-N1 passa.
# "depois" sozinho ficou de fora de propósito: é palavra comum demais e desligaria o gate.
PEDIU_TEMPO = re.compile(
    r"\b(quarta|quinta|sexta|s[áa]bado|domingo|segunda|ter[çc]a)(-feira)?\b|\bamanh[ãa]\b|semana que vem|mais tarde|"
    r"de madrugada|quando (ele|tiver|der|puder)|assim que|[àa]s \d{1,2}( ?h|:)\d{0,2}|\bdia \d{1,2}\b|agend", re.I)
PARA_OPERADOR = re.compile(
    r"decis[ãa]o (para|do|pro) (o )?o operador|cabe ao operador|o operador (decide|precisa decidir|deve decidir|escolhe)|"
    r"pergunt(ar|e|a) ao operador|para o operador (decidir|escolher|aprovar)|aguardando (a )?decis[ãa]o do operador", re.I)


def ultimo_texto(caminho):
    """Texto da última mensagem do assistente num transcrito .jsonl do Claude Code."""
    if not caminho or not os.path.exists(caminho):
        return ""
    ult = ""
    with io.open(caminho, encoding="utf-8", errors="replace") as f:
        for linha in f:
            if '"assistant"' not in linha:
                continue
            try:
                ev = json.loads(linha)
            except ValueError:
                continue
            msg = ev.get("message") or {}
            if ev.get("type") != "assistant" and msg.get("role") != "assistant":
                continue
            partes = msg.get("content")
            if isinstance(partes, str):
                t = partes
            else:
                t = "\n".join(p.get("text", "") for p in (partes or []) if isinstance(p, dict) and p.get("type") == "text")
            if t.strip():
                ult = t
    return ult


def ultima_humana(caminho):
    """Última fala humana do transcrito (sem tool_result, sem aviso do sistema, sem retorno de hook)."""
    ult = ""
    if not caminho or not os.path.exists(caminho):
        return ult
    with io.open(caminho, encoding="utf-8", errors="replace") as f:
        for linha in f:
            if '"user"' not in linha:
                continue
            try:
                ev = json.loads(linha)
            except ValueError:
                continue
            if ev.get("type") != "user" or ev.get("isSidechain"):
                continue
            c = (ev.get("message") or {}).get("content")
            t = c if isinstance(c, str) else "\n".join(
                p.get("text", "") for p in (c or []) if isinstance(p, dict) and p.get("type") == "text")
            if t.strip() and not t.lstrip().startswith(("<", "Stop hook feedback", "[Image", "[Subagent", "[Usage")):
                ult = t
    return ult


def julgar_fecho(texto):
    cauda = texto.strip()[-600:]
    m = OFERTA.search(cauda)
    if not m:
        return None
    janela = cauda[max(0, m.start() - 300): m.end() + 100]
    if LISTA.search(janela):
        return None
    return m.group(0)


def julgar_adiou(texto):
    """Nível 1: a resposta segurou ou adiou o ato pedido por regra mecânica, sem trava da lista 1–4."""
    m = ADIOU.search(texto or "")
    if not m:
        return None
    janela = texto[max(0, m.start() - 300): m.end() + 200]
    return None if TRAVA_LEGITIMA.search(janela) else m.group(0)


def julgar_sub(texto):
    m = PARA_OPERADOR.search(texto or "")
    return m.group(0) if m else None


def registrar(evento, trecho, sessao):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with io.open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"data": time.strftime("%Y-%m-%d %H:%M"), "evento": evento,
                                "trecho": trecho[:120], "sessao": sessao}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def bloquear(razao):
    print(json.dumps({"decision": "block", "reason": razao}, ensure_ascii=False))


def main():
    a = sys.argv[1:]
    if a[:1] in (["-h"], ["--help"]):
        print(__doc__); return
    if a[:1] == ["--testar"]:
        r = julgar_fecho(" ".join(a[1:])); print("BLOQUEIA:" if r else "passa", r or ""); return
    if a[:1] == ["--testar-adiou"]:
        r = julgar_adiou(" ".join(a[1:])); print("BLOQUEIA:" if r else "passa", r or ""); return
    if a[:1] == ["--testar-pediu-tempo"]:
        r = PEDIU_TEMPO.search(" ".join(a[1:])); print("ADIAMENTO DELE:" if r else "não pede tempo", r.group(0) if r else ""); return
    if a[:1] == ["--testar-sub"]:
        r = julgar_sub(" ".join(a[1:])); print("DEVOLVE:" if r else "passa", r or ""); return
    try:
        ev = json.load(sys.stdin)
    except Exception:
        return
    if ev.get("stop_hook_active"):
        return
    nome = ev.get("hook_event_name", "")
    sessao = ev.get("session_id", "")
    if nome == "SubagentStop":
        texto = ev.get("last_assistant_message") or ultimo_texto(ev.get("agent_transcript_path"))
        r = julgar_sub(texto)
        if r:
            registrar("SubagentStop", r, sessao)
            bloquear(f"Gate de fecho (CLAUDE.md §5.2): o relatório endereça o operador (\"{r}\"). Subagente devolve à sessão "
                     "principal, nunca ao operador. Reescreva o fecho do relatório: para cada ponto, o achado (caminho e linha), "
                     "a recomendação e a classe do ato: R (reversível no repo, a sessão principal faz) ou L1–L7 (item da lista "
                     "fechada: dinheiro, contrato, mensagem a terceiro/publicação, apagar de vez/tirar do ar, infraestrutura "
                     "compartilhada, componente externo, divergir de regra escrita).")
        return
    texto = ev.get("last_assistant_message") or ultimo_texto(ev.get("transcript_path"))
    r = julgar_adiou(texto)
    if r and PEDIU_TEMPO.search(ultima_humana(ev.get("transcript_path"))):
        registrar("Stop-N1-passou", r + " (adiamento pedido por ele)", sessao)
        r = None
    if r:
        registrar("Stop-N1", r, sessao)
        bloquear(f"Gate de fecho (CLAUDE.md §5.2, decisões em três níveis): a resposta segura ou adia um ato (\"{r}\") por "
                 "regra ou mecanismo nosso. Se foi o operador quem pediu o ato, o pedido já é a decisão de iterar a regra (nível 1): "
                 "execute agora, escreva a exceção onde a regra age (código ou política), registre e diga no fecho. Só segura "
                 "item 1 a 4 da lista fechada (dinheiro, contrato, mensagem a terceiro, apagar de vez) sem a palavra dele sobre "
                 "o ato; nesse caso, diga qual item. Se ninguém pediu o ato (rotina automática), reescreva o fecho dizendo isso.")
        return
    r = julgar_fecho(texto)
    if r:
        registrar("Stop", r, sessao)
        bloquear(f"Gate de fecho (CLAUDE.md §5.2): a resposta termina oferecendo um ato (\"{r}\") sem citar item da lista "
                 "fechada. Ato reversível dentro da casa se faz e se avisa: faça-o agora, teste, registre em uma linha e "
                 "reescreva o fecho dizendo o que foi feito. Se o ato é da lista (L1–L7: dinheiro, contrato, mensagem a "
                 "terceiro/publicação, apagar de vez/tirar do ar, infraestrutura compartilhada, componente externo, divergir "
                 "de regra escrita), diga qual item o segura, com a recomendação. Pergunta de FATO que falta continua valendo.")


if __name__ == "__main__":
    main()
