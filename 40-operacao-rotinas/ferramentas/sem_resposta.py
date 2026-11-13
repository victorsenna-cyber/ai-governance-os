"""sem_resposta.py — "a última mensagem é deles e está sem resposta nossa".

A régua do retorno atrasado (`00-core/roteador/ARVORE-ESCRITA.md` §7) pede abrir com ela toda mensagem de cliente, prospect
ou parceiro com 3+ dias sem resposta nossa. Os detectores do painel (`comercial_regras.py`: 7/21 dias; `onboarding_regras.py`:
7/14) medem silêncio de CONTATO, que um "ok" do cliente já zera. Este mede o inverso: quem falou por último, e se foi ele.

Fonte: o literal das capturas, por conta (clientes, subprojetos, parceiros e prospects):
  `01 - contexto/Evolution/texto/AAAA-MM-DD - <Nome>.md`  e  `01 - contexto/OpenWA/texto/…`
Formato lido: `**HH:MM:SS · <Quem>:** <texto>` (o texto pode seguir em linhas abaixo, até a próxima mensagem).
O `sem_resposta_nossa` do `contexto.py` (Haiku, só do trecho novo) NÃO entra como fonte: é amostra de trecho, sem data
contínua; o literal já diz quem falou por último, sem LLM. (O campo segue servindo ao `contexto/` da conta.)

Regra, por conversa (chat id do cabeçalho `- Conversa:`; Evolution e OpenWA da mesma conversa se fundem):
  1. NOSSOS remetentes: o operador (qualquer variação), a automação da casa, e quem mais a equipe listar em NOSSOS. Todo o resto é "deles".
  2. Pega a ÚLTIMA mensagem da conversa. Se é nossa → nada pendente.
  3. Se é deles → o bloco final de mensagens deles, desde a nossa última mensagem. Dentro do bloco, só contam as que PEDEM
     resposta (regra abaixo). Sem nenhuma → nada pendente.
  4. Dias = hoje − data da PRIMEIRA mensagem que pede resposta do bloco (há quanto tempo ele espera). Alerta a partir de 3.

O que NÃO pede resposta (regra simples, por mensagem):
  · marcadores da captura: figurinha, reação, mensagem apagada;
  · texto só de emoji/pontuação;
  · texto curto (até 4 palavras) formado só de fórmulas de cortesia/ciência: ok, blz, beleza, certo, show, valeu, obrigado(a),
    vlw, top, perfeito, combinado, fechado, tmj, boa, massa, entendi, bom dia/tarde/noite, kkk… (lista `CORTESIA`, editável aqui).
  Pergunta ("?") nunca é cortesia. Imagem, documento, vídeo, áudio e contato PEDEM resposta (alguém mandou algo a nós);
  mídia sem baixar (`_voice [mídia …`) também. Erra para o lado de avisar: falso alerta custa um olhar, silêncio custa o cliente.

Uso:
  python3 -X utf8 sem_resposta.py --listar [--min 3] [--todas]     lista de hoje (padrão: só a partir de 3 dias)
  python3 -X utf8 sem_resposta.py --json                           payload (o painel-projetos.py importa `calcular`)
  python3 -X utf8 sem_resposta.py --conta "Nome"                   mostra o bloco pendente da conta, mensagem a mensagem
Só lê. Não envia nada, não escreve nada.
"""
import argparse, datetime as dt, json, os, re, sys, unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FUSO = dt.timezone(dt.timedelta(hours=-3))
LIMIAR = 3
TEXTO = "texto"
FONTES = ("Evolution", "OpenWA")

NOSSOS = re.compile(r"^\s*(operador|continuum)", re.I)   # ajuste aos nomes de quem fala por nós nas capturas
MSG = re.compile(r"^\*\*(\d{2}):(\d{2}):(\d{2}) · (.+?):\*\*\s?(.*)$")
CONVERSA = re.compile(r"^- Conversa:\s*`([^`]+)`")
DATA_ARQ = re.compile(r"^(20\d{2})-(\d{2})-(\d{2})")
MARCADOR_VAZIO = re.compile(r"^_?\[(figurinha|reação|reacao|mensagem apagada|mensagem apa)", re.I)
MIDIA = re.compile(r"^(🎙️|🖼️|📎|🩹|_voice|_image|_document|_video|_\[contato)")
RISADA = re.compile(r"^(k{1,}|(ha){2,}h?|(he){2,}|(rs){1,}|kkk+)$")
FORTES = {"ok", "okay", "blz", "beleza", "valeu", "vlw", "obg", "brigado", "brigada", "show", "perfeito", "combinado", "fechado",
          "tmj", "top", "massa", "entendi", "certo", "joia", "amem"}
CORTESIA = {
    "ok", "okay", "oks", "blz", "beleza", "certo", "certinho", "show", "valeu", "vlw", "obrigado", "obrigada", "obg", "brigado",
    "brigada", "top", "perfeito", "combinado", "fechado", "tmj", "boa", "massa", "entendi", "entendido", "otimo", "excelente",
    "sim", "isso", "tá", "ta", "tudo", "bem", "bom", "dia", "tarde", "noite", "kk", "kkk", "kkkk", "haha", "rs", "rsrs", "amem",
    "abraco", "abracos", "grato", "grata", "demais", "legal", "joia", "dahora", "ei", "opa", "ola", "oi", "e", "ai", "de", "nada",
    "por", "nada", "muito", "super", "mt", "grande", "irmao", "mano", "fica", "tranquilo", "tranquila", "sussa", "positivo",
}


def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def pede_resposta(texto):
    """True se a mensagem pede resposta nossa (regra no docstring)."""
    t = (texto or "").strip()
    if not t or MARCADOR_VAZIO.match(t):
        return False
    if "?" in t:
        return True
    if MIDIA.match(t):                            # áudio, imagem, documento, vídeo: mandaram algo a nós
        return True
    limpo = re.sub(r"https?://\S+", " ", t)
    pal = re.findall(r"[A-Za-zÀ-ú0-9]+", limpo)
    if not pal:                                   # só emoji / pontuação
        return False
    norm = [_sem_acento(p.lower()) for p in pal]
    if len(pal) <= 4 and all(p in CORTESIA or RISADA.match(p) for p in norm):
        return False
    # até 6 palavras com uma fórmula forte de ciência/agradecimento ou risada e sem pergunta ("Obrigado meu amor", "Deus me livre kkkk")
    if len(pal) <= 6 and any(p.startswith("obrigad") or p in FORTES or RISADA.match(p) for p in norm):
        return False
    return True


def _mensagens_do_arquivo(caminho, dia):
    """[(datetime, quem, texto)] e o chat id do arquivo. O corpo da mensagem vai até a próxima linha `**HH:MM:SS ·`."""
    try:
        with open(caminho, encoding="utf-8-sig", errors="replace") as f:
            linhas = f.read().splitlines()
    except OSError:
        return [], None
    chat, msgs, atual = None, [], None
    for ln in linhas:
        if chat is None:
            mc = CONVERSA.match(ln)
            if mc:
                chat = mc.group(1)
        m = MSG.match(ln)
        if m:
            h, mi, s, quem, resto = m.groups()
            atual = [dt.datetime(dia.year, dia.month, dia.day, int(h), int(mi), int(s)), quem.strip(), resto]
            msgs.append(atual)
        elif atual is not None and ln.strip() and not ln.startswith(("#", "- ")):
            atual[2] += " " + ln.strip().lstrip("> ")
    return [tuple(x) for x in msgs], chat


def mensagens_da_pasta(pasta):
    """{chave_da_conversa: {"nome": str, "msgs": [(datetime, quem, texto, fonte)]}} lendo Evolution e OpenWA da conta."""
    conv = {}
    for fonte in FONTES:
        base = os.path.join(pasta, "01 - contexto", fonte, TEXTO)
        if not os.path.isdir(base):
            continue
        for a in sorted(os.listdir(base)):
            m = DATA_ARQ.match(a)
            if not (m and a.endswith(".md")):
                continue
            try:
                dia = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                continue
            msgs, chat = _mensagens_do_arquivo(os.path.join(base, a), dia)
            nome = a[len(m.group(0)):].lstrip(" -").rsplit(".", 1)[0] or "?"
            chave = chat or "nome:" + nome.lower()
            c = conv.setdefault(chave, {"nome": nome, "msgs": []})
            c["msgs"] += [(d, q, t, fonte) for d, q, t in msgs]
    return conv


def _unicas(msgs):
    """Evolution e OpenWA capturam a mesma conversa: tira a repetição (mesma hora e mesmo remetente)."""
    visto, out = set(), []
    for d, q, t, f in sorted(msgs, key=lambda x: (x[0], x[3])):
        k = (d, _sem_acento(q.lower()))
        if k in visto:
            continue
        visto.add(k)
        out.append((d, q, t, f))
    return out


def analisar_conversa(msgs, agora):
    """-> dict(dias, desde, quem, trecho, n, fonte) ou None. msgs: [(datetime, quem, texto, fonte)]."""
    ms = _unicas(msgs)
    if not ms or NOSSOS.match(ms[-1][1]):
        return None
    bloco = []
    for x in reversed(ms):
        if NOSSOS.match(x[1]):
            break
        bloco.append(x)
    bloco.reverse()
    pedem = [x for x in bloco if pede_resposta(x[2])]
    if not pedem:
        return None
    d0 = pedem[0][0]
    dias = (agora.date() - d0.date()).days
    return dict(dias=dias, desde=d0.strftime("%Y-%m-%d %H:%M"), quem=pedem[0][1], n=len(pedem), fonte=pedem[0][3],
                ultima=bloco[-1][0].strftime("%Y-%m-%d %H:%M"),
                trecho=re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]\(<[^>]*>\)\s*(—\s*)?", "", pedem[0][2])).strip()[:140] or "(mídia)")


def _contas(raiz):
    """[(nome, pasta, tipo)]: clientes/subprojetos/parceiros pela regra da casa + fichas de prospect."""
    out = []
    try:
        import contas_da_casa
        for nome, pasta, _rel in contas_da_casa.contas(raiz):
            if contas_da_casa.eh_subprojeto(raiz, pasta):
                continue                     # a captura mora na conta-mãe; não duplica o alerta
            out.append((nome, pasta, "parceiro" if os.sep + "parceiros" + os.sep in pasta else "cliente"))
    except ImportError:
        cli = os.path.join(raiz, "clientes")
        for n in sorted(os.listdir(cli)) if os.path.isdir(cli) else []:
            if not n.startswith(("_", ".")) and os.path.isdir(os.path.join(cli, n)):
                out.append((n, os.path.join(cli, n), "cliente"))
    base = os.path.join(raiz, "30-comercial", "assessoria-prospects")
    for p in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        pasta = os.path.join(base, p)
        if os.path.isdir(pasta) and not p.startswith(("_", ".")):
            nome = p
            try:
                with open(os.path.join(pasta, "PAINEL.md"), encoding="utf-8-sig") as f:
                    mm = re.search(r"^prospect:\s*(.+)$", f.read(3000), re.M)
                if mm:
                    nome = mm.group(1).strip().strip("\"'")
            except OSError:
                pass
            out.append((nome, pasta, "prospect"))
    return out


def calcular(raiz=RAIZ, agora=None, minimo=LIMIAR):
    """Lista ordenada (mais antiga primeiro) de contas esperando resposta nossa há `minimo`+ dias. Uma linha por conversa."""
    agora = agora or dt.datetime.now(FUSO).replace(tzinfo=None)
    out = []
    for nome, pasta, tipo in _contas(raiz):
        convs = mensagens_da_pasta(pasta)
        # resposta nossa em QUALQUER conversa da conta, depois da dele, vale (a mesma pessoa tem chat individual e grupo)
        ultima_nossa = max((d for c in convs.values() for d, q, _t, _f in c["msgs"] if NOSSOS.match(q)), default=None)
        for chave, c in convs.items():
            r = analisar_conversa(c["msgs"], agora)
            if r and ultima_nossa and ultima_nossa.strftime("%Y-%m-%d %H:%M") > r["desde"]:
                continue
            if r and r["dias"] >= minimo:
                out.append(dict(r, conta=nome, tipo=tipo, conversa=c["nome"], chat=chave,
                                pasta=os.path.relpath(pasta, raiz).replace(os.sep, "/"),
                                texto=f"{r['quem']} espera resposta há {r['dias']} d — abrir com a régua do retorno atrasado",
                                ato="abrir com a régua do retorno atrasado (ARVORE-ESCRITA §7): falha nomeada, sem desculpa, mini bônus"))
    # a mesma conversa chega por dois ids (lid × telefone) nas duas capturas: uma linha por conta, quem e instante
    vistos, unicos = set(), []
    for x in sorted(out, key=lambda x: (-x["dias"], x["conta"])):
        k = (x["conta"], _sem_acento(x["quem"].lower()), x["desde"])
        if k not in vistos:
            vistos.add(k)
            unicos.append(x)
    return unicos


def por_conta(lista):
    """{nome_da_conta: pior_entrada} — o que o painel-projetos.py cola em cada conta."""
    d = {}
    for x in lista:
        if x["conta"] not in d or x["dias"] > d[x["conta"]]["dias"]:
            d[x["conta"]] = x
    return d


def nivel(dias):
    return "vermelho" if dias >= 7 else "amarelo"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min", type=int, default=LIMIAR, help="dias mínimos (padrão 3)")
    ap.add_argument("--todas", action="store_true", help="inclui de 0 a %d dias (conferência)" % (LIMIAR - 1))
    ap.add_argument("--conta", help="mostra o bloco pendente de uma conta")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    minimo = 0 if a.todas else a.min
    lista = calcular(minimo=minimo)
    if a.conta:
        lista = [x for x in lista if a.conta.lower() in x["conta"].lower()]
        for x in lista:
            print(f"{x['conta']} · {x['conversa']} · desde {x['desde']} ({x['dias']} d) · {x['n']} msg que pedem resposta · {x['fonte']}")
            print(f"  {x['quem']}: {x['trecho']}")
        if not lista:
            print("nada pendente (a última mensagem é nossa, não pede resposta, ou está abaixo do mínimo)")
        return
    if a.json:
        print(json.dumps(lista, ensure_ascii=False, indent=1))
        return
    print(f"# Esperando resposta nossa — {dt.datetime.now(FUSO):%d/%m/%Y %H:%M} · {len(lista)} conversa(s) · mínimo {minimo} d")
    for x in lista:
        print(f"{x['dias']:>3} d · {nivel(x['dias']):8} · {x['tipo']:8} · {x['conta']} / {x['conversa']} · desde {x['desde']} · "
              f"{x['quem']}: \"{x['trecho'][:80]}\"")


if __name__ == "__main__":
    main()
