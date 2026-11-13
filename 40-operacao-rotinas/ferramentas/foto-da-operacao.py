#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
foto-da-operacao.py — a FOTO DA OPERAÇÃO da empresa.

Responde, em dado, a pergunta "como está a operação hoje?". Não escreve frase: monta o JSON que o agente
lê para redigir o relatório e que o verificador usa para conferir cada número do texto.

Fonte: o mesmo payload do painel de projetos (`painel-projetos.py`, importado; ele lê PAINEL.md das contas,
tasks, DECISOES-PENDENTES e o A receber do 45-financeiro). Nada é lido fora dele: se a fonte é nova, ela
entra no painel-projetos primeiro, para o painel e o relatório nunca divergirem.

Uso (da raiz da Governança):
  python3 40-operacao-rotinas/ferramentas/foto-da-operacao.py                       # resumo na tela
  python3 40-operacao-rotinas/ferramentas/foto-da-operacao.py --json <arquivo>      # grava a foto
  python3 40-operacao-rotinas/ferramentas/foto-da-operacao.py --salvar              # grava em
        40-operacao-rotinas/operacao-hoje/AAAA-MM-DD-HHhMM-foto.json

Esquema (o mesmo do template, 90-templates/repo-agentes/ferramentas/FOTO-DA-OPERACAO.md):
  empresa · pergunta · gerado_em · areas[{area, agente, itens[{id, rotulo, valor, fonte, lido_em, ...}]}]
  · precisa_de_voce[{id, texto, fonte, prazo?}] · nao_lido[{fonte, motivo}] · contagens{...}
Procedência: template Continuum.
"""
import argparse, datetime as dt, importlib.util, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SAIDA = os.path.join(RAIZ, "40-operacao-rotinas", "operacao-hoje")
# Quem é "o dono" nos marcos do PAINEL.md: o nome do operador, ou a palavra "operador".
DONOS = ("{{OPERADOR}}".lower(), "operador")


def do_dono(quem):
    quem = (quem or "").lower()
    return any(d in quem for d in DONOS)


def painel():
    spec = importlib.util.spec_from_file_location("painel_projetos", os.path.join(AQUI, "painel-projetos.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.montar()


def montar_foto(p):
    lido = p["gerado_em"]
    hora = lido[-5:]
    ativas = [c for c in p["contas"] if c.get("ativa")]
    por_saude = {s: [c for c in ativas if c.get("saude") == s] for s in ("vermelho", "amarelo", "verde")}

    contas = [
        {"id": "contas.ativas", "rotulo": "contas ativas", "valor": len(ativas), "fonte": "clientes/*/PAINEL.md", "lido_em": hora},
        {"id": "contas.vermelhas", "rotulo": "vermelhas", "valor": len(por_saude["vermelho"]), "fonte": "clientes/*/PAINEL.md", "lido_em": hora},
        {"id": "contas.amarelas", "rotulo": "amarelas", "valor": len(por_saude["amarelo"]), "fonte": "clientes/*/PAINEL.md", "lido_em": hora},
        {"id": "contas.verdes", "rotulo": "verdes", "valor": len(por_saude["verde"]), "fonte": "clientes/*/PAINEL.md", "lido_em": hora},
    ]
    for c in por_saude["vermelho"] + por_saude["amarelo"]:
        md = c.get("marco_dias")
        contas.append({
            "id": "conta." + c["conta"], "conta": c["conta"], "saude": c["saude"], "fase": c.get("fase"),
            "motivos": c.get("motivos", []), "proximo_marco": c.get("proximo_marco"), "marco_prazo": c.get("marco_prazo"),
            "marco_dono": c.get("marco_dono"),
            "atraso_dias": (-md if md is not None and md < 0 else None),
            "faltam_dias": (md if md is not None and md >= 0 else None),
            "sem_toque_dias": c.get("sem_toque_dias"),
            "marcos_vencidos": [{"o_que": m.get("o_que"), "prazo": m.get("prazo"), "dono": m.get("dono"),
                                 "atraso_dias": -m["dias"]} for m in c.get("marcos", []) if m.get("vencido")],
            "fonte": (c.get("arquivos") or {}).get("painel") or f"clientes/{c['conta']}/PAINEL.md", "lido_em": hora})

    receber = [dict(r, conta_painel=c["conta"]) for c in p["contas"] for r in c.get("a_receber", [])]
    vencidos = [r for r in receber if r.get("dias") is not None and r["dias"] < 0]
    caixa = [
        {"id": "caixa.a_receber_total", "rotulo": "a receber, total", "valor": round(sum(r["valor"] for r in receber), 2),
         "fonte": "45-financeiro/LANCAMENTOS-EMPRESA.md (A receber)", "lido_em": hora},
        {"id": "caixa.a_receber_itens", "rotulo": "títulos a receber", "valor": len(receber),
         "fonte": "45-financeiro/LANCAMENTOS-EMPRESA.md (A receber)", "lido_em": hora},
        {"id": "caixa.a_receber_vencido", "rotulo": "a receber vencido", "valor": round(sum(r["valor"] for r in vencidos), 2),
         "fonte": "45-financeiro/LANCAMENTOS-EMPRESA.md (A receber)", "lido_em": hora},
    ]
    for r in receber:
        caixa.append({"id": "receber." + r["id"], "contraparte": r.get("contraparte"), "valor": r["valor"],
                      "vencimento": r.get("vencimento"), "estado": r.get("estado"),
                      "atraso_dias": (-r["dias"] if r.get("dias") is not None and r["dias"] < 0 else None),
                      "fonte": r.get("origem"), "lido_em": hora})

    decisoes = [{"id": "decisoes.abertas", "rotulo": "decisões abertas", "valor": len(p["decisoes"]),
                 "fonte": "40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md", "lido_em": hora}]
    for d in p["decisoes"]:
        decisoes.append({"id": d["id"], "conta": d.get("conta"), "titulo": d.get("titulo"), "prazo": d.get("prazo"),
                         "autonomia": d.get("autonomia"), "fonte": "40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md", "lido_em": hora})

    tasks = p.get("tasks_casa", []) + [t for c in p["contas"] for t in c.get("tasks", [])]
    por_pasta = {}
    for t in tasks:
        por_pasta[t.get("pasta")] = por_pasta.get(t.get("pasta"), 0) + 1
    t_venc = [t for t in tasks if t.get("vencido")]
    tarefas = [{"id": f"tarefas.{k}", "rotulo": f"tasks em {k}/", "valor": v, "fonte": f"40-operacao-rotinas/tarefas/{k}/",
                "lido_em": hora} for k, v in sorted(por_pasta.items()) if k]
    tarefas.append({"id": "tarefas.vencidas", "rotulo": "tasks vencidas", "valor": len(t_venc),
                    "fonte": "40-operacao-rotinas/tarefas/", "lido_em": hora})
    for t in t_venc + [t for t in tasks if t.get("pasta") in ("decisao", "falhou") and not t.get("vencido")]:
        tarefas.append({"id": t["id"], "titulo": t.get("titulo"), "conta": t.get("conta"), "pasta": t.get("pasta"),
                        "prazo": t.get("prazo"), "atraso_dias": (-t["dias"] if t.get("dias") is not None and t["dias"] < 0 else None),
                        "fonte": f"40-operacao-rotinas/tarefas/{t.get('pasta')}/", "lido_em": hora})

    precisa = []
    for d in p["decisoes"]:
        precisa.append({"id": d["id"], "texto": d.get("titulo"), "conta": d.get("conta"), "prazo": d.get("prazo"),
                        "fonte": "40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md"})
    for c in por_saude["vermelho"]:
        md = c.get("marco_dias")
        vistos = set()
        if md is not None and md < 0 and do_dono(c.get("marco_dono")):
            vistos.add(c.get("proximo_marco"))
            precisa.append({"id": "marco." + c["conta"], "texto": c.get("proximo_marco"), "conta": c["conta"],
                            "prazo": c.get("marco_prazo"), "atraso_dias": -md, "fonte": (c.get("arquivos") or {}).get("painel") or f"clientes/{c['conta']}/PAINEL.md"})
        for i, m in enumerate(c.get("marcos", [])):
            if m.get("vencido") and do_dono(m.get("dono")) and m.get("o_que") not in vistos:
                precisa.append({"id": f"marco.{c['conta']}.{i}", "texto": m.get("o_que"), "conta": c["conta"],
                                "prazo": m.get("prazo"), "atraso_dias": -m["dias"], "fonte": (c.get("arquivos") or {}).get("painel") or f"clientes/{c['conta']}/PAINEL.md"})
    for r in vencidos:
        precisa.append({"id": "receber." + r["id"], "texto": f"cobrar {r.get('contraparte')}", "valor": r["valor"],
                        "atraso_dias": -r["dias"], "fonte": r.get("origem")})
    for t in tasks:
        if t.get("pasta") == "decisao":
            precisa.append({"id": t["id"], "texto": t.get("titulo"), "conta": t.get("conta"),
                            "fonte": "40-operacao-rotinas/tarefas/decisao/"})

    nao_lido = [{"fonte": f"clientes/{n}/PAINEL.md", "motivo": "conta sem PAINEL.md"} for n in p["resumo"].get("sem_painel", [])]
    nao_lido += [{"fonte": f"clientes/{n}/PAINEL.md", "motivo": "painel inválido"} for n in p["resumo"].get("invalidas", [])]
    nao_lido.append({"fonte": "Gerenciador de Anúncios, e-mail, agenda", "motivo": "fora do painel de projetos"})

    return {
        "empresa": "{{EMPRESA}}",
        "pergunta": "como está a operação hoje?",
        "gerado_em": lido,
        "hoje": p["hoje"],
        "areas": [
            {"area": "Contas", "agente": "contas", "itens": contas},
            {"area": "Caixa", "agente": "caixa", "itens": caixa},
            {"area": "Decisões", "agente": "coordenador", "itens": decisoes},
            {"area": "Tarefas da casa", "agente": "coordenador", "itens": tarefas},
        ],
        "precisa_de_voce": precisa,
        "nao_lido": nao_lido,
        "contagens": {"precisa_de_voce": len(precisa), "nao_lido": len(nao_lido), "areas": 4,
                      "precisa_por_conta": {k: sum(1 for x in precisa if (x.get("conta") or "casa") == k)
                                            for k in sorted({x.get("conta") or "casa" for x in precisa})},
                      "maior_atraso_por_conta": {k: max(x["atraso_dias"] for x in precisa
                                                        if (x.get("conta") or "casa") == k and x.get("atraso_dias"))
                                                 for k in sorted({x.get("conta") or "casa" for x in precisa if x.get("atraso_dias")})}},
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Foto da operação.")
    ap.add_argument("--json")
    ap.add_argument("--salvar", action="store_true")
    a = ap.parse_args(argv)
    foto = montar_foto(painel())
    destino = a.json
    if a.salvar:
        os.makedirs(SAIDA, exist_ok=True)
        destino = os.path.join(SAIDA, foto["gerado_em"].replace(":", "h").replace(" ", "-") + "-foto.json")
    if destino:
        with open(destino, "w", encoding="utf-8") as f:
            json.dump(foto, f, ensure_ascii=False, indent=1)
        print(destino)
    c = {a["area"]: len(a["itens"]) for a in foto["areas"]}
    print(f"foto {foto['gerado_em']} · itens por área {c} · precisa de você {len(foto['precisa_de_voce'])} · não lido {len(foto['nao_lido'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
