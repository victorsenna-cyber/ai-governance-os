#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verificar_relatorio.py — o gate do relatório da operação (template repo-agentes, Continuum).

Nenhum número, hora, data ou código sai num relatório se não estiver na FOTO DA OPERAÇÃO.
Quem calcula é o script que monta a foto; o agente só escreve; este verificador confere.

Uso:
  python3 verificar_relatorio.py --foto foto.json --texto relatorio.md   # sai 0 se passou, 1 se reprovou, 2 se erro de uso
  python3 verificar_relatorio.py --autoteste                              # roda os casos embutidos

O que o texto pode conter (fora disso, reprova):
  1. Número (inteiro, decimal, dinheiro, %, "30d") → igual a um campo NUMÉRICO da foto (o valor ou o módulo).
     Dinheiro abreviado ("R$ 18,2 mil", "R$ 1,2 mi") aceita a diferença do arredondamento escrito.
  2. Hora ("06h40", "14:08", "7h") e data ("31/10", "31/10/2026", "2026-10-31") → presentes em algum campo da foto.
  3. Código ("D-2026-01-15-008", "DEC-AB-42", "R8") → presente em algum texto da foto.
  4. Trecho entre aspas (“…”, "…", «…», `…`) → cópia literal de algum texto da foto. Dentro dele, nada mais
     é conferido, porque o trecho inteiro já foi.
  5. Marcador de lista no começo da linha ("1.", "2)") não é número.
Número por extenso ("três") não é conferido: a skill manda escrever em algarismo.
Nome próprio e adjetivo não são conferidos aqui: são do revisor. Este script confere o que código confere.

Procedência: escrito pela Continuum em 31/10/2026. Sem dependência externa.
"""
import argparse
import json
import re
import sys
import unicodedata

ASPAS = re.compile(r"“([^”]{3,})”|\"([^\"]{3,})\"|«([^»]{3,})»|`([^`]{3,})`")
CODIGO = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b|\b[A-Z]{1,3}\d{1,3}\b")
DATA_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
DATA_BR = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b")
HORA = re.compile(r"\b(\d{1,2})(?:h(\d{2})?|:(\d{2}))\b")
DINHEIRO = re.compile(r"R\$\s*(-?[\d.]+(?:,\d+)?)\s*(mil|mi|milhão|milhões|bi)?\b", re.I)
PERCENT = re.compile(r"(-?\d+(?:,\d+)?)\s*%")
LISTA = re.compile(r"^(\s*)\d{1,2}[.)](?=\s)", re.M)
NUMERO = re.compile(r"(?<![\w/])-?\d+(?:\.\d{3})*(?:,\d+)?(?:\.\d+)?(?=d\b|\b)")
MULT = {"mil": 1e3, "mi": 1e6, "milhão": 1e6, "milhões": 1e6, "bi": 1e9}


def norm(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def num_br(tok):
    """'1.250' → 1250 · '18,2' → 18.2 · '1.234,56' → 1234.56 · '3.5' → 3.5"""
    t = tok.strip()
    if "," in t:
        return float(t.replace(".", "").replace(",", "."))
    if re.fullmatch(r"-?\d{1,3}(\.\d{3})+", t):
        return float(t.replace(".", ""))
    return float(t)


def casas(tok):
    return len(tok.split(",")[1]) if "," in tok else 0


def coletar(foto):
    numeros, textos = set(), []

    def andar(v):
        if isinstance(v, bool) or v is None:
            return
        if isinstance(v, (int, float)):
            numeros.add(round(float(v), 4))
            numeros.add(round(abs(float(v)), 4))
        elif isinstance(v, str):
            textos.append(v)
        elif isinstance(v, dict):
            for x in v.values():
                andar(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                andar(x)

    andar(foto)
    corpo = "\n".join(textos)
    datas, horas = set(), set()
    for a, m, d in DATA_ISO.findall(corpo):
        datas.add((int(d), int(m), int(a)))
    for d, m, a in DATA_BR.findall(corpo):
        datas.add((int(d), int(m), int(a) + (2000 if a and len(a) == 2 else 0) if a else None))
    for h, m1, m2 in HORA.findall(corpo):
        horas.add((int(h), int(m1 or m2 or 0)))
    for hh, mm in re.findall(r"\b(\d{2}):(\d{2})\b", corpo):
        horas.add((int(hh), int(mm)))
    return numeros, corpo, norm(corpo), datas, horas


def tem_numero(numeros, valor, tol=0.005):
    return any(abs(valor - n) <= tol for n in numeros)


def verificar(foto, texto):
    numeros, corpo, corpo_n, datas, horas = coletar(foto)
    falhas, conferidos = [], 0
    linhas = texto.splitlines()

    def onde(trecho):
        for i, l in enumerate(linhas, 1):
            if trecho in l:
                return i
        return "?"

    # 4. aspas: trecho literal da foto; depois sai do texto
    def tirar_aspas(m):
        nonlocal conferidos
        trecho = next(g for g in m.groups() if g)
        conferidos += 1
        if norm(trecho) not in corpo_n:
            falhas.append((onde(trecho), f"«{trecho[:60]}»", "citação que não está na foto"))
        return " "

    t = ASPAS.sub(tirar_aspas, texto)
    # 5. marcador de lista
    t = LISTA.sub(r"\1", t)

    # 3. códigos
    def tirar_codigo(m):
        nonlocal conferidos
        c = m.group(0)
        conferidos += 1
        if c not in corpo:
            falhas.append((onde(c), c, "código que não está na foto"))
        return " "

    t = CODIGO.sub(tirar_codigo, t)

    # 2. datas
    def tirar_iso(m):
        nonlocal conferidos
        a, mm, d = (int(x) for x in m.groups())
        conferidos += 1
        if (d, mm, a) not in datas:
            falhas.append((onde(m.group(0)), m.group(0), "data que não está na foto"))
        return " "

    def tirar_br(m):
        nonlocal conferidos
        d, mm, a = m.group(1), m.group(2), m.group(3)
        conferidos += 1
        d, mm = int(d), int(mm)
        ok = any(x[0] == d and x[1] == mm and (a is None or x[2] in (None, int(a) + (2000 if len(a) == 2 else 0)))
                 for x in datas)
        if not ok:
            falhas.append((onde(m.group(0)), m.group(0), "data que não está na foto"))
        return " "

    t = DATA_ISO.sub(tirar_iso, t)
    t = DATA_BR.sub(tirar_br, t)

    # 2. horas
    def tirar_hora(m):
        nonlocal conferidos
        h, m1, m2 = m.group(1), m.group(2), m.group(3)
        conferidos += 1
        if (int(h), int(m1 or m2 or 0)) not in horas:
            falhas.append((onde(m.group(0)), m.group(0), "hora que não está na foto"))
        return " "

    t = HORA.sub(tirar_hora, t)

    # 1. dinheiro
    def tirar_dinheiro(m):
        nonlocal conferidos
        tok, suf = m.group(1).rstrip("."), (m.group(2) or "").lower()
        conferidos += 1
        try:
            v = num_br(tok)
        except ValueError:
            falhas.append((onde(m.group(0)), m.group(0), "valor ilegível"))
            return " "
        if suf:
            mult = MULT[suf]
            v, tol = v * mult, 0.5 * (10 ** -casas(tok)) * mult
        else:
            tol = 0.5 if casas(tok) == 0 else 0.005
        if not tem_numero(numeros, v, tol):
            falhas.append((onde(m.group(0)), m.group(0), "valor que não está na foto"))
        return " "

    t = DINHEIRO.sub(tirar_dinheiro, t)

    def tirar_pct(m):
        nonlocal conferidos
        conferidos += 1
        v = num_br(m.group(1))
        if not tem_numero(numeros, v, 0.05 if casas(m.group(1)) else 0.5):
            falhas.append((onde(m.group(0)), m.group(0), "percentual que não está na foto"))
        return " "

    t = PERCENT.sub(tirar_pct, t)

    # 1. números soltos
    for m in NUMERO.finditer(t):
        tok = m.group(0)
        conferidos += 1
        try:
            v = num_br(tok)
        except ValueError:
            falhas.append((onde(tok), tok, "número ilegível"))
            continue
        if not tem_numero(numeros, v):
            falhas.append((onde(tok), tok, "número que não está na foto"))
    return falhas, conferidos


def relatar(falhas, conferidos):
    if falhas:
        print(f"❌ REPROVADO · {len(falhas)} de {conferidos} itens conferidos não estão na foto:")
        for linha, tok, motivo in falhas:
            print(f"   linha {linha}: {tok} — {motivo}")
        print("O relatório não sai. Corrija pelo que a foto diz, ou diga «não consegui ler» onde a foto não tem o dado.")
        return 1
    print(f"✅ PASSOU · {conferidos} itens conferidos contra a foto.")
    return 0


FOTO_TESTE = {
    "gerado_em": "2026-10-31 14:08",
    "areas": [
        {"area": "Caixa", "itens": [
            {"id": "caixa.entra_hoje", "rotulo": "entra hoje", "valor": 18240.0, "fonte": "R8", "lido_em": "05:00"},
            {"id": "caixa.sai_hoje", "rotulo": "sai hoje", "valor": 11900.0, "fonte": "R8", "lido_em": "05:00"}]},
        {"area": "Contas", "itens": [
            {"id": "contas.ativas", "rotulo": "contas ativas", "valor": 10, "fonte": "PAINEL.md", "lido_em": "14:08"},
            {"id": "conta.a", "conta": "Conta A", "marco": "Entregar o documento com as 3 etapas",
             "atraso_dias": 30, "prazo": "2026-10-01", "fonte": "clientes/Conta A/PAINEL.md"}]},
        {"area": "Decisões", "itens": [
            {"id": "D-2026-01-15-008", "titulo": "publicar a página nova hoje?", "conta": "Conta B"}]},
    ],
    "precisa_de_voce": [{"id": "D-2026-01-15-008", "texto": "publicar a página nova hoje?"}],
    "contagens": {"precisa_de_voce": 1},
}

CASOS = [
    ("passa: tudo da foto", "Bom dia. Entram R$ 18,2 mil e saem R$ 11.900 hoje (R8, 05h00).\n"
     "10 contas ativas. Conta A: marco vencido há 30 dias (prazo 01/10).\n"
     "Precisa de você:\n1. D-2026-01-15-008: \"publicar a página nova hoje?\"", True),
    ("reprova: número inventado", "11 contas ativas.", False),
    ("reprova: dinheiro fora do arredondamento", "Entram R$ 19 mil hoje.", False),
    ("passa: dinheiro dentro do arredondamento", "Entram R$ 18 mil hoje.", True),
    ("reprova: hora que não houve leitura", "Lido às 06h40.", False),
    ("reprova: citação inventada", "Ele disse: \"publicar tudo amanhã\".", False),
    ("reprova: código que não existe", "Decisão D-2026-01-16-001 aberta.", False),
    ("passa: marcador de lista e citação com número", "1. \"Entregar o documento com as 3 etapas\"", True),
    ("reprova: data errada", "Prazo era 02/10.", False),
]


def autoteste():
    ruins = 0
    for nome, texto, espera in CASOS:
        falhas, _ = verificar(FOTO_TESTE, texto)
        ok = (not falhas) == espera
        ruins += not ok
        print(f"{'✅' if ok else '❌'} {nome}" + ("" if ok else f" → falhas: {falhas}"))
    print(f"\n{len(CASOS) - ruins}/{len(CASOS)} casos ok")
    return 1 if ruins else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere o relatório da operação contra a foto.")
    ap.add_argument("--foto")
    ap.add_argument("--texto")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args(argv)
    if a.autoteste:
        return autoteste()
    if not (a.foto and a.texto):
        ap.print_usage()
        return 2
    with open(a.foto, encoding="utf-8") as f:
        foto = json.load(f)
    with open(a.texto, encoding="utf-8") as f:
        texto = f.read()
    return relatar(*verificar(foto, texto))


if __name__ == "__main__":
    sys.exit(main())
