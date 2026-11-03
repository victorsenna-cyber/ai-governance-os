# ARQUITETURA DE CAMADAS E CATÁLOGO — {{EMPRESA}}

> ⚠️ MODELO — preencher com a oferta da {{EMPRESA}}; o desenho é o método, os valores são seus.

> **Tipo:** decisão de arquitetura comercial (camada 2) · **Alçada:** {{OPERADOR}}
> **Destino no repo:** `30-comercial/ARQUITETURA-DE-CAMADAS-E-CATALOGO.md`
> **O que resolve:** a casa passa a ter produtos em várias camadas, de diagnóstico a sistema. **Sem uma régua de camadas, isso vira catálogo canibalizado** — que é exatamente o vermelho que o Mapa da Ordem diagnostica nos clientes.
> **Amarrações:** `oferta.md` · `servicos.md` · `ICP.md` §4-bis · `POLITICAS` §5 · `100-métodos/METODO-DIAGNOSTICO-DE-OPERACAO.md`

---

# PARTE 1 · AS CAMADAS

## 1. A RÉGUA QUE SEPARA TUDO

**Duas perguntas classificam qualquer produto da casa:**

> **1 · Qual é o objeto?** O que muda quando o produto é bem entregue.
> **2 · Quem executa?** De quem é a mão que faz.

| Camada | **Objeto** | **Quem executa** | Hora nossa | Preço de referência |
|---|---|---|---|---|
| **1 · Produto** | o conhecimento | **o cliente, sozinho** | zero marginal | `{{FAIXA_PRODUTO}}` |
| **2 · Mentoria** | **a pessoa** — a capacidade dela | o cliente, com direção | baixa, recorrente | `{{FAIXA_MENTORIA}}`/mês |
| **3 · Consultoria** | **uma decisão** | o cliente | média, pontual | `{{FAIXA_CONSULTORIA}}` |
| **4 · Assessoria** | **o sistema do negócio** | **nós e o cliente, juntos** | alta, recorrente | setup + `{{FAIXA_ASSESSORIA_MENSAL}}`/mês |
| **5 · Sistema (OS)** | **a operação rodando** | **o sistema**, sem hora humana no loop | setup alto, operação baixa | `{{FAIXA_SISTEMA_SETUP}}` + MRR |

---

## 2. ⭐ AS DISTINÇÕES QUE MAIS CONFUNDEM

### Consultoria × Assessoria — **a fronteira é a mão, não a profundidade**

| | **Consultoria** | **Assessoria** |
|---|---|---|
| Entrega | **uma decisão fundamentada** | **o sistema construído e operando** |
| Termina | quando a decisão está tomada | quando o contrato acaba |
| Quem faz | o cliente | nós, com ele, toda semana |
| Formato | escopo e prazo fechados | recorrente |
| O que o cliente compra | **saber o que fazer** | **não precisar fazer sozinho** |

> **A régua em uma frase: consultoria entrega o quê; assessoria entrega o feito.**
> Confundir as duas é a origem da deriva de escopo — cliente que comprou consultoria e espera execução, ou assessoria vendida a preço de consultoria.

### Mentoria × Consultoria — **o objeto muda de lugar**

| | **Mentoria** | **Consultoria** |
|---|---|---|
| Objeto | **a pessoa** | **o negócio** |
| Depois dela | ele sabe decidir sozinho | a decisão está tomada |
| Pauta | dele | nossa |
| Sucesso | ele não precisa mais de você | o problema não volta |

> **Mentoria se compra pelo que a pessoa vira. Consultoria se compra pelo que o negócio resolve.**
> **E é por isso que mentoria escala e consultoria não:** numa mentoria a agenda é o produto, e dá para atender em grupo. Numa consultoria o diagnóstico é o produto, e ele é sempre único.

### Diagnóstico × Consultoria — **amplitude × foco**

O **Mapa da Ordem** mapeia a operação **inteira** e devolve a ordem. Uma **Consultoria** ataca **uma pergunta já nomeada**, em profundidade.

> **O Mapa serve a quem não sabe onde está o problema. A Consultoria serve a quem já sabe.**
> ⚠️ **É aqui que a canibalização nasce**, e a trava está na §5.

---

## 3. AS TRÊS RÉGUAS DE CATÁLOGO

**1 · Um produto por pergunta do cliente.** Se dois produtos respondem à mesma pergunta, um deles é redundante e a base aprende a esperar o mais barato.

**2 · Nenhum produto barato é a versão gravada de um caro.** É o erro que a casa diagnostica nos clientes: um curso barato que é a mentoria cara gravada. **Se o produto low ticket entrega o mesmo, ele não é degrau — é vazamento.**

**3 · Todo degrau tem gatilho de subida escrito.** Escada sem gatilho é lista de preços.

---

# PARTE 2 · O CATÁLOGO {{EMPRESA}}

> Todos os preços verificados contra o piso de `{{VALOR_HORA_PISO}}`/h (`POLITICAS` §5), como checagem interna — nunca argumento de venda.

## 4. O MAPA GERAL

```
CAMADA 5 · SISTEMA      {{EMPRESA}} OS ................. {{FAIXA_SISTEMA_SETUP}} + MRR
                        Repo de Governança ........... setup {{PRECO_REPO_SETUP}} + {{PRECO_REPO_MRR}}/mês   ⭐

CAMADA 4 · ASSESSORIA   Assessoria Estratégica ....... setup + mensalidade
                        · Alicerce (ICP B) ........... {{TICKET_ALICERCE}}, escopo fechado

CAMADA 3 · CONSULTORIA  Mapa da Ordem · Núcleo ....... {{TICKET_MAPA_NUCLEO}}
                        Mapa da Ordem · Operação ..... {{TICKET_MAPA_OPERACAO}}+
                        Consultorias de escopo único . {{FAIXA_CONSULTORIA_ESCOPO_UNICO}}   ⭐

CAMADA 2 · MENTORIA     Formação Repositório {{EMPRESA}} . {{TICKET_FORMACAO}} · 6 semanas, turma
                        Mentoria de Operador ......... {{PRECO_MENTORIA_OPERADOR}}/mês, 6 meses   ⭐
                        Mentoria em grupo ............ {{PRECO_MENTORIA_GRUPO}}/mês, turma       ⭐

CAMADA 1 · PRODUTO      → decisão de arquitetura (abaixo)
```

> ⭐ **Decisão de arquitetura do modelo (altere se decidir diferente):** **a {{EMPRESA}} não vende produto digital.** Low ticket é território da marca pessoal do {{OPERADOR}}, fora desta arquitetura. Isso mantém a {{EMPRESA}} com uma promessa só — estrutura comercial para quem já opera — e impede que ela vire loja.

---

## 5. ⭐ CONSULTORIAS DE ESCOPO ÚNICO

**O que são:** uma pergunta nomeada, resolvida em profundidade, com escopo e prazo fechados. **O cliente executa.**

### A trava contra canibalização do Mapa

> **Consultoria de escopo único só se vende a quem chega com o problema já nomeado E com a fundação de pé.**
>
> **O teste, na primeira conversa:** *"como você sabe que é isso?"*
> Se a resposta trouxer evidência — número, padrão observado, teste que ele fez — é Consultoria.
> Se a resposta for palpite, **é Mapa da Ordem**, e dizer isso em voz alta é o serviço.

**Por que a trava importa:** vender consultoria de funil a quem tem a camada 1 aberta entrega um funil ótimo para o cliente errado. **O cliente paga, recebe trabalho bom, e não vende.** É o pior desfecho possível, porque parece culpa nossa e é ordem errada.

### As quatro consultorias

| Consultoria | A pergunta que resolve | Entregável | Horas | Preço |
|---|---|---|---:|---:|
| ⭐ **Funil de Vendas** | *por qual caminho o meu lead chega até o pagamento?* | o percurso desenhado passo a passo · o **Pivô de Conversão** de cada ativo · roteiro da conversa de venda · pontos de medição | ~14h | **{{PRECO_CONSULTORIA_FUNIL}}** |
| **Arquitetura de Oferta e Preço** | *o que eu vendo, por quanto, em quais degraus?* | escada com preço por degrau · gatilhos de subida · o que sai do catálogo · fronteira escrita | ~12h | **{{PRECO_CONSULTORIA_OFERTA}}** |
| **Narrativa e Mecanismo** | *por que comprar de mim?* | inimigo · mecanismo nomeado · promessa e fronteira · as 3 provas que sustentam | ~10h | **{{PRECO_CONSULTORIA_NARRATIVA}}** |
| **Conteúdo que Converte** | *por que o meu conteúdo não vira venda?* | matriz de leitura aplicada · hook, pivô e CTA diagnosticados · 10 roteiros na voz dele · linha editorial de 30 dias | ~18h | **{{PRECO_CONSULTORIA_CONTEUDO}}** |

**Formato padrão de todas:** 1 call de extração (90 min) → produção → entrega do documento → 1 call de devolutiva (60 min) → **1 call de revisão 30 dias depois**, para corrigir sobre o que a execução mostrou.

> **A call dos 30 dias é o que separa consultoria de PDF.** Ela custa 1h e é o que faz o cliente executar — porque existe uma data em que alguém vai perguntar.

**O que fica fora, sempre:** execução, produção de peça final, gestão de campanha. **Consultoria entrega o quê.**

---

## 6. ⭐ MENTORIAS

**O objeto é a pessoa.** Não o negócio dela.

### 6.1 Mentoria de Operador — individual

| | |
|---|---|
| **Para quem** | fundador ou o braço direito dele, que vai **executar a estratégia** e precisa aprender a decidir sozinho |
| **Formato** | 2 calls de 60 min por mês + canal assíncrono de dúvidas |
| **Pauta** | **dele.** Ele traz a decisão da semana; a gente decide junto e nomeia a régua |
| **O que se entrega** | não é material: é **critério**. Ao fim, ele tem um conjunto de réguas próprias, escritas |
| **Duração** | 6 meses, mínimo |
| **Horas** | ~4h/mês |
| **Preço** | **{{PRECO_MENTORIA_OPERADOR}}/mês** (~4h/mês: confira o valor-hora; acima do piso é assim que mentoria se paga) |
| **Gate de saída** | ele toma três decisões seguidas sem consultar, e as três seguem as réguas que ele escreveu |

> **Por que mentoria vale mais por hora que assessoria:** na assessoria você compra trabalho. Na mentoria você compra critério, e critério não se consome — **ele fica com a pessoa depois que o contrato acaba.**

### 6.2 Mentoria em Grupo — turma

| | |
|---|---|
| **Para quem** | operadores em estágio parecido, de negócios que não competem entre si |
| **Formato** | 1 encontro de 90 min por semana, turma de 8 a 12 · grupo permanente |
| **Estrutura** | 12 semanas, uma camada da **Ordem da Receita** por bloco |
| **Horas** | ~8h/mês para a turma inteira |
| **Preço** | **{{PRECO_MENTORIA_GRUPO}}/mês** por pessoa · 3 meses |
| **Economia** | 8 pessoas × preço mensal, por ~8h de trabalho. Calcule o valor-hora: é, em geral, o produto de maior valor-hora da casa |
| **Gate de entrada** | 🔴 **só abre com 6 inscritos confirmados.** Turma com 3 vira consultoria coletiva mal paga |

> ⚠️ **A régua que protege a turma:** ninguém entra sem ter operação rodando. **Mistura de estágios mata turma** — quem já vende acha raso, quem não vende acha inaplicável, e os dois saem.

---

## 7. ⭐ REPO CONTINUUM DE GOVERNANÇA EMPRESARIAL

> **É o produto mais diferenciado da casa, e o único que nasce de um ativo que já existe e já está em uso.**

### O que é

**O sistema de governança que a {{EMPRESA}} roda internamente, instanciado para a empresa do cliente:** um repositório vivo onde decisão, método, política e estado da operação moram em arquivos — e onde IA opera **sobre** a governança, não ao lado dela.

**A estrutura que se instancia:**

| Camada | O que vive nela |
|---|---|
| **Kernel** | princípio, prioridade, regras permanentes, modos de resposta |
| **Políticas** | os números que decidem: pisos, tetos, alçadas, gates |
| **Métodos** | o *como* de cada frente recorrente, versionado |
| **Skills** | procedimentos executáveis por qualquer modelo de IA |
| **Contas / áreas** | estado vivo, log de decisões com o descartado e o porquê |
| **Rituais** | o que se olha, quando, e o que dispara ação |

### O problema que ele resolve, e é maior que "organização"

> **Empresa sem governança escrita repete decisão.** A mesma discussão volta a cada três meses porque ninguém registrou o que foi descartado e por quê. **Decisão sem descarte registrado é meia decisão: alguém refaz o caminho já andado.**
>
> **E com IA isso piora, não melhora.** Modelo sem governança dá resposta plausível sobre um contexto que ele não conhece. **Quem coloca IA numa operação sem regra escrita não automatizou a decisão: automatizou a improvisação.**

### O que se entrega

| Fase | O quê | Prazo |
|---|---|---|
| **1 · Extração** | as regras que já existem na cabeça do dono viram texto | semanas 1–3 |
| **2 · Estrutura** | kernel, políticas, métodos e taxonomia instanciados para o negócio dele | semanas 4–6 |
| **3 · Operação com IA** | skills executáveis, protocolo multi-modelo, roteador | semanas 7–9 |
| **4 · Ritual** | cadência de atualização, gate de registro, quem escreve o quê | semanas 10–12 |

| | |
|---|---|
| **Preço** | **setup {{PRECO_REPO_SETUP}}** (~48h) **+ {{PRECO_REPO_MRR}}/mês** de curadoria e atualização |
| **Recorrência — por que existe** | 🔴 **repositório sem curadoria apodrece em três meses.** A mensalidade não é suporte: é o que impede o ativo de virar arquivo morto |
| **ICP** | operação com 5+ pessoas, ou fundador que já delega e vê decisão se repetir. **Não é para operação de uma pessoa só** |
| **Gate de entrada** | ⚠️ **o dono precisa escrever.** Se ele não aceitar registrar decisão, o repo não sobrevive ao mês 2 — e é recusa, não desconto |

> **A prova que este produto pode ter e nenhum outro da casa tem:** rodar dentro da própria empresa que o vende, com log de decisões, correções de fato registradas e métodos versionados. **É o único produto que se demonstra ao vivo, abrindo a tela.**

---

## 8. A ESCADA COMPLETA E OS GATILHOS DE SUBIDA

```
Mentoria em grupo ──── vende mais e quer individual ──→ Mentoria de Operador
                                                              │
Mapa da Ordem ──── quer que alguém execute ──→ Assessoria Estratégica
     │                                                │
     └── sabe onde é o problema ──→ Consultoria      │
                                                      ├──→ {{EMPRESA}} OS
                                                      └──→ Repo de Governança
Alicerce ──── começou a vender ──→ vira ICP A e entra pelo Mapa
```

| De | Para | Gatilho escrito |
|---|---|---|
| Mapa | Assessoria | o cliente pede execução na devolutiva · abate em 15 dias |
| Mapa Núcleo | Mapa Operação | quer as camadas de aquisição e medição · abate em 60 dias |
| Consultoria | Assessoria | a decisão foi tomada e ele não executou em 30 dias. **A régua da call dos 30 dias existe para revelar isso** |
| Mentoria grupo | Mentoria individual | ele traz decisão que não cabe no grupo |
| Assessoria | {{EMPRESA}} OS | volume de atendimento vira gargalo, com número |
| Assessoria | Repo de Governança | a equipe cresceu e a decisão começou a se repetir |

---

## 9. GATE DE CAPACIDADE — o que este catálogo obriga

**Sete produtos é muita superfície para uma pessoa.** As travas:

| Produto | Teto simultâneo | Razão |
|---|---:|---|
| Alicerce | **1** | construção pura, ~40h/mês |
| Repo de Governança | **1** | setup de 48h concentrado |
| Assessoria | 3 | já registrado |
| Consultoria | 2 | escopo fechado, mas concentra hora |
| Mapa da Ordem | sem teto rígido | 8h a 20h, previsível |
| Mentoria individual | 4 | 4h/mês cada |
| Mentoria em grupo | 1 turma | 8h/mês |

> 🔴 **A régua que decide a ordem de lançamento:** **não abrir dois produtos novos no mesmo mês.** Produto novo sem caso consome o dobro de hora prevista, e dois ao mesmo tempo param a aquisição.

**Ordem de lançamento recomendada:**

| # | Produto | Por quê primeiro |
|---:|---|---|
| **1** | **Consultoria de Funil de Vendas** | usa método que já existe, escopo fechado, e responde ao pedido que mais chega |
| **2** | **Mentoria de Operador** | maior valor-hora, carga baixa, e cabe junto de qualquer outra coisa |
| **3** | **Repo de Governança** | maior diferencial e maior ticket — mas exige um caso do próprio repo documentado como demonstração |
| **4** | Mentoria em grupo | depende de 6 inscritos, que dependem de audiência |

---

## 10. DECISÕES ABERTAS

| # | Decisão | Trava |
|---:|---|---|
| **1** | Os 4 nomes de consultoria são descritivos. **Nomear como produto** (ex.: "Consultoria <nome do mecanismo>") ou manter descritivo? | material de venda |
| **2** | Repo de Governança: o preço de setup é estimativa de 48h. **Validar com o primeiro escopo real** | `POLITICAS` §5 |
| **3** | A mentoria individual conflita com o gate de delegação de estratégia (`continuum-operacao`)? **Não — mentoria é o {{OPERADOR}} ensinando, não delegando** | registrar |
| **4** | Ordem de lançamento: confirmar Consultoria de Funil como primeira | calendário |

---
*Preços verificados contra `POLITICAS` §5. Marca pessoal e produtos low/mid ticket vivem fora desta arquitetura.*
