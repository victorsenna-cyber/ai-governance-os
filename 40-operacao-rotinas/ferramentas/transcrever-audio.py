#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
transcrever-audio.py — a REGRA DE TRANSCRIÇÃO, mecanizada.

Tipo: ferramenta (00-core/TAXONOMIA-DE-ARTEFATOS.md)
Alçada {{OPERADOR}} · README por pasta, modo incremental, modelo escolhível
Método: 100-métodos/METODO-TRANSCRICAO-DE-AUDIO.md (regra, ferramentas, README da pasta, veto)

A regra ({{OPERADOR}}): transcrições de áudios do WhatsApp NUNCA vão para pasta
diferente da do contexto. Todas as transcrições são feitas com o mesmo nome e ao
lado do áudio correspondente, ipsis litteris, sempre. E um README é criado em
cada pasta de contexto/whatsapp para que conste o último áudio transcrito: ao
precisar transcrever, lê-se esse arquivo e transcreve-se a partir dali.

  áudio:        <pasta>/WhatsApp Ptt AAAA-MM-DD at HH.MM.SS.ogg
  transcrição:  <pasta>/WhatsApp Ptt AAAA-MM-DD at HH.MM.SS.md   (um .md por áudio)
  README:       <pasta>/README.md  →  bloco com o último áudio transcrito, os novos e as lacunas

Ipsis litteris: o corpo é o texto da máquina na íntegra, sem limpeza, sem
pontuação acrescentada, sem corte. Leitura, destilação e citação vivem em
outro arquivo e APONTAM para este; nunca o substituem.

Ferramentas, todas locais: ffmpeg (decodifica para WAV 16 kHz mono) +
faster-whisper (CTranslate2, CPU int8). Nada sai da máquina.

Uso (a partir da raiz da Governança):
  python3 40-operacao-rotinas/ferramentas/transcrever-audio.py --pasta <pasta>
        lê o README da pasta e transcreve só os áudios MAIS NOVOS que o último
        transcrito; depois atualiza o README
  ... --pasta <pasta> --lacunas      idem, e também os áudios antigos sem .md
  ... --colocar <pasta>              só põe ao lado do áudio as transcrições que já existem na conta; não transcreve nada

NUNCA REFAZ (regra do {{OPERADOR}}: não se refazem transcrições já feitas): antes de
transcrever, procura na pasta da conta inteira (clientes/<conta>/, antessala do Codex
inclusive) uma transcrição deste áudio — mesmo nome em .md/.txt, data e hora em qualquer
formato no nome (TRANSCRICAO-WHATSAPP-AAAA-MM-DD-HHMMSS.md…) ou trecho dentro de um arquivo
de transcrição consolidado. Achou arquivo → move para o lado do áudio (da antessala, copia).
Achou trecho → avisa e não transcreve. Só o que não existe em lugar nenhum é transcrito.
  ... <áudio> [<áudio> ...]          transcreve estes e atualiza o README de cada pasta
  ... --status [<raiz>]              por pasta com áudio: último transcrito, novos e lacunas (não altera nada)
  ... --readme <pasta> [<pasta> ...] só (re)escreve o bloco do README
  ... --readme-todas [<raiz>]        idem, para toda pasta com áudio sob um caminho de "contexto"
  --modelo <nome>   large-v3 (padrão, mais preciso) · large-v3-turbo (local, ~4x mais rápido) · medium · small
  --refazer         sobrescreve um .md existente

Armadilhas (faster-whisper): o áudio entra como array numpy, não
como caminho (bug do `av`); nunca usar initial_prompt. O antigo --pasta
(sem README) retranscreveu áudios cujo .md morava numa subpasta: agora a pasta
sem README só é varrida depois do inventário (--status) e o .md fora do lugar é
movido para o lado do áudio, nunca refeito em silêncio.
"""
import io, os, re, subprocess, sys, tempfile, time, wave
from datetime import datetime

EXT = (".ogg", ".opus", ".m4a", ".mp3", ".wav", ".aac")
MODELO_PADRAO = "large-v3"
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IGNORAR = ("_arquivos", "90-staging-remoto", "node_modules", ".git", "_legado", "execução Codex")
INI, FIM = "<!-- transcricao:inicio -->", "<!-- transcricao:fim -->"
RE_ULT = re.compile(r"<!-- ultimo: (.+?) -->")
RE_DATA = re.compile(r"(\d{4})-(\d{2})-(\d{2}) at (\d{2})\.(\d{2})\.(\d{2})")

def log(*a): print(*a, flush=True)

def ts(s):
    h, r = divmod(s, 3600); m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

def rel(p):
    try: return os.path.relpath(os.path.abspath(p), RAIZ).replace("\\", "/")
    except ValueError: return os.path.abspath(p).replace("\\", "/")

# ---------- estado da pasta ----------

def chave(nome, pasta):
    """Ordem cronológica: data e hora do nome do WhatsApp; sem elas, data do arquivo."""
    m = RE_DATA.search(nome)
    if m: return ("".join(m.groups()), nome)
    p = os.path.join(pasta, nome)
    if os.path.exists(p):
        return (datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y%m%d%H%M%S"), nome)
    return None

def audios(pasta):
    fs = [f for f in os.listdir(pasta) if f.lower().endswith(EXT) and os.path.isfile(os.path.join(pasta, f))]
    return sorted(fs, key=lambda f: chave(f, pasta))

def tem_md(pasta, f):
    return os.path.exists(os.path.join(pasta, os.path.splitext(f)[0] + ".md"))

def ler_readme(pasta):
    p = os.path.join(pasta, "README.md")
    if not os.path.exists(p): return None
    with io.open(p, encoding="utf-8", newline="") as fh: return fh.read()

def marcador(pasta):
    txt = ler_readme(pasta)
    m = RE_ULT.search(txt or "")
    return m.group(1).strip() if m else None

def raiz_conta(pasta):
    """Onde procurar transcrição existente: a pasta da conta (clientes/<conta>/) ou a própria pasta."""
    partes = os.path.abspath(pasta).replace("\\", "/").split("/")
    if "clientes" in partes and partes.index("clientes") + 1 < len(partes):
        return "/".join(partes[:partes.index("clientes") + 2])
    return os.path.abspath(pasta)

_INDICE = {}
def indice_transcricoes(raiz):
    """Todo .md/.txt da conta que possa ser transcrição: (caminho, nome, conteúdo se o nome diz TRANSCRI…)."""
    if raiz in _INDICE: return _INDICE[raiz]
    itens = []
    for dp, dns, fs in os.walk(raiz):
        dns[:] = [d for d in dns if d not in ("node_modules", ".git", "_legado") and not d.startswith(".")]
        for f in fs:
            if not f.lower().endswith((".md", ".txt")) or f == "README.md": continue
            p = os.path.join(dp, f); txt = None
            if "transcri" in f.lower() and os.path.getsize(p) < 3_000_000:
                with io.open(p, encoding="utf-8", errors="replace") as fh: txt = fh.read()
            itens.append((p, f, txt))
    _INDICE[raiz] = itens
    return itens

def existente(pasta, audio):
    """Transcrição já feita deste áudio em qualquer lugar da conta. Devolve (tipo, caminho) ou None.
    tipo 'arquivo' = um arquivo só deste áudio (vai para o lado dele) · 'consolidado' = trecho dentro de outro arquivo."""
    base = os.path.splitext(audio)[0]
    m = RE_DATA.search(base)
    nomes = {base + ".md", base + ".txt"}
    if m:
        a, mo, d, h, mi, s = m.groups(); dt = f"{a}-{mo}-{d}"
        variantes = [f"{dt}-{h}-{mi}-{s}", f"{dt}-{h}{mi}{s}", f"{dt}_{h}{mi}{s}", f"{dt}_{h}-{mi}-{s}", f"{dt} at {h}.{mi}.{s}"]
    else:
        variantes = []
    proprio = os.path.join(pasta, base + ".md")
    consol = None
    for p, f, txt in indice_transcricoes(raiz_conta(pasta)):
        if os.path.abspath(p) == os.path.abspath(proprio): continue
        par = os.path.splitext(p)[0]
        if any(os.path.exists(par + x) for x in EXT) and os.path.basename(par) != base:
            continue  # é o .md de OUTRO áudio que está ao lado dele
        if f in nomes or any(v in f for v in variantes):
            return ("arquivo", p)
        if txt and m and (f"`{h}.{mi}.{s}" in txt or f"at {h}.{mi}.{s}" in txt) and (dt in f or dt in txt):
            consol = consol or p
    return ("consolidado", consol) if consol else None

def por_ao_lado(pasta, audio, origem):
    """Põe a transcrição existente ao lado do áudio, sem retranscrever: move; da antessala do Codex, copia."""
    import shutil
    destino = os.path.join(pasta, os.path.splitext(audio)[0] + ".md")
    if "execução Codex" in origem.replace("\\", "/"):
        shutil.copyfile(origem, destino); acao = "copiado da antessala"
    else:
        r = subprocess.run(["git", "-C", RAIZ, "mv", origem, destino], capture_output=True)
        if r.returncode != 0: os.replace(origem, destino)
        acao = "movido"
    log(f"já transcrito, {acao} para o lado do áudio (sem retranscrever): {rel(origem)} → {rel(destino)}")

def estado(pasta):
    lista = audios(pasta)
    feitos = [f for f in lista if tem_md(pasta, f)]
    ultimo = feitos[-1] if feitos else None
    marca = marcador(pasta)
    k = chave(marca, pasta) if marca else None
    if k is None and ultimo: k = chave(ultimo, pasta)          # sem README: o último com .md
    if k and ultimo and chave(ultimo, pasta) > k: k = chave(ultimo, pasta)  # alguém transcreveu depois
    sem = [f for f in lista if not tem_md(pasta, f)]
    novos = [f for f in sem if k is None or chave(f, pasta) >= k]  # >=: o marcado no README que perdeu o .md volta a ser novo
    lacunas = [f for f in sem if k is not None and chave(f, pasta) < k]
    return {"lista": lista, "feitos": feitos, "ultimo": ultimo, "marca": marca,
            "novos": novos, "lacunas": lacunas}

# ---------- README ----------

def bloco_readme(pasta, eol):
    e = estado(pasta)
    ult = e["ultimo"]
    lin = [
        INI,
        "## Transcrição dos áudios desta pasta",
        "",
        "> Bloco escrito por `40-operacao-rotinas/ferramentas/transcrever-audio.py`. Não editar à mão.",
        "> Regra, ferramentas e veto: `100-métodos/METODO-TRANSCRICAO-DE-AUDIO.md`.",
        "",
        "| | |",
        "|---|---|",
        "| **Último áudio transcrito** | " + (f"`{ult}` (`.md` ao lado)" if ult else "nenhum") + " |",
        "| **Atualizado em** | " + datetime.now().astimezone().strftime("%Y-%m-%d %H:%M") + " |",
        f"| **Áudios na pasta** | {len(e['lista'])} · com `.md` ao lado: {len(e['feitos'])} · novos: {len(e['novos'])} · lacunas: {len(e['lacunas'])} |",
        "",
        "**Para transcrever o que chegou** (a partir da raiz da Governança) — transcreve só o que é mais novo que o último áudio acima, com modelo local, e atualiza este bloco:",
        "",
        f'`python3 40-operacao-rotinas/ferramentas/transcrever-audio.py --pasta "{rel(pasta)}"`',
        "",
    ]
    fora = {}
    for f in e["novos"] + e["lacunas"]:
        ex = existente(pasta, f)
        if ex: fora[f] = ex
    if fora:
        lin.append("**Já transcritos fora do lugar (pôr ao lado, nunca retranscrever — `--colocar`):**")
        lin += [f"- `{f}` ← `{rel(ex[1])}`" + (" (trecho dentro do arquivo)" if ex[0] == "consolidado" else "") for f, ex in fora.items()]
        lin.append("")
    lin.append("**Novos (depois do último):** " + ("nenhum" if not e["novos"] else ""))
    lin += [f"- `{f}`" for f in e["novos"]]
    lin.append("")
    lin.append("**Lacunas (mais antigos que o último, sem `.md` ao lado — transcrever com `--lacunas`):** "
               + ("nenhuma" if not e["lacunas"] else ""))
    lin += [f"- `{f}`" for f in e["lacunas"]]
    lin.append("")
    if ult: lin.append(f"<!-- ultimo: {ult} -->")
    lin.append(FIM)
    return eol.join(lin)

def escrever_readme(pasta):
    txt = ler_readme(pasta)
    if txt is None:
        eol = "\n"
        novo = f"# {os.path.basename(os.path.abspath(pasta))} — README{eol}{eol}" + bloco_readme(pasta, eol) + eol
    else:
        eol = "\r\n" if "\r\n" in txt else "\n"
        b = bloco_readme(pasta, eol)
        i, j = txt.find(INI), txt.find(FIM)
        if i >= 0 and j > i:
            novo = txt[:i] + b + txt[j + len(FIM):]
        else:
            novo = txt.rstrip("\r\n") + eol + eol + b + eol
    with io.open(os.path.join(pasta, "README.md"), "w", encoding="utf-8", newline="") as fh:
        fh.write(novo)
    return estado(pasta)

# ---------- transcrição ----------

def carregar(path):
    import numpy as np
    fd, wav = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    try:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ar", "16000", "-ac", "1", wav], check=True)
        w = wave.open(wav)
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        dur = w.getnframes() / 16000; w.close()
    finally:
        os.remove(wav)
    return a, dur

def transcrever(modelo, nome_modelo, path, refazer=False):
    base = os.path.splitext(path)[0]
    destino = base + ".md"
    if os.path.exists(destino) and not refazer:
        log("pulado (já tem .md):", rel(destino)); return False
    t0 = time.time()
    a, dur = carregar(path)
    segs, info = modelo.transcribe(a, language="pt", beam_size=5, condition_on_previous_text=False)
    linhas = [f"[{ts(s.start)} --> {ts(s.end)}] {s.text.strip()}" for s in segs]
    nome = os.path.basename(base)
    agora = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    txt = (f"# Transcrição — {nome}\n\n"
           f"- Fonte: `{os.path.basename(path)}` (nesta mesma pasta)\n"
           f"- Duração: {ts(dur)}\n"
           f"- Gerado em: {agora}\n"
           f"- Modelo: faster-whisper `{nome_modelo}` (CPU int8, local), sem initial_prompt\n"
           f"- Idioma: pt\n\n"
           "> Íntegra da máquina, sem edição (regra de transcrição). Erro de reconhecimento fica como saiu; "
           "a correção, quando houver, vai em quem cita, com o timestamp. Para fala que decide (contrato, prova, citação "
           "em peça), conferir de ouvido.\n\n"
           "## Transcrição\n\n" + "\n".join(linhas) + "\n")
    with io.open(destino, "w", encoding="utf-8") as f: f.write(txt)
    log(f"ok ({ts(dur)} de áudio em {time.time() - t0:.0f}s):", rel(destino))
    return True

def carregar_modelo(nome):
    from faster_whisper import WhisperModel
    log(f"carregando faster-whisper `{nome}` (CPU int8, local)…")
    return WhisperModel(nome, device="cpu", compute_type="int8")

# ---------- varredura ----------

def pastas_com_audio(raiz, so_contexto=False):
    for dp, dns, fs in os.walk(raiz):
        dns[:] = [d for d in dns if d not in IGNORAR and not d.startswith(".")]
        if so_contexto and "contexto" not in rel(dp).lower(): continue
        if any(f.lower().endswith(EXT) for f in fs):
            yield dp

def status(raiz):
    log(f"| Pasta | Áudios | Último transcrito | Novos | Lacunas | README |")
    log("|---|---|---|---|---|---|")
    for p in pastas_com_audio(raiz):
        e = estado(p)
        log(f"| `{rel(p)}` | {len(e['lista'])} | {e['ultimo'] or '—'} | {len(e['novos'])} | {len(e['lacunas'])} | "
            f"{'ok' if INI in (ler_readme(p) or '') else ('sem bloco' if ler_readme(p) is not None else 'falta')} |")

# ---------- main ----------

def tirar(args, flag, com_valor=False):
    if flag not in args: return (None if com_valor else False), args
    i = args.index(flag)
    if com_valor:
        v = args[i + 1]; return v, args[:i] + args[i + 2:]
    return True, args[:i] + args[i + 1:]

def main(args):
    refazer, args = tirar(args, "--refazer")
    lacunas, args = tirar(args, "--lacunas")
    nome_modelo, args = tirar(args, "--modelo", True)
    nome_modelo = nome_modelo or MODELO_PADRAO

    if args[:1] == ["--status"]:
        status(args[1] if len(args) > 1 else os.path.join(RAIZ, "clientes")); return
    if args[:1] == ["--readme"]:
        for p in args[1:]:
            e = escrever_readme(p); log(f"README: {rel(p)} · último {e['ultimo'] or '—'} · novos {len(e['novos'])} · lacunas {len(e['lacunas'])}")
        return
    if args[:1] == ["--readme-todas"]:
        raiz = args[1] if len(args) > 1 else os.path.join(RAIZ, "clientes")
        for p in pastas_com_audio(raiz, so_contexto=True):
            e = escrever_readme(p); log(f"README: {rel(p)} · último {e['ultimo'] or '—'} · novos {len(e['novos'])} · lacunas {len(e['lacunas'])}")
        return

    somente_colocar = args[:1] == ["--colocar"]
    if somente_colocar: args = ["--pasta"] + args[1:]; lacunas = True
    if args[:1] == ["--pasta"]:
        pasta = args[1]
        e = estado(pasta)
        log(f"pasta: {rel(pasta)} · README marca: {e['marca'] or '— (sem README: vale o último com .md)'}")
        alvos = e["novos"] + (e["lacunas"] if lacunas else [])
        if not lacunas and e["lacunas"]:
            log(f"aviso: {len(e['lacunas'])} lacuna(s) antiga(s) sem .md, não transcritas (use --lacunas): " + ", ".join(e["lacunas"][:5]))
        alvos = [os.path.join(pasta, f) for f in sorted(alvos, key=lambda f: chave(f, pasta))]
    else:
        alvos = args
    if not alvos and args[:1] != ["--pasta"]:
        print(__doc__); sys.exit(1)

    pastas = sorted({os.path.dirname(os.path.abspath(p)) for p in alvos} | ({os.path.abspath(args[1])} if args[:1] == ["--pasta"] else set()))
    # 🔴 nunca refazer: o que já foi transcrito em qualquer lugar da conta vai para o lado do áudio
    faltam = []
    for p in alvos:
        d, f = os.path.dirname(os.path.abspath(p)), os.path.basename(p)
        ex = None if refazer else existente(d, f)
        if ex and ex[0] == "arquivo":
            por_ao_lado(d, f, ex[1])
        elif ex:
            log(f"já transcrito dentro de {rel(ex[1])}: extrair o trecho para o lado do áudio (não retranscrito): {f}")
        else:
            faltam.append(p)
    if faltam and not somente_colocar:
        log(f"{len(faltam)} áudio(s) sem transcrição em lugar nenhum: transcrevendo")
        modelo = carregar_modelo(nome_modelo)
        for i, p in enumerate(faltam, 1):
            log(f"[{i}/{len(faltam)}]", os.path.basename(p))
            transcrever(modelo, nome_modelo, p, refazer)
    elif faltam:
        log(f"{len(faltam)} áudio(s) sem transcrição em lugar nenhum (não transcritos: modo --colocar)")
    else:
        log("nada novo para transcrever")
    for p in pastas:
        e = escrever_readme(p)
        log(f"README atualizado: {rel(p)} · último {e['ultimo'] or '—'} · novos {len(e['novos'])} · lacunas {len(e['lacunas'])}")

if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main(sys.argv[1:])
