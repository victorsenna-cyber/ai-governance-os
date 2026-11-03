# TAXONOMIA DE ARTEFATOS — framework, método, política, gate, trilho, blueprint

> **Tipo:** framework · secundário: política (§7) *(antes: "vocabulário" — um tipo fora do próprio vocabulário; corrigido 26/09/2026)* · camada 1, identidade · **Instituído:** 26/09/2026 · **Alçada:** {{OPERADOR}}
> **Por que vive em `00-core/` e não em `100-métodos/`:** um arquivo que define nomes não é um método. **Colocá-lo em `100-métodos/` seria o primeiro erro que ele existe para corrigir.**
> **Gatilho:** a necessidade de diferenciar o que é framework, o que é método, o que são blueprints, o que estava confundido e como aprimorar.

---

## 0. O DIAGNÓSTICO — e ele é contável, não impressão

| Medida | Valor |
|---|---|
| Arquivos com prefixo `METODO-` em `100-métodos/` | **28** |
| ~~Deles, com **etapas numeradas** (procedimento de verdade)~~ | ~~🔴 **6**~~ → 🔴 **errado — ver §0-bis** |
| Naturezas distintas convivendo sob o mesmo prefixo | **6** |
| Variações do campo `Tipo:` — todas dizendo "método" | **7** (`método-raiz`, `método canônico`, `método`, `método-raiz autoral`, `método-raiz (camada 2)`, `(camada 2, política)`, `(camada de método)`) |
| Arquivos **sem** campo `Tipo:` | **8** |
| Arquivos em `100-métodos/` que **não são método nem nada disso** — são registros | **3** |

> ## ~~🔴 22 dos 28 arquivos chamados "MÉTODO" não contêm procedimento nenhum.~~ *(errado — corrigido no §0-bis, no mesmo dia)*
>
> **E o repositório já sabia disso sem perceber.** O §0 do `METODO-DIRECT-RESPONSE.md`, escrito em 18/09, classifica os próprios irmãos: *"um formato · uma prática · uma teoria · uma técnica"*. **Quatro naturezas nomeadas corretamente na mesma tabela — e todas as quatro chamadas de método no nome do arquivo.**

**O custo, e ele é o que o `METODO-GATE-DE-CONGRUENCIA.md` §P0 já mede sem saber a causa:** quem carrega *"o método X"* espera procedimento. Recebe princípio, ou gate, ou tabela de alçada. **Método que sobrou no output quase sempre não sobrou — foi carregado esperando fazer uma coisa que ele nunca fez.**

---

## 0-bis. 🔴 ⭐ CORREÇÃO NO MESMO DIA — o número do §0 estava errado, e quem achou foi a auditoria independente

> **O que aconteceu:** o §0 foi escrito sobre uma varredura por `grep` que contava títulos no formato *"Etapa N"* ou *"Fase N"*. **Ela mediu o FORMATO do cabeçalho, não a existência de procedimento.** Apresentei o resultado como *"contável, não impressão"* — e era uma impressão com um número.
>
> **Como apareceu:** agentes independentes, em contexto isolado, **leram o acervo na íntegra** sem acesso a esta taxonomia nem ao `STATUS.md`. É o buraco 4 do `METODO-GATE-DE-CONGRUENCIA.md` — **autoauditoria no mesmo contexto** — confirmado com dado: a minha própria classificação tinha passado pela minha própria revisão.

| Medida | Minha leitura (grep) | Leitura integral independente |
|---|---|---|
| Arquivos de conhecimento em `100-métodos/` | 28 | **29** (28 `METODO-` + `MATRIZ-LEITURA-CONTEUDO`) · mais 3 registros |
| Com procedimento real | ~~6~~ | **~19** — em forma de passos, fases com letra, rito ou sequência numerada |
| **Método por natureza dominante** | 10 | **14** |
| **Outra natureza sob o nome `METODO-`** | — | **15** — 9 framework · 2 política · 2 gate · 1 trilho · 1 ponteiro |
| **Híbridos (2+ tipos secundários)** | "dois" | 🔴 **quase todos** |

**Concordância: 20 de 29.** As 9 diferenças, e o que se decidiu em cada uma:

| Arquivo | Eu | Auditoria | Decisão |
|---|---|---|---|
| `PONTOS-LOGICOS` | método | framework (~60% é teoria; procedimento no §8) | ✅ **framework** |
| `ANCORAGEM-DE-PROPOSTA` | política | método (§1 → §2 → veredito) | ✅ **método** |
| `ESTIMATIVA-DE-CARGA` | política | framework (~60% é reenquadre) | ✅ **framework** |
| `FUNIL-DE-VSL` | trilho | método (Fases 0–4, saída nomeada) | ✅ **método** |
| `ABORDAGEM-FRIA` · `SALESFORCE-INBOUND` · `TRAFEGO-PAGO` | 🔴 **"ponteiro"** | método · framework · método | 🔴 **erro meu:** contei os ponteiros da RAIZ como se fossem os arquivos de `100-métodos/`, que são as **fontes ativas** |
| `DIAGNOSTICO-DE-OPERACAO` | 🔴 omitido | método | erro meu — ficou fora da lista |
| `MATRIZ-LEITURA-CONTEUDO` | "a classificar" | framework | ✅ fechado |

> ## ⭐ O diagnóstico corrigido é MAIS útil que o errado.
>
> **O defeito do acervo não é falta de procedimento — é HÍBRIDO SEM MAPA.** Quase todo arquivo é um pequeno "todo" com framework, método, gate e política dentro, e **nada diz ao leitor qual seção abrir em qual momento.** Quem abre para decidir lê o procedimento; quem abre para conferir lê a tese.
>
> **Por isso a correção deixou de ser "partir os dois maiores" (§5) e passou a ser uma linha no cabeçalho de cada híbrido — `Abrir por momento: decidir §x · produzir §y · conferir §z`.** Ela entrega o benefício da partição sem o custo: nenhum link quebrado, nenhuma fonte duplicada. **Aplicada em 26/09 a 18 arquivos**, com o `Tipo:` reclassificado nos 32 e a proveniência declarada em cada um (*"antes: …"*).

**Dois achados da auditoria que não eram o pedido e ficam registrados:**
- 🔴 **Duas fontes da mesma tabela:** a matriz de leitura de conteúdo existe em `MATRIZ-LEITURA-CONTEUDO.md` §3 (8 linhas) **e** em `METODO-DIAGNOSTICO-DE-OPERACAO.md` §5.4 (6 linhas). Divergência silenciosa esperando acontecer.
- Um método pode ter cópia de elaboração na antessala (`execução Codex/`), marcada *"não carregar"* — é a antessala funcionando, não duplicata de canônico.

---

## 1. OS SEIS TIPOS — e cada um tem um teste de uma linha

**A pergunta que classifica qualquer artefato:** *o que ele faz com quem o lê?*

| Tipo | O que faz | Teste de uma linha | Tem etapas? | Como se usa |
|---|---|---|---|---|
| ⭐ **FRAMEWORK** | muda o que você **acredita** | *"isto explica POR QUE funciona?"* | **não, e não deve** | se **carrega** antes de decidir |
| ⭐ **MÉTODO** | diz o que você **faz, em ordem** | *"tem etapa 1, e uma saída com nome?"* | **sim, sempre** | se **roda**, do início ao fim |
| **POLÍTICA** | diz o que você **pode e não pode** | *"tem número, piso, teto ou alçada?"* | não | se **consulta** para validar |
| **GATE** | diz se o que saiu **passa** | *"tem item que reprova sozinho?"* | não — tem checklist | se **roda no fim**, e devolve |
| **TRILHO** | diz em que **ordem** os outros rodam | *"ele ordena outros artefatos?"* | tem **etapas de OUTROS** | se **abre** no começo da frente |
| **BLUEPRINT** | é a **forma vazia** | *"eu copio e preencho?"* | não | se **copia** e preenche |

> **Classes auxiliares — não são tipo e não contam como sétimo:** **registro** (relato datado do que foi feito ou verificado) · **ponteiro** (só aponta para a fonte ativa) · **índice** (navegação: `README`, `MAPA-DO-REPO`, tabela de vetos). Elas descrevem **estado e navegação**, não conhecimento — e é por isso que o campo `Tipo:` as aceita sem violar o teto do §7.

### 1.1 🔴 As três fronteiras que mais se confundem

> **FRAMEWORK × MÉTODO.** *"A copy é uma sequência de atos persuasivos"* é framework — muda como você lê qualquer peça e **não tem passo nenhum.** *"Segmente o transcript, marque cada elemento, conte por bloco"* é método. 🔴 **Framework carregado como método produz passos inventados**, porque quem espera procedimento e recebe princípio preenche a lacuna.

> **POLÍTICA × GATE.** Política diz **antes** o que se pode (*"margem mínima 40%"*). Gate diz **depois** se passou (*"a peça tem pivô apontável?"*). 🔴 **O `METODO-GATE-DE-CONTRATACAO.md` é o exemplo vivo do erro: o nome diz gate, a natureza é política** — ele tem escada, piso e alçada, e não tem checklist de saída.

> **MÉTODO × TRILHO.** Método produz **um artefato**. Trilho produz **uma ordem** e não produz artefato nenhum — **é o índice da frente.** O `METODO-TRILHO-DE-CONTA-NOVA.md` declara isso na própria abertura (*"não cria método: ORDENA os que existem"*) e ainda se chama método.

---

## 2. A CLASSIFICAÇÃO DO ACERVO — os 28, por natureza dominante

> ⚠️ **Primeira leitura, preservada como registro. A classificação vigente é a reconciliada do §0-bis** — e ela está gravada no campo `Tipo:` de cada arquivo, que é onde o roteador e o verificador a leem.

### 2.1 FRAMEWORK — 5

`DIRECT-RESPONSE` *(o tronco de DR)* · `ESTRUTURA-INVISIVEL` · `GERACAO-DE-RESULTADOS` · `CAMADA-DE-VER` · `PIVO-DE-CONVERSAO`

⚠️ **Nenhum tem etapa, e está correto que não tenham.** O erro é o nome prometer procedimento.

### 2.2 MÉTODO — 10

**Com etapas explícitas (6):** `DESTILACAO-DE-VSL` (9) · `DESTILACAO-DE-CALLS` (7) · `EMPILHAMENTO-DE-HOOKS` (7) · `LATERALIZACAO-DE-CRIATIVOS` (7) · `ARQUEOLOGIA-DE-ICP` (5) · `ALICERCE` (3)

**Com procedimento em outra forma (4):** `BENCHMARKING` (6 fases em letra, por isso a varredura não pegou) · `MECANISMO-E-ONE-BELIEF` · `PONTOS-LOGICOS` · `CONSTRUCAO-DE-CRIATIVOS-DR`

### 2.3 POLÍTICA — 4

`ALCADA-DE-ESTRUTURA` *(é a `REGRA Nº 0` em forma longa)* · `GATE-DE-CONTRATACAO` 🔴 *(nome errado)* · `ANCORAGEM-DE-PROPOSTA` *(dominante; ver §3.3)* · `ESTIMATIVA-DE-CARGA`

### 2.4 GATE — 2

`GATE-DE-CONGRUENCIA` · `TESTE-DE-PILARES` *(5 perguntas binárias que bloqueiam produção — gate com nome de teste, e aqui o nome está quase certo)*

### 2.5 TRILHO — 2, e **um sem arquivo**

`TRILHO-DE-CONTA-NOVA` · `FUNIL-DE-VSL` *(dominante; ver §3.3)*
🔴 **E o terceiro: o CIRCUITO DE PÁGINA, que é trilho puro e vive dentro do `CLAUDE.md` §6.3, sem arquivo próprio.** Mesma natureza, dois lugares diferentes.

### 2.6 BLUEPRINT — 7, e são os únicos coerentes hoje

Tudo em `90-templates/`: `repo-cliente/` · `conta-nova/` · `benchmark-vsl/` · `lexico-icp/` · `diagnostico-operacao/` · `pdf-noturno/` · `pdf-continuum/` · `CONTRATO-EXECUTOR.md`

> ⭐ **A pasta de blueprints é a parte mais bem organizada do repositório, e por um motivo que vale roubar: o nome da pasta declara a natureza, não o assunto.** É exatamente o que `100-métodos/` não faz.

### 2.7 PONTEIRO — 4 · e **REGISTRO no lugar errado — 3**

**Ponteiros (corretos):** `ABORDAGEM-FRIA` · `PAGINA-DE-VENDAS` · `SALESFORCE-INBOUND` · `TRAFEGO-PAGO` na raiz.

🔴 **Registros morando em `100-métodos/`** (auditorias de circuito, verificações de versão, promoções de peça — datados e nomeados pelo ato). **Não são método, framework nem gate — são o registro de que algo foi verificado.** Pertencem a um `registros/`, e estão ali porque a pasta virou "onde se guarda o que é importante".

⚠️ **`MATRIZ-LEITURA-CONTEUDO` fica `A CLASSIFICAR`** — não abri o conteúdo nesta auditoria, e classificar por título é o que produz o erro que este arquivo corrige.

---

## 3. O QUE ESTÁ CONFUNDIDO — cinco achados, em ordem de custo

### 3.1 🔴 O prefixo `METODO-` não discrimina nada

**28 arquivos, 6 naturezas, um nome.** O prefixo deixou de significar *"isto é um procedimento"* e passou a significar *"isto é importante"*. **Quando um rótulo vale para tudo, ele deixa de informar** — e o roteador, que é o único mecanismo de carga (`REGRA Nº 1`), carrega às cegas.

### 3.2 🔴 O campo `Tipo:` existe e está vazio de conteúdo

Sete variações — `método-raiz`, `método canônico`, `método`, `método-raiz autoral` — **e nenhuma diz a natureza.** Mais 8 arquivos sem o campo.

> ⭐ **Isto é a boa notícia da auditoria: o mecanismo já existe.** Não falta campo, falta **vocabulário no campo.** A correção é de valor, não de estrutura — e é por isso que ela é barata.

### 3.3 🔴 Os dois maiores arquivos do repositório são os dois menos classificáveis

| Arquivo | Linhas | Faz | Natureza |
|---|---:|---|---|
| `FUNIL-DE-VSL` | **725** | ordena a produção · explica por que funciona · reprova no fim | **trilho + framework + gate** |
| `ANCORAGEM-DE-PROPOSTA` | **702** | 7 âncoras com números · 6 gates de saída · folha para preencher | **política + gate + blueprint** |

> ## ⭐ Não é coincidência que os dois maiores sejam os dois híbridos. É causa.
>
> **Arquivo que faz três coisas não tem critério para parar de crescer** — toda régua nova cabe em algum dos três papéis. **E arquivo que ninguém consegue nomear é arquivo que ninguém abre inteiro**, o que produz exatamente o defeito que o `METODO-ESTIMATIVA-DE-CARGA.md` §3 registra: produção acima da absorção.

### 3.4 Nome que contradiz natureza, em dois casos

`GATE-DE-CONTRATACAO` **é política** (escada D1-D4, pisos, alçada — nenhum checklist de saída).
`TESTE-DE-PILARES` **é gate** (5 binárias, P1/P4 reprovam produção de copy).

**Os dois nomes estão trocados entre si.**

### 3.5 ⚠️ Falta o nível acima — e é o único achado que não se resolve renomeando

**O `DIRECT-RESPONSE` se declara "TRONCO", e é — da família de resposta direta.** Mas não há tronco da **casa**: nenhum framework diz o que a {{EMPRESA}} acredita sobre como um negócio cresce, e de onde os métodos comerciais, de operação e de precificação derivam.

O `PRINCIPIO-CONTINUUM.md` existe em `00-core/` e **não conversa com nenhum método** — é citado como identidade, nunca como premissa de decisão. 🔴 **Consequência: temos três famílias de método (DR · operação · precificação) e nada que explique por que as três pertencem à mesma empresa.**

**Declarado como lacuna, não resolvido aqui.** Escrever o framework da casa é trabalho próprio, e fazê-lo no fim de uma auditoria de nomes seria o mesmo erro de construir galho antes de tronco — **desta vez com o tronco sabendo que está sendo improvisado.**

---

## 4. A CORREÇÃO — barata por decisão, em três atos

> 🔴 **O que NÃO se faz: renomear os 28 arquivos.** São 200+ referências cruzadas em `CLAUDE.md`, `AGENTS.md`, skills e pastas de cliente. **O ganho é de clareza; o custo seria uma semana de links quebrados e duas fontes divergentes** — exatamente o que os ponteiros existem para evitar.

| # | Ato | Custo |
|---:|---|---|
| **1** | ⭐ **O campo `Tipo:` passa a carregar a natureza real**, do vocabulário do §1: `framework` · `método` · `política` · `gate` · `trilho` · `blueprint`. **Uma linha por arquivo, 28 arquivos** | baixo |
| **2** | 🔴 **O roteador do `§6` declara o tipo junto do caminho** — `METODO-DIRECT-RESPONSE.md` *(framework)*. **É o que informa o agente sobre o que esperar antes de abrir** | baixo |
| **3** | **Híbrido declara a natureza dominante e as secundárias** no cabeçalho, sem partir o arquivo: *"trilho, com framework embutido no §5 e gate no §10"* | baixo |

### 4.1 ⭐ O que o tipo muda na ORDEM DE CARGA — e é aqui que a taxonomia paga

**Não é catalogação. É protocolo:**

```
FRAMEWORK   → carrega PRIMEIRO, antes de decidir qualquer coisa
TRILHO      → abre a frente e diz quais métodos rodam, em que ordem
MÉTODO      → roda, e produz o artefato
BLUEPRINT   → recebe o que o método produziu
POLÍTICA    → consultada quando há número, piso ou alçada em jogo
GATE        → roda por ÚLTIMO, e devolve
```

🔴 **Carregar fora desta ordem tem sintoma nomeável:** gate antes de método reprova o que não existe · método antes de framework produz peça tecnicamente correta e estrategicamente errada · **blueprint antes de método é a pasta preenchida a palpite**, que é como uma matriz de benchmark passa o gate sem ter medido nada.

---

### 4.2 🔴 ⭐ O PROCESSO — a ordem que liga os tipos, e por que ela é o que teria evitado o erro de uma conta *(26/09/2026)*

> **Os seis tipos são os substantivos. O PROCESSO é a sintaxe.** Não é um sétimo tipo: é **a ordem em que os tipos entram em qualquer tarefa** — `framework → trilho → método → blueprint → política → gate`.

**Processo × trilho, porque os dois ordenam e não são a mesma coisa:**

| | Ordena | Vale para |
|---|---|---|
| **PROCESSO** | **TIPOS** — o que se carrega antes do quê | **toda tarefa**, sem exceção |
| **TRILHO** | **ARTEFATOS** de uma frente — diagnóstico → ICP → pilares → copy | **uma frente** (conta nova, VSL, página) |

⭐ **Um trilho é o processo instanciado para uma frente.** O processo é o que garante que todo trilho novo nasça com a mesma forma.

#### O caso que o processo explica

**Uma conta:** um lote de peças com estrutura aprovada em todos os gates e cenas de ICP inventadas, porque o ICP nunca tinha rodado.

**Lido pelo processo:** rodou-se **método** (a skill de copy) e **gate** (os passes dela). **Pulou-se o trilho** — ICP antes de copy — e o framework que diz de onde a cena vem. E **o gate aprovou**, porque conferia a forma da própria etapa.

> ## 🔴 A regra que decorre: GATE NÃO SUBSTITUI ETAPA ANTERIOR.
>
> **Um gate confere duas coisas, e não uma: a própria etapa, E a existência das etapas anteriores com saída.** O veto de procedência da arqueologia (*grau `I` em bloco de espelho reprova*) é exatamente esse remendo, feito depois da perda — **o processo o torna regra geral em vez de exceção de um método.**

**E a régua de urgência do `CLAUDE.md` §6.1** (*"reduz-se o volume, nunca a dependência"*) **é o processo dito de outro jeito: urgência encolhe a quantidade de peças, nunca a quantidade de tipos.**

#### O que o processo exige do roteador

**Rotear para um arquivo solto não aplica o processo — rotear para uma ÁRVORE aplica.** Uma árvore declara, para uma família de pedidos, **qual framework, qual trilho, qual método, qual blueprint, qual política e qual gate** — na ordem. É o objeto da auditoria de roteamento de 26/09/2026.

---

## 5. OS HÍBRIDOS QUE VALEM PARTIR — e são só dois

> ~~Partir os dois maiores~~ → 🔴 **substituído em 26/09 pela linha `Abrir por momento` (§0-bis)**: mesmo benefício, sem link quebrado nem fonte duplicada. Seção preservada como registro do raciocínio descartado.

**Partir arquivo é caro. Só se justifica quando o arquivo é grande, é carregado com frequência e as partes têm ordens de carga DIFERENTES** — que é o caso de exatamente dois:

| Arquivo | Partir em | Por quê |
|---|---|---|
| `FUNIL-DE-VSL` (725) | **trilho** (a ordem das fases) + **framework** (por que o formato funciona) + **gate** (as 6 condições de recusa) | as três partes carregam em **momentos opostos** do trabalho: o framework antes de decidir se há VSL, o trilho ao produzir, o gate no fim |
| `ANCORAGEM-DE-PROPOSTA` (702) | **política** (as 7 âncoras e os números) + **blueprint** (a folha interna) + **gate** (os 6 de saída) | hoje quem precisa só da folha carrega 702 linhas, **e quem precisa do gate também** |

⚠️ **Nenhum dos dois se parte nesta tarefa.** Cada um é o procedimento de quatro passos do `§7.1` item 3 — conteúdo íntegro para `_legado/`, ponteiro no caminho antigo, linha no índice, roteamento atualizado. **Duas tarefas próprias, e a fila já tem dívida aberta.**

---

## 6. ONDE ISTO TOCA O `repo-cliente/`

⭐ **A taxonomia resolve uma pergunta que o template de 23/09 deixou implícita: o repo do cliente recebe qual tipo de artefato?**

| Tipo | Vai no repo do cliente? |
|---|---|
| **BLUEPRINT** preenchido com os dados dele | ✅ **sim — é o que ele compra** |
| **POLÍTICA** da operação dele (preço, o que não se promete) | ✅ sim |
| **GATE** de publicação da operação dele | ✅ sim |
| **TRILHO** de produção dele | ✅ sim |
| 🔴 **FRAMEWORK** e **MÉTODO** nossos | ❌ **nunca** — é a vara, e ela fica na casa |

> **É a fronteira *peixe × vara* do `90-templates/repo-cliente/README.md` §2, agora com vocabulário que a torna decidível em vez de intuitiva.** O teste antigo era *"serviria a outro cliente com um copiar-colar?"*; **o novo é mais rápido: qual é o `Tipo:` do arquivo?**

---

## 7. O QUE ESTA TAXONOMIA NÃO FAZ

- **Não renomeia nada.** Ver §4.
- **Não cria tipo novo por conveniência.** Seis é o teto; **sétimo tipo exige decisão registrada**, porque taxonomia de oito categorias é pior que nenhuma — ninguém decora, e todos chutam.
- **Não classifica por assunto.** Dois arquivos sobre VSL podem ser de tipos diferentes, e é justamente isso que o nome `METODO-` esconde hoje.
- 🔴 **Não resolve a lacuna do §3.5.** O framework da casa continua faltando, **e agora está escrito que falta.**

---
*Instituído em 26/09/2026, alçada {{OPERADOR}}. Diagnóstico medido por varredura do acervo (28 arquivos), não por leitura de títulos. **A evidência de que a confusão era real e antiga: o §0 do `METODO-DIRECT-RESPONSE.md` nomeou quatro naturezas corretamente em 18/09 e chamou as quatro de método.** 🟡 Vigência provisória: o vocabulário vale desde já; a aplicação do campo `Tipo:` nos 28 arquivos é tarefa própria, e é ela que testa a taxonomia em caso real.*
