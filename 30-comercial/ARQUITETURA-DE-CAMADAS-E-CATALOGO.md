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

# PARTE 2 · O CATÁLOGO {{EMPRESA}} — modelo a preencher

> ⚠️ **MODELO.** A casa de origem tinha aqui a escada dela; ela não vem. O que fica é a forma: **um produto por camada ocupada, preço de referência, gatilho de subida escrito, teto de capacidade.** Todo preço se verifica contra o piso de `{{VALOR_HORA_PISO}}`/h (`POLITICAS` §5), como checagem interna — nunca argumento de venda. Os produtos que os métodos já nomeiam (G0 pago: Mapa da Ordem; ICP B: Alicerce; recorrência: Assessoria) entram aqui com o preço de `POLITICAS` §5; o resto é seu.

## 4. O MAPA GERAL

```
CAMADA 5 · SISTEMA      <produto, se houver>.......... <setup> + <MRR>
CAMADA 4 · ASSESSORIA   Assessoria Estratégica......... setup + {{TICKET_ASSESSORIA}}/mês
                        · Alicerce (ICP B)............. {{TICKET_ALICERCE}}, escopo fechado
CAMADA 3 · CONSULTORIA  Mapa da Ordem · Núcleo......... {{TICKET_MAPA_NUCLEO}}
                        Mapa da Ordem · Operação....... a partir de {{TICKET_MAPA_OPERACAO}}
                        <consultoria de escopo único>.. <preço>
CAMADA 2 · MENTORIA     <produto, se houver>.......... <preço>/mês
CAMADA 1 · PRODUTO      <decisão: vende ou não>
```

> **Camada sem produto fica escrita como "não ocupada", com o motivo.** Camada vazia sem motivo vira produto improvisado na primeira conversa em que o cliente pede.

---

## 5. FICHA POR PRODUTO — uma por linha do mapa

| Campo | Preencher |
|---|---|
| **Camada** | 1 a 5 (§1) |
| **Objeto** — o que muda quando é bem entregue | |
| **Quem executa** | o cliente · o cliente com direção · nós e o cliente · o sistema |
| **A pergunta do cliente que ele responde** (régua 1 do §3) | uma só; se outro produto responde à mesma, um dos dois sai |
| **Escopo fechado** — o que entra · o que não entra | |
| **Preço de referência** e hora prevista | verificado contra `{{VALOR_HORA_PISO}}`/h |
| **Gatilho de subida** (régua 3 do §3) | para qual produto e com que sinal medido |
| **Teto simultâneo** | número e razão |
| **Caso que prova** | `n=0` até existir; escreve-se assim |

---

## 6. A ESCADA E OS GATILHOS DE SUBIDA

```
<produto de entrada> ──── <gatilho medido> ──→ <produto seguinte>
Alicerce ──── começou a vender ──→ vira ICP A e entra pelo Mapa
Mapa da Ordem ──── pede execução na devolutiva ──→ Assessoria
```

| De | Para | Gatilho escrito |
|---|---|---|
| Mapa da Ordem | Assessoria | o cliente pede execução na devolutiva · abate em `<N>` dias |
| Mapa Núcleo | Mapa Operação | quer as camadas de aquisição e medição · abate em `<N>` dias |
| `<…>` | `<…>` | `<sinal medido>` |

**Escada sem gatilho é lista de preços** (régua 3). O gatilho é um número ou um pedido literal do cliente, nunca "quando fizer sentido".

---

## 7. GATE DE CAPACIDADE — o que este catálogo obriga

| Produto | Teto simultâneo | Razão |
|---|---:|---|
| Alicerce | **1** | construção pura; `ICP.md` §4-bis |
| Assessoria | `a calibrar` | horas de entrega por semana (`POLITICAS` §4) |
| Mapa da Ordem | sem teto rígido | hora previsível por diagnóstico |
| `<…>` | | |

> 🔴 **Não abrir dois produtos novos no mesmo mês.** Produto novo sem caso consome o dobro da hora prevista, e dois ao mesmo tempo param a aquisição.

**Ordem de lançamento:** primeiro o que usa método que já existe e responde ao pedido que mais chega; por último o que depende de audiência.

---

## 8. DECISÕES ABERTAS

| # | Decisão | Trava |
|---:|---|---|
| 1 | | |

---
*Preços verificados contra `POLITICAS` §5. O que não tem dado fica `n=0`, escrito assim.*
