#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
avisar-prazos.py — avisa o operador de prazo vencido e vencendo, sem ele abrir o painel.

Não tem cálculo de prazo próprio: carrega painel-projetos.py e usa montar(), tasks(), decisoes(), financeiro(),
iso(), dias() e hoje(). Quem muda a leitura de prazo muda lá, e o aviso acompanha.

O que entra:
  marco      contas ativas (mesma regra da aba Hoje: marcos + marco_prazo, se não estiver nos marcos)
  task       todas com prazo, da conta que for
  decisão    todos os cartões abertos com prazo
  a receber  todo o aberto, em conta ativa ou não
Janela: vencidos + próximos 7 dias (--janela), a mesma do painel.
Diferença de propósito em relação à aba Hoje: o painel só mostra task, decisão e a receber cujo nome casa com
uma conta ativa; aqui eles entram mesmo sem casar, porque prazo sem dono é o que mais precisa de aviso.
Prazo que o leitor não entendeu (data sem ano num cartão, data inválida num PAINEL.md) sai numa seção própria:
prazo ilegível é aviso que ninguém daria.

Uso:
  python3 -X utf8 40-operacao-rotinas/ferramentas/avisar-prazos.py                    # simulação: mostra na tela, não grava nada
  python3 -X utf8 .../avisar-prazos.py --janela 3                                     # simulação com outra janela
  python3 -X utf8 .../avisar-prazos.py --enviar --canal <canal>                       # envia e marca o que foi avisado hoje
  python3 -X utf8 .../avisar-prazos.py --enviar --canal arquivo --saida X --estado Y  # ensaio de ponta a ponta, sem envio real
  --teste-prazo "texto"   acrescenta um prazo fictício vencendo hoje (nada é escrito no repo)

Não repete no mesmo dia: a chave é tipo|conta|o_que|prazo, gravada em tarefas/log/AVISOS-PRAZOS.json só DEPOIS do
envio dar certo. Simulação nunca marca, para não silenciar o aviso real. Prazo adiado é chave nova; prazo vencido
volta a avisar no dia seguinte, de propósito.

🔴 Destinatário: só o operador. Não existe parâmetro de destinatário, e nenhum canal pode ler contato de cliente.
Canal: `telegram`, o bot do mensageiro em ferramentas/evolution/;
  exige token e pareamento (configurar.py --telegram). Sem --canal, --enviar recusa e sai 2. Canal novo entra em CANAIS,
como função (texto) -> None que levanta exceção se falhar, com o segredo vindo do ambiente, nunca do repo.
A mensagem leva nome de cliente e valor (classe C): canal público, como tópico aberto de ntfy, é vedado.

Saída: 0 ok · 1 falha no envio · 2 uso errado ou canal não escolhido.
"""
import argparse, importlib.util, io, json, os, re, sys

# como o operador aparece em `dono:` nos marcos, cartões e a receber (configurável: OPERADOR_DONO)
OPERADOR = os.environ.get("OPERADOR_DONO", "operador")

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("painel_projetos", os.path.join(AQUI, "painel-projetos.py"))
painel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(painel)

ESTADO = os.path.join(painel.TAREFAS, "log", "AVISOS-PRAZOS.json")
DIAS_DE_HISTORICO = 7
ROTULO = {"marco": "marco", "task": "task", "decisao": "decisão", "receber": "a receber", "teste": "TESTE", "gatilho": "gatilho de plano"}


# ── o que tem prazo ────────────────────────────────────────────────────────

def item(tipo, conta, o_que, prazo, dono="", duro=False):
    d = painel.dias(painel.iso(prazo)) if prazo else None
    return dict(tipo=tipo, conta=conta, o_que=o_que, prazo=prazo, dias=d, dono=dono, duro=duro)


def coletar(payload):
    out = []
    nomes_ativas = []
    for c in payload["contas"]:
        if not c["ativa"]:
            continue
        nomes_ativas.append(c["conta"])
        for m in c["marcos"]:
            out.append(item("marco", c["conta"], m["o_que"], m["prazo"], m["dono"], m["duro"]))
        if c["marco_prazo"] and not any(m["prazo"] == c["marco_prazo"] for m in c["marcos"]):
            out.append(item("marco", c["conta"], c["proximo_marco"], c["marco_prazo"], c["marco_dono"]))
    for t in painel.tasks():
        out.append(item("task", t["conta"], t["titulo"] or t["id"], t["prazo"], "", t["duro"]))
    for d in payload["decisoes"]:
        out.append(item("decisao", d["conta"], d["titulo"] or d["id"], d["prazo"], OPERADOR))
    for r in painel.financeiro()["a_receber"]:
        cp = r.get("contraparte") or "?"
        conta = next((n for n in nomes_ativas if painel.casa(n, cp)), cp)
        valor = "R$ %s" % ("%.2f" % float(r.get("valor") or 0)).replace(".", ",")
        out.append(item("receber", conta, " · ".join(x for x in (valor, r.get("descricao")) if x), r.get("vencimento"), "cliente"))
    return out


def ilegiveis(payload):
    """Prazo escrito que o leitor do painel não converteu em data."""
    out = []
    texto = painel.ler(painel.PENDENTES)
    abertas = texto.split("## Abertas", 1)[1].split("## Decididas", 1)[0] if "## Abertas" in texto else ""
    for did, cab in re.findall(r"^### (D-[\d-]+) · (.*)$", abertas, re.M):
        m = re.search(r"prazo\s*:?\s*([^·]*)", cab)
        if m and "sem prazo" not in cab.lower() and not next((d for d in payload["decisoes"] if d["id"] == did and d["prazo"]), None):
            out.append(f"{did}: \"{m.group(1).strip()[:40]}\" (sem data completa em DECISOES-PENDENTES.md)")
    for c in payload["contas"]:
        out += [f"{c['conta']}: {e}" for e in c["erros"] if "prazo" in e.lower()]
    return out


def selecionar(itens, janela):
    com_data = [i for i in itens if i["dias"] is not None and i["dias"] <= janela]
    return sorted(com_data, key=lambda i: (i["dias"], i["conta"], i["o_que"]))


def chave(i):
    return "|".join((i["tipo"], i["conta"], i["o_que"], i["prazo"] or ""))


# ── estado do dia ──────────────────────────────────────────────────────────

def ler_estado(caminho):
    try:
        return json.loads(io.open(caminho, encoding="utf-8").read())
    except (OSError, ValueError):
        return {}


def gravar_estado(caminho, estado, dia, chaves):
    estado[dia] = sorted(set(estado.get(dia, [])) | set(chaves))
    limite = (painel.hoje() - painel.dt.timedelta(days=DIAS_DE_HISTORICO)).isoformat()
    estado = {k: v for k, v in estado.items() if k >= limite}
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    io.open(caminho, "w", encoding="utf-8", newline="\n").write(json.dumps(estado, ensure_ascii=False, indent=1) + "\n")


# ── mensagem ───────────────────────────────────────────────────────────────

def quando(i):
    br = "/".join(reversed(i["prazo"].split("-")[1:]))
    if i["dias"] < 0:
        return f"{br}, há {-i['dias']}d"
    return f"{br}, hoje" if i["dias"] == 0 else f"{br}, em {i['dias']}d"


def linha(i):
    extra = " · DURO" if i["duro"] else ""
    extra += f" · {i['dono']}" if i["dono"] and i["dono"] != OPERADOR else ""
    return f"- [{quando(i)}] {i['conta']} · {ROTULO[i['tipo']]}: {i['o_que']}{extra}"


def mensagem(novos, ruins, janela, dia):
    venc = [i for i in novos if i["dias"] < 0]
    prox = [i for i in novos if i["dias"] >= 0]
    br = "/".join(reversed(dia.split("-")))
    partes = [f"Prazos em {br}: {len(venc)} vencido(s), {len(prox)} em até {janela} dia(s)."]
    if venc:
        partes += ["", "VENCIDOS"] + [linha(i) for i in venc]
    if prox:
        partes += ["", "VENCENDO"] + [linha(i) for i in prox]
    if ruins:
        partes += ["", "PRAZO ILEGÍVEL (não dá para calcular)"] + ["- " + r for r in ruins]
    return "\n".join(partes)


# ── canais ─────────────────────────────────────────────────────────────────

def canal_arquivo(texto, saida):
    """Duplo de teste: acrescenta num arquivo. Não chega a ninguém; existe para ensaiar envio e não repetição."""
    with io.open(saida, "a", encoding="utf-8", newline="\n") as f:
        f.write(texto + "\n\n")


def canal_telegram(texto):
    """O Telegram do operador, pelo bot do mensageiro (ferramentas/evolution/): POST /avisar por túnel SSH.
    Exige token e pareamento (configurar.py --telegram); sem eles o mensageiro responde 409 e nada é marcado."""
    import sys as _sys
    _sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "evolution"))
    from _comum import Tunel, ler_env, mensageiro  # noqa: E402
    env = ler_env()
    if not env:
        raise RuntimeError("/srv/evolution/.env não existe (python3 ferramentas/evolution/publicar.py)")
    with Tunel():
        st, r = mensageiro(env, "POST", "/avisar", {"texto": texto})
    if st != 200:
        raise RuntimeError(f"mensageiro HTTP {st}: {r}")


CANAIS = {"telegram": canal_telegram}


def main():
    ap = argparse.ArgumentParser(description="Avisa o operador de prazo vencido e vencendo.")
    ap.add_argument("--janela", type=int, default=7, help="dias à frente (padrão 7, igual ao painel)")
    ap.add_argument("--enviar", action="store_true", help="envia de verdade; sem isto é simulação")
    ap.add_argument("--canal", help="canal de envio; 'arquivo' é o ensaio, exige --saida e --estado")
    ap.add_argument("--saida", help="arquivo do canal 'arquivo'")
    ap.add_argument("--estado", help="estado alternativo (padrão: tarefas/log/AVISOS-PRAZOS.json)")
    ap.add_argument("--teste-prazo", help="acrescenta um prazo fictício vencendo hoje")
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    ensaio = a.canal == "arquivo"
    if a.enviar:
        if not a.canal:
            print("🔴 --enviar sem --canal. O canal do operador é 'telegram': --canal telegram.", file=sys.stderr)
            return 2
        if ensaio and not (a.saida and a.estado):
            print("🔴 o canal 'arquivo' exige --saida e --estado próprios, para o ensaio não silenciar o aviso real.", file=sys.stderr)
            return 2
        if not ensaio and a.canal not in CANAIS:
            print(f"🔴 canal '{a.canal}' não existe. Disponíveis: {', '.join(sorted(CANAIS)) or 'nenhum real ainda'}.", file=sys.stderr)
            return 2
    if a.teste_prazo and a.enviar and not ensaio:
        print("🔴 --teste-prazo em canal real exige decisão explícita; não está habilitado.", file=sys.stderr)
        return 2

    payload = painel.montar()
    dia = painel.hoje().isoformat()
    itens = coletar(payload)
    if a.teste_prazo:
        itens.append(item("teste", "casa", a.teste_prazo, dia))
    caminho = a.estado or ESTADO
    estado = ler_estado(caminho)
    ja = set(estado.get(dia, []))
    todos = selecionar(itens, a.janela)
    novos = [i for i in todos if chave(i) not in ja]
    ruins = ilegiveis(payload)
    print(f"{len(todos)} prazo(s) na janela · {len(todos) - len(novos)} já avisado(s) hoje · {len(novos)} novo(s)")
    if not novos:
        print("nada novo a avisar")
        return 0
    texto = mensagem(novos, ruins, a.janela, dia)

    if not a.enviar:
        print("── SIMULAÇÃO: nada enviado, nada marcado ──")
        print(texto)
        return 0
    try:
        if ensaio:
            canal_arquivo(texto, a.saida)
        else:
            CANAIS[a.canal](texto)
    except Exception as e:  # noqa: BLE001  — falha de canal não marca nada, e a próxima rodada tenta de novo
        print(f"🔴 envio falhou por '{a.canal}': {e}. Nada marcado como avisado.", file=sys.stderr)
        return 1
    gravar_estado(caminho, estado, dia, [chave(i) for i in novos])
    print(f"✅ {len(novos)} prazo(s) avisado(s) por '{a.canal}'" + (" (ensaio: não chegou a ninguém)" if ensaio else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
