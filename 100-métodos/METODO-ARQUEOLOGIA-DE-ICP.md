# MÉTODO — Arqueologia de ICP (a língua de quem ouve)

> **Tipo:** método · secundário: framework (§1–§2), gate (§5) *(reclassificado 26/09/2026 por auditoria independente de leitura integral; antes: sem campo)*
> **Abrir por momento:** decidir §1–§2 · produzir §3 · conferir §5 *(mapa proposto pela auditoria de 26/09 — conferir no primeiro uso)*
> **Instituído em:** 10/09/2026 · **Gatilho:** perda de uma conta (Conta B) · **Dono:** {{OPERADOR}}
> **Registro do caso:** o encerramento da conta e a auditoria independente do circuito de copy, ambos no histórico da casa.
> **Irmão simétrico:** `100-métodos/Método de extração de linguagem/` (MEL). **O MEL extrai quem assina. Este extrai quem ouve.**

---

## 0. POR QUE ESTE MÉTODO EXISTE

Tínhamos, em 09/09/2026, duas skills de voz completas (`voz-operador` com corpus medido, `voz-<cliente>` com corpus hasheado), um gate anti-slop, um gate de voz com veto, um papel de arqueólogo, e um método de destilação de calls com 13 eixos e IDs estáveis.

**E escrevemos uma série de peças para um público que não existia.**

O ICP real estava documentado no próprio repositório, com ID: sinais sobre o poder de compra e a experiência do público, e uma frase vívida de dor, relatada pela equipe da conta. Essa frase foi marcada como a melhor do material colhido. Semanas depois, saiu um roteiro que pressupunha um público com o perfil oposto.

**Três buracos produziram isso, e nenhum deles era falta de dado:**

| # | Buraco | Onde estava |
|---|---|---|
| 1 | O eixo 4 da destilação (ICP, dor e desejo) **não tinha destino de propagação** | `METODO-DESTILACAO-DE-CALLS.md`, Etapa 7 |
| 2 | Nenhum gate testava **procedência**; todos testavam coerência interna | skill de copy, 10 passes |
| 3 | O MEL **autorizava** inferir o léxico do público a partir do da falante | MEL §2.5.3, "público-espelho" |

> **O veredito, e ele cabe em uma linha: cena inventada é internamente coerente por construção.** Ela é verossímil, específica e bem escrita — exatamente o que os gates de humanização premiam. **Um texto pode passar em todos os testes de qualidade e estar falando com ninguém.**

---

## 1. O PRINCÍPIO

> **A voz de quem vende e a voz de quem compra são duas línguas diferentes. Quanto mais especialista for quem vende, maior a distância entre elas.**

O especialista fala a língua do **método**. O comprador fala a língua do **sintoma**.

| Quem assina diz | Quem compra diz |
|---|---|
| "padrão de autossabotagem" | "começo e sempre largo no meio" |
| "problema de posicionamento" | "ninguém me procura" |
| "processo de individuação" | "não aguento mais ser a chata da família" |
| "gestão de fluxo de caixa" | "não sei se sobra no fim do mês" |

**Nenhuma dessas colunas se deduz da outra.** A da esquerda se colhe com o MEL. A da direita se colhe com este método. Usar a esquerda para escrever para quem fala a direita produz uma peça tecnicamente correta que o leitor não reconhece como sobre ele — e o cliente reconhece o problema antes de saber nomeá-lo, o que costuma sair como *"não ficou com a minha cara"*.

**Corolário incômodo:** quanto melhor a skill de voz do cliente, **maior** o risco. Uma skill de voz excelente torna a peça perfeitamente fiel a quem assina, o que faz o desalinhamento com quem ouve passar por todos os filtros de qualidade.

---

## 2. OS TRÊS GRAUS DE PROCEDÊNCIA

**Toda frase do banco entra com um grau. Frase sem grau equivale ao grau mais baixo.**

| Grau | O que é | Fontes típicas | Uso |
|---|---|---|---|
| **D · direta** | **o próprio ICP falando** | DM recebida, comentário em post, depoimento espontâneo, resposta de formulário, transcrição de call de venda com o cliente final, áudio de WhatsApp de cliente, avaliação pública | ✅ **entra em peça** |
| **R · relatada** | **o cliente ou a equipe citando o público.** Evidência de segunda mão | destilação de call com o cliente, entrevista com a equipe comercial, relato de atendimento | 🟡 **entra marcada.** Orienta a colheita e sustenta bloco quando não há `D`. **Não funda a cena central** |
| **I · inferida** | **formulação nossa**, por mais plausível que soe | nossa cabeça | 🔴 **nunca entra em peça.** Só vale como hipótese a colher |

### Por que o grau `R` merece uma seção própria

**A frase de dor do caso de origem (§0) é grau `R`.** Ela é a equipe da conta contando o que o público diz, não alguém do público dizendo. Tem fonte, tem timestamp, tem ID, e ainda assim é alguém traduzindo a fala de outra pessoa.

**Mesmo se tivesse sido usada, seria evidência de segunda mão.** Isso muda o desenho da correção: não bastava usar o dado que existia — **faltava colher o grau `D`, que ninguém tinha colhido.**

> **O `R` é o grau perigoso porque ele parece `D`.** Literal, citado, rastreável, e ainda assim filtrado pela cabeça de quem relatou. A equipe comercial descreve o cliente com o vocabulário que a empresa usa internamente, não com o que o cliente usou.

---

## 3. O PROCEDIMENTO — 5 ETAPAS

### Etapa 1 · Inventariar as fontes disponíveis, por grau

Antes de colher, listar **o que existe** e **o que dá para conseguir em 48 horas**, separando por grau. A maior parte das contas descobre aqui que tem muito `R` e quase nenhum `D`, e que o `D` está a um pedido de distância.

**Fontes de grau `D` que quase toda conta já tem e ninguém abre:**

- a caixa de entrada do Direct e do WhatsApp (a fonte mais rica e a menos usada)
- comentários dos posts que performaram
- respostas do formulário de aplicação, no campo aberto
- depoimentos que o cliente já publicou, **no texto original e não no recorte**
- áudios de clientes atuais
- prints de conversa de venda que a equipe comercial guarda

### Etapa 2 · Colher literal, sem corrigir

Copiar a frase **como foi dita**, com a pontuação torta, a gíria, o erro de concordância e o palavrão. **A frase corrigida perde exatamente o que a tornava útil.**

Registrar por frase: o texto literal · a fonte (qual canal, qual data) · o grau · quem falou, se identificável · o contexto em que apareceu.

### Etapa 3 · Classificar em 4 baldes

| Balde | O que é | Para que serve na peça |
|---|---|---|
| **Dor** | como ele descreve o problema, **na vida dele** | cena de abertura, conflito, bloco de espelho |
| **Desejo** | como ele descreve o depois | promessa, imagem de resultado |
| **Objeção** | como ele justifica não agir | coreografia de objeção, quebra |
| **Cena e rotina** ⭐ | **o que ele faz, com quem convive, que hora acorda, o que já tentou** | **é o balde que não existia, e é onde a invenção mora** |
| **Conclusão** ⭐ *(18/10/2026)* | **a causa que ele dá ao fracasso, e quem ele culpa**: a vontade da pessoa, o preparo, o engajamento, ele mesmo, o processo | **a crença-alvo do contrarian do lead** — o lead existe para derrubar uma conclusão (§6-quater) |

> **O quarto balde é a razão deste método.** Os três primeiros já existiam na arqueologia da skill de copy. **Cena nunca teve balde, nunca teve ID, e por isso era o único material que se fabricava sem acionar nenhum alarme.**

### Etapa 4 · Dar ID e alimentar o banco

ID estável, no padrão `<SIGLA-DO-CLIENTE>-LEX-<n>`. **Frase colhida que não volta para o banco morre no arquivo em que foi colhida** — foi exatamente o que aconteceu no caso de origem (§0).

### Etapa 5 · Fechar com a lacuna nomeada e a fonte que a resolve

Não basta dizer "falta dado". Nomear **qual grau falta, sobre qual tema, e qual fonte resolveria em quanto tempo**:

> *"Faltam frases de grau `D` sobre dinheiro. Resolve com 10 DMs do Direct ou 3 respostas do campo aberto do formulário. Uma hora de trabalho da equipe da conta."*

---

## 4. O ARTEFATO — `clientes/<cliente>/lexico-icp/` *(pasta da conta, no repositório da conta)*

Desenho idêntico ao das skills de voz, porque o problema é o mesmo com o sujeito trocado.

```
clientes/<cliente>/lexico-icp/
├── BANCO.md          ← as frases, com ID, grau, fonte e balde
├── FONTES.md         ← de onde veio cada corpus, com data e volume
└── LACUNAS.md        ← o que falta, por grau e por tema, com a fonte que resolve
```

**Template pronto em `90-templates/lexico-icp/`.** Copiar os três arquivos para a pasta do cliente e preencher. **A pasta se abre no onboarding, não na primeira peça** — abrir na primeira peça é abrir tarde.

**`BANCO.md` tem uma linha por frase:**

| ID | Frase literal | Balde | Grau | Fonte | Data |
|---|---|---|---|---|---|
| `XX-LEX-01` | *"…"* | dor | `D` | DM recebida | 00/00 |

**O banco é vivo.** Toda destilação de call nova alimenta o banco pelo eixo 4 (propagação obrigatória, `METODO-DESTILACAO-DE-CALLS.md` Etapa 7). Toda peça nova consulta o banco antes de escrever.

---

## 5. O GATE — veto, não checklist

Roda como **passe 11** da skill de copy (`copywriter-senior-continuum` v3.1) e vale para qualquer peça voltada a humano.

**Bloco de espelho** é toda passagem que afirma ao leitor o que ele faz, sente, fala, já tentou ou já viveu: *"você já…"*, *"quando você…"*, *"tem gente que…"*, e qualquer cena em segunda pessoa.

| # | Regra | Consequência |
|---|---|---|
| 1 | Todo bloco de espelho aponta o **ID** da frase de origem | sem ID, o bloco volta |
| 2 | **Grau `I` em bloco de espelho** | 🔴 **P0. Reprova a peça sozinha**, independentemente do score |
| 3 | Banco com **menos de 3 frases de grau `D`** | peça sai **marcada como rascunho**, e a marca vai na entrega ao cliente, não só no arquivo interno |
| 4 | **Banco inexistente** | **não se escreve.** A entrega é a lista do que colher |
| 5 | Lacuna declarada | **não substitui origem.** Declarar que falta não aprova a frase |
| 6 | 🔴 **Crença-alvo do lead com uma fonte só, ou tirada do fecho de um caso isolado** *(18/10/2026)* | **reprova sozinha.** A crença que o contrarian derruba é a de maior contagem no balde `conclusão` (§6-quater); frase única serve de cor de cena, nunca de alvo |

> **O teste, e ele é de dez segundos:** apontar **quem disse aquilo e onde**. Se a resposta for *"é plausível"*, a cena sai.

---

## 6. A REGRA DE ORDEM (a que teria mudado o desfecho)

**Nenhuma regra deste método teria salvado a Conta B.** A copy saiu **antes do diagnóstico**, por pedido urgente aceito, e **gate nenhum opera sobre material que não foi colhido.**

> **Pedido urgente de cliente não altera a ordem de dependência da entrega.** Copy depende de ICP. ICP depende de diagnóstico.
>
> **Quando a urgência é real, reduz-se o volume, nunca a dependência.** Uma peça com procedência vale mais que dez sem.

**As três respostas possíveis a "preciso para ontem", e só uma não pode dar certo:**

| Resposta | Veredito |
|---|---|
| Entregar **uma** peça, marcada como rascunho, sobre o único material com procedência | ✅ honesta e útil |
| Dizer que não cabe, e dizer **o que cabe e quando** | ✅ honesta |
| Entregar **dez peças completas como se fossem definitivas**, sobre ICP não colhido | 🔴 **a única que não podia dar certo** |

**E o agravante de leitura, registrado porque o repositório já tinha o sinal:** cliente com histórico de frustração com fornecedores e desconfiança sobre a entrega, **pedindo copy urgente antes do diagnóstico, está fazendo um teste de conformidade disfarçado de pedido operacional.** Entregar rápido e errado confirma exatamente esse medo.

---

## 6-bis. ⭐ O MESMO CORPUS TEM GRAUS DIFERENTES CONFORME O BANCO QUE ALIMENTA

**Achado da verificação de 10/09/2026** (replay do circuito de copy v3.1 contra um caso real).

A fala de um cliente sobre a própria dor é:

- **grau `D` no banco do NOSSO ICP** — ele é o nosso comprador, falando de si
- **grau `R` no banco do ICP DELE** — ali ele está descrevendo terceiros

> **Consequência operacional que estava sendo descartada: toda destilação de call com cliente produz, de graça, grau `D` para o nosso próprio banco.** Várias contas de material direto sobre o nosso ICP, e nenhum banco onde ele viva.

**Regra:** ao colher, declarar **para qual banco** a frase vai antes de atribuir o grau. A mesma citação pode entrar duas vezes, em bancos diferentes, com graus diferentes — e isso não é duplicação, é a coisa certa.

## 6-ter. ⭐ O QUE A IA PODE FAZER AQUI — e o que reprova na hora (20/09/2026)

> **Instituído depois de ler um material de terceiro que pede à IA um perfil do público em sete camadas, com instrução de soar específico e visceral e de devolver uma frase de efeito por dor e uma cena de vida.**

🔴 **Um artefato assim é grau `I` por construção — e é exatamente o que custou a Conta B.** Ele não se usa como insumo, por melhor que pareça. **E ele parece muito bom: é essa a armadilha.** Texto gerado com instrução de ser visceral soa mais verdadeiro que fala real, porque fala real é hesitante, repetitiva e sem clímax.

### 6-ter.1 A régua, em uma linha

> **A IA pode formular a PERGUNTA. Ela nunca pode fornecer a RESPOSTA.**

| Uso | Grau | Veredito |
|---|---|---|
| Gerar **hipótese de dor, desejo, medo e objeção**, para virar **roteiro de pergunta** na colheita | `I` | ✅ **legítimo, e útil** — acelera a entrevista e a varredura de fonte |
| Gerar **pauta de onde procurar**: que comunidade, que busca, que tipo de fonte teria essa fala | `I` | ✅ legítimo |
| Ser **contraditada pela colheita** — e o que ela errou é achado | `I` | ⭐ **o uso de maior valor**, ver 6-ter.3 |
| Virar **cena, fala, dor ou frase** numa peça | 🔴 `I` | **reprova a peça, sem exceção** |
| Entrar no `BANCO.md` | 🔴 `I` | **nunca. O banco é de grau `D`** |

### 6-ter.2 As sete camadas, convertidas em pauta de colheita

**A estrutura do prompt é boa; o que não presta é a saída ser tratada como dado. Convertida, ela vira um roteiro de sete perguntas — e cada uma tem fonte de grau `D` conhecida:**

| # | Camada | A pergunta que a colheita responde | Onde procurar |
|---:|---|---|---|
| 1 | quem é | *como ela se descreve, nas palavras dela?* | bio, apresentação em call, primeira mensagem |
| 2 | as maiores dores, **em ordem** | *o que ela diz primeiro quando pedem para falar do problema?* | call, áudio, comentário, DM |
| 3 | o que ela não admite em voz alta | *o que aparece como piada, hedge ou correção de si mesma?* | 🔴 é o mais difícil, e **não se infere** — vem de call longa |
| 4 | o que já tentou e falhou | *quais soluções ela nomeia?* | call, review de concorrente, fórum |
| 5 | o que ela acredita ser o problema | *como ela completa "eu não consigo porque…"?* | pergunta direta, em entrevista |
| 6 | o que teme | *o que ela diz que acontece se nada mudar?* | call, comentário |
| 7 | o que sonha, **com cena** | *que situação concreta ela descreve?* | 🔴 **cena é grau `D` ou não é cena** |

⚠️ **A camada 3 é a que mais atrai invenção, e é onde o dano é maior.** *"O que ela não admite em voz alta"* é um convite explícito a preencher com plausível. **Se não foi dito, fica como lacuna nomeada** (`LACUNAS.md`), com a fonte que a resolveria.

## 6-quater. 🔴 ⭐ A CRENÇA-ALVO DO LEAD — derivar, contar, perguntar (instituído 18/10/2026, alçada {{OPERADOR}})

**Caso que instituiu:** uma VSL em produção. O lead derrubava uma crença com fonte `D`, literal, aprovada pelo auditor de procedência. Mas era o **fecho de um caso** de **um** entrevistado, e uma versão mais geral já estava no corpus, destilada em call anterior e nunca levada ao banco. Ao ler o lead em voz alta, quem assina a peça corrigiu na hora: a conclusão real do público era outra, e pouca gente pensava como a frase dizia. **Procedência estava certa; representatividade, não.**

**O procedimento, antes de qualquer lead:**
1. **Derivar do mecanismo.** Se o mecanismo diz por que o resultado falha, quem não o conhece explica a falha com o que tem — em geral, um traço da pessoa. Escrever essa previsão como hipótese em `LACUNAS.md` (§6-ter.3).
2. **Colher contra a hipótese.** Varrer o corpus (calls, entrevistas, áudios) atrás de toda atribuição de causa e classificar no balde `conclusão`, por **quem é culpado**.
3. **Contar.** A crença-alvo é a de **maior número de fontes independentes**. Nunca a mais vívida.
4. **Perguntar o fato à expert** quando a contagem for fraca (< 2 fontes): *"quando o resultado não vem, o que o seu cliente diz que aconteceu?"* — lacuna de FATO, permitida pela REGRA Nº 0. Nunca *"o que faria você ficar no vídeo?"*, que é estrutura.

Veto: §5, regra 6.

### 6-ter.3 ⭐ O uso que vale mais que todos: a hipótese errada

**Gerar a hipótese ANTES de colher, guardá-la, e comparar depois.**

> **Onde a IA acertou, o nicho é óbvio — e argumento óbvio já está na peça de todo concorrente.**
> **Onde ela errou, está a vantagem** — é o que só quem colheu sabe, e é o que o `ESPACO-VAZIO.md` do benchmark procura por outro caminho.

**Fica registrado em `LACUNAS.md`, num bloco próprio:** *hipótese inicial · o que a colheita mostrou · a distância entre as duas.*

---

## 7. O QUE ESTE MÉTODO NÃO RESOLVE

- **Não substitui o diagnóstico.** Banco cheio com oferta errada produz peça precisa sobre a coisa errada.
- **Não substitui a voz de quem assina.** As duas entradas são necessárias, e são diferentes.
- **Não protege contra ordem invertida.** §6 é conduta, não gate — e conduta não se automatiza.
- **Não protege conta que já está fora de política.** Contrato que nasce abaixo do piso da casa é problema anterior a qualquer linha de copy.

---

**Base:** encerramento da Conta B e auditoria do circuito de copy (10/09/2026) · `100-métodos/METODO-DESTILACAO-DE-CALLS.md` Etapa 7 (eixo 4) · `100-métodos/Método de extração de linguagem/` §2.5.3 (fronteira do espelho) · `10-skills/copywriter-senior-continuum/` v3.1 (passe 11) · `CLAUDE.md` §6, §6.1
