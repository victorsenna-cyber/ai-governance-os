"""Painel de resultado: servidor local que grava os dados de cada cliente no repo.

    python3 servir.py            # abre o painel (é o que o atalho da área de trabalho roda)
    python3 servir.py --atalho    # cria o atalho "Painel de Resultado" na área de trabalho

Os dados de cada cliente moram na pasta de tráfego dele: clientes/<Cliente>/NN - tráfego pago/painel.json
(ou NN - mídia paga, conforme o nome da pasta).
Depois de cada gravação, e de 90 s sem outra, roda o sincronizar.py (commit e push para a main).
Só escuta em 127.0.0.1. Se o painel já estiver aberto, só abre outra janela. Fecha sozinho
10 min depois de a última janela do painel ser fechada.

Compartilhar com o cliente: publica uma página só com os números dele, só leitura, em
https://{{DOMINIO}}/painel-resultado/c/<código>/ pela API da Hostinger. O token da API
fica em ~/.continuum/hostinger-token.txt (ou na variável HOSTINGER_API_TOKEN), nunca no repo.
A página do cliente se republica sozinha 15 s depois de cada leitura nova dele.
"""
import datetime
import json
import os
import re
import secrets
import socket
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]                      # raiz da Governança
CLIENTES = RAIZ / "clientes"                # cada cliente tem a pasta dele; o painel.json mora na de tráfego
SINCRONIZAR = RAIZ / "40-operacao-rotinas" / "ferramentas" / "sincronizar.py"
ICONE = AQUI / "icone.ico"  # opcional: a empresa põe o dela aqui
PORTA = 8765
ID_OK = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")
PASTA_TRAFEGO = re.compile(r"^(\d+) - (tráfego pago|mídia paga)$")
# id do painel (primeira palavra do nome, sem acento) -> pasta do cliente em clientes/. Cliente fora daqui é achado
# pela mesma regra do id; se a pasta não existir, é criada com o nome digitado no painel.
PASTA_DO_ID = {}  # id do painel -> nome da pasta em clientes/ (preencher por conta)  # id do painel → nome da pasta em clientes/ (preencher por conta)
ESPERA_SYNC = 90       # segundos sem gravação antes de sincronizar
ESPERA_PUBLICAR = 15   # segundos depois de uma leitura antes de republicar a página do cliente
OCIOSO = 600           # segundos sem nenhuma janela aberta antes de encerrar

CONTA, DOMINIO = "{{HOSTINGER_CONTA}}", "{{DOMINIO}}"
SITE = f"https://{DOMINIO}/painel-resultado/c/"
API = "https://developers.hostinger.com/api/hosting/v1/files/upload-urls"
TOKEN_ARQ = Path.home() / ".continuum" / "hostinger-token.txt"
# A Cloudflare da Hostinger barra o agente padrão do Python (erro 1010): o painel se identifica como navegador.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ContinuumPainel/1.0"
# O que vai para a página do cliente: só os dados dele, nada do controle interno.
PUBLICO = ("nome", "ticket", "tipo", "assessoria", "teto", "verbaDia", "horizonte", "metas", "leituras")

estado = {"ultimo_pulso": time.time(), "sync": "nada gravado ainda nesta sessão", "pendente": None}
compart = {}           # cid -> {"erro": str|None}; o resto mora no painel.json
trava = threading.Lock()
trava_arq = threading.Lock()
timers = {}


def id_de(nome):
    """Id do painel: primeira palavra do nome, sem acento, em minúsculas."""
    base = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9-]", "", (base.split() or [""])[0])


def pastas_trafego(cliente):
    return sorted(p for p in cliente.iterdir() if p.is_dir() and PASTA_TRAFEGO.match(p.name))


def clientes_com_painel():
    """Percorre clientes/<Cliente>/NN - tráfego pago|mídia paga/painel.json e devolve (id, arquivo)."""
    achados = []
    if not CLIENTES.is_dir():
        return achados
    for cli in sorted(p for p in CLIENTES.iterdir() if p.is_dir()):
        cid = next((i for i, n in PASTA_DO_ID.items() if n == cli.name), None) or id_de(cli.name)
        for pasta in pastas_trafego(cli):
            if (pasta / "painel.json").exists():
                achados.append((cid, pasta / "painel.json"))
                break
    return achados


def achar_arq(cid):
    return next((arq for i, arq in clientes_com_painel() if i == cid), None)


def destino_novo(cid, nome=None):
    """Onde gravar o painel.json de um cliente que ainda não tem: a pasta de tráfego dele (criada se faltar)."""
    cli = CLIENTES / PASTA_DO_ID[cid] if cid in PASTA_DO_ID else None
    if cli is None and CLIENTES.is_dir():
        cli = next((p for p in sorted(CLIENTES.iterdir()) if p.is_dir() and id_de(p.name) == cid), None)
    if cli is None:
        limpo = re.sub(r'[<>:"/\\|?*]', "", str(nome or cid)).strip() or cid
        cli = CLIENTES / limpo
    pastas = pastas_trafego(cli) if cli.is_dir() else []
    if pastas:
        return pastas[0] / "painel.json"
    usados = [int(m.group(1)) for p in (cli.iterdir() if cli.is_dir() else []) if (m := re.match(r"^(\d+) - ", p.name))]
    return cli / f"{max(usados, default=0) + 1:02d} - tráfego pago" / "painel.json"


def existe(cid):
    return bool(cid) and achar_arq(cid) is not None


def ler(cid):
    arq = achar_arq(cid)
    if arq is None:
        raise FileNotFoundError(cid)
    return json.loads(arq.read_text(encoding="utf-8"))


def escrever(cid, dados):
    arq = achar_arq(cid) or destino_novo(cid, dados.get("nome"))
    arq.parent.mkdir(parents=True, exist_ok=True)
    tmp = arq.with_name("painel.json.tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, arq)


def ler_clientes():
    saida = []
    for cid, arq in clientes_com_painel():
        try:
            dados = json.loads(arq.read_text(encoding="utf-8"))
            dados["id"] = cid
            saida.append(dados)
        except (OSError, ValueError):
            continue
    return saida


def gravar(cid, corpo):
    with trava_arq:
        corpo.pop("id", None)
        corpo.pop("compartilhar", None)
        try:  # o compartilhamento é do servidor: a página nunca o sobrescreve
            antigo = ler(cid).get("compartilhar")
        except (OSError, ValueError):
            antigo = None
        if antigo:
            corpo["compartilhar"] = antigo
        escrever(cid, corpo)


def agendar_sync(motivo):
    with trava:
        estado["pendente"] = (time.time() + ESPERA_SYNC, motivo)
        estado["sync"] = f"gravado no repo · sincroniza com a main em {ESPERA_SYNC} s"


def laco_sync():
    while True:
        time.sleep(5)
        with trava:
            pend = estado["pendente"]
            if not pend or time.time() < pend[0]:
                continue
            estado["pendente"] = None
            motivo = pend[1]
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        exe = sys.executable.replace("pythonw.exe", "python.exe")
        try:
            r = subprocess.run([exe, str(SINCRONIZAR), "-m", f"painel: {motivo}"], cwd=RAIZ, capture_output=True,
                               text=True, encoding="utf-8", errors="replace", env=env, timeout=300,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            linha = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["sem saída"])[-1]
        except Exception as e:  # noqa: BLE001 — qualquer falha vira aviso na tela, nunca derruba o servidor
            linha = f"falhou: {e}"
        with trava:
            estado["sync"] = linha


def laco_ocioso(servidor):
    while True:
        time.sleep(30)
        with trava:
            parado = time.time() - estado["ultimo_pulso"] > OCIOSO and not estado["pendente"] and not timers
        if parado:
            servidor.shutdown()
            return


# ---------- compartilhar com o cliente ----------
def token():
    t = os.environ.get("HOSTINGER_API_TOKEN", "").strip()
    if not t and TOKEN_ARQ.exists():
        t = TOKEN_ARQ.read_text(encoding="utf-8").strip()
    return t


def salvar_token(t):
    TOKEN_ARQ.parent.mkdir(exist_ok=True)
    TOKEN_ARQ.write_text(t.strip() + "\n", encoding="utf-8")


# ---------- dados da Meta (Marketing API) ----------
GRAPH = "https://graph.facebook.com/v21.0"
META_ARQ = Path.home() / ".continuum" / "meta-token.txt"
ACAO_CONVERSA = "onsite_conversion.messaging_conversation_started_7d"
ACOES_COMPRA = ("offsite_conversion.fb_pixel_purchase", "purchase")


def token_meta():
    t = os.environ.get("META_API_TOKEN", "").strip()
    if not t and META_ARQ.exists():
        t = META_ARQ.read_text(encoding="utf-8").strip()
    return t


def salvar_token_meta(t):
    META_ARQ.parent.mkdir(exist_ok=True)
    META_ARQ.write_text(t.strip() + "\n", encoding="utf-8")


def graph(caminho, params, t):
    url = f"{GRAPH}/{caminho}?" + urllib.parse.urlencode({**params, "access_token": t})
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode("utf-8") or "{}").get("error", {})
        except ValueError:
            err = {}
        raise RuntimeError(f"Meta {err.get('code', e.code)}: {err.get('message', 'sem mensagem')}") from e


def valor_acao(lista, tipos):
    for a in lista or []:
        if a.get("action_type") in tipos:
            return float(a.get("value") or 0)
    return 0.0


def montar_leitura(resp, tipo, hoje=None):
    """Transforma a resposta de insights na leitura acumulada de hoje (sem vendas de conversa)."""
    hoje = hoje or datetime.date.today()
    linhas = resp.get("data") or []
    if not linhas:
        raise RuntimeError("a Meta não devolveu dados para esta conta/campanha")
    gasto = sum(float(x.get("spend") or 0) for x in linhas)
    inicio = min(x.get("date_start") or hoje.isoformat() for x in linhas)
    dias = max(1, (hoje - datetime.date.fromisoformat(inicio)).days)
    acoes = [a for x in linhas for a in (x.get("actions") or [])]
    leitura = {"data": hoje.isoformat(), "dias": dias, "gasto": round(gasto, 2), "origem": "meta"}
    if tipo == "site":
        leitura["conversas"] = int(sum(valor_acao(x.get("actions"), ACOES_COMPRA) for x in linhas))
        leitura["vendas"] = leitura["conversas"]
        leitura["custo"] = round(gasto / leitura["conversas"], 2) if leitura["conversas"] else 0
    else:
        conv = int(sum(valor_acao(x.get("actions"), (ACAO_CONVERSA,)) for x in linhas))
        leitura["conversas"] = conv
        leitura["custo"] = round(gasto / conv, 2) if conv else 0
    return leitura


def buscar_meta(cid, t=None):
    t = t or token_meta()
    if not t:
        raise RuntimeError("falta o token da Meta")
    with trava_arq:
        dados = ler(cid)
    conta = re.sub(r"\D", "", str(dados.get("metaConta") or ""))
    if not conta:
        raise RuntimeError("cliente sem conta de anúncios")
    params = {"level": "account", "date_preset": "maximum", "fields": "spend,actions,cost_per_action_type,date_start"}
    camps = [str(c).strip() for c in dados.get("metaCampanhas") or [] if str(c).strip()]
    if camps:
        params["filtering"] = json.dumps([{"field": "campaign.id", "operator": "IN", "value": camps}])
    nova = montar_leitura(graph(f"act_{conta}/insights", params, t), dados.get("tipo"))
    with trava_arq:
        dados = ler(cid)
        ls = dados.get("leituras") or []
        hoje = next((l for l in ls if l.get("data") == nova["data"]), None)
        if hoje:
            nova["id"] = hoje.get("id") or secrets.token_hex(6)
            nova["vendas"] = hoje.get("vendas", 0)
            ls = [l for l in ls if l is not hoje]
        else:
            ant = max(ls, key=lambda l: l.get("data", ""), default=None)
            nova["id"] = secrets.token_hex(6)
            nova["vendas"] = (ant or {}).get("vendas", 0)
        if dados.get("tipo") == "site":
            nova["vendas"] = nova["conversas"]
        dados["leituras"] = ls + [nova]
        escrever(cid, dados)
    agendar_sync(f"dados da Meta de {dados.get('nome', cid)}")
    if (dados.get("compartilhar") or {}).get("codigo") and token():
        agendar_publicacao(cid)
    return nova


def atualizar_meta():
    erros, feitos = {}, []
    for c in ler_clientes():
        if not c.get("metaConta"):
            continue
        try:
            buscar_meta(c["id"])
            feitos.append(c["id"])
        except Exception as e:  # noqa: BLE001
            erros[c["id"]] = f"{c.get('nome', c['id'])}: {e}"
    return {"atualizados": feitos, "erros": erros}


def pedir_upload_url(t=None):
    req = urllib.request.Request(API, data=json.dumps({"username": CONTA, "domain": DOMINIO}).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {t or token()}", "Content-Type": "application/json", "User-Agent": UA,
                                          "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode("utf-8") or "{}").get("message", "")
        except ValueError:
            msg = ""
        motivo = f" (Hostinger {e.code}{': ' + msg if msg else ''})"
        if e.code in (401, 403):
            raise RuntimeError("a Hostinger recusou o token" + motivo) from e
        raise RuntimeError("a Hostinger não liberou o envio" + motivo) from e


def subir(caminho, dados):
    j = pedir_upload_url()
    base = {"X-Auth": j["auth_key"], "X-Auth-Rest": j["rest_auth_key"], "Tus-Resumable": "1.0.0", "User-Agent": UA}
    alvo = f"{j['url']}/{caminho}"
    for metodo, extra, corpo, esperado in (
            ("POST", {"Upload-Length": str(len(dados)), "Upload-Offset": "0"}, b"", 201),
            ("PATCH", {"Upload-Offset": "0", "Content-Type": "application/offset+octet-stream"}, dados, 204)):
        req = urllib.request.Request(alvo + ("?override=true" if metodo == "POST" else ""), data=corpo,
                                     method=metodo, headers={**base, **extra})
        with urllib.request.urlopen(req, timeout=60) as r:
            if r.status != esperado:
                raise RuntimeError(f"envio para o site falhou ({metodo} {r.status})")


def pagina_cliente(cid, dados):
    html = (AQUI / "index.html").read_text(encoding="utf-8")
    publico = {k: dados[k] for k in PUBLICO if k in dados}
    publico["id"] = cid
    bloco = json.dumps(publico, ensure_ascii=False).replace("</", "<\\/")
    marca = "<script>\n// ---------- utilidades"
    if html.count(marca) != 1:
        raise RuntimeError("não achei onde embutir os dados na página")
    html = html.replace(marca, f'<script id="dados-cliente" type="application/json">{bloco}</script>\n{marca}', 1)
    return html.replace('"logo-continuum.png"', '"../../logo-continuum.png"').encode("utf-8")


def publicar(cid):
    with trava_arq:
        dados = ler(cid)
        comp = dict(dados.get("compartilhar") or {})
    if not comp.get("codigo"):
        comp = {"codigo": secrets.token_hex(8), "desde": datetime.date.today().isoformat()}
    subir(f"painel-resultado/c/{comp['codigo']}/index.html", pagina_cliente(cid, dados))
    comp["atualizado"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    with trava_arq:
        dados = ler(cid)
        dados["compartilhar"] = comp
        escrever(cid, dados)
    compart[cid] = {"erro": None}
    agendar_sync(f"página do cliente {cid} publicada")
    return SITE + comp["codigo"] + "/"


def parar(cid):
    with trava_arq:
        comp = ler(cid).get("compartilhar")
    if comp and comp.get("codigo"):
        aviso = ('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
                 '<title>Link desativado</title><body style="background:#030303;color:#B5B5B5;font-family:system-ui;'
                 'display:grid;place-items:center;height:100vh;margin:0"><p>Este link foi desativado. Peça um novo à {{EMPRESA}}.</p>')
        subir(f"painel-resultado/c/{comp['codigo']}/index.html", aviso.encode("utf-8"))
    with trava_arq:
        dados = ler(cid)
        dados.pop("compartilhar", None)
        escrever(cid, dados)
    compart.pop(cid, None)
    agendar_sync(f"compartilhamento de {cid} desativado")


def agendar_publicacao(cid):
    def rodar():
        timers.pop(cid, None)
        try:
            publicar(cid)
        except Exception as e:  # noqa: BLE001
            compart[cid] = {"erro": str(e)}
    if cid in timers:
        timers[cid].cancel()
    timers[cid] = threading.Timer(ESPERA_PUBLICAR, rodar)
    timers[cid].daemon = True
    timers[cid].start()


class Painel(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def responder(self, codigo, corpo=b"", tipo="application/json; charset=utf-8"):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def json(self, obj, codigo=200):
        self.responder(codigo, json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def corpo(self):
        try:
            c = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0) or 0)).decode("utf-8") or "{}")
            return c if isinstance(c, dict) else None
        except ValueError:
            return None

    def cid(self, prefixo):
        m = re.fullmatch(re.escape(prefixo) + r"([^/]+)", self.path)
        return m.group(1) if m and ID_OK.match(m.group(1)) else None

    def do_GET(self):
        with trava:
            estado["ultimo_pulso"] = time.time()
        if self.path in ("/", "/index.html"):
            self.responder(200, (AQUI / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/logo-continuum.png":
            logo = AQUI / "logo-continuum.png"  # opcional: a empresa põe o dela aqui
            self.responder(200, logo.read_bytes() if logo.exists() else b"", "image/png")
        elif self.path == "/api/clientes":
            self.json(ler_clientes())
        elif self.path == "/api/config":
            self.json({"token": bool(token()), "meta": bool(token_meta())})
        elif self.path == "/api/estado":
            with trava:
                self.json({"sync": estado["sync"], "pendente": bool(estado["pendente"])})
        elif self.path.startswith("/api/compartilhar/"):
            cid = self.cid("/api/compartilhar/")
            if not existe(cid):
                return self.json({"erro": "cliente não encontrado"}, 404)
            comp = ler(cid).get("compartilhar") or {}
            self.json({"url": SITE + comp["codigo"] + "/" if comp.get("codigo") else None, "atualizado": comp.get("atualizado"),
                       "erro": (compart.get(cid) or {}).get("erro"), "token": bool(token())})
        else:
            self.responder(404, b"{}")

    def do_POST(self):
        corpo = self.corpo()
        if self.path == "/api/token":
            t = str((corpo or {}).get("token", "")).strip()
            if not t:
                return self.json({"erro": "Cole o token."}, 400)
            try:
                pedir_upload_url(t)  # confere com a Hostinger antes de salvar
            except Exception as e:  # noqa: BLE001
                return self.json({"erro": f"Token não salvo: {e}."}, 400)
            salvar_token(t)
            return self.json({"ok": True})
        if self.path == "/api/token-meta":
            t = str((corpo or {}).get("token", "")).strip()
            if not t:
                return self.json({"erro": "Cole o token."}, 400)
            try:
                graph("me", {}, t)  # confere com a Meta antes de salvar
            except Exception as e:  # noqa: BLE001
                return self.json({"erro": f"Token não salvo: {e}."}, 400)
            salvar_token_meta(t)
            return self.json({"ok": True})
        if self.path == "/api/meta/atualizar":
            if not token_meta():
                return self.json({"erro": "falta o token da Meta (Configurações)"}, 400)
            return self.json(atualizar_meta())
        cid = self.cid("/api/compartilhar/")
        if not existe(cid) or corpo is None:
            return self.json({"erro": "pedido inválido"}, 400)
        if corpo.get("token"):
            salvar_token(corpo["token"])
        if not token():
            return self.json({"erro": "falta o token da API da Hostinger"}, 400)
        try:
            self.json({"url": publicar(cid)})
        except Exception as e:  # noqa: BLE001
            compart[cid] = {"erro": str(e)}
            self.json({"erro": f"Não publicou: {e}."}, 502)

    def do_PUT(self):
        cid = self.cid("/api/clientes/")
        corpo = self.corpo()
        if not cid or not corpo:
            return self.json({"erro": "pedido inválido"}, 400)
        gravar(cid, corpo)
        agendar_sync(f"leitura de {corpo.get('nome', cid)}")
        if (ler(cid).get("compartilhar") or {}).get("codigo") and token():
            agendar_publicacao(cid)
        self.json({"ok": True})

    def do_DELETE(self):
        if self.path.startswith("/api/compartilhar/"):
            cid = self.cid("/api/compartilhar/")
            if not existe(cid):
                return self.json({"erro": "cliente não encontrado"}, 404)
            try:
                parar(cid)
                return self.json({"ok": True})
            except Exception as e:  # noqa: BLE001
                return self.json({"erro": f"Não desativou: {e}."}, 502)
        cid = self.cid("/api/clientes/")
        if not existe(cid):
            return self.json({"erro": "não encontrado"}, 404)
        if (ler(cid).get("compartilhar") or {}).get("codigo") and token():
            try:
                parar(cid)  # cliente excluído não deixa link vivo no site
            except Exception:  # noqa: BLE001
                pass
        achar_arq(cid).unlink()
        agendar_sync(f"cliente {cid} excluído do painel")
        self.json({"ok": True})


def abrir_janela():
    url = f"http://127.0.0.1:{PORTA}/"
    sys.path.insert(0, str(AQUI.parent))
    try:
        from navegador import chrome_path  # Windows, macOS e Linux
        nav = chrome_path(obrigatorio=False)
    except Exception:  # noqa: BLE001
        nav = None
    if nav:
        subprocess.Popen([nav, f"--app={url}", "--window-size=1440,900"])
        return
    import webbrowser
    webbrowser.open(url)


def porta_ocupada():
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", PORTA)) == 0


def criar_atalho():
    if os.name != "nt":
        print("Atalho automático só no Windows. No macOS: Automator > Aplicativo > Executar Shell Script com "
              f"cd \"{AQUI}\" && python3 servir.py  -- ou rode python3 servir.py e fixe a aba no Dock.")
        return
    pyw = Path(sys.executable).with_name("pythonw.exe")
    ps = f"""
$d = [Environment]::GetFolderPath('Desktop')
$s = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $d 'Painel de Resultado.lnk'))
$s.TargetPath = '{pyw}'
$s.Arguments = '"{AQUI / 'servir.py'}"'
$s.WorkingDirectory = '{AQUI}'
$s.IconLocation = '{ICONE}'
$s.Save()
Write-Output (Join-Path $d 'Painel de Resultado.lnk')
"""
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())


def main():
    if "--atalho" in sys.argv:
        return criar_atalho()
    if porta_ocupada():
        return abrir_janela()
    servidor = ThreadingHTTPServer(("127.0.0.1", PORTA), Painel)
    threading.Thread(target=laco_sync, daemon=True).start()
    threading.Thread(target=laco_ocioso, args=(servidor,), daemon=True).start()
    abrir_janela()
    servidor.serve_forever()


if __name__ == "__main__":
    main()
