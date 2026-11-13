# -*- coding: utf-8 -*-
"""
decisoes_cartao.py — a fonte única do formato do cartão de decisão: quem LÊ (painel-projetos.py → tela do sistema)
e quem CONFERE (verificar-propagacao.py → régua V-DEC) usam as mesmas funções.

Tipo: ferramenta · gate (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Origem: o plano de decisões no painel (60-planos/decisoes-no-painel-*/PLANO-DECISOES-NO-PAINEL.md): a decisão tem de chegar
ao operador numa forma que se decide, não numa frase de registro.

O cartão tem duas camadas, no próprio DECISOES-PENDENTES.md:
  FACE   o que o operador lê para decidir. Teto por campo, língua comum, nada de código da casa. Vai inteira para a tela.
  LASTRO o registro (fonte, citação com hora, id, conta por extenso, adendos). Sem teto. Abre em "ver o lastro".

Molde (tarefas/modelos/cartao-decisao.md; a linha de opção continua casando com o regex do propagar-decisoes.py):
  ### D-AAAA-MM-DD-NNN · <Conta> — <Pergunta?> · tipo `x` · autonomia A1 · prazo: AAAA-MM-DD|sem prazo · aberta: AAAA-MM-DD HH:MM
  **Em jogo:** …
  **Números:** rótulo: valor (nota) · rótulo: valor          ← obrigatório em cartão de dinheiro
  - **A)** rótulo
    ↳ efeito
  **Recomendação:** A. porquê
  **Supondo:** premissa. Se não for, …
  **Lastro:**
  texto livre
Cartão antigo (com **Contexto:**) continua lido: tudo o que não é opção vira lastro, inteiro, sem corte.

Uso:
  python3 -X utf8 decisoes_cartao.py --lint                 todos os abertos; sai 1 se algum reprovar
  python3 -X utf8 decisoes_cartao.py --lint --id D-…        um só (quem acabou de escrever)
  python3 -X utf8 decisoes_cartao.py --novo "<Conta>" "<Pergunta?>" --tipo x [--prazo AAAA-MM-DD]
  python3 -X utf8 decisoes_cartao.py --json                 os cartões lidos, como a tela recebe
  [--arquivo <outro .md>] [--compat] (confere que o propagar-decisoes.py lê igual)
Python direto (Python\\bin\\python.exe) na automação; `py` só no PowerShell do operador.
"""
import argparse, datetime, io, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PEND = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas", "DECISOES-PENDENTES.md")

# tetos da face (plano §2.1; H4: três cartões seguidos estourando o mesmo teto com texto que não é gordura → o teto sobe aqui, com registro)
LIM = dict(pergunta=90, em_jogo=160, porque=200, supondo=140, rotulo=60, efeito=150, num_pares=4, num_rotulo=24, num_valor=40,
           face=1200)
DINHEIRO = {"preco", "preco_oferta", "oferta_preco", "dinheiro", "desconto", "cobranca", "despesa", "remuneracao_parceiro",
            "remuneracao", "oferta_catalogo_preco"}

# o que não entra na face: é código da casa, não é a língua do operador (regra: falar o conteúdo, não o código)
PROIBIDO = [
    (r"`", "crase (trecho de código)"),
    (r"\*", "asterisco de markdown"),
    (r"\b[DTO]-\d{4}", "id de cartão, task ou ordem"),
    (r"\bDEC-[A-Z]{2,3}-\d+", "id de decisão de conta"),
    (r"\b[A-Z]\d-\d{1,3}\b", "id de ponto de destilação"),
    (r"§", "sinal de seção"),
    (r"\bitem \d+ d[ao] (lista|anexo)", "número de item de regra ou anexo"),
    (r"\b[\w-]+\.(md|py|json|html|sql|txt|vbs|jsonl)\b", "nome de arquivo"),
    (r"(?<![\w/])[\w-]+/[\w-]+/", "caminho de pasta"),
    (r"(?<!\w)--[a-z]", "opção de linha de comando"),
    (r"\b[0-9a-f]{8,}\b", "hash"),
    (r"\bn\s*=\s*\d", "notação n=…"),
    (r"\b(A[0-3]|N[0-5]|L[1-7])\b(?!\))", "sigla de nível (A1, N4, L3)"),
    (r"\b(ontem|anteontem|amanhã)\b", "data relativa (o cartão vive dias: escreva a data)"),
]
AVISO = [
    (r"\bhoje\b", "'hoje': se for data, escreva a data (o cartão vive dias); se for 'atualmente', fica"),
]


def _campo(corpo, nome):
    m = re.search(r"^\*\*%s:\*\*[ \t]*(.*?)[ \t]*$" % re.escape(nome), corpo, re.M)
    return m.group(1).strip() if m else ""


def _prazo_iso(txt):
    txt = (txt or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", txt):
        return txt
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", txt)   # o leitor antigo do painel aceitava dd/mm/aaaa
    return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1))) if m else None


def ler_cartao(did, cab, corpo):
    partes = [p.strip() for p in cab.split(" · ")]
    conta, titulo = (partes[0].split(" — ", 1) + [""])[:2]
    tipo = re.search(r"tipo `([^`]+)`", cab)
    auton = re.search(r"autonomia (A\d)", cab)
    mp = re.search(r"prazo\s*:\s*([^·]*)", cab)
    prazo_txt = mp.group(1).strip() if mp else ""
    ma = re.search(r"aberta\s*:\s*(\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?)", cab)
    novo = bool(re.search(r"^\*\*Em jogo:\*\*", corpo, re.M))
    # no molde, opção e recomendação só valem ANTES do **Lastro:** (o lastro pode citar o texto antigo do cartão)
    frente = re.split(r"^\*\*Lastro:\*\*", corpo, maxsplit=1, flags=re.M)[0] if novo else corpo
    opcoes = []
    for m in re.finditer(r"^- \*\*([A-C])\)\*\*[ \t]*(.*?)[ \t]*$(?:\n[ \t]+↳[ \t]*(.*?)[ \t]*$)?", frente, re.M):
        opcoes.append(dict(letra=m.group(1), rotulo=m.group(2).strip(), efeito=(m.group(3) or "").strip()))
    rec = re.search(r"\*\*Recomendação:\*\*[ \t]*([A-C])[.:),]?[ \t]*(.*?)(?=[ \t]*\*\*O que acontece|\n|\Z)", frente)
    c = dict(id=did, conta=conta.replace("Casa", "casa").strip(), titulo=titulo.strip(), tipo=tipo.group(1) if tipo else None,
             autonomia=auton.group(1) if auton else None, prazo=_prazo_iso(prazo_txt), prazo_texto=prazo_txt,
             aberta=ma.group(1) if ma else None, formato="novo" if novo else "antigo", opcoes=opcoes,
             recomendado=rec.group(1) if rec else None, porque=(rec.group(2).strip() if rec else ""),
             em_jogo="", supondo="", numeros=[], lastro="", atualizado=None)
    if novo:
        c["em_jogo"] = _campo(frente, "Em jogo")
        c["supondo"] = _campo(frente, "Supondo")
        for par in [p.strip() for p in _campo(frente, "Números").split(" · ") if p.strip()]:
            rot, _, val = par.partition(": ")
            nota = re.search(r"\s*\(([^)]*)\)\s*$", val)
            c["numeros"].append(dict(rotulo=rot.strip(), valor=(val[:nota.start()] if nota else val).strip(),
                                     nota=nota.group(1) if nota else ""))
        ml = re.search(r"^\*\*Lastro:\*\*[ \t]*\n?(.*)\Z", corpo, re.M | re.S)
        c["lastro"] = ml.group(1).strip() if ml else ""
    else:
        # antigo: nada se perde. Tudo o que não é linha de opção vai para o lastro, na ordem em que está.
        resto = re.sub(r"^- \*\*[A-C]\)\*\*.*$\n?", "", corpo, flags=re.M)
        c["lastro"] = re.sub(r"\n{3,}", "\n\n", resto).strip()
    # "⟲ **Adendo DD/MM, HH:MM–HH:MM (Evolution):**" → "DD/MM, HH:MM–HH:MM" (a hora tem ':'; para no parêntese ou no fim do negrito)
    ad = re.findall(r"⟲ \*\*Adendo ([^*(]*?)\s*(?:\(|:?\*\*)", corpo)
    c["atualizado"] = ad[-1].strip(" ,") if ad else None
    # apelidos para a aba antiga ainda aberta num navegador (plano §4.2; saem na limpeza seguinte)
    for o in c["opcoes"]:
        o["texto"] = o["rotulo"]
    c["contexto"] = c["em_jogo"]
    return c


def _abertas(texto):
    if "## Abertas" not in texto:
        return ""
    return texto.split("## Abertas", 1)[1].split("## Decididas", 1)[0]


def ler(texto=None):
    """Cartões da seção Abertas. Sem argumento, lê o DECISOES-PENDENTES.md."""
    if texto is None:
        texto = io.open(PEND, encoding="utf-8").read()
    texto = texto.replace("\r\n", "\n")
    return [ler_cartao(m.group(1), m.group(2), m.group(3))
            for m in re.finditer(r"^### (D-[\d-]+) · (.*?)$\n((?:(?!^### ).*\n?)*)", _abertas(texto), re.M)]


def resolvidos_em_abertas(texto):
    """Cabeçalhos começando por ### ✅ ainda na seção Abertas (V-DEC-6)."""
    texto = texto.replace("\r\n", "\n")
    return [(re.search(r"(D-\d{4}-\d{2}-\d{2}-\d{3})", l) or re.search(r"(.{0,40})", l)).group(1)
            for l in _abertas(texto).split("\n") if l.startswith("### ✅")]


def face(c):
    """Todo texto que o operador lê sem abrir o lastro, com o nome do campo."""
    out = [("pergunta", c["titulo"]), ("em_jogo", c["em_jogo"]), ("porque", c["porque"]), ("supondo", c["supondo"])]
    for o in c["opcoes"]:
        out += [("rotulo " + o["letra"], o["rotulo"]), ("efeito " + o["letra"], o["efeito"])]
    for n in c["numeros"]:
        out += [("número", n["rotulo"]), ("número", (n["valor"] + " " + n["nota"]).strip())]
    return out


def tamanho_face(c):
    return sum(len(t) for _, t in face(c))


def lint(c, agora=None):
    """Lista de (nível, régua, mensagem). nível 🔴 reprova; ⚠️ só avisa."""
    r = []
    def add(n, regua, msg):
        r.append((n, regua, msg))
    def lim(campo, texto, chave):
        if len(texto) > LIM[chave]:
            add("🔴", "V-DEC-2", "%s com %d caracteres (teto %d)" % (campo, len(texto), LIM[chave]))
    if c["formato"] == "antigo":
        add("🔴", "V-DEC-1", "formato antigo (sem **Em jogo:**): reescrever no molde tarefas/modelos/cartao-decisao.md")
        return r   # o resto da régua só faz sentido no molde
    if not c["titulo"].rstrip().endswith("?"):
        add("🔴", "V-DEC-2", "a pergunta não termina em '?'")
    if "(" in c["titulo"]:
        add("🔴", "V-DEC-2", "parêntese na pergunta: o detalhe vai para 'Em jogo' ou para o lastro")
    lim("pergunta", c["titulo"], "pergunta")
    for campo, nome in (("em_jogo", "Em jogo"), ("supondo", "Supondo")):
        if not c[campo]:
            add("🔴", "V-DEC-4" if campo == "supondo" else "V-DEC-1", "falta **%s:**" % nome)
        lim(nome, c[campo], campo)
    if c["supondo"] and not re.search(r"\b[Ss]e\b", c["supondo"]):
        add("⚠️", "aviso", "'Supondo' sem o 'se não for…': diga o que muda se a premissa cair")
    if not c["lastro"]:
        add("⚠️", "aviso", "lastro vazio: de onde veio o fato?")
    if not c["recomendado"]:
        add("🔴", "V-DEC-4", "sem **Recomendação:** com letra")
    elif c["recomendado"] not in [o["letra"] for o in c["opcoes"]]:
        add("🔴", "V-DEC-4", "recomenda %s, que não está nas opções" % c["recomendado"])
    if not c["porque"]:
        add("🔴", "V-DEC-4", "recomendação sem porquê")
    lim("porquê da recomendação", c["porque"], "porque")
    if not 2 <= len(c["opcoes"]) <= 3:
        add("🔴", "V-DEC-4", "%d opção(ões): são 2 ou 3" % len(c["opcoes"]))
    for o in c["opcoes"]:
        lim("rótulo da " + o["letra"], o["rotulo"], "rotulo")
        if not o["efeito"]:
            add("🔴", "V-DEC-4", "opção %s sem a linha ↳ (o que acontece se ele clicar)" % o["letra"])
        lim("efeito da " + o["letra"], o["efeito"], "efeito")
    if not c["prazo"] and c["prazo_texto"].lower() != "sem prazo":
        add("🔴", "V-DEC-5", "prazo '%s' não é data nem 'sem prazo': a tela perde o prazo (o motivo vai no 'Em jogo')" % c["prazo_texto"])
    if not c["aberta"]:
        add("🔴", "V-DEC-5", "sem 'aberta: AAAA-MM-DD HH:MM' no cabeçalho (hora de Brasília; é a linha de base da medição)")
    if c["tipo"] in DINHEIRO and not c["numeros"]:
        add("🔴", "V-DEC-6", "cartão de dinheiro sem **Números:**")
    if len(c["numeros"]) > LIM["num_pares"]:
        add("🔴", "V-DEC-2", "%d números (teto %d)" % (len(c["numeros"]), LIM["num_pares"]))
    for n in c["numeros"]:
        lim("rótulo de número", n["rotulo"], "num_rotulo")
        lim("valor de número", (n["valor"] + " " + n["nota"]).strip(), "num_valor")
    tf = tamanho_face(c)
    if tf > LIM["face"]:
        add("🔴", "V-DEC-2", "face com %d caracteres somados (teto %d)" % (tf, LIM["face"]))
    for campo, texto in face(c):
        for rx, nome in PROIBIDO:
            m = re.search(rx, texto)
            if m:
                add("🔴", "V-DEC-3", "%s tem %s: '%s'" % (campo, nome, m.group(0)))
        for rx, nome in AVISO:
            if re.search(rx, texto):
                add("⚠️", "aviso", "%s: %s" % (campo, nome))
    if c["prazo"]:
        agora = agora or datetime.datetime.now()
        venc = datetime.datetime.strptime(c["prazo"], "%Y-%m-%d") + datetime.timedelta(days=1)
        if (agora - venc).total_seconds() > 72 * 3600:
            add("⚠️", "aviso", "prazo %s vencido há mais de 72 h: decidir, reescrever ou tirar a data" % c["prazo"])
    return r


def conferir(raiz=RAIZ):
    """(ok, linhas) — no contrato dos outros verificadores (entregaveis.py, derivados.py). Chamado pelo verificar-propagacao.py."""
    p = os.path.join(raiz, "40-operacao-rotinas", "tarefas", "DECISOES-PENDENTES.md")
    if not os.path.exists(p):
        return True, ["sem DECISOES-PENDENTES.md"]
    texto = io.open(p, encoding="utf-8").read()
    linhas, falhas = [], 0
    for c in ler(texto):
        achados = lint(c)
        verm = [a for a in achados if a[0] == "🔴"]
        falhas += len(verm)
        for n, regua, msg in achados:
            linhas.append("%s %s %s · %s" % (n, regua if regua != "aviso" else "", c["id"], msg))
    for did in resolvidos_em_abertas(texto):
        falhas += 1
        linhas.append("🔴 V-DEC-6 %s · cartão já resolvido (### ✅) parado em Abertas: descer para Decididas sem mudar uma letra" % did)
    n = len(ler(texto))
    if not falhas:
        linhas.insert(0, "✅ %d cartão(ões) aberto(s), todos no molde" % n)
    return falhas == 0, linhas


def compat(texto, c):
    """Os três regex do propagar-decisoes.py (linhas 79-88) têm de continuar achando o cartão, a letra, o tipo e a conta."""
    abertas = texto.replace("\r\n", "\n").split("## Decididas", 1)[0]
    m = re.search(r"(### %s[^\n]*\n(?:(?!### ).*\n?)*)" % re.escape(c["id"]), abertas)
    if not m:
        return ["propagar não acha o cartão"]
    cartao, f = m.group(1), []
    rec = re.search(r"\*\*Recomendação:\*\*\s*([A-C])", cartao)
    if not rec or rec.group(1) != c["recomendado"]:
        f.append("propagar lê recomendação %r, o leitor leu %r" % (rec.group(1) if rec else None, c["recomendado"]))
    if not re.search(r"tipo `([^`]+)`", cartao):
        f.append("propagar não acha o tipo")
    if not re.search(r"### [^·]+· ([^—·]+?) —", cartao):
        f.append("propagar não acha a conta")
    return f


def novo(conta, pergunta, tipo, prazo=None, texto=None, agora=None):
    """O molde preenchido com o próximo id do dia e a hora de abertura (Brasília = relógio desta máquina)."""
    agora = agora or datetime.datetime.now()
    dia = agora.strftime("%Y-%m-%d")
    if texto is None:
        texto = io.open(PEND, encoding="utf-8").read() if os.path.exists(PEND) else ""
    usados = [int(n) for n in re.findall(r"D-%s-(\d{3})" % dia, texto)]
    did = "D-%s-%03d" % (dia, (max(usados) + 1) if usados else 1)
    return ("### %s · %s — %s · tipo `%s` · autonomia A1 · prazo: %s · aberta: %s\n"
            "**Em jogo:** <o que se perde ou se ganha, e por que a decisão é agora; até 160>\n"
            "**Números:** <rótulo: valor (nota) · … até 4 pares; obrigatório em cartão de dinheiro, senão apague a linha>\n"
            "- **A)** <rótulo, até 60>\n  ↳ <o que o clique dispara e o que custa, até 150>\n"
            "- **B)** <rótulo>\n  ↳ <efeito>\n"
            "- **C)** <rótulo>\n  ↳ <efeito>\n"
            "**Recomendação:** A. <o porquê, até 200>\n"
            "**Supondo:** <a premissa em que as opções se apoiam>. Se não for, <o que muda>. <até 140>\n"
            "**Lastro:**\n<contexto com fonte, citações com hora, ids, contas por extenso, adendos ⟲>\n"
            % (did, conta, pergunta, tipo, prazo or "sem prazo", agora.strftime("%Y-%m-%d %H:%M")))


def main():
    ap = argparse.ArgumentParser(description="cartão de decisão: leitor, régua e molde")
    ap.add_argument("--arquivo", default=PEND)
    ap.add_argument("--lint", action="store_true")
    ap.add_argument("--id")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--compat", action="store_true")
    ap.add_argument("--novo", nargs=2, metavar=("CONTA", "PERGUNTA"))
    ap.add_argument("--tipo")
    ap.add_argument("--prazo")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if a.novo:
        if not a.tipo:
            print("--novo pede --tipo"); return 2
        print(novo(a.novo[0], a.novo[1], a.tipo, a.prazo))
        return 0
    texto = io.open(a.arquivo, encoding="utf-8").read().replace("\r\n", "\n")
    cs = ler(texto)
    if a.id:
        cs = [c for c in cs if c["id"] == a.id]
        if not cs:
            print("%s não está em Abertas" % a.id); return 1
    if a.json:
        print(json.dumps(cs, ensure_ascii=False, indent=1))
        return 0
    falhas = 0
    for c in cs:
        print("\n%s · %s · formato %s · face %d caracteres · lastro %d" % (c["id"], c["conta"], c["formato"], tamanho_face(c), len(c["lastro"])))
        if a.lint or not a.compat:
            achados = lint(c)
            falhas += sum(1 for n, _, _ in achados if n == "🔴")
            for n, regua, msg in achados:
                print("  %s %s %s" % (n, regua if regua != "aviso" else "", msg))
            if not achados:
                print("  ✅ no molde")
        if a.compat:
            f = compat(texto, c)
            falhas += len(f)
            print("  " + ("✅ propagar-decisoes.py lê igual" if not f else "🔴 " + "; ".join(f)))
    if not a.id:
        for did in resolvidos_em_abertas(texto):
            falhas += 1
            print("\n🔴 V-DEC-6 %s · resolvido (### ✅) parado em Abertas" % did)
    print("\n%d cartão(ões) · %s" % (len(cs), "✅" if not falhas else "🔴 %d falha(s)" % falhas))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
