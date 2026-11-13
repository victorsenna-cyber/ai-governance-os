#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capturar.py — captura das conversas de WhatsApp para o contexto de cada contato, via OpenWA local.

Tipo: ferramenta (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Alçada {{OPERADOR}} · etiquetas, três raízes, script por conversa
Intenção: o motor roda e o Claude capta os dados das conversas do {{OPERADOR}} para alimentar o repo,
em vez de ele printar, salvar áudios e transcrever à mão a cada vez. Cada tipo de arquivo fica numa pasta
paralela, em clientes/<cliente>/01 - contexto/OpenWA/texto, PDF, html, imagens e áudios, criada automaticamente
em cada pasta de cliente. A etiqueta é o interruptor (fácil de aplicar a qualquer momento) e há uma pasta com
1 script para cada grupo e cada pessoa individual, para capturar sem puxar tudo de todos.

Motor: OpenWA instalado fora da Governança (Docker, whatsapp-web.js, só 127.0.0.1).
Esta ferramenta SÓ LÊ o WhatsApp: nenhuma rota de envio, de etiqueta ou de conversa é escrita.

QUEM ENTRA: toda conversa com a etiqueta Cliente, Parceiro ou Prospect no WhatsApp Business (nomes
em `conversas.json` → "etiquetas"), mais as conversas postas à mão no mapa. Tirou a etiqueta, a
conversa para de ser capturada; o que já foi capturado fica.

ONDE CAI (a raiz pelo tipo de relação):
  cliente  → clientes/<Nome>/
  parceiro → parceiros/<Nome>/
  prospect → 30-comercial/assessoria-prospects/<nome>/
  <raiz>/<Nome>/01 - contexto/OpenWA/
    texto/AAAA-MM-DD - <conversa>.md   literal, horário de Brasília, áudio transcrito embutido
    áudios/ · imagens/ · PDF/ · html/  (vídeos/ · outros/ só quando aparece arquivo desse tipo)
    .estado.json                       cursor por conversa
A pasta do contato que não existe é criada com um README de abertura. A captura NUNCA cria
STATUS.md nem DECISOES.md: conta se abre pelo trilho de conta nova, por decisão. A estrutura
OpenWA/ nasce em todo cliente; em parceiro e prospect, só quando há conversa no mapa.

UM SCRIPT POR CONVERSA: `por-conversa/<Tipo> - <Pasta> - <conversa>.bat`, refeito a cada rodada.
Dois cliques capturam só aquela conversa.

LEITURA LEVE (alçada {{OPERADOR}}: não se captura tudo de todas as mensagens toda vez;
ler muitas conversas inteiras numa mesma rodada pode derrubar a conexão do WhatsApp pelo volume):
  - só lê a conversa que teve atividade depois do cursor (a lista de conversas diz a última atividade);
  - lê no máximo LIMITE_ROTINA mensagens por conversa, inclusive na 1ª captura;
  - histórico fundo (até 2.000) só com --historico, e só junto de --chat: uma conversa por vez;
  - pausa entre conversas e para a rodada depois de 2 falhas de conexão seguidas;
  - flag desconhecida para tudo antes de ler qualquer coisa (um --help ignorado virou rodada completa).

Uso (de qualquer lugar):
  python3 capturar.py                     captura o que é novo nas conversas do mapa e transcreve os áudios novos
  python3 capturar.py --chat <chatId>     só esta conversa (é o que os scripts por conversa rodam)
  python3 capturar.py --chat <chatId> --historico   histórico fundo desta conversa (até 2.000 mensagens)
  python3 capturar.py --so "<Pasta>"      só as conversas desta pasta
  python3 capturar.py --mapa              só atualiza o mapa pelas etiquetas, as pastas e os scripts
  python3 capturar.py --listar            lista as conversas da sessão (id, tipo, nome)
  python3 capturar.py --estrutura         só cria a estrutura OpenWA/ em todos os clientes
  python3 capturar.py --sem-transcrever   baixa os áudios e deixa a transcrição para a próxima rodada
  python3 capturar.py --desde AAAA-MM-DD  na 1ª captura de uma conversa, não volta antes desta data
  --modelo <nome>                    repassado ao transcrever-audio.py (padrão large-v3)

Chaves (fora do repositório): o script usa `OPENWA_KEY` ou `<OpenWA>/data/.api-key` (admin); a
chave do MCP do Claude (viewer, só as conversas do mapa) fica em `<OpenWA>/data/.mcp-key.json`.
"""
import base64, io, json, os, re, shutil, subprocess, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
GOV = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))          # raiz da Governança
CONTINUUM = os.path.dirname(os.path.dirname(GOV))                       # dois níveis acima da Governança
OPENWA = os.environ.get("OPENWA_DIR") or os.path.join(CONTINUUM, "repos-externos", "OpenWA")
URL = (os.environ.get("OPENWA_URL") or "http://127.0.0.1:2785").rstrip("/") + "/api"
MAPA = os.path.join(AQUI, "conversas.json")
POR_CONVERSA = os.path.join(AQUI, "por-conversa")
TRANSCREVER = os.path.join(GOV, "40-operacao-rotinas", "ferramentas", "transcrever-audio.py")

# 🔴 a tabela de raízes mora só aqui: quando a T1 reorganizar o repo, muda esta linha
RAIZES = {"cliente": os.path.join(GOV, "clientes"),
          "parceiro": os.path.join(GOV, "parceiros"),
          "prospect": os.path.join(GOV, "30-comercial", "assessoria-prospects")}
ETIQUETAS_PADRAO = {"Cliente": "cliente", "Parceiro": "parceiro", "Prospect": "prospect"}

BRT = timezone(timedelta(hours=-3))      # Brasil sem horário de verão desde 2019
PASTAS = ("texto", "PDF", "html", "imagens", "áudios")
RE_CONTEXTO = re.compile(r"^01\s*-\s*contexto$", re.I)
PENDENTE = re.compile(r"<!-- transcricao-pendente: (.+?) -->")
LIMITE_HISTORICO = 2000                  # teto do OpenWA com deep=true: só com --historico --chat
LIMITE_ROTINA = 50                       # teto de leitura por conversa em toda rodada, inclusive a 1ª
PAUSA = 3                                # segundos entre conversas, para não afogar o WhatsApp Web
FALHAS_PARA_PARAR = 2                    # falhas de conexão seguidas que encerram a rodada
VAZIAS = {"assessoria", "continuum", "ai", "grupo", "de", "da", "do", "das", "dos", "e", "x", "com",
          "paginas", "pagina", "vendas", "plano", "estrategico", "site", "projeto", "equipe", "time"}

def log(*a): print(*a, flush=True)

# ---------- API ----------

def chave():
    k = os.environ.get("OPENWA_KEY")
    if k: return k.strip()
    p = os.path.join(OPENWA, "data", ".api-key")
    if os.path.exists(p): return io.open(p, encoding="utf-8").read().strip()
    sys.exit(f"sem chave do OpenWA: nem OPENWA_KEY nem {p}")

def api(caminho, params=None, binario=False, tempo=120, metodo="GET", corpo=None):
    q_ = ("?" + urllib.parse.urlencode(params)) if params else ""
    h = {"X-API-Key": CHAVE}
    if corpo is not None: h["Content-Type"] = "application/json"
    req = urllib.request.Request(URL + caminho + q_, headers=h, method=metodo,
                                 data=json.dumps(corpo).encode("utf-8") if corpo is not None else None)
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(req, timeout=tempo) as r:
                corpo_r = r.read()
                return (corpo_r, r.headers.get("Content-Type", "")) if binario else json.loads(corpo_r.decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code != 429 or tentativa == 3: raise
            espera = int(e.headers.get("Retry-After") or 0) or 5 * (tentativa + 1)
            log(f"  limite de requisições do OpenWA (429): esperando {espera}s")
            time.sleep(espera)

def q(s): return urllib.parse.quote(s, safe="")

def sessao_pronta(preferida):
    """Espera a API e uma sessão em `ready` (o container reconecta a sessão sozinho ao subir)."""
    for i in range(45):
        try:
            ss = api("/sessions", tempo=10)
        except (urllib.error.URLError, ConnectionError, TimeoutError):
            if i == 0: log("esperando o OpenWA responder em", URL, "…")
            time.sleep(2); continue
        if preferida: ss = [s for s in ss if preferida in (s.get("id"), s.get("name"))]
        if not ss:
            sys.exit("nenhuma sessão no OpenWA. Abra o app OpenWA, crie a sessão e escaneie o QR.")
        prontas = [s for s in ss if s.get("status") == "ready"]
        if prontas: return prontas[0]
        st = ", ".join(f"{s.get('name')}={s.get('status')}" for s in ss)
        if any(s.get("status") in ("qr_ready", "action_required", "failed") for s in ss):
            sys.exit(f"sessão sem conexão ({st}). Abra o app OpenWA e reconecte pelo QR.")
        if i % 5 == 0: log("sessão ainda não pronta:", st)
        time.sleep(2)
    sys.exit("o OpenWA não ficou pronto em 90 s. Confira o Docker Desktop e o container openwa-api.")

# ---------- nomes ----------

def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")

def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s|&.-]", "", (s or "").casefold())).strip()

def tokens(s):
    return [t for t in re.split(r"[^a-z0-9]+", sem_acento(s).casefold()) if t]

def seguro(s, n=60):
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", s or "").strip().rstrip(".")
    return s[:n].strip() or "sem-nome"

def nome_de_pasta(chat, relacao):
    """Nome para a pasta nova: o do contato; de grupo, o nome sem 'Assessoria' e sem o que vem depois de '|' ou ' - '."""
    n = chat.get("name") or chat["id"].split("@")[0]
    if chat.get("isGroup"):
        n = re.split(r"\s+[|–-]\s+|\|", n)[0]
        n = re.sub(r"^\s*assessoria\s+", "", n, flags=re.I)
    n = seguro(re.sub(r"[^\w\s&.-]", "", n).strip())
    return "-".join(tokens(n)) if relacao == "prospect" else n   # prospect segue o padrão da pasta: minúsculas-com-hífen

# ---------- pastas ----------

def pastas_da_raiz(relacao):
    r = RAIZES[relacao]
    if not os.path.isdir(r): return []
    return sorted(d for d in os.listdir(r) if os.path.isdir(os.path.join(r, d)) and not d.startswith(("_", ".")))

def achar_pasta(chat, relacao):
    """Pasta existente do contato: na raiz do tipo; se não houver, nas outras (tipo divergente). Pelo 1º nome."""
    chave_nome = [t for t in tokens(chat.get("name")) if t not in VAZIAS]
    for r in [relacao] + [x for x in RAIZES if x != relacao]:
        cands = [d for d in pastas_da_raiz(r) if tokens(d) and tokens(d)[0] in chave_nome]
        if len(cands) == 1: return r, cands[0]
        if len(cands) > 1: return r, None   # ambíguo: não chuta
    return None, None

def pasta_contexto(base):
    """Usa a pasta de contexto que o contato já tem (01-contexto, 01- contexto…); sem ela, `01 - contexto`."""
    if os.path.isdir(base):
        for d in sorted(os.listdir(base)):
            if RE_CONTEXTO.match(d.strip()) and os.path.isdir(os.path.join(base, d)):
                return os.path.join(base, d)
    return os.path.join(base, "01 - contexto")

def estrutura(base):
    raiz = os.path.join(pasta_contexto(base), "OpenWA")
    for p in PASTAS:
        d = os.path.join(raiz, p)
        os.makedirs(d, exist_ok=True)
        if not os.listdir(d):  # git não guarda pasta vazia
            io.open(os.path.join(d, ".gitkeep"), "w").close()
    return raiz

def tirar_gitkeep(d):
    g = os.path.join(d, ".gitkeep")
    if os.path.exists(g) and len(os.listdir(d)) > 1: os.remove(g)

def abrir_pasta(relacao, pasta, conversa):
    """Pasta nova de contato: só o contexto e um README que diz que a conta NÃO foi aberta."""
    base = os.path.join(RAIZES[relacao], pasta)
    os.makedirs(base, exist_ok=True)
    estrutura(base)
    p = os.path.join(base, "README.md")
    if not os.path.exists(p):
        hoje = datetime.now(BRT)
        io.open(p, "w", encoding="utf-8", newline="\n").write(
            f"# {pasta}\n\n"
            f"- **Tipo:** {relacao}\n"
            f"- **Pasta aberta pela captura de WhatsApp em {hoje:%d/%m/%Y %H:%M}** "
            f"(`40-operacao-rotinas/ferramentas/openwa/capturar.py`), a partir da conversa *{conversa}*.\n"
            "- 🔴 **Conta NÃO aberta.** Esta pasta só guarda o contexto capturado em `01 - contexto/OpenWA/`. "
            "Não há `STATUS.md` nem `DECISOES.md` porque a máquina não abre conta: cliente se abre pelo trilho de conta nova "
            "(`100-métodos/METODO-TRILHO-DE-CONTA-NOVA.md`); parceiro e prospect, pelo registro do §11.1.\n")
    return base

# ---------- mapa: etiquetas + manual ----------

def carregar_mapa():
    m = json.load(io.open(MAPA, encoding="utf-8")) if os.path.exists(MAPA) else {}
    m.setdefault("sessao", ""); m.setdefault("etiquetas", dict(ETIQUETAS_PADRAO)); m.setdefault("conversas", [])
    for c in m["conversas"]:                     # formato antigo: "cliente": "<pasta>"
        if "cliente" in c and "pasta" not in c:
            c["pasta"] = c.pop("cliente"); c.setdefault("relacao", "cliente")
        c.setdefault("origem", "manual"); c.setdefault("ativa", True)
    return m

def salvar_mapa(m):
    io.open(MAPA, "w", encoding="utf-8", newline="\n").write(json.dumps(m, ensure_ascii=False, indent=2) + "\n")

def resolver_busca(chats, mapa):
    """Conversa posta à mão só com `busca` (o nome no WhatsApp): acha o chatId pelo nome."""
    for c in [c for c in mapa["conversas"] if not c.get("chatId") and c.get("busca")]:
        grupo = {"grupo": True, "privada": False}.get(c.get("tipo"))
        cands = [x for x in chats if grupo is None or bool(x.get("isGroup")) == grupo]
        b = norm(c["busca"])
        achados = [x for x in cands if norm(x.get("name")) == b] or [x for x in cands if norm(x.get("name")).startswith(b)]
        if len(achados) == 1:
            c["chatId"] = achados[0]["id"]; log(f"  mapa: {c['busca']} → {c['chatId']}")
        else:
            log(f"  ⚠️ mapa: '{c['busca']}' bate com {len(achados)} conversa(s); preencher o chatId à mão (--listar)")

def por_etiqueta(sessao, mapa):
    """Lê as etiquetas do WhatsApp Business e põe no mapa toda conversa marcada. Devolve avisos."""
    avisos = []
    try:
        labels = api(f"/sessions/{q(sessao)}/labels")
    except urllib.error.HTTPError as e:
        return [f"etiquetas indisponíveis (HTTP {e.code}): o número conectado é WhatsApp Business?"]
    alvo = {norm(k): v for k, v in mapa["etiquetas"].items()}
    marcadas = {}
    for lb in labels:
        rel = alvo.get(norm(lb.get("name")))
        if not rel: continue
        for ch in api(f"/sessions/{q(sessao)}/labels/{q(lb['id'])}/chats"):
            if ch["id"] in marcadas and marcadas[ch["id"]][0] != rel:
                avisos.append(f"{ch.get('name')}: duas etiquetas de tipo ({marcadas[ch['id']][0]} e {rel}); vale {marcadas[ch['id']][0]}")
                continue
            marcadas[ch["id"]] = (rel, ch)
    faltando = [k for k in mapa["etiquetas"] if norm(k) not in {norm(l.get("name")) for l in labels}]
    if faltando: avisos.append("etiqueta ainda não criada no WhatsApp: " + ", ".join(faltando))

    por_id = {c.get("chatId"): c for c in mapa["conversas"] if c.get("chatId")}
    for cid, (rel, ch) in marcadas.items():
        c = por_id.get(cid)
        if c:
            c["ativa"] = True
            if c.get("origem") == "manual": c["origem"] = "manual+etiqueta"
            if c.get("relacao") != rel:
                avisos.append(f"{c.get('nome')}: etiqueta diz {rel}, a pasta está em {c.get('relacao')} ({c.get('pasta')}); "
                              "promoção de tipo é decisão: mover a pasta à mão e corrigir 'relacao' no mapa")
            continue
        r_achada, pasta = achar_pasta(ch, rel)
        if r_achada and pasta is None:
            avisos.append(f"{ch.get('name')}: mais de uma pasta possível em {r_achada}; preencher 'pasta' no mapa à mão")
            mapa["conversas"].append({"chatId": cid, "relacao": rel, "pasta": "", "nome": ch.get("name"),
                                      "tipo": "grupo" if ch.get("isGroup") else "privada", "origem": "etiqueta", "ativa": True})
            continue
        if r_achada and r_achada != rel:
            avisos.append(f"{ch.get('name')}: etiqueta {rel}, mas a pasta existente está em {r_achada}/{pasta}; capturando lá")
            rel_final = r_achada
        elif r_achada:
            rel_final = rel
        else:
            rel_final, pasta = rel, nome_de_pasta(ch, rel)
            abrir_pasta(rel, pasta, ch.get("name"))
            avisos.append(f"pasta nova: {os.path.relpath(os.path.join(RAIZES[rel], pasta), GOV)} (conta não aberta)")
        mapa["conversas"].append({"chatId": cid, "relacao": rel_final, "pasta": pasta, "nome": ch.get("name"),
                                  "tipo": "grupo" if ch.get("isGroup") else "privada", "origem": "etiqueta", "ativa": True})
        log(f"  mapa: + {ch.get('name')} → {rel_final}/{pasta}")
    for c in mapa["conversas"]:
        if c.get("origem") == "etiqueta" and c.get("chatId") not in marcadas and c.get("ativa"):
            c["ativa"] = False; log(f"  mapa: etiqueta retirada, captura parada (o já capturado fica): {c.get('nome')}")
        elif c.get("origem") == "manual+etiqueta" and c.get("chatId") not in marcadas:
            c["origem"] = "manual"
    return avisos

def scripts_por_conversa(mapa):
    """Um .bat por conversa ativa: captura só aquela. Refeito a cada rodada; os de conversa inativa somem."""
    os.makedirs(POR_CONVERSA, exist_ok=True)
    quero = {}
    for c in mapa["conversas"]:
        if not (c.get("ativa") and c.get("chatId") and c.get("pasta")): continue
        nome = seguro(f"{c['relacao'].capitalize()} - {c['pasta']} - {c.get('nome') or c['chatId']}", 120) + ".bat"
        quero[nome] = ("@echo off\r\n"
                       "rem Gerado pelo capturar.py: captura so esta conversa. Nao editar: e refeito a cada rodada.\r\n"
                       f"rem {c.get('nome')} -> {c['relacao']}/{c['pasta']}\r\n"
                       f'call "%~dp0..\\capturar.bat" --chat "{c["chatId"]}"\r\n')
    for f in os.listdir(POR_CONVERSA):
        if f.endswith(".bat") and f not in quero: os.remove(os.path.join(POR_CONVERSA, f))
    for f, txt in quero.items():
        p = os.path.join(POR_CONVERSA, f)
        if not os.path.exists(p) or io.open(p, encoding="utf-8", newline="").read() != txt:
            io.open(p, "w", encoding="utf-8", newline="").write(txt)
    return len(quero)

def chave_mcp(ids):
    """Chave só leitura (viewer) limitada às conversas do mapa: é a que o Claude usa no MCP. Fica em data/, fora do repo."""
    p = os.path.join(OPENWA, "data", ".mcp-key.json")
    atual = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else None
    ids = sorted(set(ids))
    if atual and sorted(atual.get("allowedChats", [])) == ids: return
    if atual:
        api(f"/auth/api-keys/{q(atual['id'])}", metodo="PUT", corpo={"allowedChats": ids})
        log(f"chave do MCP atualizada: {len(ids)} conversa(s)")
    else:
        r = api("/auth/api-keys", metodo="POST", corpo={"name": "claude-mcp-leitura", "role": "viewer", "allowedChats": ids})
        atual = {"id": r["id"], "apiKey": r["apiKey"]}
        log(f"chave do MCP criada (viewer, {len(ids)} conversa(s)) em {p}")
    atual["allowedChats"] = ids
    io.open(p, "w", encoding="utf-8").write(json.dumps(atual, indent=2) + "\n")

def atualizar_mapa(sessao, mapa):
    chats = api(f"/sessions/{q(sessao)}/chats", {"limit": 1000})
    global ATIVIDADE   # última atividade de cada conversa: decide quem é lido na rodada
    ATIVIDADE = {c["id"]: c.get("timestamp") or 0 for c in chats if c.get("id")}
    resolver_busca(chats, mapa)
    avisos = por_etiqueta(sessao, mapa)
    salvar_mapa(mapa)
    n = scripts_por_conversa(mapa)
    ids = [c["chatId"] for c in mapa["conversas"] if c.get("chatId") and c.get("ativa")]
    if ids:
        try: chave_mcp(ids)
        except urllib.error.HTTPError as e: avisos.append(f"chave do MCP não sincronizada (HTTP {e.code})")
    sem_conta = sorted({f"{c['relacao']}/{c['pasta']}" for c in mapa["conversas"] if c.get("ativa") and c.get("pasta")
                        and c["relacao"] == "cliente" and not os.path.exists(os.path.join(RAIZES["cliente"], c["pasta"], "STATUS.md"))})
    if sem_conta: avisos.append("cliente com conversa e sem STATUS.md (conta não aberta): " + ", ".join(sem_conta))
    log(f"mapa: {len(ids)} conversa(s) ativa(s) · {n} script(s) em por-conversa/")
    return avisos

# ---------- mensagens ----------

EXT_MIME = {"audio/ogg": ".ogg", "audio/mpeg": ".mp3", "audio/mp4": ".m4a", "audio/aac": ".aac",
            "audio/wav": ".wav", "image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp",
            "image/gif": ".gif", "video/mp4": ".mp4", "video/3gpp": ".3gp", "video/quicktime": ".mov",
            "application/pdf": ".pdf", "text/html": ".html"}

def destino_tipo(tipo, mime, ext):
    mime = (mime or "").split(";")[0].strip().lower()
    if tipo in ("voice", "audio") or mime.startswith("audio/"): return "áudios"
    if tipo in ("image", "sticker") or mime.startswith("image/"): return "imagens"
    if tipo == "video" or mime.startswith("video/"): return "vídeos"
    if mime == "application/pdf" or ext == ".pdf": return "PDF"
    if mime in ("text/html", "application/xhtml+xml") or ext in (".html", ".htm"): return "html"
    return "outros"

def nome_arquivo(m, quando, mime, pasta, original=""):
    mime = (mime or "").split(";")[0].strip().lower()
    original = (original or "").strip()
    ext = os.path.splitext(original)[1].lower() or EXT_MIME.get(mime, "")
    carimbo = quando.strftime("%Y-%m-%d at %H.%M.%S")
    rotulo = {"voice": "Ptt", "audio": "Audio", "image": "Image", "video": "Video", "sticker": "Sticker"}.get(m.get("type"))
    if rotulo:   # mesmo padrão do export do WhatsApp: o transcrever-audio.py reconhece e não refaz o que já existe
        base = f"WhatsApp {rotulo} {carimbo}"
    else:
        base = f"{carimbo} - {seguro(os.path.splitext(original)[0] or m.get('type') or 'arquivo')}"
    nome, n = base + ext, 2
    while os.path.exists(os.path.join(pasta, nome)):
        nome, n = f"{base} ({n}){ext}", n + 1
    return nome, ext

def autor(m, conversa):
    if m.get("fromMe"): return "{{OPERADOR}}"
    c = m.get("contact") or {}
    if m.get("isGroup"):
        return c.get("name") or c.get("pushName") or c.get("shortName") or (m.get("author") or "").split("@")[0] or "?"
    return conversa.get("nome") or c.get("name") or c.get("pushName") or (m.get("from") or "").split("@")[0]

TIPOS_MIDIA = ("image", "video", "voice", "audio", "document")

class AoVivo:
    """Mídia que o OpenWA não guardou (chegou antes da conexão): baixada do WhatsApp na hora pelo
    history?includeMedia=true. Cada chamada tem orçamento (CHAT_HISTORY_MEDIA_BUDGET_BYTES), gasto da mais
    antiga para a mais nova; por isso as janelas crescem de 20 em 20 até achar todas. O teto do OpenWA são as
    100 mensagens mais recentes da conversa: mídia mais antiga que isso não baixa por aqui."""
    def __init__(self, sessao, chat_id, ids, ordem):
        self.sessao, self.chat_id, self.faltam, self.achadas, self.feito = sessao, chat_id, set(ids), {}, False
        self.ordem = ordem   # ids da conversa inteira, do mais antigo ao mais novo
    def _janela(self, k):
        try:
            ms = historico(self.sessao, self.chat_id, {"limit": k, "includeMedia": "true"})
        except Exception as e:
            log(f"  aviso: download ao vivo falhou ({type(e).__name__})"); return None
        for x in ms:
            md = x.get("media") or {}
            if x.get("id") in self.faltam and md.get("data"):
                self.achadas[x["id"]] = (base64.b64decode(md["data"]), md.get("mimetype") or "", md.get("filename"))
                self.faltam.discard(x["id"])
        return ms
    def pegar(self, mid):
        if not self.feito:
            self.feito = True
            # uma janela só, do tamanho das mensagens novas (janelas crescentes rebaixavam a mesma mídia)
            if self.faltam: self._janela(min(len(self.ordem), 100))
            # arquivo grande que ficou sem orçamento: uma janela que começa nele, para ele gastar primeiro
            for i in sorted((len(self.ordem) - self.ordem.index(x) for x in list(self.faltam) if x in self.ordem), reverse=True):
                if i <= 100 and self.ordem[-i] in self.faltam: self._janela(i)
        return self.achadas.get(mid)

CONECTADO = 0   # epoch da conexão da sessão: antes dela o OpenWA não guardou mídia nenhuma

def nome_original(m, nome_vivo=None):
    """Nome do arquivo: o da mídia; num documento sem ele, o corpo da mensagem (o WhatsApp põe o nome ali)."""
    n = nome_vivo or (m.get("media") or {}).get("filename") or ""
    corpo = (m.get("body") or "").strip()
    if not n and m.get("type") == "document" and corpo and "\n" not in corpo and len(corpo) < 150: n = corpo
    return n

def baixar(sessao, conversa, m, quando, raiz, aovivo):
    tipo = m.get("type")
    mime_meta = (m.get("media") or {}).get("mimetype", "")
    r, nome_vivo = None, None
    if m["timestamp"] >= CONECTADO:   # 1º: o que o OpenWA guardou (o que chegou depois da conexão)
        try:
            r = api(f"/sessions/{q(sessao)}/messages/{q(conversa['chatId'])}/{q(m['id'])}/media", binario=True)
        except urllib.error.HTTPError as e:
            if e.code not in (404, 429): return None, f"[mídia indisponível: HTTP {e.code}]"
        except Exception as e:
            return None, f"[mídia indisponível: {type(e).__name__}]"
    if not r:                          # 2º: baixar do WhatsApp na hora
        v = aovivo.pegar(m["id"])
        if not v: return None, "[mídia não baixável: anterior às 100 mensagens mais recentes da conversa, grande demais ou expirada no WhatsApp]"
        dados, mime, nome_vivo = v
    else:
        dados, mime = r
    mime = mime if mime and "octet-stream" not in mime else (mime_meta or mime)
    original = nome_original(m, nome_vivo)
    pasta = os.path.join(raiz, destino_tipo(tipo, mime, os.path.splitext(original)[1].lower()))
    os.makedirs(pasta, exist_ok=True)
    nome, _ = nome_arquivo(m, quando, mime, pasta, original)
    with open(os.path.join(pasta, nome), "wb") as f: f.write(dados)
    tirar_gitkeep(pasta)
    return os.path.join(pasta, nome), None

# 🔴 limpeza na entrada (10/11/2026: senha numa mensagem CITADA passou, porque este script não limpava nada;
# a limpeza vale para o corpo E para o texto citado). Mesmos padrões do evolution/puxar.py.
MARCA_SENHA = "[senha removida da captura]"
RE_SENHA = re.compile(r"(?i)\b(senha|password|passwd|pwd)\b\s*[:=.]?\s*[\"']?[^\s\"']{4,}")
RE_SENSIVEL = [
    re.compile(r"(?<![\d.])\d{3}\.\d{3}\.\d{3}-\d{2}(?!\d)"),
    re.compile(r"(?i)\bcpf\b\D{0,6}\d{11}(?!\d)"),
    re.compile(r"\b(ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{20,}"),
    re.compile(r"\bsk-(ant-)?[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{30,}"),
]

def limpar(texto):
    if not texto: return texto
    texto = RE_SENHA.sub(MARCA_SENHA, texto)
    for rx in RE_SENSIVEL: texto = rx.sub("[dado sensível removido]", texto)
    return texto

def linha(sessao, conversa, m, raiz, aovivo):
    quando = datetime.fromtimestamp(m["timestamp"], BRT)
    tipo, corpo = m.get("type") or "unknown", limpar((m.get("body") or "").strip())
    cab = f"**{quando:%H:%M:%S} · {autor(m, conversa)}:**"
    cit = limpar((m.get("quotedMessage") or {}).get("body"))
    pre = f"> ↪ _{cit.strip()[:200]}_\n\n" if cit else ""
    if tipo == "text":
        return pre + f"{cab} {corpo}"
    if tipo == "revoked":
        return f"{cab} _[mensagem apagada]_"
    if tipo == "call":
        return f"{cab} _[chamada de voz/vídeo]_"
    if tipo == "location":
        loc = m.get("location") or {}
        return f"{cab} _[localização {loc.get('latitude')}, {loc.get('longitude')}]_ {corpo}".rstrip()
    if tipo == "contact":
        return f"{cab} _[contato compartilhado]_ {corpo[:300]}".rstrip()
    if tipo == "poll":
        return f"{cab} _[enquete]_ {corpo}".rstrip()
    if tipo == "sticker":
        return f"{cab} _[figurinha]_"
    if tipo in TIPOS_MIDIA:
        arq, erro = baixar(sessao, conversa, m, quando, raiz, aovivo)
        if erro: return pre + f"{cab} _{tipo} {erro}_ {corpo}".rstrip()
        relp = os.path.relpath(arq, os.path.join(raiz, "texto")).replace("\\", "/")
        link = f"[{os.path.basename(arq)}](<{relp}>)"
        if tipo in ("voice", "audio"):
            md = os.path.splitext(relp)[0] + ".md"
            return pre + f"{cab} 🎙️ {link}\n\n<!-- transcricao-pendente: {md} -->"
        icone = {"image": "🖼️", "video": "🎬", "document": "📎"}[tipo]
        return pre + f"{cab} {icone} {link}" + (f" — {corpo}" if corpo and tipo != "document" else "")
    if not corpo: return None          # notificação de sistema (criptografia, entrou no grupo…)
    return f"{cab} _[{tipo}]_ {corpo}"

def historico(sessao, chat_id, params):
    ms = api(f"/sessions/{q(sessao)}/messages/{q(chat_id)}/history", params, tempo=300)
    return sorted(ms, key=lambda m: (m.get("timestamp") or 0, m.get("id") or ""))

def novas(sessao, chat_id, est, desde, fundo=False):
    primeira = not est.get("ultimo_ts")
    ms = historico(sessao, chat_id, {"limit": LIMITE_HISTORICO, "deep": "true"} if fundo else {"limit": LIMITE_ROTINA})
    corte, vistos = est.get("ultimo_ts", 0), set(est.get("ids", []))
    if not fundo and len(ms) >= LIMITE_ROTINA and ms[0].get("timestamp", 0) > corte:
        # não busca fundo sozinho: avisa a lacuna e quem quiser roda a conversa com --historico
        log(f"  ⚠️ {'1ª captura: só as últimas' if primeira else f'{LIMITE_ROTINA}+ mensagens desde o cursor, lidas as últimas'} "
            f"{LIMITE_ROTINA}; o que vem antes de "
            f"{datetime.fromtimestamp(ms[0]['timestamp'], BRT):%d/%m %H:%M} não foi lido. "
            f"Para completar: python3 capturar.py --chat \"{chat_id}\" --historico")
    if primeira and desde: corte = int(desde.timestamp()) - 1
    return [m for m in ms if m.get("timestamp") and not m.get("isStatusBroadcast")
            and (m["timestamp"] > corte or (m["timestamp"] == corte and m.get("id") not in vistos))]

def capturar(sessao, conversa, raiz, estado, desde, atividade=None, fundo=False):
    cid = conversa["chatId"]
    est = estado.setdefault(cid, {})
    if not fundo and atividade is not None and est.get("ultimo_ts") and atividade <= est["ultimo_ts"]:
        log(f"  {conversa.get('nome') or cid}: nada novo (sem leitura)"); return 0
    ms = novas(sessao, cid, est, desde, fundo)
    if not ms:
        log(f"  {conversa.get('nome') or cid}: nada novo"); return 0
    por_dia = {}
    aovivo = AoVivo(sessao, cid, [m["id"] for m in ms if m.get("type") in TIPOS_MIDIA],
                    [m["id"] for m in ms])   # as novas são sempre a cauda da conversa: a posição a partir do fim vale
    for m in ms:
        txt = linha(sessao, conversa, m, raiz, aovivo)
        if txt: por_dia.setdefault(datetime.fromtimestamp(m["timestamp"], BRT).date(), []).append(txt)
    nome_conv = seguro(conversa.get("nome") or cid.split("@")[0])
    for dia, linhas in sorted(por_dia.items()):
        p = os.path.join(raiz, "texto", f"{dia:%Y-%m-%d} - {nome_conv}.md")
        novo = not os.path.exists(p)
        with io.open(p, "a", encoding="utf-8", newline="\n") as f:
            if novo:
                f.write(f"# WhatsApp — {conversa.get('nome') or cid} — {dia:%d/%m/%Y}\n\n"
                        f"- Conversa: `{cid}`\n- Fonte: OpenWA local (`40-operacao-rotinas/ferramentas/openwa/capturar.py`)\n"
                        "- Horário de Brasília. Texto literal, sem edição; áudio transcrito pela máquina, "
                        "íntegra ao lado do áudio em `áudios/`.\n\n---\n\n")
            f.write("\n\n".join(linhas) + "\n\n")
    tirar_gitkeep(os.path.join(raiz, "texto"))
    ult = ms[-1]["timestamp"]
    est.update(ultimo_ts=ult, ids=[m["id"] for m in ms if m["timestamp"] == ult],
               capturado_em=datetime.now(BRT).isoformat(timespec="seconds"), nome=conversa.get("nome"))
    log(f"  {conversa.get('nome') or cid}: {len(ms)} mensagem(ns) em {len(por_dia)} dia(s)")
    return len(ms)

# ---------- transcrição embutida ----------

def texto_transcricao(md):
    corpo = io.open(md, encoding="utf-8").read().split("## Transcrição", 1)[-1]
    return " ".join(re.sub(r"^\[[\d:.]+ --> [\d:.]+\]\s*", "", l).strip()
                    for l in corpo.strip().splitlines() if l.strip()).strip()

def pendentes(raiz):
    """Áudios citados na conversa ainda sem .md ao lado (rodada anterior com --sem-transcrever ou interrompida)."""
    pasta, achados = os.path.join(raiz, "texto"), []
    for f in os.listdir(pasta):
        if f.endswith(".md"):
            for md in PENDENTE.findall(io.open(os.path.join(pasta, f), encoding="utf-8").read()):
                base = os.path.splitext(os.path.normpath(os.path.join(pasta, md)))[0]
                achados += [base + e for e in (".ogg", ".opus", ".m4a", ".mp3", ".wav", ".aac")
                            if os.path.exists(base + e) and not os.path.exists(base + ".md")]
    return achados

def ja_transcritos(fila):
    """O áudio capturado é uma 2ª cópia de um áudio que pode já ter sido transcrito à mão em outra pasta da conta.
    O transcrever-audio.py MOVERIA aquele .md para cá (git mv), tirando-o do lado do áudio original e quebrando
    quem o cita. Aqui ele é COPIADO, e o original fica onde está. Devolve só o que falta transcrever."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("transcrever_audio", TRANSCREVER)
    ta = importlib.util.module_from_spec(spec); spec.loader.exec_module(ta)
    faltam = []
    for a in fila:
        pasta, nome = os.path.dirname(a), os.path.basename(a)
        ex = ta.existente(pasta, nome)
        destino = os.path.splitext(a)[0] + ".md"
        if ex and ex[0] == "arquivo":
            shutil.copyfile(ex[1], destino)
            log(f"  já transcrito, copiado (original intacto): {ta.rel(ex[1])}")
        elif ex:
            io.open(destino, "w", encoding="utf-8", newline="\n").write(
                f"# Transcrição — {os.path.splitext(nome)[0]}\n\n- Já transcrito dentro de `{ta.rel(ex[1])}` (não refeito).\n\n"
                f"## Transcrição\n\n[já transcrito em {ta.rel(ex[1])}]\n")
            log(f"  já transcrito dentro de {ta.rel(ex[1])}: apontado, não refeito")
        else:
            faltam.append(a)
    return faltam

def embutir(raiz):
    pasta, n = os.path.join(raiz, "texto"), 0
    for f in os.listdir(pasta):
        if not f.endswith(".md"): continue
        p = os.path.join(pasta, f)
        s = io.open(p, encoding="utf-8").read()
        if "transcricao-pendente" not in s: continue
        def troca(mt):
            nonlocal n
            md = os.path.normpath(os.path.join(pasta, mt.group(1)))
            if not os.path.exists(md): return mt.group(0)
            n += 1
            return f"> {texto_transcricao(md) or '[áudio sem fala reconhecida]'}"
        s2 = PENDENTE.sub(troca, s)
        if s2 != s: io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
    return n

# ---------- main ----------

def tirar(args, flag, com_valor=False):
    if flag not in args: return (None if com_valor else False), args
    i = args.index(flag)
    if com_valor: return args[i + 1], args[:i] + args[i + 2:]
    return True, args[:i] + args[i + 1:]

MODOS = ("--estrutura", "--listar", "--mapa")

def main(args):
    global CHAVE
    if "--help" in args or "-h" in args:
        log(__doc__); return
    so, args = tirar(args, "--so", True)
    chat, args = tirar(args, "--chat", True)
    desde, args = tirar(args, "--desde", True)
    modelo, args = tirar(args, "--modelo", True)
    sem_transcrever, args = tirar(args, "--sem-transcrever")
    fundo, args = tirar(args, "--historico")
    # 🔴 nada desconhecido passa (um --help virou rodada completa e derrubou a conexão)
    if len(args) > 1 or (args and args[0] not in MODOS):
        sys.exit(f"argumento desconhecido: {' '.join(args)}\nnada foi lido. Uso: python3 capturar.py --help")
    if fundo and not chat:
        sys.exit("--historico só vale com --chat <chatId>: histórico fundo é uma conversa por vez.")
    desde = datetime.strptime(desde, "%Y-%m-%d").replace(tzinfo=BRT) if desde else None

    for c in pastas_da_raiz("cliente"): estrutura(os.path.join(RAIZES["cliente"], c))
    if not os.path.isdir(RAIZES["parceiro"]):
        os.makedirs(RAIZES["parceiro"])
        io.open(os.path.join(RAIZES["parceiro"], "README.md"), "w", encoding="utf-8", newline="\n").write(
            "# parceiros/\n\nUma pasta por parceiro estratégico, no mesmo molde de `clientes/` "
            "(pasta vazia no início). A captura de WhatsApp abre a pasta de quem tem a "
            "etiqueta **Parceiro**, só com `01 - contexto/OpenWA/` e um README; o registro da relação segue o §11.1.\n")
    if args[:1] == ["--estrutura"]:
        log(f"estrutura OpenWA conferida em {len(pastas_da_raiz('cliente'))} clientes"); return

    CHAVE = chave()
    mapa = carregar_mapa()
    sessao = sessao_pronta(mapa.get("sessao") or None)
    log(f"sessão {sessao.get('name')} ({sessao.get('phone') or '?'}) pronta")
    global CONECTADO
    try: CONECTADO = int(datetime.fromisoformat((sessao.get("connectedAt") or "").replace("Z", "+00:00")).timestamp())
    except ValueError: CONECTADO = 0

    if args[:1] == ["--listar"]:
        chats = api(f"/sessions/{q(sessao['id'])}/chats", {"limit": 1000})
        mapeados = {c.get("chatId") for c in mapa["conversas"] if c.get("ativa")}
        log("| mapeada | tipo | chatId | nome | última atividade |\n|---|---|---|---|---|")
        for c in sorted(chats, key=lambda c: -(c.get("timestamp") or 0)):
            ult = datetime.fromtimestamp(c["timestamp"], BRT).strftime("%d/%m/%Y %H:%M") if c.get("timestamp") else "—"
            log(f"| {'✅' if c['id'] in mapeados else ''} | {'grupo' if c.get('isGroup') else 'privada'} | `{c['id']}` | {c.get('name') or ''} | {ult} |")
        return

    avisos = atualizar_mapa(sessao["id"], mapa)
    if args[:1] == ["--mapa"]:
        for a in avisos: log("⚠️", a)
        return

    conversas = [c for c in mapa["conversas"] if c.get("ativa") and c.get("chatId") and c.get("pasta")]
    if so: conversas = [c for c in conversas if c["pasta"] == so]
    if chat: conversas = [c for c in conversas if c["chatId"] == chat]
    if not conversas:
        for a in avisos: log("⚠️", a)
        log("nenhuma conversa para capturar. Ponha a etiqueta Cliente, Parceiro ou Prospect na conversa, no WhatsApp."); return

    total, raizes, lidas, falhas = 0, {}, 0, 0
    for chave_p in sorted({(c["relacao"], c["pasta"]) for c in conversas}):
        if falhas >= FALHAS_PARA_PARAR: break
        rel, pasta = chave_p
        base = os.path.join(RAIZES[rel], pasta)
        if not os.path.isdir(base): abrir_pasta(rel, pasta, pasta)
        raiz = estrutura(base); raizes[chave_p] = raiz
        pe = os.path.join(raiz, ".estado.json")
        est = json.load(io.open(pe, encoding="utf-8")) if os.path.exists(pe) else {}
        log(f"{rel}/{pasta}:")
        for conv in [c for c in conversas if (c["relacao"], c["pasta"]) == chave_p]:
            if falhas >= FALHAS_PARA_PARAR:
                log(f"🔴 {falhas} falhas de conexão seguidas: rodada parada para não derrubar o WhatsApp. "
                    "Confira o celular e o app OpenWA; o que não foi lido entra na próxima rodada."); break
            ativ = ATIVIDADE.get(conv["chatId"])
            vai_ler = fundo or not (ativ is not None and est.get(conv["chatId"], {}).get("ultimo_ts")
                                    and ativ <= est[conv["chatId"]]["ultimo_ts"])
            if vai_ler and lidas: time.sleep(PAUSA)
            try:
                total += capturar(sessao["id"], conv, raiz, est, desde, ativ, fundo)
                falhas = 0
            except urllib.error.HTTPError as e:
                log(f"  {conv.get('nome') or conv['chatId']}: falhou (HTTP {e.code}: {e.read()[:200]!r})")
                if e.code >= 500: falhas += 1
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                log(f"  {conv.get('nome') or conv['chatId']}: falhou ({type(e).__name__})"); falhas += 1
            finally:   # grava o cursor a cada conversa: queda no meio não duplica o que já foi escrito
                io.open(pe, "w", encoding="utf-8", newline="\n").write(json.dumps(est, ensure_ascii=False, indent=2) + "\n")
            if vai_ler: lidas += 1

    fila = list(dict.fromkeys(a for r in raizes.values() for a in pendentes(r)))
    if fila and not sem_transcrever: fila = ja_transcritos(fila)
    if fila and not sem_transcrever:
        log(f"transcrevendo {len(fila)} áudio(s) (local, faster-whisper)…")
        cmd = [sys.executable, TRANSCREVER] + (["--modelo", modelo] if modelo else []) + fila
        subprocess.run(cmd, cwd=GOV)
    embutidas = sum(embutir(r) for r in raizes.values())
    for a in avisos: log("⚠️", a)
    log(f"fim: {total} mensagem(ns) nova(s) · {embutidas} transcrição(ões) embutida(s) na conversa")

if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try: s.reconfigure(encoding="utf-8")
        except Exception: pass
    CHAVE = None
    ATIVIDADE = {}
    main(sys.argv[1:])
