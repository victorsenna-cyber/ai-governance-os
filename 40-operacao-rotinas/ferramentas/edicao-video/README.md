# Ferramenta — edição de vídeo curto

> Execução do `100-métodos/METODO-EDICAO-DE-VIDEO-CURTO.md`. **O método diz o que e em que ordem; esta pasta só executa.**
> Roda local (Windows, Mac ou Linux) ou no Claude Code na nuvem. O vídeo nunca entra no git.

## 1. Instalação (uma vez)

**Windows** (PowerShell):

```powershell
winget install Gyan.FFmpeg          # ffmpeg + ffprobe no PATH (reabrir o terminal depois)
pip install faster-whisper          # transcrição com tempo por palavra
```

**macOS / Linux** (bash):

```bash
brew install ffmpeg                 # Linux: sudo apt install ffmpeg
python3 -m pip install faster-whisper numpy
```

Fonte da legenda: ver `fontes/LEIA.md` (Montserrat ExtraBold, um arquivo `.ttf`).

Conferir: `ffmpeg -version` e `python -c "import faster_whisper"` sem erro.

## 2. Fluxo

```text
950-marketing/conteudo-perfil/<AAAA-MM-DD-tema>/
  bruto/VID.mp4                 ← original da galeria (NUNCA o do WhatsApp)
  bruto/VID.palavras.json       ← gerado pelo transcrever.py
  bruto/VID.transcricao.md      ← gerado; é o que o Claude lê
  corte.json                    ← roteiro de corte (Claude escreve, {{OPERADOR}} aprova)
  final/VID-c1.mp4              ← gerado pelo editar.py
```

```powershell
$F = "40-operacao-rotinas/ferramentas/edicao-video"
python $F/transcrever.py "950-marketing/conteudo-perfil/AAAA-MM-DD-tema/bruto/VID.mp4"
# → o Claude lê a transcrição, escreve o corte.json, o {{OPERADOR}} aprova
python $F/editar.py "950-marketing/conteudo-perfil/AAAA-MM-DD-tema/corte.json" --previa --quadros
# → revisar a prévia; ajustar o corte.json; depois o render final:
python $F/editar.py "950-marketing/conteudo-perfil/AAAA-MM-DD-tema/corte.json"
```

Tempos de referência (vídeo final de 60 s, CPU comum): transcrição de 15 min com `medium` ≈ 5–15 min · prévia ≈ 30 s · final ≈ 1–3 min. Máquina lenta: `--modelo small` na transcrição.

## 3. O roteiro de corte — `corte.json`

Caminhos relativos à pasta do próprio `corte.json`.

```json
{
  "fonte": "bruto/VID.mp4",
  "saida": "final/VID-c1.mp4",
  "gancho": { "texto": "<pergunta ou promessa do gancho>", "duracao": 3.0 },
  "trechos": [
    { "de": "S004" },
    { "de": "S012", "ate": "S015" },
    { "inicio": 512.4, "fim": 519.8, "zoom": 1.15 }
  ],
  "cortar_silencios": 0.45,
  "zoom_alternado": 1.12,
  "destaques": ["<palavra-chave 1>", "<palavra-chave 2>"],
  "correcoes": { "<como o Whisper escreveu>": "<como se escreve>" },
  "legenda": true,
  "barra_progresso": true
}
```

| Campo | O que faz | Padrão |
|---|---|---|
| `trechos` | o que entra, **na ordem em que aparece no vídeo final** (pode reordenar a fala). Por segmento (`de`/`ate` = IDs `Sxxx` da transcrição) ou por segundo (`inicio`/`fim`). `de` + `inicio`/`fim` refina o segmento | obrigatório |
| `cortar_silencios` | pausa (s) acima da qual vira jump cut. `0` desliga | `0.45` |
| `zoom_alternado` | punch-in nos clipes alternados — simula segunda câmera. `null` desliga | `1.12` |
| `gancho` | texto na caixa do topo nos primeiros segundos | — |
| `destaques` | palavras que ficam na cor de destaque o tempo todo | — |
| `correcoes` | troca palavra que o Whisper errou, **só na legenda** | — |
| `estilo` | caminho de um JSON que sobrescreve parte do `estilo.json` (por conta, por série) | — |

**O que a ferramenta não faz, e quando chamar outra coisa:** cortar palavra no meio da frase (vício de linguagem dentro do segmento) → refinar com `inicio`/`fim` · b-roll, música, setas, ícones, imagem ilustrativa → fora do escopo desta ferramenta; motion elaborado: `../video-por-codigo/README.md` · estabilização → regravar com o celular apoiado.

## 4. `estilo.json`

Identidade visual da legenda, do gancho, da barra, da cor e do áudio. Cores em `#RRGGBB`. `legenda.posicao_y` é a altura da legenda (0 = topo, 1 = base); `0.70` fica acima da interface do Instagram. `audio.rnnoise_modelo` aceita um modelo `.rnnn` (denoise neural mais forte que o padrão FFT) — baixar em <https://github.com/GregorR/rnnoise-models> se o ruído de fundo for alto.

## 5. Cadeia aplicada (para auditoria)

- **Imagem:** recorte central 9:16 → punch-in → 1080×1920 lanczos → 30 fps → contraste 1,04 · saturação 1,08 → nitidez leve → legenda ASS → barra de progresso.
- **Áudio:** micro-fade de 15 ms em cada corte → passa-alta 80 Hz → denoise FFT (−25 dB) → compressor 3:1 → +2,5 dB em 3,2 kHz (presença) · −1,5 dB em 250 Hz (embolado) → loudnorm −14 LUFS / −1,5 dBTP em **duas passadas**.

*Verificada com vídeo sintético (16:9 → 9:16, 3 jump cuts, legenda, gancho, barra, −14,0 LUFS medidos). 🟡 Falta o primeiro vídeo real da sua operação.*
