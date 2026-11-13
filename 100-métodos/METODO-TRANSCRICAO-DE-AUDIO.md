# MÉTODO — Transcrição de Áudio

> **Tipo:** método
> **Origem:** casa de origem do template (a regra) · **ampliado** (ferramentas declaradas, README por pasta, modo incremental) · **Alçada:** {{OPERADOR}} · ✅ vigente
> **Aplica-se a:** todo áudio de WhatsApp (e nota de voz) de cliente, prospect, parceiro ou nosso que entra no repositório. Call gravada com mais de uma voz segue para a destilação depois de transcrita (`METODO-DESTILACAO-DE-CALLS.md`).
> **Ferramenta:** `40-operacao-rotinas/ferramentas/transcrever-audio.py`
> **Decisões de alçada:** transcrições de áudios do WhatsApp nunca vão para pasta diferente da do contexto; toda transcrição é feita com o mesmo nome e ao lado do áudio correspondente, ipsis litteris, sempre (18/10) · cada transcrição fica num arquivo paralelo ao áudio, em `.md`; a regra do repositório declara métodos e ferramentas (sempre locais, de preferência) e há um `README` em cada pasta de contexto/WhatsApp com o último áudio transcrito, de onde a próxima transcrição parte (21/10) · não se refazem transcrições já feitas: só se transcreve o que ainda não foi transcrito, quando houver requisição (21/10)

---

## 0. Por que existe

Transcrição é o primeiro elo de toda citação literal da casa: destilação, léxico do público, voz, registro de negociação. Se a transcrição some, é editada ou mora longe do áudio, **a fala passa a existir só na versão de quem leu**, e nada mais é verificável.

Dois incidentes fizeram a regra crescer:
- **Primeiro:** a transcrição dos áudios de uma conta foi parar, limpa, dentro de uma destilação em outra pasta. O áudio ficou sem par.
- **Segundo:** o modo "pasta inteira" da ferramenta, sem ponto de partida, retranscreveu áudios antigos cuja transcrição morava numa subpasta (`transcricoes/`). Tempo de CPU e memória gastos para refazer o que já existia. **Sem um marcador do último áudio transcrito, a máquina não sabe de onde partir e varre tudo.**

## 1. A regra

| | |
|---|---|
| 🔴 **Nunca refazer** | transcrição que já existe **em qualquer lugar da conta** (ao lado, em subpasta, na antessala do Codex, com outro nome, dentro de um arquivo consolidado) **não se refaz: se põe ao lado do áudio** — move; da antessala, copia; do consolidado, extrai o trecho sem editar |
| 🔴 **Só sob pedido** | transcreve-se quando o {{OPERADOR}} pede ou manda áudio, e só o que **ainda não foi transcrito**. Nada de lote por iniciativa própria em pasta que ninguém pediu |
| **Um áudio, um `.md`** | `WhatsApp Ptt 2026-10-18 at 15.57.02.ogg` → `WhatsApp Ptt 2026-10-18 at 15.57.02.md` |
| **Mesmo nome, mesma pasta** | o `.md` fica ao lado do áudio. Nunca em subpasta (`transcricoes/`), nunca em `.txt`, nunca com outro nome (`TRANSCRICAO-…`) |
| **Íntegra da máquina** | sem limpeza, sem pontuação acrescentada, sem corte. Erro de reconhecimento fica como saiu; a correção vai em quem cita, com o timestamp |
| **Cabeçalho** | fonte, duração, data de geração, **modelo e onde rodou** |
| **Quem lê aponta** | destilação, léxico e registro citam o `.md` do áudio; nunca copiam a transcrição para dentro de si |
| **README em cada pasta de áudio** | bloco com o **último áudio transcrito**, os novos e as lacunas (§3). É dele que a próxima transcrição parte |

## 2. Ferramentas: locais, sempre que possível

**Nada sai da máquina por padrão.** Áudio de cliente traz dado pessoal, preço, conflito; mandar para serviço externo é publicar (`CLAUDE.md`, ações externas).

| Peça | O que faz | Onde |
|---|---|---|
| **`transcrever-audio.py`** | a ferramenta da regra: lê o README, transcreve, escreve o `.md` ao lado, atualiza o README | `40-operacao-rotinas/ferramentas/` |
| **ffmpeg** | decodifica o áudio (ogg, opus, m4a, mp3, wav, aac) para WAV 16 kHz mono | local, no PATH |
| **faster-whisper** (CTranslate2, CPU `int8`) | reconhecimento de fala em português | local, modelos no cache do Hugging Face (`~/.cache/huggingface/hub`) |

**Modelos (todos locais, já baixados):**

| Modelo | Quando | Custo medido nesta máquina (21/10) |
|---|---|---|
| **`large-v3`** (padrão) | áudio novo do dia a dia: fala que pode virar citação | ~1 min por áudio curto · ~2 GB de memória · ~30% de CPU |
| **`large-v3-turbo`** (`--modelo large-v3-turbo`) | volume: atraso de várias pastas, lote grande | ~4× mais rápido, precisão próxima em português |
| `medium` · `small` | conferência rápida de um trecho | mais rápidos e menos precisos; não para citação |

- **Nuvem só como exceção:** se a ferramenta local não rodar, a transcrição por serviço externo exige ok do {{OPERADOR}} para aquele lote, e o cabeçalho do `.md` declara o serviço. Gravação de Zoom/Meet/TurboScribe que já chega transcrita é fonte bruta (`METODO-DESTILACAO-DE-CALLS.md`, Etapa 1), não exceção.
- **Separação de falante:** o faster-whisper não identifica quem fala. Áudio de WhatsApp tem uma voz e não precisa; call com várias vozes que vai virar citação precisa de ferramenta que separe vozes antes da destilação (`METODO-DESTILACAO-DE-CALLS.md`, §6).

## 3. O README da pasta: o marcador do último áudio

Toda pasta que guarda áudio sob um caminho de contexto (`01 - contexto/WhatsApp/`, `contexto/WhatsApp/`, subpastas por data) tem um `README.md` com um bloco escrito pela ferramenta:

- **Último áudio transcrito:** o mais recente, pela data e hora do nome do WhatsApp, que tem `.md` ao lado;
- **Novos:** áudios mais recentes que ele, sem `.md`;
- **Lacunas:** áudios mais antigos que ele, sem `.md` (só se transcrevem com `--lacunas`);
- o comando pronto para aquela pasta e o marcador de máquina `<!-- ultimo: … -->`.

O bloco fica entre `<!-- transcricao:inicio -->` e `<!-- transcricao:fim -->`. **Não se edita à mão:** a ferramenta o reescreve a cada rodada e preserva o resto do README.

## 4. Procedimento

1. **Abrir o `README.md` da pasta do áudio.** Ele diz o último transcrito, o que chegou depois e o que já está transcrito fora do lugar.
2. **Rodar a ferramenta na pasta** (a partir da raiz da Governança):
   `python3 40-operacao-rotinas/ferramentas/transcrever-audio.py --pasta "<pasta>"`
   Antes de transcrever, ela procura transcrição existente na conta inteira (mesmo nome, data e hora em qualquer formato no nome, trecho em arquivo `TRANSCRI…` consolidado). Achou arquivo → põe ao lado; achou trecho → avisa e não transcreve. Só o que não existe em lugar nenhum é transcrito. Depois atualiza o README.
   - só pôr ao lado o que já existe, sem transcrever nada: `… transcrever-audio.py --colocar "<pasta>"`
   - áudios específicos: `… transcrever-audio.py "<áudio>" ["<áudio>" …]`
   - lote grande: `--modelo large-v3-turbo`
   - inventário do repositório inteiro, sem alterar nada: `… transcrever-audio.py --status`
3. **Conferir de ouvido** só o trecho que decide (contrato, prova, citação em peça). O resto vale como saiu.
4. **Registrar quem leu:** a destilação ou o registro apontam para os `.md`.

**Áudio novo chegou numa pasta sem README:** rodar `--colocar` primeiro e depois `--status`. Só então transcrever o que sobrar.

## 5. Armadilhas

- O áudio entra no faster-whisper como array numpy, não como caminho (bug do `av`).
- Nunca usar `initial_prompt` com a frase suspeita: o modelo "ouve" o que o prompt sugere.
- Saída com `| tail` ou `grep` sem `--line-buffered` esconde o progresso até o fim. Rodar com `PYTHONUNBUFFERED=1`.
- Salvar código não muda o modelo em uso: a ferramenta carrega o modelo uma vez por rodada.

## 6. Régua de veto

Reprova sozinho, e está na tabela do `METODO-GATE-DE-CONGRUENCIA.md` §3:
- 🔴 **transcrição refeita** quando já existia em algum lugar da conta;
- transcrição de áudio **que o {{OPERADOR}} não pediu** (lote por iniciativa própria);
- transcrição **fora da pasta do áudio**, com **outro nome**, em **`.txt`** ou **editada**;
- README da pasta **não atualizado** depois de transcrever;
- transcrição feita em **serviço de nuvem sem ok do {{OPERADOR}}** ou sem o serviço declarado no cabeçalho.

## 7. Fronteiras

- **Transcrição × captura automática:** o áudio que chega pela captura do WhatsApp (`40-operacao-rotinas/ferramentas/openwa/`) é transcrito na mesma rodada, sem pedido à parte. **Apertar o botão Capturar WhatsApp é o pedido.** Vale o resto da regra inteira: o áudio fica em `01 - contexto/OpenWA/áudios/`, o `.md` vai ao lado com o mesmo nome, o README é atualizado, nada se refaz e só ferramenta local. O texto também entra embutido na conversa (`OpenWA/texto/`), e a íntegra é sempre o `.md` ao lado do áudio.

- **Transcrição × destilação:** este método entrega o `.md` íntegro. Ler, classificar e citar é `METODO-DESTILACAO-DE-CALLS.md`.
- **Vídeo também se transcreve:** `.mov`, `.mp4`, `.m4v`, `.mkv` e `.webm` entram na varredura do `transcrever-audio.py` (o ffmpeg tira o áudio direto), com a mesma regra: `.md` com o mesmo nome, ao lado do vídeo. Vídeo fora da Governança: `.md` ao lado dele **e** cópia em `01 - contexto/_transcripts/` da conta ou da ficha de prospect, no mesmo ato, depois a leitura no `REGISTRO.md`.
- **Transcrição × legenda de vídeo:** a legenda de vídeo curto tem cadeia própria (`METODO-EDICAO-DE-VIDEO-CURTO.md`, `40-operacao-rotinas/ferramentas/edicao-video/`).
- **Caso de normalização (exemplo trabalhado):** numa limpeza do repositório, transcrições espalhadas foram postas ao lado do áudio (as que estavam numa subpasta, as em `.txt`, convertidas para `.md`, e as com outro nome, renomeadas) e criaram-se READMEs em toda pasta de áudio de contexto. **Erro corrigido:** um lote por iniciativa própria refez transcrições que já existiam (num arquivo consolidado, com outro nome ou na antessala). As refeitas foram apagadas e as originais postas ao lado (extraídas, renomeadas ou copiadas da antessala, que fica intacta). Daí as duas regras de cima: nunca refazer, só sob pedido. Os áudios que não tinham transcrição ficaram aguardando pedido.
