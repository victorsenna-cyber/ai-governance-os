#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
decisoes-do-painel.py — a letra clicada no painel de Projetos vira registro no repo, sozinha.

O operador clica na letra da decisão no painel, em vez de vir à sessão com o id e mandar a letra: o clique vai ao Supabase,
atualiza o GitHub e chega ao repositório local na próxima sincronia.

  python3 decisoes-do-painel.py            # uma rodada: lê o Supabase, propaga, publica na main, carimba
  python3 decisoes-do-painel.py --dry-run  # mostra o que propagaria; não grava, não publica, não carimba
  python3 decisoes-do-painel.py --estado   # só lista o que está esperando no Supabase

Caminho: painel (clique) → Supabase public.decisoes_escolhas (escolher_decisao) → AQUI: decisoes_pendentes(token) →
tarefas/log/decisoes-pagina.json → propagar-decisoes.py (cartão para "Decididas" + DECISOES.md da conta + autonomia) →
sincronizar.py (commit e publicação na main) → decisoes_marcar(token, ids, commit). O PC recebe na próxima sincronia.

Quem roda: a VPS, dentro do laço do contexto.service (a cada 2 min, com a trava do clone). Sem escolha pendente, a rodada
é uma chamada HTTP e nada mais. Pode rodar no PC também (é idempotente: cartão já decidido não se move duas vezes),
mas a VPS é o escritor normal.

Token da ponte: DECISOES_TOKEN no ambiente, ou em /srv/ordens/.env (VPS), ou ~/.continuum/decisoes-token.txt (PC).
Só o hash dele está no Supabase (980-web-design/painel-projetos/supabase/007-decisoes.sql). Sem token: sai em silêncio.
"""
import argparse, datetime, io, json, os, re, subprocess, sys, urllib.error, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FERR = RAIZ / "40-operacao-rotinas" / "ferramentas"
TAR = RAIZ / "40-operacao-rotinas" / "tarefas"
PEND = TAR / "DECISOES-PENDENTES.md"
JSON_SAIDA = TAR / "log" / "decisoes-pagina.json"
REGISTRO = TAR / "log" / "DECISOES-DO-PAINEL.md"
SUPABASE_URL = os.environ.get("FINANCAS_SUPABASE_URL", "https://<projeto>.supabase.co")   # o projeto Supabase do painel; no ambiente
SUPABASE_KEY = os.environ.get("FINANCAS_SUPABASE_KEY", "")   # chave publicável do painel (config.js do painel-financeiro)
BRT = datetime.timezone(datetime.timedelta(hours=-3))


def token():
    t = os.environ.get("DECISOES_TOKEN", "").strip()
    env_vps = Path("/srv/ordens/.env")
    if not t and env_vps.exists():
        for l in env_vps.read_text(encoding="utf-8").splitlines():
            if l.strip().startswith("DECISOES_TOKEN="):
                t = l.split("=", 1)[1].strip()
    arq = Path.home() / ".continuum" / "decisoes-token.txt"
    if not t and arq.exists():
        t = arq.read_text(encoding="utf-8").strip()
    return t


def rpc(nome, corpo):
    req = urllib.request.Request(f"{SUPABASE_URL}/rest/v1/rpc/{nome}", method="POST", data=json.dumps(corpo).encode("utf-8"),
                                 headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8") or "null")


def abertas_no_arquivo():
    t = PEND.read_text(encoding="utf-8")
    abertas = t.split("## Abertas", 1)[-1].split("## Decididas", 1)[0]
    return set(re.findall(r"^### (D-[\d-]+) ·", abertas, re.M))


def quando_brt(iso):
    try:
        d = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d.astimezone(BRT).strftime("%Y-%m-%d %H:%M")
    except Exception:  # noqa: BLE001
        return datetime.datetime.now(BRT).strftime("%Y-%m-%d %H:%M")


def git(*a):
    return subprocess.run(["git", *a], cwd=str(RAIZ), capture_output=True, text=True, encoding="utf-8")


def ja_registradas():
    """(id, clicada em) já no registro. Com a publicação falhando, a decisão não é carimbada no Supabase,
    volta como pendente a cada rodada e a linha era regravada a cada 2 min (152 commits iguais na VPS)."""
    if not REGISTRO.exists():
        return set()
    vistos = set()
    for l in REGISTRO.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 6 and c[1].startswith("D-"):
            vistos.add((c[1], c[-1]))
    return vistos


def registrar(linhas):
    novo = not REGISTRO.exists()
    with io.open(REGISTRO, "a", encoding="utf-8", newline="\n") as f:
        if novo:
            f.write("# DECISÕES DO PAINEL — as letras clicadas no painel de Projetos\n\n"
                    "> Registro vivo, escrito por `40-operacao-rotinas/ferramentas/decisoes-do-painel.py`. Uma linha por escolha "
                    "propagada. O cartão vai para *Decididas* em `DECISOES-PENDENTES.md` e a decisão para o `DECISOES.md` da conta.\n\n"
                    "| Propagada em | Decisão | Conta | Letra | Ajuste | Clicada em |\n|---|---|---|---|---|---|\n")
        for l in linhas:
            f.write(l + "\n")


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--sem-sync", action="store_true", help="propaga e carimba, mas não chama o sincronizar.py (quem chamou publica)")
    ap.add_argument("--instalar-vps", action="store_true", help="no PC: põe o token no /srv/ordens/.env, atualiza o clone e religa o contexto.service")
    a = ap.parse_args()
    tk = token()
    if a.instalar_vps:
        if not tk:
            sys.exit("sem ~/.continuum/decisoes-token.txt")
        remoto = ('read -r TK; f=/srv/ordens/.env; '
                  'if grep -q "^DECISOES_TOKEN=" $f; then sed -i "s|^DECISOES_TOKEN=.*|DECISOES_TOKEN=$TK|" $f; '
                  'else printf "\\n# ponte das decisões do sistema (decisoes-do-painel.py)\\nDECISOES_TOKEN=%s\\n" "$TK" >> $f; fi; '
                  'sudo -u ordens git -C /srv/governanca pull -q origin main; '
                  'systemctl restart contexto.service; sleep 3; systemctl is-active contexto.service; '
                  'sudo -u ordens python3 -X utf8 /srv/governanca/40-operacao-rotinas/ferramentas/decisoes-do-painel.py --estado')
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=20", os.environ.get("VPS_SSH", "root@{{VPS_IP}}"), remoto],
                           input=tk + "\n", text=True, encoding="utf-8")
        return r.returncode
    if not tk:
        print("decisoes-do-painel: sem DECISOES_TOKEN; nada a fazer")
        return 0
    msg = []
    if (TAR / "PAUSA").exists() and not (a.dry_run or a.estado):
        print("PAUSA em tarefas/: nada roda")
        return 0
    def buscar(nome, sql):
        try:
            return rpc(nome, {"token": tk}) or []
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"decisoes-do-painel: a função {nome} não existe no Supabase (rodar o {sql})")
                return []
            raise
    # a aba Mensagens — espelha a fila do mensageiro e aplica os cliques (mensagens_do_painel.py)
    msgs_repo = False
    if not (a.dry_run or a.estado):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("mensagens_do_painel", FERR / "mensagens_do_painel.py")
            mdp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mdp)
            _, msgs_repo = mdp.rodar(tk)
        except Exception as e:  # noqa: BLE001
            print(f"🔴 mensagens do painel: {type(e).__name__}: {e}")
    # o botão WhatsApp da aba Entregáveis — põe na fila o que o operador confirmou no popup (entregaveis_do_painel.py)
    ents_repo = False
    if not (a.dry_run or a.estado):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("entregaveis_do_painel", FERR / "entregaveis_do_painel.py")
            edp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(edp)
            _, ents_repo = edp.rodar(tk)
        except Exception as e:  # noqa: BLE001
            print(f"🔴 entregáveis do painel: {type(e).__name__}: {e}")
    # rascunhos da aba Entregáveis — o texto do operador vai literal ao RASCUNHOS.md do entregável, ou abre um
    # entregável novo na esteira (rascunhos_do_painel.py, 013-rascunhos.sql). Sem a tabela no Supabase, só avisa.
    rasc_repo = False
    if not (a.dry_run or a.estado):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("rascunhos_do_painel", FERR / "rascunhos_do_painel.py")
            rdp = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(rdp)
            _, rasc_repo = rdp.rodar(tk)
        except Exception as e:  # noqa: BLE001
            print(f"🔴 rascunhos do painel: {type(e).__name__}: {e}")
    msgs_repo = msgs_repo or ents_repo or rasc_repo
    pend = buscar("decisoes_pendentes", "007-decisoes.sql")
    acoes = buscar("acoes_pendentes", "008-acoes.sql")      # feito, descartar, nova data, nota, fase
    if msgs_repo:
        msg.append("mensagens do sistema")
    if a.estado or not (pend or acoes or msgs_repo):
        for p in pend:
            print(f"{p['id']}: {p['escolha']}{' · ' + p['ajuste'] if p.get('ajuste') else ''} · {p.get('conta') or '?'} · clicada {quando_brt(p['escolhido_em'])}")
        for x in acoes:
            print(f"ação #{x['id']}: {x['acao']} · {x['alvo']} · {x.get('conta') or ''} · {(x.get('ref') or '')[:60]}")
        if not (pend or acoes):
            print("decisoes-do-painel: nenhuma escolha esperando")
        return 0

    feitas = []
    if pend:
        docs = [dict(id=p["id"], escolha=p["escolha"], escolhido_em=quando_brt(p["escolhido_em"]), conta=p.get("conta") or "",
                     ajuste=p.get("ajuste") or "") for p in pend]
        JSON_SAIDA.parent.mkdir(parents=True, exist_ok=True)
        JSON_SAIDA.write_text(json.dumps({"documents": docs}, ensure_ascii=False, indent=1), encoding="utf-8")
        cmd = [sys.executable, "-X", "utf8", str(FERR / "propagar-decisoes.py"), "--json", str(JSON_SAIDA)] + (["--dry-run"] if a.dry_run else [])
        r = subprocess.run(cmd, cwd=str(RAIZ), capture_output=True, text=True, encoding="utf-8")
        print(r.stdout.strip())
        if r.returncode:
            print(r.stderr.strip(), file=sys.stderr)
            return 1
        if not a.dry_run:
            abertas = abertas_no_arquivo()
            feitas = [p for p in pend if p["id"] not in abertas]           # saiu de "Abertas": propagada agora ou antes
            presas = [p["id"] for p in pend if p["id"] in abertas]
            if presas:
                print("⚠️ continuam em Abertas (cartão não casou): " + ", ".join(presas))
            vistos = ja_registradas()
            novas = [p for p in feitas if (p["id"], quando_brt(p["escolhido_em"])) not in vistos]
            if novas:
                agora = datetime.datetime.now(BRT).strftime("%Y-%m-%d %H:%M")
                registrar([f"| {agora} | {p['id']} | {p.get('conta') or '—'} | **{p['escolha']}** | {(p.get('ajuste') or '—').replace('|', '/')} | {quando_brt(p['escolhido_em'])} |" for p in novas])
                msg.append("decisões " + " ".join(p["id"] for p in novas))
            elif feitas:
                msg.append("carimbo de " + " ".join(p["id"] for p in feitas))   # já no registro: só falta publicar e carimbar
    if a.dry_run:
        for x in acoes:
            print(f"[dry-run] ação #{x['id']}: {x['acao']} · {x['alvo']} · {x.get('conta') or ''} · {(x.get('ref') or '')[:60]}")
        return 0

    aplicadas, erros = [], {}
    if acoes:
        import importlib.util
        spec = importlib.util.spec_from_file_location("acoes_do_painel", FERR / "acoes_do_painel.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        aplicadas, erros = mod.aplicar(acoes)
        for k, v in erros.items():
            print(f"🔴 ação #{k}: {v}")
        if aplicadas:
            msg.append(f"{len(aplicadas)} ação(ões)")
    if not (feitas or aplicadas or erros or msgs_repo):
        return 0

    publicado = True
    if (feitas or aplicadas or msgs_repo) and not a.sem_sync:
        s = subprocess.run([sys.executable, "-X", "utf8", str(FERR / "sincronizar.py"), "-m", "do sistema: " + " · ".join(msg)],
                           cwd=str(RAIZ), capture_output=True, text=True, encoding="utf-8")
        print((s.stdout or "").strip())
        if s.returncode:
            publicado = False
            print("🔴 a publicação falhou; o que foi commitado sobe na próxima sincronia\n" + (s.stderr or "").strip(), file=sys.stderr)
    sha = git("rev-parse", "--short", "HEAD").stdout.strip()
    # ação aplicada já está commitada no clone: carimba mesmo se o push falhou (reaplicar quebraria; o push vem na próxima)
    if aplicadas or erros:
        n = rpc("acoes_marcar", {"token": tk, "ids": aplicadas, "sha": sha, "erros": erros})
        print(f"✅ {n} ação(ões) do sistema no repo (commit {sha})" if n else f"ações com erro: {len(erros)}")
    if feitas and publicado:
        n = rpc("decisoes_marcar", {"token": tk, "ids": [p["id"] for p in feitas], "sha": sha})
        print(f"✅ {n} decisão(ões) do painel no repo (commit {sha})")
    return 0 if publicado else 1

if __name__ == "__main__":
    sys.exit(main())
