#!/usr/bin/env python3
"""Cliente N1 do FreeLLMAPI (so biblioteca padrao).

REGUA: so dado de classe P (publico) ou I (interno sem cliente) passa por aqui.
Dado C (cliente) ou S (sensivel) NUNCA. O CLI recusa C e S (saida 2).

Uso:
  python3 n1_cliente.py --saude
  python3 n1_cliente.py --classe P --perfil auto:continuum-rapido "pergunta"
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

CLASSES_PERMITIDAS = ("P", "I")
CLASSES_PROIBIDAS = ("C", "S")


class FreeLLMAPIErro(RuntimeError):
    pass


def _http(metodo, url, chave=None, corpo=None, timeout=120):
    cab = {"Content-Type": "application/json"}
    if chave:
        cab["Authorization"] = "Bearer " + chave
    dados = json.dumps(corpo).encode("utf-8") if corpo is not None else None
    req = urllib.request.Request(url, data=dados, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
        raise FreeLLMAPIErro(
            "servidor FreeLLMAPI fora do ar em %s (%s). Suba com: "
            "cd <pasta do freellmapi> && npm run dev -w server" % (url, e)
        )


def saude(url=None):
    """True se o servidor responde (/livez). Lanca FreeLLMAPIErro se esta fora."""
    url = (url or os.environ.get("FREELLMAPI_URL", "http://localhost:3001")).rstrip("/")
    status, corpo = _http("GET", url + "/livez", timeout=5)
    if status != 200:
        raise FreeLLMAPIErro("/livez devolveu HTTP %s: %s" % (status, corpo[:200]))
    return True


def perguntar(prompt, sistema=None, perfil="auto:continuum-rapido",
              url=os.environ.get("FREELLMAPI_URL", "http://localhost:3001"),
              chave=os.environ.get("FREELLMAPI_KEY")):
    """Pergunta via /v1/chat/completions (compativel OpenAI) e devolve o texto.

    Lanca FreeLLMAPIErro se o servidor esta fora, sem chave unificada, sem
    provedor com chave cadastrada, ou se o perfil nao existe.
    """
    if not chave:
        raise FreeLLMAPIErro("sem chave unificada: defina FREELLMAPI_KEY (freellmapi-..., painel > Keys)")
    msgs = []
    if sistema:
        msgs.append({"role": "system", "content": sistema})
    msgs.append({"role": "user", "content": prompt})
    status, corpo = _http("POST", url.rstrip("/") + "/v1/chat/completions", chave,
                          {"model": perfil, "messages": msgs})
    try:
        j = json.loads(corpo)
    except ValueError:
        raise FreeLLMAPIErro("resposta nao-JSON (HTTP %s): %s" % (status, corpo[:200]))
    if status != 200:
        err = j.get("error", {}) if isinstance(j, dict) else {}
        if not isinstance(err, dict):
            err = {"message": str(err)}
        msg = err.get("message", corpo[:300])
        if status == 401:
            raise FreeLLMAPIErro("chave unificada invalida (HTTP 401): " + msg)
        if status == 503 or err.get("code") == "no_providers_configured":
            raise FreeLLMAPIErro("sem provedor com chave cadastrada (HTTP %s): %s" % (status, msg))
        raise FreeLLMAPIErro("HTTP %s: %s" % (status, msg))
    try:
        return j["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise FreeLLMAPIErro("resposta sem choices[0].message.content: " + corpo[:300])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cliente N1 FreeLLMAPI (so classe P ou I).")
    ap.add_argument("pergunta", nargs="?", help="texto da pergunta")
    ap.add_argument("--classe", help="classe do dado: P, I (permitidas); C, S sao recusadas")
    ap.add_argument("--perfil", default="auto:continuum-rapido")
    ap.add_argument("--sistema", default=None)
    ap.add_argument("--saude", action="store_true", help="so testa se o servidor responde")
    a = ap.parse_args(argv)

    if a.saude:
        try:
            saude()
        except FreeLLMAPIErro as e:
            print("ERRO: %s" % e, file=sys.stderr)
            return 1
        print("ok: servidor responde")
        return 0

    if not a.classe:
        ap.error("--classe e obrigatorio (P ou I)")
    classe = a.classe.strip().upper()
    if classe in CLASSES_PROIBIDAS:
        print("RECUSADO: dado de classe %s (cliente/sensivel) nunca passa pelo FreeLLMAPI. "
              "So P (publico) ou I (interno sem cliente)." % classe, file=sys.stderr)
        return 2
    if classe not in CLASSES_PERMITIDAS:
        print("RECUSADO: classe '%s' desconhecida; use P ou I." % a.classe, file=sys.stderr)
        return 2
    if not a.pergunta:
        ap.error("falta a pergunta")
    try:
        print(perguntar(a.pergunta, a.sistema, a.perfil))
    except FreeLLMAPIErro as e:
        print("ERRO: %s" % e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
