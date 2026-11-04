# ÁRVORE — LEITURA

> **Tipo:** trilho · **Origem:** casa de origem do template · **Alçada:** {{OPERADOR}}
> **Carrega-se quando:** o pedido é **ler o que já existe** — call nossa, peça de terceiro (VSL, podcast, página, anúncio), benchmark, léxico do público, voz de quem assina, perfil de conteúdo.
> **Réguas transversais** (§8 REGRAS Nº 0, 1, 2 · procedência · ordem) **valem aqui e não se repetem.**

---

## 1. Pré-condição — a classificação da fonte, antes de qualquer método

> 🔴 **Toda leitura começa respondendo uma pergunta: isto é CONVERSA NOSSA ou ARTEFATO DE TERCEIRO?**
>
> | Fonte | Produz | Grau | Método |
> |---|---|---|---|
> | call, reunião, áudio **com cliente, prospect ou contraparte** | **FATO** | `D` | `METODO-DESTILACAO-DE-CALLS` |
> | VSL, **podcast**, aula, página, anúncio **de terceiro** | **ESTRUTURA** | `R` / `[B]` | `METODO-DESTILACAO-DE-VSL` (+ benchmarking) |
>
> **Confundir as duas é colher cena de concorrente como se fosse fala do nosso público — o erro que custou uma conta.** *"Destila isso"* não decide a árvore: **a fonte decide.**

## 2. O processo desta árvore

| Tipo | O que se carrega |
|---|---|
| **framework** | `100-métodos/METODO-ESTRUTURA-INVISIVEL.md` · `100-métodos/MATRIZ-LEITURA-CONTEUDO.md` |
| **trilho** | *— a leitura é um passo de outra frente: quem ordena é a árvore que pediu a leitura (CONTA, ESCRITA, NEGÓCIO)* |
| **método** | `100-métodos/METODO-TRANSCRICAO-DE-AUDIO.md` \| `100-métodos/METODO-DESTILACAO-DE-CALLS.md` \| `100-métodos/METODO-DESTILACAO-DE-VSL.md` \| `100-métodos/METODO-BENCHMARKING.md` \| `100-métodos/METODO-ARQUEOLOGIA-DE-ICP.md` \| `10-skills/extracao-linguagem.skill.md` (MEL) |
| **blueprint** | `90-templates/benchmark-vsl/` · `90-templates/lexico-icp/` |
| **política** | **REGRA Nº 2** (§8) — só referência **escalada** serve de base |
| **gate** | o gate de cada método (tabela do `METODO-GATE-DE-CONGRUENCIA.md` §3) |

## 3. Linhas — sinal → carga → veto

| Sinais | Carga, na ordem do processo | 🔴 Veto |
|---|---|---|
| transcript de **call nossa**, gravação de reunião, "o que saiu da reunião", áudio de cliente, extrair dores e insumos de conversa | `clientes/<cliente>/STATUS.md` + `DECISOES.md` **antes** — a fala se lê contra o que a pessoa está respondendo *(replay de verificação, 26/09: sem isto o roteador novo carregava menos que o antigo)* → `100-métodos/METODO-DESTILACAO-DE-CALLS.md` *(método — 14 eixos; o 13º audita a NOSSA língua e propaga para a skill de voz; o 14º registra o que a outra parte já ouviu de nós)* · **áudio de WhatsApp: `40-operacao-rotinas/ferramentas/transcrever-audio.py` primeiro — `.md` com o mesmo nome, ao lado do áudio, íntegra** *(regra de transcrição, 18/10)* · **depois da destilação, o passe do outro lado: `.claude/agents/leitor-sintetico.md` em modo call** — reouve a call como a contraparte, construída só do que ela disse: o que ela disse e ninguém respondeu, o que ficou combinado na versão dela, o que a faria sumir, os follow-ups por timestamp; laudo `LEITOR-CALL-<data>.md` ao lado do transcrito, e o orquestrador propaga | citação sem timestamp · **propagação para STATUS/DECISOES/diário fora da mesma tarefa** · saída que não é `.md` · 🔴 **transcrição de áudio fora da pasta do áudio, com outro nome ou editada** · leitura do leitor sintético registrada como fato (é leitura, e vai marcada) · follow-up do laudo enviado sem passar pelo registro da conta |
| **transcrever áudio**, "transcreva os áudios", áudio novo de WhatsApp, nota de voz, `.ogg` sem `.md` ao lado | **o `README.md` da pasta do áudio primeiro** (último transcrito, novos, lacunas) → `100-métodos/METODO-TRANSCRICAO-DE-AUDIO.md` *(método, ✅ desde 18/10, ampliado 21/10)* → `40-operacao-rotinas/ferramentas/transcrever-audio.py --pasta "<pasta>"` (local: ffmpeg + faster-whisper; `--status` para o inventário) → a destilação, se a fala vai ser lida, na linha acima | 🔴 **refazer transcrição que já existe** em qualquer lugar da conta · transcrever **sem pedido** · transcrição **fora da pasta do áudio, com outro nome, em `.txt` ou editada** · README não atualizado · **serviço de nuvem sem ok do {{OPERADOR}}** · varrer pasta sem README sem rodar `--status` antes |
| **capturar o WhatsApp**, "puxa as conversas", "o que o cliente mandou", conversa ou grupo novo de cliente para entrar na captura, botão Capturar WhatsApp | `40-operacao-rotinas/ferramentas/openwa/README.md` *(ferramenta, 🟡 provisória até a 1ª captura real)* → `python3 40-operacao-rotinas/ferramentas/openwa/capturar.py` (entra quem tem a **etiqueta Cliente, Parceiro ou Prospect** no WhatsApp Business; `--chat <id>` para uma conversa só; `--listar` para achar o `chatId`; mapa em `openwa/conversas.json`) → saída em `<clientes|parceiros|30-comercial/assessoria-prospects>/<Nome>/01 - contexto/OpenWA/` (texto · áudios · imagens · PDF · html) → ler a conversa: a linha de call acima, com `STATUS` + `DECISOES` da conta antes | 🔴 **envio de mensagem pela ferramenta ou pelo MCP** · chave do OpenWA dentro da Governança · conversa pessoal ou fora da operação no mapa · texto capturado editado · captura tratada como destilação · **máquina abrindo conta** (`STATUS.md`/`DECISOES.md` criados pela captura) · promoção de tipo (prospect → cliente) feita pelo script |
| **VSL, podcast ou peça de terceiro**, "analisa essa VSL", modelar estrutura, extrair blocos e elementos, contar dose | `100-métodos/METODO-BENCHMARKING.md` Fases B/C → `100-métodos/METODO-DESTILACAO-DE-VSL.md` *(método)* → `90-templates/benchmark-vsl/DESTILACAO-VSL.md` *(blueprint)* | bloco "o que a peça NÃO informa" ausente · eixo 9 fora do grau `R` · **colher cena, dor ou fala como grau `D`** |
| benchmarking, "o que o mercado está fazendo", referência de nicho, swipe file, contar palavras por bloco | `100-métodos/METODO-BENCHMARKING.md` *(método — 7 famílias de elemento, 15 dimensões)* + `30-comercial/swipe-file/` | referência **sem estado de escala** (escalado / em escala / testando + sinal + fonte) · referência "testando" usada como base |
| anúncio de concorrente, "achei essa peça boa", mercado saturado, comprador que se orgulha da própria competência | `10-skills/copywriter-senior-continuum/` **módulo 08** (reenquadre) + biblioteca de anúncios para medir o degrau | copiar o degrau em vez de **medir e subir** |
| léxico do público, "como o ICP fala", cena de espelho, banco de falas, montar o `lexico-icp/` | `100-métodos/METODO-ARQUEOLOGIA-DE-ICP.md` *(método)* → `clientes/<cliente>/lexico-icp/` *(blueprint)* | 🔴 grau `I` em bloco de espelho · **derivar a fala do público da fala do cliente** · 🔴 **crença-alvo do lead sem contagem no balde `conclusão`** (§6-quater) |
| voz de **quem assina**, perfil linguístico, skill de voz de cliente, auditoria de voz | `10-skills/extracao-linguagem.skill.md` (MEL; fonte completa em `100-métodos/Método de extração de linguagem/`) | inferir pelo MEL a voz de **quem ouve** — léxico, cena ou dor narrada |
| "por que o perfil não converte", leitura de conteúdo em 60s, diagnóstico de Instagram, gargalo do conteúdo | `100-métodos/MATRIZ-LEITURA-CONTEUDO.md` *(framework — fluxo no §6)* | amostra abaixo de 10 peças como diagnóstico · **fonte única: este arquivo §3 (8 linhas)**; o `DIAGNOSTICO` §5.4 aponta para cá (27/09) |

## 4. Desempate interno

- **Quem assina × quem ouve:** *"perfil linguístico dela"* → MEL · *"como o público dela fala"* → arqueologia.
- **Medir o mercado × escrever contra ele:** medir → benchmarking · o pedido é a peça que sobe o degrau → ESCRITA, com esta leitura como insumo.

---
*Linhas migradas do roteador v1 (R22, R25, R26, R41, R42, R44) e do ponto cego roteado em 26/09 (matriz de leitura).
