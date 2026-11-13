# MÉTODO CONTINUUM DE DESTILAÇÃO DE CALLS

> **Tipo:** método · secundário: gate (§9), política (§2), blueprint (§6) *(reclassificado por auditoria independente de leitura integral; antes: "método-raiz autoral")* · **Origem:** casa de origem do template · **Status:** VIGENTE
> **Abrir por momento:** decidir §2 · produzir §3 · conferir §9 *(mapa proposto pela auditoria de 26/09 — conferir no primeiro uso)*
> **Origem:** primeira execução completa, sobre uma call longa, que passou a ser o exemplar de referência (§10).
> **Vale para:** toda call gravada com cliente, prospect, parceiro, fornecedor ou sócio (se houver).
> **Atualizado:** treze eixos. O eixo 13 (§5-bis) audita **a nossa própria língua na call** e alimenta a skill de voz.
> **Atualizado:** **catorze eixos.** O eixo 14 (§5-ter) registra **o que a outra parte já ouviu de nós** (produto, fase, preço, promessa) e a divergência com o canônico; caminhos alinhados à convenção `01 - contexto/` do repo; glossário de grafia da máquina (Etapa 4); linha de prospect na propagação (Etapa 7); pergunta 8 no gate (§9).
> **Atualizado:** **quinze eixos.** O eixo 15 (§5-quater) registra **o que prometemos entregar** e manda cada promessa à fila de produção (`entregaveis.py --nova`), no mesmo ato; linha na Etapa 7; pergunta 10 no gate (§9).

---

> 🔴 ⭐ **FRONTEIRA — o que NÃO cai aqui.** Call é **conversa nossa** e produz **FATO**, de grau `D`. VSL, página, anúncio ou podcast de terceiro é **artefato publicado** e produz **ESTRUTURA**, de grau `R`/`[B]` → `METODO-DESTILACAO-DE-VSL.md`. **Confundir os dois é colher cena de concorrente como se fosse fala do nosso público — o erro que custou a Conta B.**

## 1. POR QUE ESTE MÉTODO EXISTE

Uma call de duas horas com um cliente contém, tipicamente, mais informação sobre o negócio dele do que todo o resto do nosso repositório sobre aquela conta. Preço, estrutura interna do produto, vocabulário real, dores nominais, objeções, o que já foi tentado e falhou, o que ele descartou e por quê. **Nada disso está no briefing, no contrato ou no WhatsApp.**

E some no dia seguinte.

O padrão que este método corta: **a call vira "resumo da reunião" com cinco bullets, o resumo vira uma tarefa, e a informação de maior valor — a que só se acessa ouvindo a pessoa explicar o próprio negócio — evapora.** Resumo é perda deliberada de informação. Destilação é o contrário: é reter tudo o que decide, organizado por onde vai ser usado.

**A régua que governa tudo abaixo:**

> **Resumir é escolher o que jogar fora. Destilar é escolher onde cada coisa vai ser usada.**
> Se o artefato serve a um destino só, ele é ata. Se serve a oito, é destilação.

---

## 2. GATILHO E OBRIGATORIEDADE

| Situação | Obrigatório? |
|---|---|
| Call gravada com cliente ativo | **sim** |
| Call de vendas / diagnóstica com prospect | **sim** |
| Negociação com fornecedor, parceiro ou contraparte jurídica | **sim** |
| Call interna entre sócios (se houver) com decisão material | sim, versão curta (§7) |
| Call operacional de 15 min sem decisão | não |
| **Call de venda curta, conduzida como pitch (< 45 min)** | **sim, inteira.** Os eixos 2, 3, 6 e 7 costumam sair vazios; **os eixos 9, 13 e 14 pesam mais**, porque o que decide a proposta é o que ele já ouviu de nós e o que não perguntamos |

**Prazo:** a destilação é feita **na mesma janela de trabalho em que a call é lida**, nunca agendada para depois. Call lida e não destilada é pior que call não lida — cria a sensação de que o material foi aproveitado.

**Formato obrigatório: `.md`.** O PDF é opcional e existe só quando o artefato vai ser enviado a alguém de fora (§8).

---

## 3. AS SETE ETAPAS

### Etapa 1 — Preservar a fonte bruta, intacta

O arquivo original (`.vtt`, `.srt`, `.txt` do Zoom/Meet/TurboScribe) vai para **`01 - contexto/_transcripts/`** da conta (ou do prospect, em `30-comercial/assessoria-prospects/<nome>/`) e **nunca é editado**. É a única prova de que a citação é literal. *(o Zoom grava em `clientes/.transcripts/`, que é caixa de entrada; de lá o arquivo se **copia**, nunca se move nem se edita.)*

> 🔴 ⭐ **REGRA DE TRANSCRIÇÃO (regra da casa).** Decisão de alçada: transcrições de áudios do WhatsApp nunca vão para pasta diferente da do contexto; todas são feitas com o mesmo nome e ao lado do áudio correspondente, ipsis litteris, sempre.
> **Um áudio, um `.md`, mesmo nome, mesma pasta:** `WhatsApp Ptt AAAA-MM-DD at HH.MM.SS.ogg` → `WhatsApp Ptt AAAA-MM-DD at HH.MM.SS.md`, ao lado. **Corpo = a íntegra da máquina, sem limpeza, sem pontuação acrescentada, sem corte.** Leitura, destilação e citação vivem em outro arquivo e **apontam** para o `.md` do áudio; nunca levam a transcrição para dentro de si. **Ferramenta, nunca à mão:** `40-operacao-rotinas/ferramentas/transcrever-audio.py --pasta <pasta>`, que lê o `README.md` da pasta e transcreve só o que chegou depois do último áudio transcrito (ou `<áudio>` nomeado). **Regra completa, ferramentas locais, README por pasta e veto: `100-métodos/METODO-TRANSCRICAO-DE-AUDIO.md`.** Vale para áudio de WhatsApp de qualquer conta, prospect ou parceiro.
> *Por que existe: transcrição que vai parar, limpa, dentro de outro documento deixa o áudio sem par, e a fala passa a existir só na versão editada.*


### Etapa 2 — Limpar por script, nunca à mão

Gerar a versão legível com o script padrão (§6): agrupa falas consecutivas do mesmo interlocutor, preserva timestamps, remove blocos vazios. Salvar como `01 - contexto/TRANSCRIPT-CALL-<CLIENTE>-<DD-MM-AAAA>-LIMPO.md`.

Limpeza manual é proibida: introduz edição silenciosa no material que existe justamente para ser inegociável.

### Etapa 3 — Ler integralmente

**Sem exceção e sem amostragem.** O material de maior valor de uma call quase nunca está onde se espera: aparece em digressão, em correção de si mesmo, em resposta lateral a uma pergunta sobre outra coisa.

Já aconteceu de o preço de um produto aparecer **incidentalmente**, no meio de uma explicação sobre outro assunto. Nenhuma busca por palavra-chave teria encontrado.

Se o transcript for grande, ler em blocos sequenciais. **Nunca por busca.**

### Etapa 4 — Extrair ponto a ponto, com ID estável

Cada informação que decide vira um ponto com **ID sequencial e permanente**: `C-01`, `C-02`, …

O ID é o que torna o artefato citável. Depois dele, `STATUS.md`, `DECISOES.md`, a copy e a proposta referenciam `C-17` em vez de reescrever o fato — e a origem continua rastreável até o timestamp.

**Cada ponto carrega, sempre:**

| Campo | Regra |
|---|---|
| **ID** | sequencial, nunca reaproveitado |
| **Enunciado** | o fato em uma frase, sem adjetivo |
| **Citação literal** | entre aspas, **com timestamp** `[hh:mm:ss]` |
| **Consequência** | o que fecha, abre ou muda no repositório |

**Regras de fidelidade — as cinco que não se negociam:**

1. **Citação literal, sempre.** Paráfrase perde exatamente a palavra que a pessoa escolheu — que é o insumo de voz.
2. **Fato ≠ leitura nossa.** Leitura vai em bloco próprio, rotulado.
3. **Transcrição automática erra.** Trecho duvidoso vai marcado `[transcrição incerta]`, com a grafia provável ao lado. Nunca "corrigir" silenciosamente o que a pessoa disse. **Erro que se repete ("Cloud" por Claude, "Ia" por IA) entra uma vez num glossário de grafia da máquina no cabeçalho**, e nas citações a palavra vai como a máquina escreveu, com a provável entre colchetes: a correção fica declarada, a citação fica literal.
4. **Registrar o descartado e o porquê.** "Considerou X e descartou porque Y" vale mais que o resultado.
5. **Registrar o que a pessoa não disse.** Ver §5 — é a etapa que mais gente pula.

### Etapa 5 — Classificar por eixo, não por entregável

**A classificação errada é a que organiza por página, por tarefa ou por produto.** Ela produz um artefato que serve à tarefa da semana e morre com ela.

A classificação certa é por **natureza da informação**, porque cada natureza tem um destino diferente e uma vida útil diferente:

| # | Eixo | O que entra | Vida útil |
|---|---|---|---|
| 1 | **Fatos comerciais duros** | preço, prazo, plataforma, ciclo, pipeline nominal | até mudarem |
| 2 | **Arquitetura de produto** | o que é entregue, como, em que ordem, por quê | anos |
| 3 | **Ecossistema e funil** | como as ofertas se alimentam, onde o dinheiro passa | meses |
| 4 | **ICP, dor e desejo** | quem compra, o que dói, caso real com nome e situação | anos |
| 5 | **Voz e linguagem** | frases dela, vocabulário proibido, regras de registro | **permanente** |
| 6 | **Direção visual** | cor, símbolo, referência, regra estética | anos |
| 7 | **Arquitetura de informação** | menu, destinos, hierarquia acordada | meses |
| 8 | **Método e conhecimento transferido** | o que **nós** ensinamos na call | **reutilizável em outras contas** |
| 9 | **Compromissos** | dela e nossos, com timestamp | até cumpridos |
| 10 | **Pendências movidas** | fechadas · abertas com caminho · novas | corrente |
| 11 | **Riscos e lacunas** | inclusive o que não foi dito | corrente |
| 12 | **Leitura executiva** | o que a call resolveu, revelou e custou | decisória |
| 13 | **⭐ Nossa língua na call** | violação de metamodelo, salto de lógica, muleta e hedge **do nosso lado**, com citação literal | **permanente → skill de voz** |
| 14 | **⭐ O que ele já ouviu de nós** | produto, fase, preço, condição e promessa **ditos por nós**, com timestamp, e a **divergência com a oferta canônica** marcada | **até a proposta escrita; depois, camada 4 do registro** |

Nem toda call tem os treze. **Eixo vazio some; eixo não se inventa para preencher tabela.**

### Etapa 6 — Indexar por destino de uso

**É esta etapa que transforma o documento em ativo.** Abre-se o artefato com uma tabela de duas colunas: *"se você vai fazer X, leia as seções Y"*.

Sem ela, quem abre o arquivo seis semanas depois para escrever um anúncio não sabe que a resposta está numa seção chamada "ICP e dor". O índice de uso é o que faz o mesmo documento servir a copy, oferta, produto, onboarding, design, precificação e proposta.

### Etapa 7 — Propagar, e só então fechar

Destilação que não sai do próprio arquivo não mudou o estado da empresa. **Na mesma tarefa:**

| Destino | O que vai |
|---|---|
| `STATUS.md` da conta | fatos que mudam estado, pendências fechadas e abertas |
| `DECISOES.md` da conta | uma DEC por decisão, com autoridade e **o que foi descartado** |
| `DIARIO-DE-BORDO.md` | o que a call destravou, revelou e custou |
| `STATUS.md` da Governança | se houver impacto na carteira ou no caixa |
| skill de voz do cliente | eixo 5 |
| **`clientes/<cliente>/lexico-icp/` — banco de frases do público** | **eixo 4** 🔴 **instituído após a perda de uma conta.** Até então o eixo 4 era **o único eixo de vida útil longa sem destino de propagação**: ele era extraído, marcado, e morria na destilação. **Consequência medida:** uma frase de dor foi colhida, marcada como a melhor da call, e semanas depois a copy da mesma conta descreveu um público oposto ao que ela documentava. **Toda frase entra com grau de procedência: `D` direta (o próprio ICP), `R` relatada (a cliente ou a equipe citando o público), `I` inferida (nossa). Grau `I` nunca entra em peça.** Auditoria completa do circuito de copy: registrada no histórico da casa. |
| **skill de voz de quem falou do nosso lado** (`10-skills/voz-operador.skill.md`) | **eixo 13** |
| `CONTEXTO.md` da conta | eixos 2 e 3 |
| **agenda do {{OPERADOR}}** (calendário da sessão, por conector) | **eixo 9, compromissos com data e hora** 🔴: evento criado no mesmo ato, no fuso do operador, com o relógio da contraparte, o timestamp da fala e a pauta na descrição; hipótese até confirmação por escrito. O marco segue no `PAINEL.md` |
| `100-métodos/` ou skill | eixo 8, quando o que ensinamos for reaproveitável |
| **proposta escrita** (ESCRITA) e `REGISTRO.md` camada 4 | **eixo 14**: a proposta usa o que ele já ouviu ou declara que está corrigindo; nunca contradiz em silêncio |
| **fila de produção** (`40-operacao-rotinas/tarefas/fila/`, `tipo: entregavel`) | **eixo 15**: uma task por promessa, no mesmo ato, pelo `entregaveis.py --nova`, com fonte = arquivo + ID do ponto; marco do `PAINEL.md` só com `task:` apontando |
| **prospect** (`30-comercial/assessoria-prospects/<nome>/`) | `REGISTRO.md` camadas 1 a 4 · `FOLHA-INTERNA` com as células `[dado dele]` preenchidas e o **veredito** (`CLAUDE.md` §9.1) · `STATUS.md` da Governança. Não há `DECISOES.md` nem diário antes de virar conta |

**Gate:** enquanto a propagação não estiver feita, a destilação está **incompleta**, não "pronta para depois".

---

## 4. NOMES E LUGARES

| Artefato | Caminho |
|---|---|
| Fonte bruta | `clientes/<cliente>/01 - contexto/_transcripts/<nome original do arquivo>` |
| **Transcrição de áudio de WhatsApp** | **ao lado do áudio, mesmo nome, `.md`** — `<pasta do áudio>/<nome do áudio>.md`, íntegra (Etapa 1, regra de transcrição) |
| Transcript limpo | `clientes/<cliente>/01 - contexto/TRANSCRIPT-CALL-<CLIENTE>-<DD-MM-AAAA>-LIMPO.md` |
| **Destilação** | `clientes/<cliente>/DESTILACAO-CALL-<AAAA-MM-DD>.md` |
| PDF, quando houver | `clientes/<cliente>/DESTILACAO-CALL-<CLIENTE>-<DD-MM-AAAA>.pdf` |

Prospect usa `30-comercial/assessoria-prospects/<nome>/`, com a mesma subárvore `01 - contexto/_transcripts/`. Jurídico usa `80-juridico/registros/`. Caixa de entrada do Zoom: `clientes/.transcripts/` (só origem; nunca destino de destilação).

---

## 5. O QUE NÃO FOI DITO

**A etapa que mais gente pula, e a que mais custa quando falta.**

Ao fechar a destilação, listar explicitamente **o que era esperado na pauta e não apareceu na call**. Silêncio sobre um assunto que estava na pauta não é neutro: é informação.

Já aconteceu de o item mais grave de uma destilação ser exatamente isso — **uma oferta à venda, com compra já feita, não foi mencionada uma única vez na call inteira**, por nenhum dos dois lados. A ausência disse o que nenhuma frase disse: a oferta provavelmente não existia mais.

Formato: uma seção curta, com a pergunta que a ausência abre e o dono da resposta.

---

## 5-BIS. EIXO 13 — NOSSA LÍNGUA NA CALL (regra da casa)

**Por que este eixo existe.** Antes, o método capturava a voz do cliente (eixo 5) e o método que nós ensinamos (eixo 8). **O nosso próprio jeito de falar não era capturado por eixo nenhum.** Ele aparecia só no eixo 11, e sempre travestido de falha comercial: *"não marcou data"*, *"ofereceu escopo de graça"*, *"ouviu o número e não explorou"*.

A diferença não é semântica:

> **Falha comercial vira lição de uma call. Padrão de linguagem vira régua permanente.**

Enquanto o eixo não existiu, a `10-skills/voz-operador.skill.md` não tinha como iterar: a matéria-prima dela — fala espontânea, com o que a pessoa deixa de dizer — passava por baixo da destilação e sumia junto com o transcript.

### O que entra — quatro blocos, todos com citação literal e timestamp

| Bloco | O que registrar | Exemplo de entrada válida |
|---|---|---|
| **13.1 · Violações de metamodelo** | omissão (índice referencial vago, nominalização, comparativo sem termo) · generalização (quantificador universal, modal sem agente) · distorção (leitura mental, causa-efeito, equivalência complexa) | `[hh:mm:ss]` *"isso funciona bem melhor"* — comparativo sem termo |
| **13.2 · Saltos de lógica** | troca de camada (dado → leitura → plano → prova) sem ponte declarada, **com o custo medido em turnos** | `[hh:mm:ss]` prova solta do gancho → `[hh:mm:ss]` a outra parte não acompanhou. Custou N turnos |
| **13.3 · Muletas e hedges, contados** | frequência bruta e por 1.000 palavras, sobre o transcript limpo | *"[muleta]"* N× em M palavras |
| **13.4 · O que funcionou e o que não fizemos** | o padrão a repetir, e **a ausência que assina** (o que a pessoa nunca usa) | `[hh:mm:ss]` ancoragem de preço sem hedge → a outra parte engajou com o número |

### Como rodar — 5 minutos sobre o transcript limpo

1. **Isolar as nossas falas** por falante e contar as palavras. Sem denominador não há frequência, e sem frequência a leitura vira impressão.
2. **Contar a lista fixa de marcadores** (hedges, dêiticos vagos, nominalizações-curinga, tags de checagem, quantificadores universais, diminutivos). Contagem por script, nunca de cabeça.
3. **Ler os dez turnos mais longos nossos.** É onde o salto de lógica mora — turno curto raramente troca de camada.
4. **Marcar cada achado com timestamp.** Sem timestamp não entra, exatamente como no eixo 5.

### Convenção de ID

Pontos do eixo 13 usam prefixo próprio: **`L-01`, `L-02`…** (*língua*), com numeração independente por call. Não consomem a sequência `C-` dos fatos, porque não são fato do cliente: são fato nosso.

### A régua de honestidade deste eixo

O eixo 13 é sobre **a nossa fala**, não sobre a nossa performance. *"A call foi mal conduzida"* não é entrada válida — é adjetivo. *"Às `[hh:mm:ss]` disse '[citação literal]' sobre o próprio plano, na frente de quem ia decidir"* é entrada válida.

**Fato ≠ leitura vale aqui igual ao resto do método.** A citação é fato; o custo estimado é leitura, e vai rotulado.

### Destino

Propagação **obrigatória** para a skill de voz de quem falou:
- {{OPERADOR}} → `10-skills/voz-operador.skill.md` (§4 ficha de assinatura · §5 gate de metamodelo · §6 saltos de lógica)
- Outro falante nosso → a skill de voz da pessoa. Se não existir, o eixo 13 é o insumo que a cria.

**Método da ficha:** `10-skills/copywriter-senior-continuum/referencias/07-falhas-propositais.md`, Partes 3 e 6.

---

## 5-TER. EIXO 14 — O QUE ELE JÁ OUVIU DE NÓS (regra da casa)

**Por que este eixo existe.** O que se diz numa call de venda pode divergir do canônico: um produto descrito com as fases de outro, uma promessa na fala que a oferta vigente já retirou, um número que a transcrição não deixa claro qual a outra parte ouviu. Nada disso cabia nos treze eixos: não é fato dele (eixo 1), não é compromisso (eixo 9) e não é padrão de língua (eixo 13). **É o que a outra parte já ouviu, e a proposta escrita que o contradiz em silêncio quebra a camada 4 do `CLAUDE.md` §11.1** (*"sem isso não se sabe o que a outra parte já ouviu"*).

### O que entra, com citação literal e timestamp

| Bloco | O que registrar |
|---|---|
| **14.1 · Produto e fases ditos** | como o produto foi descrito, em que ordem, com que verbos (quem faz o quê) |
| **14.2 · Números ditos** | preço, forma de pagamento, prazo, quantidade de encontros; **número incerto na transcrição vai marcado** e a proposta o corrige por escrito |
| **14.3 · Promessas e exemplos** | o que dissemos que "é possível", "pode rodar", "faz sozinho": é a expectativa que ele levou |
| **14.4 · Divergência com o canônico** | coluna própria, linha a linha: ✅ bate · ⚠️ reenquadrar · 🔴 corrigir por escrito |

### Convenção de ID

`O-01`, `O-02`… (*ouviu*), numeração independente por call.

### Destino

**A proposta escrita** (ESCRITA, documento para o próprio cliente): usa a estrutura e os números que ele ouviu, ou **declara que está corrigindo** ("na call eu disse X; o correto é Y"). Depois, `REGISTRO.md` camada 4. **Veto** (`METODO-GATE-DE-CONGRUENCIA.md` §3): proposta que contradiz o que ele ouviu sem declarar.

---

## 5-QUATER. EIXO 15 — O QUE PROMETEMOS

**Por que este eixo existe.** Promessa nossa feita em call vira marco no painel e ninguém a produz: o marco aparece, vence, e o cliente espera. O eixo 14 guarda a expectativa que ele levou; **este guarda o que nos comprometemos a entregar**, e o destino dele é a fila de produção, não o `PAINEL.md`.

**O que entra:** toda fala nossa que compromete uma entrega, com citação literal e timestamp. Frases-sinal: *"te mando"*, *"vou te enviar"*, *"fica pronto até"*, *"amanhã eu passo"*, *"vou montar"*, *"deixa comigo"*, *"segue depois"*. Entra também a promessa **implícita por pergunta aceita** (ele: *"você manda o PDF?"*; nós: *"mando"*).

**Convenção de ID:** `P-<conta>-<n>`, numeração por call, **dentro desta seção** (o leitor só procura o ID aqui).

| ID | O quê | A quem | Forma (documento · mensagem · artefato · pacote) | Prazo dito | Citação + timestamp |
|---|---|---|---|---|---|

**Destino, no mesmo ato:** uma task `tipo: entregavel` por promessa, pelo `python3 -X utf8 40-operacao-rotinas/ferramentas/entregaveis.py --nova --conta "<C>" --o-que "…" --destinatario … --forma … --prometido-em … --prometido-para … --fonte "<arquivo da destilação> <ID> [timestamp]"`. A ferramenta calcula o prazo nosso pela régua do plano de produção de entregáveis e recusa promessa sem fonte. Marco no `PAINEL.md` só quando o próximo ato for do cliente; se ele depende do nosso entregável, a linha leva `task: T-…`. **Veto:** V-ENT-1 (`METODO-GATE-DE-CONGRUENCIA.md` §3).

---

## 6. FERRAMENTA — limpeza do VTT

Script padrão. Roda no sandbox, sobre o arquivo bruto:

```python
import re
src = "<caminho do arquivo bruto>"
raw = open(src, encoding="utf-8").read().replace("\r\n", "\n")
turns = []
for b in raw.split("\n\n"):
    lines = [l for l in b.strip().split("\n") if l.strip()]
    if not lines or lines[0].startswith("WEBVTT"):
        continue
    ts = next((l for l in lines if "-->" in l), None)
    if not ts:
        continue
    txt = " ".join(l for l in lines if "-->" not in l).strip()
    if not txt:
        continue
    start = ts.split("-->")[0].strip()[:8]
    m = re.match(r"^([^:]{1,40}?):\s*(.*)$", txt)
    spk, body = (m.group(1), m.group(2)) if m else ("?", txt)
    if turns and turns[-1][0] == spk:          # agrupa falas consecutivas
        turns[-1][2] += " " + body
    else:
        turns.append([spk, start, body])
out = "\n\n".join(f"[{t[1]}] {t[0]}: {t[2]}" for t in turns)
open("TRANSCRIPT-...-LIMPO.md", "w", encoding="utf-8").write(out)
print("turnos:", len(turns), "| palavras:", len(out.split()))
```

Se a gravação não tiver identificação de falante, transcrever antes com ferramenta que separe vozes. **Transcrição sem falante identificado não serve para citação literal** — e citação literal é o núcleo do método.

---

## 7. VERSÃO CURTA — calls internas

Para call entre sócios (se houver) com decisão material, o mínimo é: **decisões com o descartado e o porquê · compromissos com dono e data · o que ficou em aberto.** Sem os doze eixos, sem índice de uso. Vai direto no `DIARIO-DE-BORDO.md` da Governança.

---

## 8. PDF — quando e como

**Nunca obrigatório.** O `.md` é o artefato; o PDF é uma apresentação dele.

Gerar PDF apenas quando o material vai ser **enviado a alguém de fora** que não lê Markdown com conforto — cliente, prospect, parceiro, contraparte.

Gerador e instruções: **`90-templates/pdf-continuum/`**. Não escrever CSS novo por documento — o template existe para que todo PDF nosso saia com a mesma assinatura visual.

**Antes de enviar, uma checagem:** a destilação contém a nossa leitura comercial — margem, ampliação de escopo não precificada, âncoras de proposta, avaliação de risco da conta. **Decidir conscientemente se o destinatário deve ver essa seção.** O método não decide por você; ele obriga a pergunta.

---

## 9. GATE DE SAÍDA

Uma destilação só está pronta quando as dez respostas forem sim:

1. **Toda citação tem timestamp?**
2. **Fato e leitura estão visivelmente separados?**
3. **Cada ponto tem ID estável?**
4. **Existe índice por destino de uso?**
5. **O que não foi dito está registrado?**
6. **A propagação para `STATUS`, `DECISOES` e diário foi feita nesta mesma tarefa?**
7. **A nossa própria fala foi auditada (eixo 13) e propagada para a skill de voz?**
8. **O que ele já ouviu de nós está registrado (eixo 14), com a divergência marcada, e a proposta escrita a respeita ou a corrige por escrito?**
9. **Todo compromisso com data e hora está na agenda do {{OPERADOR}}, com o relógio da contraparte na descrição?**
10. **Toda promessa nossa de entregável (eixo 15) tem task `tipo: entregavel` na fila, com fonte apontável?** (`entregaveis.py --verificar`)

E o teste final, o mesmo do §11.4 do kernel:

> **Outra pessoa, ou outra IA, abrindo só este arquivo, conseguiria escrever a próxima peça — copy, proposta, onboarding — sem ouvir a call e sem perguntar nada a ninguém?**

Se a resposta for não, falta eixo 5 (voz dela), falta eixo 13 (voz nossa) ou falta citação literal.

---

## 10. EXEMPLAR DE REFERÊNCIA

A primeira destilação completa da casa (uma call longa, com pontos por eixo e índice por destino de uso) é o exemplar; o aluno guarda a sua primeira como exemplar da própria operação e a relê antes das seguintes.

---

**Base:** `../CLAUDE.md` §11 (rastro e continuidade) · `../90-templates/pdf-continuum/` · `METODO-ANCORAGEM-DE-PROPOSTA.md` · `Método de extração de linguagem/`
