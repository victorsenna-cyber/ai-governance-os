"""puxar-midia-pontual.py — baixa, de UMA conversa, as mídias de hoje (ou desde --desde), para uma pasta dada.
Só leitura. Lê no máximo 30 mensagens da conversa. Não mexe no mapa nem nos cursores do capturar.py.

Uso: python3 puxar-midia-pontual.py --conversa "Lista" --para "<pasta destino>" [--desde AAAA-MM-DD] [--limite 30]
"""
import os, sys, io, json
from datetime import datetime, timezone, timedelta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capturar as C

def arg(flag, padrao=None):
    a = sys.argv
    return a[a.index(flag) + 1] if flag in a and a.index(flag) + 1 < len(a) else padrao

nome = arg("--conversa"); destino = arg("--para"); desde = arg("--desde"); limite = int(arg("--limite", "30"))
if not nome or not destino: sys.exit(__doc__)
os.makedirs(destino, exist_ok=True)
BRT = C.BRT
corte = (datetime.strptime(desde, "%Y-%m-%d").replace(tzinfo=BRT) if desde
         else datetime.now(BRT).replace(hour=0, minute=0, second=0, microsecond=0))

C.CHAVE = C.chave()
mapa = C.carregar_mapa()
sessao = C.sessao_pronta(mapa.get("sessao") or None)
sid = sessao["id"]
try: C.CONECTADO = int(datetime.fromisoformat((sessao.get("connectedAt") or "").replace("Z", "+00:00")).timestamp())
except ValueError: C.CONECTADO = 0

chats = C.api(f"/sessions/{C.q(sid)}/chats", {"limit": 1000})
cand = [c for c in chats if (c.get("name") or "").strip().lower() == nome.strip().lower()]
if not cand: sys.exit(f"conversa '{nome}' não encontrada. Nomes parecidos: " +
                      ", ".join((c.get("name") or "") for c in chats if nome.lower() in (c.get("name") or "").lower())[:500])
chat = cand[0]
print(f"conversa: {chat.get('name')} ({'grupo' if chat.get('isGroup') else 'privada'}) {chat['id']}")

ms = C.historico(sid, chat["id"], {"limit": limite})
conv = {"chatId": chat["id"], "nome": chat.get("name")}
aovivo = C.AoVivo(sid, chat["id"], [m["id"] for m in ms if m.get("type") in C.TIPOS_MIDIA], [m["id"] for m in ms])
baixados = []
for m in ms:
    ts = m.get("timestamp") or 0
    quando = datetime.fromtimestamp(ts, BRT)
    if quando < corte: continue
    tipo = m.get("type")
    print(f"{quando:%d/%m/%Y %H:%M:%S} [{tipo}] {(m.get('body') or m.get('caption') or '')[:120]!r}")
    if tipo in C.TIPOS_MIDIA:
        caminho, erro = C.baixar(sid, conv, m, quando, destino, aovivo)
        if erro: print("   ", erro)
        else:
            print("    ->", caminho); baixados.append(caminho)
print(f"\n{len(baixados)} arquivo(s) em {destino}")
