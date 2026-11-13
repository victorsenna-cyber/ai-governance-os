#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gatilho_plano.py — avisa quando a receita recorrente contratada cruza o gatilho do plano maior da assinatura
(plano em 60-planos/agente-do-cliente-valor-e-orcamento/PLANO-VALOR-E-ORCAMENTO.md §4).

Regra do operador: só sobe o plano da assinatura quando entrarem mais clientes e a receita recorrente comportar o custo.

Não tem cálculo de receita próprio: lê payload["receita"] do painel-projetos.py (comercial_regras.receita()).
A régua mora em 40-operacao-rotinas/tokens/GATILHO-PLANO.json (alvo, mínimo por contrato, quantos contratos, decidido).
Cruzou = recorrente contratada >= mrr_alvo E pelo menos `contratos_minimos` contas mensais com mensalidade >= `mensalidade_minima`.

🔴 Só avisa. Subir de plano é dinheiro (item 1 da lista fechada): quem sobe é o operador.
Depois da decisão dele, "decidido": true no JSON cala o aviso.

Uso:
  python3 40-operacao-rotinas/ferramentas/gatilho_plano.py            # lê o painel e diz onde estamos
  python3 40-operacao-rotinas/ferramentas/gatilho_plano.py --teste    # casos fixos, sem ler o repo; sai 1 se algum falhar
Quem chama: avisar-prazos.py (a linha entra no aviso diário do operador enquanto estiver cruzado e não decidido).
Saída: 0 sempre que rodou (cruzado ou não) · 1 teste reprovado · 2 régua ilegível.
"""
import importlib.util, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REGUA = os.path.join(AQUI, "..", "tokens", "GATILHO-PLANO.json")


def brl(v):
    return "R$ " + f"{v:,.0f}".replace(",", ".")


def ler_regua(caminho=REGUA):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def avaliar(receita, regua):
    """receita: payload["receita"] do painel. Devolve dict(cruzou, avisar, mrr, alvo, falta, contratos, texto)."""
    mrr = float((receita or {}).get("recorrente_contratada") or 0)
    piso = float(regua["mensalidade_minima"])
    fortes = [c for c in (receita or {}).get("contas", [])
              if c.get("recorrencia") == "mensal" and float(c.get("mensalidade") or 0) >= piso]
    alvo = float(regua["mrr_alvo"])
    n_min = int(regua["contratos_minimos"])
    cruzou = mrr >= alvo and len(fortes) >= n_min
    falta = max(0.0, alvo - mrr)
    if cruzou:
        texto = (f"Receita recorrente contratada em {brl(mrr)}, com {len(fortes)} contrato(s) de {brl(piso)} ou mais: "
                 f"cruzou o gatilho do plano maior ({brl(alvo)}). Decidir a subida de plano "
                 f"(cartão {regua.get('cartao', 'do gatilho')}).")
    else:
        texto = (f"Gatilho do plano maior: receita recorrente contratada {brl(mrr)} de {brl(alvo)} "
                 f"(faltam {brl(falta)}); contratos de {brl(piso)} ou mais: {len(fortes)} de {n_min}.")
    return dict(cruzou=cruzou, avisar=cruzou and not regua.get("decidido"), mrr=mrr, alvo=alvo, falta=falta,
                contratos=len(fortes), texto=texto)


def do_painel():
    spec = importlib.util.spec_from_file_location("painel_projetos", os.path.join(AQUI, "painel-projetos.py"))
    painel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(painel)
    return painel.montar().get("receita") or {}


def teste():
    r = dict(mrr_alvo=6000, mensalidade_minima=2500, contratos_minimos=2, decidido=False)
    def rec(*mens):
        return dict(recorrente_contratada=sum(mens), contas=[dict(recorrencia="mensal", mensalidade=m) for m in mens])
    casos = [
        ("hoje: só um contrato pequeno", rec(1000), False, False),
        ("um contrato na mensalidade mínima", rec(1000, 2500), False, False),
        ("dois na mensalidade mínima: cruza no alvo exato", rec(1000, 2500, 2500), True, True),
        ("6.000 em contratos pequenos não cruza", rec(1000, 1000, 2000, 2000), False, False),
        ("um de 4.500 e um na mínima", rec(1000, 4500, 2500), True, True),
        ("dois fortes sem chegar ao alvo", rec(2500, 2500), False, False),
        ("projeto não conta", dict(recorrente_contratada=1000, contas=[dict(recorrencia="projeto", mensalidade=9000),
                                                                      dict(recorrencia="mensal", mensalidade=1000)]), False, False),
        ("payload vazio", {}, False, False),
    ]
    ruim = 0
    for nome, receita, cruza, avisa in casos:
        a = avaliar(receita, r)
        ok = a["cruzou"] == cruza and a["avisar"] == avisa
        ruim += not ok
        print(("✅" if ok else "🔴"), nome, "·", a["texto"])
    a = avaliar(rec(1000, 2500, 2500), dict(r, decidido=True))
    ok = a["cruzou"] and not a["avisar"]
    ruim += not ok
    print(("✅" if ok else "🔴"), "decidido cala o aviso")
    print("✅ gatilho_plano: 9 casos" if not ruim else f"🔴 {ruim} caso(s) reprovado(s)")
    return 1 if ruim else 0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    if "--teste" in sys.argv:
        return teste()
    try:
        regua = ler_regua()
    except (OSError, ValueError, KeyError) as e:
        print(f"🔴 régua ilegível ({REGUA}): {e}", file=sys.stderr)
        return 2
    a = avaliar(do_painel(), regua)
    print(("🔔 " if a["avisar"] else "") + a["texto"] + (" (já decidido: aviso calado)" if a["cruzou"] and not a["avisar"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
