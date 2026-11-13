#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate-delegacao.py — a regra "delegação por custo" (CLAUDE.md §8), mecanizada.

Tipo: ferramenta · gate (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Por que existe: o modelo caro lia capturas e rodava grep ele mesmo, em vez de delegar o trabalho mecânico ao subagente
barato. A regra existia no kernel e em memória; sem mecanismo, não pegava.

Dois hooks do Claude Code (.claude/settings.json), mesmo script:
  UserPromptSubmit  zera o contador do turno.
  PreToolUse        (Read | Grep | Glob | Bash) na sessão do modelo caro (Opus, Fable):
     1. alvo de varredura (captura de WhatsApp, transcrito, .jsonl, capturar/puxar/rodada, verificar-propagacao,
        transcrever-audio) → NEGA na primeira chamada: é do Haiku, sempre.
     2. leitura mecânica genérica (Read, Grep, Glob, Bash de leitura: cat, grep, ls, find, head, sed -n, git log…)
        → a partir da LIMITE+1ª no mesmo turno, NEGA: o resto da leitura vai para subagente.
  Passa sempre: subagente (agent_id no payload ou transcrito de subagente), modelo que não é Opus/Fable,
  sessão na nuvem (CLAUDE_CODE_REMOTE), GATE_DELEGACAO=0.
Cada bloqueio vira uma linha em 40-operacao-rotinas/tokens/GATE-DELEGACAO.jsonl (medição semanal).
Quando passa, não escreve nada (custo de contexto zero).

Teste sem hook:
  python3 -X utf8 gate-delegacao.py --testar Read "clientes/X/01 - contexto/OpenWA/texto/a.md"
  python3 -X utf8 gate-delegacao.py --testar Bash "grep -n call STATUS.md" --n 6
"""
import io, json, os, re, sys, tempfile, time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = os.path.join(RAIZ, "40-operacao-rotinas", "tokens", "GATE-DELEGACAO.jsonl")
LIMITE = int(os.environ.get("GATE_DELEGACAO_LIMITE", "5") or 5)  # leituras mecânicas genéricas livres por turno no modelo caro; o worker N4/N5 do despachante, onde a task inteira é um turno, recebe 40. Captura, transcrito e .jsonl seguem barrados na 1ª

VARREDURA = re.compile(
    # captura mora em 01 - contexto/ (OpenWA, Evolution, WhatsApp); a pasta de ferramenta ferramentas/evolution/ é código,
    # não captura (falso positivo: barrou a leitura de um compose.yml)
    r"01 - contexto|_transcripts|TRANSCRIPT-|\.jsonl\b|sessoes-claude", re.I)
# Ferramenta de captura e de conferência: só conta quando é EXECUTADA, não quando o nome aparece no texto que um
# heredoc grava (falso positivo: barrou um script que anexava ao PORTE uma linha citando o verificar-propagacao).
FERRAMENTA_VARREDURA = re.compile(
    r"capturar\.py|capturar\.bat|puxar\.py|rodada\.py|transcrever-audio|verificar-propagacao\.py|medir-(tokens|perguntas|voz)",
    re.I)
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n.*?\n[ \t]*\2[ \t]*(?=\n|$)", re.S)
BASH_LEITURA = re.compile(
    r"^\s*(cd [^&;]+(&&|;)\s*)*(cat|grep|rg|ls|find|head|tail|sed -n|awk|wc|git (log|diff|show|status|grep)|for |"
    r"echo|stat|file|tree|less|more|sort|uniq|cut)\b", re.I)
MSG_VARREDURA = ("Gate de delegação (CLAUDE.md §8): varredura de captura, transcrito, .jsonl ou ferramenta de "
                 "leitura/conferência é do Haiku, sempre. Abra o subagente varredor (Agent, subagent_type: varredor) com o alvo, "
                 "o que procurar e o formato do achado (caminho, linha, citação literal). Você decide sobre o achado.")
MSG_LIMITE = ("Gate de delegação (CLAUDE.md §8): {n} leituras mecânicas neste turno. O resto da leitura e da busca "
              "vai para o subagente varredor (Agent, subagent_type: varredor; sonnet se pedir julgamento leve), com o alvo e o formato do achado. "
              "Fica no Opus: decisão, estrutura, copy, diagnóstico e o registro.")


def estado_path(sessao):
    return os.path.join(tempfile.gettempdir(), f"gate-delegacao-{re.sub(r'[^A-Za-z0-9_-]', '', sessao or 'x')}.json")


def ler_estado(sessao):
    try:
        with io.open(estado_path(sessao), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"n": 0}


def gravar_estado(sessao, est):
    try:
        with io.open(estado_path(sessao), "w", encoding="utf-8") as f:
            json.dump(est, f)
    except Exception:
        pass


def modelo_da_sessao(transcrito):
    """Modelo da última resposta do assistente no transcrito (lê só o fim do arquivo)."""
    if not transcrito or not os.path.exists(transcrito):
        return ""
    try:
        with open(transcrito, "rb") as f:
            f.seek(0, 2)
            tam = f.tell()
            f.seek(max(0, tam - 400_000))
            cauda = f.read().decode("utf-8", errors="replace")
    except Exception:
        return ""
    achados = re.findall(r'"model"\s*:\s*"([^"]+)"', cauda)
    return achados[-1] if achados else ""


def alvo(tool, entrada):
    if tool == "Bash":
        return entrada.get("command", "") or ""
    partes = [str(entrada.get(k, "")) for k in ("file_path", "path", "pattern", "glob")]
    return " ".join(p for p in partes if p)


def classificar(tool, entrada):
    """'varredura' | 'leitura' | None"""
    a = alvo(tool, entrada)
    if tool == "Bash" and "gate-delegacao.py" in a:  # o teste do próprio gate cita os alvos como texto
        return None
    if tool in ("Read", "Grep", "Glob", "Bash") and VARREDURA.search(a):
        return "varredura"
    if tool in ("Read", "Grep", "Glob", "Bash") and FERRAMENTA_VARREDURA.search(HEREDOC.sub("<<texto", a) if tool == "Bash" else a):
        return "varredura"
    if tool in ("Read", "Grep", "Glob"):
        return "leitura"
    if tool == "Bash" and BASH_LEITURA.search(a):
        return "leitura"
    return None


def isento(payload):
    if os.environ.get("GATE_DELEGACAO") == "0" or os.environ.get("CLAUDE_CODE_REMOTE"):
        return True
    if payload.get("agent_id") or payload.get("agent_type"):
        return True
    tr = payload.get("transcript_path", "") or ""
    if re.search(r"subagent|agent-[0-9a-f]", tr, re.I):
        return True
    modelo = modelo_da_sessao(tr).lower()
    if modelo and not re.search(r"opus|fable", modelo):
        return True
    return False


def negar(motivo):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": motivo}}, ensure_ascii=False))


def registrar(payload, tipo, n):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with io.open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "sessao": payload.get("session_id", ""),
                                "tipo": tipo, "n": n, "tool": payload.get("tool_name", ""),
                                "alvo": alvo(payload.get("tool_name", ""), payload.get("tool_input", {}) or {})[:200]},
                               ensure_ascii=False) + "\n")
    except Exception:
        pass


def decidir(payload, est):
    """Devolve (motivo_de_negar | None, estado_novo)."""
    tool = payload.get("tool_name", "")
    tipo = classificar(tool, payload.get("tool_input", {}) or {})
    if tipo is None:
        return None, est
    if tipo == "varredura":
        return MSG_VARREDURA, est
    est = dict(est, n=est.get("n", 0) + 1)
    if est["n"] > LIMITE:
        return MSG_LIMITE.format(n=est["n"] - 1), est
    return None, est


def main():
    if "--testar" in sys.argv:
        i = sys.argv.index("--testar")
        tool, a = sys.argv[i + 1], sys.argv[i + 2]
        n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 0
        chave = "command" if tool == "Bash" else "file_path"
        motivo, _ = decidir({"tool_name": tool, "tool_input": {chave: a}}, {"n": n})
        print("NEGA: " + motivo if motivo else "passa")
        return
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    evento = payload.get("hook_event_name", "")
    sessao = payload.get("session_id", "")
    if evento == "UserPromptSubmit":
        gravar_estado(sessao, {"n": 0})
        return
    if evento != "PreToolUse" or isento(payload):
        return
    motivo, est = decidir(payload, ler_estado(sessao))
    gravar_estado(sessao, est)
    if motivo:
        registrar(payload, "varredura" if motivo == MSG_VARREDURA else "limite", est.get("n", 0))
        negar(motivo)


if __name__ == "__main__":
    main()
