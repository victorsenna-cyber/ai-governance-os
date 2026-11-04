# MÉTODO — Edição de Vídeo Curto

> **Tipo:** método
> **Origem:** casa de origem do template · **Alçada:** {{OPERADOR}} · 🟡 **vigência provisória até o primeiro vídeo real editado** (`CLAUDE.md` §7.1, item 4)
> **Aplica-se a:** vídeo gravado de fala (talking head) que vira peça de 15 a 90 s em 9:16 — perfil do {{OPERADOR}} primeiro; conta de cliente depois do primeiro caso real.
> **Ferramenta:** `40-operacao-rotinas/ferramentas/edicao-video/` (README com instalação, formato do roteiro e cadeia aplicada) · **área de trabalho:** `950-marketing/conteudo-perfil/`
> **Gatilho:** a pergunta de como se gera uma edição fina (motion design, legenda, efeitos, cortes, melhoria de vídeo e áudio).

---

## 0. Por que existe

Gravar deixou de ser o gargalo. **O próximo gargalo é o intervalo entre o bruto e o post** — e editor humano custa hora e dinheiro, enquanto editor de aplicativo custa a mesma hora do {{OPERADOR}}. A edição de fala é mecânica em 80%: cortar pausa, enquadrar, legendar, nivelar o áudio. **Os 20% que não são mecânicos são a escolha do trecho e do gancho — e é só aí que entra julgamento.** O método separa os dois: a máquina faz o mecânico; o julgamento fica num arquivo de uma página, aprovado antes de qualquer render.

## 1. O processo — nove passos, nesta ordem

| # | Passo | Quem | Saída |
|---:|---|---|---|
| 1 | **Captação** — câmera nativa, 1080p ou 4K a 30 fps, luz de frente, celular na altura dos olhos, microfone perto da boca. **Enviar o arquivo da galeria, nunca o do WhatsApp** | {{OPERADOR}} | `bruto/VID.mp4` |
| 2 | **Transcrição com tempo por palavra** — `transcrever.py` | máquina | `.palavras.json` + `.transcricao.md` com IDs `Sxxx` |
| 3 | **Roteiro de corte** — escolher o trecho (ou os trechos, reordenáveis), o gancho escrito, os destaques e as correções de nome. **Régua de tom aplicada aqui** (§3) | Claude | `corte.json` + uma linha de porquê para cada trecho escolhido |
| 4 | 🔴 **Aprovação do roteiro** — o {{OPERADOR}} lê o `corte.json` (ou a lista em texto) e aprova ou ajusta | {{OPERADOR}} | roteiro aprovado |
| 5 | **Prévia** — `editar.py --previa --quadros` | máquina | prévia 540×960 + 3 quadros |
| 6 | **Conferência** — quadros (enquadramento, legenda sobre o rosto, cor) e legenda contra a transcrição revisada (nome próprio, termo técnico) | Claude | ajustes no `corte.json` |
| 7 | **Render final** — `editar.py` | máquina | `final/VID-cN.mp4` (1080×1920, −14 LUFS) |
| 8 | **Revisão estética** — o julgamento final de imagem é de quem vê | {{OPERADOR}} | aprovado / nova rodada |
| 9 | **Registro** — tema, trecho, gancho e data de publicação em `950-marketing/conteudo-perfil/REGISTRO.md`; peça que bater gatilho de performance → `swipe-file/` (`CLAUDE.md` §11.5) | Claude | linha no registro |

**Por que o passo 4 é antes da prévia e não depois:** revisar vídeo custa minutos, revisar uma lista de trechos custa segundos. **O erro caro é de escolha, não de render** — e se pega no papel.

## 2. O que o roteiro de corte decide (passo 3)

1. **Um vídeo, uma ideia.** Do bruto longo sai a frase que se sustenta sozinha — e cabe em 15 a 60 s. Frase que precisa do contexto anterior não abre vídeo.
2. **O gancho é escrito por nós, não é a primeira frase dita.** A fala pode reordenar: a conclusão mais forte pode abrir. Roteiro de fala e gancho de conteúdo orgânico seguem a skill de copy, módulo 06 (`ARVORE-ESCRITA`) — **aqui só se escolhe entre o que já foi gravado.**
3. **Destaque é palavra que carrega a tese**, nunca mais de três por vídeo.
4. **Correção de nome sempre** — o Whisper erra termos próprios (`vocab.txt` reduz, não zera).

## 3. Régua de tom — o que não vai ao ar mesmo que esteja bem dito

**A voz sai de acolhimento, não de ataque.** Trecho que **manda o espectador calar, desqualifica a vida de quem assiste ou corrige antes de ver a dor** é cortado no roteiro. **Primeiro ver, depois apontar.**

## 4. 🔴 Veto — o que reprova sozinho

- **render final sem roteiro de corte aprovado pelo {{OPERADOR}}** (passo 4 pulado)
- **legenda publicada sem conferência de nome próprio e termo técnico** contra a transcrição
- **fonte do WhatsApp usada como original** quando o original da galeria existe
- **áudio fora de −14 LUFS ±1** no arquivo final
- **trecho que fere a régua de tom do §3** no corte aprovado

## 5. Fronteiras

| Pedido | Vai para |
|---|---|
| o que dizer, gancho de fala, linha editorial, "não sei o que postar" | `ARVORE-ESCRITA` — skill de copy, módulo 06 |
| anúncio pago em vídeo (texto e estrutura) | `ARVORE-ESCRITA` — `METODO-CONSTRUCAO-DE-CRIATIVOS-DR` |
| vídeo de anúncio editado para mídia | **este método** para a edição + `METODO-TRAFEGO-PAGO` para a hipótese |
| motion elaborado (b-roll, ícones, setas animadas), música | ~~fora desta versão — construir quando houver demanda real, não antes (`CLAUDE.md` §9)~~ *(a demanda real chegou — imagens ilustrativas de VSL)* → `40-operacao-rotinas/ferramentas/video-por-codigo/README.md` (motor HyperFrames + biblioteca de prompts) |
| VSL | `METODO-PRODUCAO-VSL-POR-AGENTES` — este método pode editar o bruto gravado dela |

## 6. Validação financeira (`CLAUDE.md` §9)

**Reduz desperdício:** hora do {{OPERADOR}} em aplicativo de edição → minutos de aprovação. **Via de audiência, não de caixa** — o dinheiro do mês sai de conversa direta com a base quente; o vídeo alimenta o mês seguinte. Nenhum custo novo: ffmpeg e faster-whisper são gratuitos e rodam local.

---

*Verificação inicial: pipeline rodado em vídeo sintético 16:9 → 9:16, 3 jump cuts, gancho, legenda palavra a palavra, barra de progresso, −14,0 LUFS medidos. 🟡 Fecha a vigência provisória: o primeiro vídeo real do {{OPERADOR}} percorrendo os nove passos.*
