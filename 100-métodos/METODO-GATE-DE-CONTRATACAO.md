# MÉTODO CONTINUUM DE GATE DE CONTRATAÇÃO

> **Tipo:** política · secundário: gate (§3), registro (§7) *(reclassificado por auditoria independente de leitura integral; antes: "método-raiz (camada 2, política)")* · **Origem:** casa de origem do template ({{OPERADOR}}) · **Alçada:** {{OPERADOR}}
> **Revoga:** a leitura de que falta de hora reprova uma proposta. **Nunca mais se recusa venda por teto de horas.**
> **Depende de:** `00-core/POLITICAS-DE-DECISAO.md` §§1-5 · `100-métodos/METODO-ANCORAGEM-DE-PROPOSTA.md` §Âncora 7 e §3 · `CLAUDE.md` §§8-9
> **Aplicação:** obrigatória sempre que uma entrega, proposta ou frente exigir mais horas do que existem.

---

## 0. A premissa que organiza tudo

> ### **O que {{EMPRESA}} vende é o mindset do {{OPERADOR}} — a forma de pensar estratégia. Não é hora.**

Disso decorre a regra inteira, e ela é uma inversão:

| | Pode ser comprado | Não pode ser comprado |
|---|---|---|
| **Hora de execução** | ✅ sim — é insumo, tem preço, tem mercado | |
| **A forma de pensar estratégia** | | ❌ não — é o produto, e produto não se terceiriza |

**Consequência direta:** falta de hora **nunca** é motivo de recusa, porque hora é insumo comprável. O que é motivo de recusa é a entrega exigir que **o pensamento** seja delegado a quem ainda não pode recebê-lo.

**O erro que este método corta:** tratar capacidade como estoque fixo. Capacidade não é um número dado — é uma **variável de decisão**. Quem trata hora como teto recusa receita para proteger uma restrição que ele mesmo podia ter removido.

---

## 1. A regra, em três linhas

1. **Escopo estourou o teto de horas → aciona contratação.** Nunca recusa, nunca "reduz escopo por falta de tempo".
2. **A contratação começa sempre pela ponta de baixo da escada** (§2). Delega-se execução primeiro; pensamento, por último e por piso.
3. **Se a entrega só couber delegando estratégia antes do piso do §3 → aí sim recusa ou adia.** É a única recusa por capacidade que sobrevive.

---

## 2. Escada de delegação (a ordem é inegociável)

| Faixa | O que sai da mão do {{OPERADOR}} | Régua para liberar | Estado hoje |
|---|---|---|---|
| **D1 · Execução técnica** | build, integração, deploy, QA, implementação sob spec e gate | spec escrita + gate de aceite + revisão do {{OPERADOR}} no merge | **✅ liberada — é a primeira contratação** |
| **D2 · Operação de entrega** | configuração por cliente, rotina de acompanhamento, relatório, calibração de agente | D1 estável + SOP escrito do que se delega | 🟡 `a calibrar` |
| **D3 · Atendimento/CS + back-office** | suporte ao cliente, onboarding operacional, cobrança de insumo, financeiro/admin | D2 estável + roteiro de voz da casa | 🟡 `a calibrar` |
| **D4 · Estratégia** | diagnóstico, oferta, precificação, arquitetura de solução, condução de call, decisão de escopo | **§3 — piso duro** | 🔴 **fechada** |

**Por que a ordem não inverte:** D1 tem spec, gate e teste — o erro aparece antes de chegar no cliente. D4 não tem teste: o erro de diagnóstico só aparece três meses depois, dentro de um contrato, e a conta é da relação. **Delegar de cima para baixo é o jeito mais rápido de destruir o único ativo que não se recompra.**

---

## 3. Piso de D4 — quando a estratégia começa a ser delegada

**Duas condições, cumulativas. Nenhuma sozinha basta.**

### Condição A — faturamento
**MRR ≥ `{{META_MRR}}`** (o north star de `POLITICAS` §2). Antes disso, não se delega estratégia em hipótese nenhuma.

### Condição B — a pessoa
**12 meses ou mais de operação dentro da casa**, OU aprovação na **régua de exceção** abaixo.

#### Régua da pessoa excepcional (a exceção à condição B, nunca à condição A)

Seis critérios. **Não é impressão — cada um é observável, e a ausência de um reprova.**

| # | Critério | Como se observa |
|---|---|---|
| 1 | **Diagnostica antes de executar** | recebe a tarefa e devolve a pergunta que muda a tarefa |
| 2 | **Registra decisão com o descartado** | escreve o que não escolheu e por quê, **sem ser mandado** |
| 3 | **Traz número, não adjetivo** | nunca diz "melhorou"; diz quanto, sobre qual base |
| 4 | **Discorda com argumento** | não obedece por hierarquia. Quem só concorda não pode receber estratégia |
| 5 | **Aguenta a régua** | entrega dentro do gate sem pedir exceção; exceção pedida cedo demais é sinal |
| 6 | **Aprende a linguagem da casa** | precedência, camadas, gates, fonte única de fato — operando em < 30 dias |

**Teste prático, obrigatório antes de qualquer liberação de D4:** entregar um caso real e fechado do repositório (uma conta, uma proposta já decidida) e pedir o diagnóstico. Comparar com o que o {{OPERADOR}} decidiu de fato.
- Diferença de **conteúdo** (chegou noutro diagnóstico) → **não é a pessoa**.
- Diferença de **estilo** (mesmo diagnóstico, outra redação) → pode ser.

**A decisão de liberar D4 é sempre do {{OPERADOR}} e sempre registrada** — data, pessoa, qual critério fundamentou, o que continua não delegado.

---

## 4. Gatilhos de contratação

### 4.1 Gatilho primário — antecipação por cobertura de pipeline *(regra da casa)*

> **Cobertura de pipeline qualificado ≥ 3× a meta de venda do mês → contrata, antes de a venda fechar.**

É a mesma régua de previsibilidade de `POLITICAS` §3, usada agora como **sinal de contratação** e não só como gate de escala. Motivo: quem contrata depois de assinar entrega atrasado no primeiro mês, e no regime de garantia de execução (`POLITICAS` §5) **atraso nosso é mês não faturado**. A rampa (§5.3) precisa acontecer **antes** do contrato, não durante.

⚠️ **Este gatilho assume risco de caixa deliberadamente.** Ele contrata sobre pipeline, não sobre receita realizada. Quando o caixa está curto (conferir `STATUS.md` §1), isso não é detalhe — é a aposta. **As três condições de segurança do §5 existem para essa aposta não virar dívida.**

### 4.2 Gatilho secundário — por contrato fechado

Venda assinada cujo escopo estoura o teto → **contratação acionada na assinatura**, com o custo lançado dentro do próprio contrato (§5.1). Não se pede prazo maior ao cliente para caber na agenda; compra-se a hora.

### 4.3 Gatilho de defesa — tripwire

Horas comprometidas **> 85% por 2 semanas** (`POLITICAS` §4) → **aciona contratação**. ⚠️ Não pausa mais venda ativa. A leitura antiga do tripwire fica revogada por este método.

---

## 5. Os três freios que substituem o teto de horas

Retirar um freio sem colocar outro no lugar é como o teto de horas foi quebrado em outras operações. **Os três abaixo são o que impede que "nunca recusar por horas" vire "vender tudo".**

### 5.1 Freio de caixa — a contratação é paga por receita nomeada, nunca por esperança

| Regra | Detalhe |
|---|---|
| **Custo variável antes de custo fixo** | primeira contratação em **PJ por escopo/entrega**, no mesmo regime de task e gate que o repo já usa. CLT só depois de MRR estável cobrir 3 meses do custo |
| **Toda contratação nomeia a receita que a paga** | qual contrato, qual parcela, qual data. Contratação sem receita nomeada não é investimento, é torcida |
| **Reserva mínima** | contratar com caixa em R$ 0 exige entrada de contrato assinado ou reserva equivalente a **1 ciclo** do custo. `a calibrar` — número pendente do {{OPERADOR}} |

### 5.2 Freio de pensamento — o que nunca sai, e a única recusa que sobra

**Nunca se delega, em nenhum estágio de faturamento:** posicionamento · o que {{EMPRESA}} é e não é · abertura e fechamento de nicho · precificação · aceitar ou recusar cliente · decisão societária.
**Não se delega antes do piso do §3:** diagnóstico, arquitetura de solução, oferta, condução de call de venda.

> **A única recusa por capacidade que sobrevive a este método:** *a entrega exige delegar pensamento estratégico a quem ainda não pode recebê-lo.* Substitui a condição de recusa nº 4 do `METODO-ANCORAGEM-DE-PROPOSTA.md` §3.

### 5.3 Freio de rampa — prazo que ignora a curva de aprendizado mente

Pessoa nova não entrega no dia 1. **Toda proposta cuja entrega depende de contratação declara a rampa no prazo** — faixa de referência: **2 a 4 semanas** para D1 sob spec, `a calibrar` com o primeiro caso, `n=0`.

Enquanto a rampa corre, **a hora do {{OPERADOR}} é consumida em dobro** (executa e ensina). Isso entra na Âncora 7 como custo, não some. Prazo de proposta que não absorve a rampa é o mesmo erro de vender G3 no prazo de G1 — desta vez dentro de casa.

---

## 6. O que muda na Âncora 7 do método de ancoragem

**Antes:** Âncora 7 podia **vetar** a proposta por falta de capacidade.
**Agora:** Âncora 7 **precifica** a capacidade. Hora vira linha de custo, não veto.

```
7. NOSSO   valor-hora R$ __ (≥ `{{VALOR_HORA_PISO}}`?) · margem __% (≥ `{{MARGEM_MINIMA}}`?)
           ENTREGA: {{OPERADOR}} __h  ·  contratado __h a R$ __/h  ·  rampa __ semanas
           receita que paga a contratação: __________ (contrato, parcela, data)
           exige D4 antes do piso? S/N   ← se S, RECUSA. Único veto que resta
```

**O que não muda:** o piso de valor-hora (`{{VALOR_HORA_PISO}}`), a margem mínima (`{{MARGEM_MINIMA}}`) e o teto de desconto da política (`POLITICAS` §5). Comprar hora não autoriza furar piso — **autoriza entregar mais, não cobrar menos.**

---

## 7. Primeira contratação

| Item | Definição |
|---|---|
| **Faixa** | **D1 — execução técnica** |
| **Escopo** | build, integração, deploy, QA sob spec e gate. Sem contato com cliente, sem decisão de escopo |
| **Modelo** | **PJ por escopo/task**, no regime de gates que o repo já roda | 
| **Gatilho** | cobertura de pipeline ≥ 3× a meta do mês (§4.1) — conferir a cobertura vigente em `STATUS.md` §3 |
| **O que essa contratação libera** | as horas de build que travam o sistema próprio da operação (integrações, persistência autenticada, funções de borda) — o caminho crítico de toda oferta de sistema |
| **O que ela não libera** | diagnóstico, proposta, preço, call, arquitetura de solução |

⭐ **A leitura estratégica:** D1 é a contratação que **mais devolve hora e menos toca no produto**. Build tem spec, gate e teste — é a única faixa onde o erro do delegado é barato. É também onde está o gargalo real: as pendências técnicas do repo, não a falta de ideia.

---

## 8. Anti-padrões

| Anti-padrão | Por que quebra |
|---|---|
| **Recusar venda por falta de hora** | trata insumo comprável como restrição natural. Recusa receita para proteger um teto que se remove com dinheiro |
| **Delegar estratégia para ganhar tempo** | vende o produto errado. O cliente comprou uma forma de pensar e recebeu outra pessoa pensando |
| **Contratar depois de assinar** | a rampa acontece dentro do contrato, e com garantia de execução isso é mês não faturado |
| **Contratar sem receita nomeada** | vira custo fixo em cima de caixa zero. É a dívida com data marcada, do lado da despesa |
| **Prazo que ignora a rampa** | mesma física de vender G3 no prazo de G1, agora internamente |
| **CLT antes de MRR estável** | troca flexibilidade por obrigação num estágio em que a receita ainda não é previsível (`POLITICAS` §3) |
| **Régua da pessoa excepcional aplicada por simpatia** | os 6 critérios são observáveis. "Ela é muito boa" não é nenhum deles |

---

## 9. Onde este método entra

| Situação | Combinação |
|---|---|
| Proposta cujo escopo estoura o teto de horas | **este método** §6 + `METODO-ANCORAGEM-DE-PROPOSTA.md` Âncora 7 |
| Tripwire de 85% disparado | este método §4.3 + `POLITICAS` §4 |
| Cobertura de pipeline ≥ 3× | este método §4.1 — **contrata** |
| Alguém pede para assumir diagnóstico/call/preço | este método §3 + §5.2 |
| Avaliação de candidato para D4 | este método §3, régua dos 6 critérios + teste do caso real |

---
*Calibração pendente (`n=0` em tudo): reserva mínima de caixa para contratar (§5.1) · faixa real da rampa (§5.3) · pisos de D2 e D3 (§2). Recalibrar após a primeira contratação.*
*Registro: 2026-08-28 — instituído por {{OPERADOR}}. Origem: a régua antiga reprovava proposta por teto de horas, e a reprovação estava errada na raiz — o produto da casa é a forma de pensar, não a hora.*
