#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
transcrever.py — passo 2 do METODO-EDICAO-DE-VIDEO-CURTO.

Transcreve o vídeo bruto com o tempo de CADA PALAVRA (faster-whisper) e grava,
ao lado do vídeo:
  <video>.palavras.json  — palavras e segmentos com tempo; insumo do editar.py
  <video>.transcricao.md — segmentos numerados (S001, S002…) com timestamp;
                           é o que o Claude lê para escrever o roteiro de corte

Uso:
  python transcrever.py <video> [--modelo medium] [--vocab vocab.txt]

--vocab: arquivo de texto com nomes e termos que o Whisper costuma errar
(nome da empresa, de quem fala, jargão da área…), um por linha. Entra como contexto inicial.
Por padrão usa o vocab.txt desta pasta, se existir.

Requisitos: pip install faster-whisper  (o modelo baixa na 1ª execução)
"""
import argparse, json, os, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def fmt(t):
    m, s = divmod(t, 60)
    h, m = divmod(int(m), 60)
    return f"{h:02d}:{m:02d}:{s:05.2f}" if h else f"{m:02d}:{s:05.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--modelo", default="medium",
                    help="tiny | base | small | medium | large-v3 (default: medium)")
    ap.add_argument("--vocab", default=str(AQUI / "vocab.txt"))
    ap.add_argument("--dispositivo", default="auto", help="auto | cpu | cuda")
    a = ap.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faltou instalar: pip install faster-whisper")

    video = Path(a.video).resolve()
    if not video.exists():
        sys.exit(f"vídeo não encontrado: {video}")

    prompt = None
    if a.vocab and Path(a.vocab).exists():
        termos = [l.strip() for l in Path(a.vocab).read_text(encoding="utf-8").splitlines()
                  if l.strip() and not l.startswith("#")]
        if termos:
            prompt = "Termos: " + ", ".join(termos) + "."

    tipo = "int8" if a.dispositivo != "cuda" else "float16"
    modelo = WhisperModel(a.modelo, device=a.dispositivo, compute_type=tipo)
    # 06/11/2026: o áudio entra como array numpy, decodificado pelo ffmpeg. Passar o caminho
    # faz o faster-whisper chamar av.open(), que quebra com av 19 (TypeError metadata_errors).
    # Mesmo contorno do transcrever-audio.py (memória faster-whisper, 15/10).
    import subprocess, tempfile, wave
    import numpy as np
    fd, wav = tempfile.mkstemp(suffix=".wav"); os.close(fd)
    try:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(video),
                        "-ar", "16000", "-ac", "1", wav], check=True)
        w = wave.open(wav)
        audio = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        w.close()
    finally:
        os.remove(wav)
    segs, info = modelo.transcribe(audio, language="pt", word_timestamps=True,
                                   vad_filter=True, initial_prompt=prompt)

    palavras, segmentos = [], []
    for i, s in enumerate(segs, 1):
        sid = f"S{i:03d}"
        ini = len(palavras)
        for w in (s.words or []):
            palavras.append({"w": w.word.strip(), "s": round(w.start, 3),
                             "e": round(w.end, 3), "seg": sid})
        segmentos.append({"id": sid, "s": round(s.start, 3), "e": round(s.end, 3),
                          "texto": s.text.strip(), "palavras": [ini, len(palavras)]})
        print(f"[{fmt(s.start)}] {sid} {s.text.strip()}")

    base = video.with_suffix("")
    dados = {"fonte": video.name, "duracao": round(info.duration, 3),
             "modelo": a.modelo, "palavras": palavras, "segmentos": segmentos}
    Path(f"{base}.palavras.json").write_text(
        json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")

    linhas = [f"# Transcrição — {video.name}", "",
              f"- **Duração:** {fmt(info.duration)}",
              f"- **Transcrição:** automática (faster-whisper `{a.modelo}`), sem revisão humana. "
              "Nomes próprios podem ter erro — **a legenda só sai depois de revisada.**",
              "- **Uso:** o roteiro de corte referencia os IDs `Sxxx` (ver `README.md`).",
              "", "---", ""]
    for s in segmentos:
        linhas.append(f"**{s['id']}** `[{fmt(s['s'])} → {fmt(s['e'])}]` {s['texto']}")
        linhas.append("")
    Path(f"{base}.transcricao.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nok: {base}.palavras.json · {base}.transcricao.md")


if __name__ == "__main__":
    main()
