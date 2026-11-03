#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
editar.py — passos 4 a 8 do METODO-EDICAO-DE-VIDEO-CURTO.

Lê um ROTEIRO DE CORTE (corte.json, escrito pelo Claude e aprovado pelo {{OPERADOR}})
e entrega o vídeo pronto para postar:
  cortes e jump cuts (silêncios removidos pelo tempo das palavras) · punch-in
  alternado · enquadramento 9:16 · correção leve de cor e nitidez · áudio
  tratado (graves, ruído, compressão, presença, -14 LUFS em duas passadas) ·
  legenda animada palavra a palavra · gancho escrito na tela · barra de progresso

Uso:
  python editar.py <corte.json>            render final (1080x1920)
  python editar.py <corte.json> --previa   render rápido (540x960) para revisar
  python editar.py <corte.json> --quadros  também extrai 3 quadros PNG para conferência
  python editar.py <corte.json> --manter   não apaga a pasta temporária

Requisitos: ffmpeg e ffprobe no PATH. Só biblioteca padrão do Python.
Formato do corte.json e do estilo.json: README.md desta pasta.
"""
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PAD_INI, PAD_FIM = 0.10, 0.15          # respiro antes/depois da fala em cada jump cut
FADE = 0.015                           # micro-fade para não estalar no corte


# ---------------------------------------------------------------- utilidades
def rodar(cmd, cwd=None, capturar=False):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        sys.exit(f"\nffmpeg falhou: {' '.join(map(str, cmd[:6]))} …")
    return r.stderr if capturar else None


def tem_audio(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a",
                        "-show_entries", "stream=index", "-of", "csv=p=0", str(video)],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def cor_ass(hexa, alfa=0):
    h = hexa.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alfa:02X}{b}{g}{r}".upper()


def ts_ass(t):
    t = max(0.0, t)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def mesclar(estilo_padrao, estilo):
    for k, v in estilo.items():
        if isinstance(v, dict) and isinstance(estilo_padrao.get(k), dict):
            mesclar(estilo_padrao[k], v)
        else:
            estilo_padrao[k] = v
    return estilo_padrao


# ---------------------------------------------------------------- roteiro
def resolver_trechos(corte, dados):
    segs = {s["id"]: s for s in dados.get("segmentos", [])}
    saida = []
    for t in corte["trechos"]:
        ini = segs[t["de"]]["s"] if "de" in t else None
        fim = segs[t.get("ate", t["de"])]["e"] if "de" in t else None
        ini = float(t.get("inicio", ini))      # inicio/fim explícitos refinam o segmento
        fim = float(t.get("fim", fim))
        saida.append({"s": ini, "e": fim, "zoom": float(t.get("zoom", 1.0))})
    return saida


def montar_clipes(trechos, palavras, limiar, zoom_alt):
    clipes = []
    for t in trechos:
        ws = [w for w in palavras if w["e"] > t["s"] and w["s"] < t["e"]]
        if not limiar or not ws:
            partes = [(t["s"], t["e"])]
        else:
            partes, ini, ult = [], ws[0]["s"], ws[0]["e"]
            for w in ws[1:]:
                if w["s"] - ult > limiar:
                    partes.append((ini, ult)); ini = w["s"]
                ult = w["e"]
            partes.append((ini, ult))
            partes = [(max(t["s"], a - PAD_INI), min(t["e"], b + PAD_FIM)) for a, b in partes]
        for a, b in partes:
            if b - a > 0.12:
                clipes.append({"s": a, "e": b, "zoom": t["zoom"]})
    if zoom_alt:
        for i, c in enumerate(clipes):
            if i % 2 == 1:
                c["zoom"] = round(c["zoom"] * float(zoom_alt), 4)
    off = 0.0
    for c in clipes:
        c["off"] = off
        off += c["e"] - c["s"]
    return clipes, off


def remapear(palavras, clipes, correcoes):
    corr = {k.lower(): v for k, v in (correcoes or {}).items()}
    saida = []
    for c in clipes:
        for w in palavras:
            if w["e"] <= c["s"] or w["s"] >= c["e"]:
                continue
            txt = w["w"]
            nucleo = re.sub(r"[^\wÀ-ÿ-]", "", txt).lower()
            if nucleo in corr:
                txt = re.sub(re.escape(re.sub(r"[^\wÀ-ÿ-]", "", txt)), corr[nucleo], txt, count=1)
            saida.append({"w": txt, "s": max(w["s"], c["s"]) - c["s"] + c["off"],
                          "e": min(w["e"], c["e"]) - c["s"] + c["off"]})
    return saida


# ---------------------------------------------------------------- legenda
def gerar_ass(palavras, est, corte, W, H, dur):
    L = est["legenda"]; G = est["gancho"]
    escala = W / 1080
    margem_v = int(H * (1 - L["posicao_y"]))
    destaques = {d.lower() for d in corte.get("destaques", [])}

    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Legenda,{L['fonte']},{int(L['tamanho']*escala)},{cor_ass(L['cor_texto'])},{cor_ass(L['cor_texto'])},{cor_ass(L['cor_contorno'])},&H80000000,-1,0,0,0,100,100,0,0,1,{L['contorno']*escala:.1f},{L['sombra']*escala:.1f},2,{int(60*escala)},{int(60*escala)},{margem_v},1
Style: Gancho,{G['fonte']},{int(G['tamanho']*escala)},{cor_ass(G['cor_texto'])},{cor_ass(G['cor_texto'])},{cor_ass(G['cor_caixa'])},{cor_ass(G['cor_caixa'])},-1,0,0,0,100,100,0,0,3,{int(18*escala)},0,8,{int(80*escala)},{int(80*escala)},{int(H*G['posicao_y'])},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    gancho = corte.get("gancho")
    if gancho and gancho.get("texto"):
        txt = gancho["texto"].upper() if G.get("maiusculas") else gancho["texto"]
        ev.append(f"Dialogue: 1,{ts_ass(0)},{ts_ass(min(dur, gancho.get('duracao', 3.0)))},Gancho,,0,0,0,,"
                  + txt.replace("{", "(").replace("}", ")"))

    if corte.get("legenda", True):
        def limpo(t):
            t = re.sub(r"[,.;:…]+$", "", t.strip()).replace("{", "(").replace("}", ")")
            return t.upper() if L.get("maiusculas") else t
        blocos, atual = [], []
        for w in palavras:
            if atual:
                chars = sum(len(x["w"]) + 1 for x in atual) + len(w["w"])
                if (len(atual) >= L["max_palavras"] or chars > L["max_caracteres"]
                        or w["s"] - atual[-1]["e"] > 0.6
                        or re.search(r"[.?!…]$", atual[-1]["w"])):
                    blocos.append(atual); atual = []
            atual.append(w)
        if atual:
            blocos.append(atual)
        ativa = cor_ass(L["cor_ativa"]); dest = cor_ass(L["cor_destaque"])
        esc = L.get("escala_ativa", 110)
        for bi, b in enumerate(blocos):
            fim_bloco = b[-1]["e"] + 0.12
            if bi + 1 < len(blocos):
                fim_bloco = min(fim_bloco, blocos[bi + 1][0]["s"])
            for i, w in enumerate(b):
                ini = b[0]["s"] if i == 0 else w["s"]
                fim = b[i + 1]["s"] if i + 1 < len(b) else fim_bloco
                if fim - ini < 0.02:
                    continue
                partes = []
                for j, x in enumerate(b):
                    t = limpo(x["w"])
                    nucleo = re.sub(r"[^\wÀ-ÿ-]", "", x["w"]).lower()
                    if j == i:
                        partes.append(f"{{\\c{ativa}\\fscx{esc}\\fscy{esc}}}{t}{{\\r}}")
                    elif nucleo in destaques:
                        partes.append(f"{{\\c{dest}}}{t}{{\\r}}")
                    else:
                        partes.append(t)
                ev.append(f"Dialogue: 0,{ts_ass(ini)},{ts_ass(fim)},Legenda,,0,0,0,," + " ".join(partes))
    return cab + "\n".join(ev) + "\n"


# ---------------------------------------------------------------- render
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("corte")
    ap.add_argument("--previa", action="store_true")
    ap.add_argument("--quadros", action="store_true")
    ap.add_argument("--manter", action="store_true")
    a = ap.parse_args()

    for b in ("ffmpeg", "ffprobe"):
        if not shutil.which(b):
            sys.exit(f"{b} não está no PATH (Windows: winget install Gyan.FFmpeg)")

    arq_corte = Path(a.corte).resolve()
    base = arq_corte.parent
    corte = json.loads(arq_corte.read_text(encoding="utf-8"))
    fonte = (base / corte["fonte"]).resolve()
    arq_pal = (base / corte["palavras"]).resolve() if corte.get("palavras") \
        else fonte.with_suffix("").with_name(fonte.stem + ".palavras.json")
    saida = (base / corte["saida"]).resolve()
    if a.previa:
        saida = saida.with_name(saida.stem + "-previa" + saida.suffix)
    saida.parent.mkdir(parents=True, exist_ok=True)

    est = json.loads((AQUI / "estilo.json").read_text(encoding="utf-8"))
    if corte.get("estilo"):
        mesclar(est, json.loads((base / corte["estilo"]).read_text(encoding="utf-8")))

    dados = json.loads(arq_pal.read_text(encoding="utf-8")) if arq_pal.exists() else {}
    palavras = dados.get("palavras", [])
    if not palavras and corte.get("legenda", True):
        print("aviso: sem palavras.json — sem legenda e sem corte de silêncio")

    W, H = (540, 960) if a.previa else (1080, 1920)
    trechos = resolver_trechos(corte, dados)
    clipes, dur = montar_clipes(trechos, palavras, corte.get("cortar_silencios", 0.45),
                                corte.get("zoom_alternado", 1.12))
    print(f"{len(trechos)} trecho(s) → {len(clipes)} clipe(s) · duração final {dur:.1f}s")

    tmp = Path(tempfile.mkdtemp(prefix="edicao-"))
    audio_ok = tem_audio(fonte)
    v = est["video"]
    crf_clipe, preset = ("26", "ultrafast") if a.previa else ("16", "veryfast")

    # 1) cada clipe vira um arquivo intermediário já enquadrado em 9:16
    lista = []
    for i, c in enumerate(clipes):
        d = c["e"] - c["s"]
        vf = (f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',"
              f"crop='iw/{c['zoom']}':'ih/{c['zoom']}',scale={W}:{H}:flags=lanczos,setsar=1,fps=30")
        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{c['s']:.3f}", "-i", str(fonte),
               "-t", f"{d:.3f}", "-vf", vf]
        if audio_ok:
            cmd += ["-af", f"afade=t=in:d={FADE},afade=t=out:st={max(0, d - FADE):.3f}:d={FADE}",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"]
        else:
            cmd += ["-f", "lavfi", "-t", f"{d:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
                    "-map", "0:v", "-map", "1:a", "-c:a", "pcm_s16le"]
        nome = f"c{i:03d}.mkv"
        rodar(cmd + ["-c:v", "libx264", "-crf", crf_clipe, "-preset", preset, str(tmp / nome)])
        lista.append(f"file '{nome}'")
        print(f"  clipe {i + 1}/{len(clipes)}", end="\r")
    (tmp / "lista.txt").write_text("\n".join(lista) + "\n", encoding="utf-8")
    print()

    # 2) legenda
    pal_ed = remapear(palavras, clipes, corte.get("correcoes"))
    (tmp / "legenda.ass").write_text(gerar_ass(pal_ed, est, corte, W, H, dur), encoding="utf-8")
    pasta_fontes = AQUI / "fontes"
    if pasta_fontes.exists():
        shutil.copytree(pasta_fontes, tmp / "fontes")
    else:
        (tmp / "fontes").mkdir()

    # 3) áudio: cadeia + loudnorm em duas passadas
    au = est["audio"]
    limpeza = (f"arnndn=m='{au['rnnoise_modelo']}'" if au.get("rnnoise_modelo")
               else f"afftdn=nf={au['denoise_db']}")
    cadeia = (f"highpass=f=80,{limpeza},"
              "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
              "equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-1.5")
    alvo = f"I={au['lufs']}:TP=-1.5:LRA=11"
    if a.previa:
        cadeia_final = f"{cadeia},loudnorm={alvo}"
    else:
        med = rodar(["ffmpeg", "-hide_banner", "-f", "concat", "-safe", "0", "-i", "lista.txt",
                     "-af", f"{cadeia},loudnorm={alvo}:print_format=json", "-f", "null", "-"],
                    cwd=tmp, capturar=True)
        j = json.loads(med[med.rfind("{"):med.rfind("}") + 1])
        cadeia_final = (f"{cadeia},loudnorm={alvo}:measured_I={j['input_i']}:measured_TP={j['input_tp']}"
                        f":measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}"
                        f":offset={j['target_offset']}:linear=true")

    # 4) render final
    fv = (f"[0:v]eq=contrast={v['contraste']}:saturation={v['saturacao']},"
          f"unsharp=5:5:{v['nitidez']},ass=legenda.ass:fontsdir=fontes[vs]")
    bp = est["barra_progresso"]
    if corte.get("barra_progresso", bp.get("ativa", True)):
        alt = max(4, int(bp["altura"] * W / 1080))
        fv += (f";color=c=0x{bp['cor'].lstrip('#')}:s={W}x{alt}:d={dur:.3f},format=rgba,"
               f"colorchannelmixer=aa=0.85[barra];"
               f"[vs][barra]overlay=x='-w+w*t/{dur:.3f}':y=H-{alt}:shortest=1[vout]")
    else:
        fv += ";[vs]null[vout]"
    fa = f"[0:a]{cadeia_final},aresample=48000[aout]"
    crf, preset_f = ("28", "ultrafast") if a.previa else ("19", "slow")
    rodar(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", "lista.txt",
           "-filter_complex", f"{fv};{fa}", "-map", "[vout]", "-map", "[aout]",
           "-c:v", "libx264", "-crf", crf, "-preset", preset_f, "-pix_fmt", "yuv420p",
           "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
           str(saida)], cwd=tmp)

    if a.quadros:
        for k, f in enumerate((0.1, 0.5, 0.9), 1):
            rodar(["ffmpeg", "-y", "-v", "error", "-ss", f"{dur * f:.2f}", "-i", str(saida),
                   "-frames:v", "1", str(saida.with_name(f"{saida.stem}_quadro{k}.png"))])

    if a.manter:
        print(f"temporários em: {tmp}")
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"ok: {saida}")


if __name__ == "__main__":
    main()
