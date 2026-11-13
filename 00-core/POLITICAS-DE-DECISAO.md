# POLÍTICAS DE DECISÃO — Números, Alçadas e Tripwires

> **Tipo:** política (camada 2) · **Status:** 🟡 **modelo a calibrar pelo operador no dia 1** (`LEIA-ME-TEMPLATE.md`)
> Fonte única dos números que decidem. As personas (`10-skills/`) consultam este arquivo; nenhuma skill carrega número próprio.
> Mudança aqui = decisão registrada (data + motivo no rodapé).
> **Como ler este modelo:** o que está entre `{{…}}` é número da sua operação; o que não está é regra do método e vale como está. As réguas são as que uma operação real de uma pessoa levou meses para instituir; cada uma traz o porquê. **Trocar um número é calibração; apagar uma régua é decisão, e se registra no rodapé.**

---

## 1. Alçadas de decisão (quem decide o quê)

> **Premissa do template: um operador, `{{OPERADOR}}`, com 100% da empresa.** Não existe "consenso obrigatório entre sócios". Toda alçada desta tabela é do operador. A linha "decisão estrutural societária" permanece como categoria, aplicável a decisões futuras (entrada de sócio, CNPJ, cap table). Se houver sócios, a tabela ganha uma coluna por sócio e a linha societária volta a exigir consenso — e **nada disso vale sem instrumento escrito** (`80-juridico/POLITICAS-JURIDICAS.md` §1).

| Decisão | Alçada |
|---|---|
| Posicionamento, preço, exceção comercial | **{{OPERADOR}}** |
| Processo interno, ajuste de escopo de cliente ativo | **{{OPERADOR}}** |
| Aceitar novo cliente | **{{OPERADOR}} aprova + {{OPERADOR}} valida capacidade (§4).** **Os dois gates são obrigatórios**, e numa operação de uma pessoa são a mesma pessoa fazendo duas contas diferentes: uma quer vender, a outra tem que entregar. **O gate de capacidade não deixa de existir por não ter um segundo par de olhos: ele passa a exigir disciplina no lugar de conversa** |
| Investimento / despesa > `{{TETO_DESPESA}}` | **{{OPERADOR}}** |
| Desconto acima do teto (§5) | **{{OPERADOR}}** |
| Abrir/fechar nicho ou frente comercial | **{{OPERADOR}}**, com critério do §6 atendido |
| Decisão estrutural societária | **{{OPERADOR}}**. Categoria mantida para decisões futuras: entrada de sócio, CNPJ, cap table |
| **Fato que falta sobre um cliente** (preço dele, capacidade, prova, o que entrega) | **{{OPERADOR}} primeiro, com a leitura default declarada; o cliente só quando ele mandar.** A resposta dele entra na conta com fonte `{{OPERADOR}}, data`. Regra em `CLAUDE.md` §5.2 |
| **Ato reversível dentro do repositório** (consertar, mover, criar, registrar, propagar) | **O agente, com aviso no fecho.** Só a lista fechada do `CLAUDE.md` §5.2 (fonte: `40-operacao-rotinas/ferramentas/autonomia.py`) pede a palavra do {{OPERADOR}} |
| **Conserto de ferramenta, modelo ou rota achado no caminho** | **O agente, na mesma tarefa, testado.** Se a ferramenta roda em infraestrutura compartilhada (servidor, serviço sempre ligado): código pronto e testado, deploy do {{OPERADOR}} (lista fechada, item 5) |
| **Ato de infraestrutura exigido por um pedido que já nomeia o resultado funcionando** ("roda todo dia", "na nuvem", "no ar", "ligado") | **O agente: testa, liga e avisa.** O pedido é a palavra (`CLAUDE.md` §5.2, estado final). **Dinheiro, contrato, mensagem a terceiro e apagar de vez continuam com o {{OPERADOR}}**, ato a ato. Pergunta dele "já está pronto/rodando?" sobre o que pediu = falha nossa: executa-se no mesmo turno |
| **Correção de falha do kernel** (`CLAUDE.md`, `00-core/`, gates) | **O agente, com backup antes** (`40-operacao-rotinas/ferramentas/backup-governanca.py --marco`), registro no `STATUS.md` e aviso. Encolher a lista fechada, Regras Nº 0–2, validação financeira e revogar decisão literal dele: **{{OPERADOR}}** |
| **Mensagem a cliente, grupo ou prospect por canal automatizado** (número de automação, robô de envio) | **{{OPERADOR}}, uma a uma (A1):** ordem literal na sessão, ou aprovação no canal dele. Origem A2 só com a palavra dele, tipo a tipo (`40-operacao-rotinas/ferramentas/autonomia.py`) |

## 2. Norte e trajetória (o que estamos construindo)

- **North star: `{{META_MRR}}` de MRR** (horizonte: `{{DATA_HORIZONTE}}`; marcos intermediários em `60-planos/PLANO-90-DIAS.md`).
- **Trajetória em 3 estágios com gates de transição:**

| Estágio | Motor comercial | Gate de saída (quando muda o foco) |
|---|---|---|
| **A — Caixa** | `{{MOTOR_DE_CAIXA}}` (o produto de ciclo curto que paga o mês) | MRR ≥ `{{MRR_ESTAGIO_B}}` → o motor de caixa cai a 50% da energia comercial |
| **B — Carteira → MRR** | conversão da carteira do Estágio A em recorrência + primeiros contratos de maior ticket | MRR ≥ `{{MRR_ESTAGIO_C}}` **e** 2 segmentos com n≥3 clientes recorrentes → foco muda |
| **C — Sistemas** | venda direta do produto de maior valor; o motor de caixa só como porta oportunista | MRR ≥ `{{META_MRR}}` → decisão de contratação e productização |

- A tese de investimento (se existir) aponta o destino; este arquivo governa o caminho.

## 3. Previsibilidade (definição operacional)

"Não escalar sem previsibilidade" significa, verificavelmente:

- **Pipeline coverage ≥ 3×**: valor qualificado no pipeline ≥ 3× a meta de venda do mês.
- **Forecast confiável**: 2 meses consecutivos com realização ≥ 80% do previsto.
- **Retenção comprovada**: churn ≤ 3%/mês por 2 meses.

Só com os três atendidos escalamos aquisição, preço ou estrutura. (Exceção condicional: janela de blitzscaling, `00-core/BLITZSCALING.md` — por padrão **fechada**.)

## 4. Capacidade (régua de aceite de cliente)

**Capacidade é número, não sensação:**

- **Horas de entrega disponíveis:** `{{HORAS_ENTREGA_SEMANA}}` h/semana do operador. 🔴 **`a calibrar` na primeira semana — este número decide sozinho quantos clientes cabem.** Medir, não presumir (§4-quater).
- **Teto de comprometimento: 70%** das horas de entrega. *(Exemplo: a 20h/semana, ~87h/mês, o teto é ~61h/mês.)*
- **Tripwire:** horas comprometidas > 85% por 2 semanas → 🔴 **aciona contratação** (§4-bis). Nunca "pausa de venda ativa".

| Horas de entrega reais | Teto 70% | O que cabe (exemplo: 40h/mês comprometidas, somando contas em operação e contrato novo) |
|---:|---:|---|
| 20h/sem (~87h/mês) | 61h/mês | ✅ 40h comprometidas = 66% do teto, 21h de folga |
| 24h/sem (~104h/mês) | 73h/mês | ✅ 55% do teto |
| 30h/sem (~130h/mês) | 91h/mês | ✅ 44% do teto |

> **A lição que esta tabela carrega:** medir a carga de uma conta só pela fase de construção, quando ela já está em operação, infla o número várias vezes — e leva a recusar contrato novo "por capacidade estourada" sobre um número inflado. A causa está no §4-ter e é mais cara que o número.

## 4-ter. ⭐ CURVA DE CARGA — carga de conta não é constante mensal

**O erro acima não é de aritmética. É de modelo:** tratar carga como número fixo por conta, quando carga de conta é **curva com duas fases de ordem de grandeza diferente.**

| Fase | O que consome | Carga | Ordem de grandeza |
|---|---|---|---|
| **Construção** | tracking, BM de anúncios, domínio, ICP, oferta, produto, narrativa, páginas, funil | **alta** | dezenas de horas por mês, durante toda a construção |
| **Operação** | execução, cadência, iteração, leitura de dado, ajuste | **baixa** | **poucas horas por mês** |

**Duas consequências, e a segunda é a que custa dinheiro.**

**1. Toda estimativa de horas declara em qual fase está.** Número de carga sem fase declarada é inutilizável — subestima a construção e superestima a operação, e erra nas duas direções ao mesmo tempo.

**2. 🔴 Preço único para contrato com duas fases de carga é sempre errado — e a conta mostra por quê:** a mesma mensalidade sobre cargas de ordem de grandeza diferente dá valores-hora de ordem de grandeza diferente:

| Fase | Preço mensal | Horas | **Valor-hora real** |
|---|---:|---:|---:|
| Construção (ciclo 1) | a mesma mensalidade | dezenas de horas por mês | 🔴 **muito abaixo do piso** |
| Operação (ciclo 2, renovação) | a mesma mensalidade | poucas horas por mês | ✅ **acima do piso** |

> ⭐ **O que isso obriga a registrar: o contrato que fura o piso é o ORIGINAL, não a renovação.** O ciclo 1 vende construção a preço de operação e roda **muito abaixo do piso** enquanto dura. **A renovação ao mesmo preço não é desconto: é a primeira fase do contrato em que a conta se paga.**
>
> **E explica um sintoma que costuma ficar sem causa:** a operação entregou muito, o cliente está satisfeito, e o caixa não melhorou. **Não foi falta de venda. Foi vender construção a preço de operação — e o ciclo acabar justo antes da fase lucrativa.**

**A régua que fecha:** contrato com fase de construção sai em **duas linhas — setup + mensal**, ou a construção é subsidiada pela operação **e o cliente que sai no fim do ciclo 1 leva o subsídio embora.** Preço liso em contrato de duas fases não é simplificação: é o subsídio escondido de quem escreveu.

## 4-quater. Estimativa de hora presume operação manual — e a nossa não é

**Números de carga herdados por analogia com agência tradicional são hipótese.** Uma operação que executa com IA tem a diferença justamente na fase de operação, onde a curva do §4-ter cai.

**Duas regras, e a segunda protege a primeira:**

1. **Hora se mede, não se presume.** Toda carga declarada em folha interna traz a marca de proveniência: `[medido]` · `[estimado por analogia]` · `[hipótese]`. **Analogia com agência tradicional é hipótese, nunca dado.**
2. 🔴 **Ganho de IA sobe a margem, não desce o preço.** A economia de hora é **nossa vantagem competitiva e a fonte de capacidade** — repassá-la integralmente ao cliente entrega a vantagem e mantém o mesmo aperto com mais entrega. **O preço continua se decidindo por capacidade geradora de riqueza (§5), nunca por quanto tempo levamos.**

> **Corolário para a régua de exposição de §5:** com IA, hora exposta a cliente é ainda mais perigosa — porque a conta fica boa demais e convida a pergunta errada. **O produto continua sendo o ativo que sobra, não o tempo gasto.**

> **⭐ A régua que mudou de peso.** Estourar capacidade sempre custou sono. **Com a garantia de execução (§5), custa dinheiro: entrega nossa atrasada por culpa nossa é um mês não faturado.** O gate de capacidade deixou de ser higiene interna e virou risco de receita direto.

- **Onboardings simultâneos: máximo 3** — e o onboarding inteiro é do operador (`30-comercial/onboarding.md`).
- **Novo cliente só entra se**: horas projetadas do contrato + carteira atual ≤ `{{TETO_HORAS_MES}}` h/mês **e** há vaga de onboarding. Senão: 🔴 **aciona contratação (§4-bis)** — fila com data e preço de exceção continuam sendo alternativas, **recusar por horas não é uma delas**.
- **Tripwire:** horas comprometidas > 85% por 2 semanas → 🔴 **aciona contratação** (§4-bis). Automatizar é alternativa; pausar venda **não é**.

## 4-bis. ⭐ GATE DE CONTRATAÇÃO — hora é insumo, não é teto

> **Regra-mãe: nunca se recusa venda, escopo ou frente por falta de horas.**
> **O que a {{EMPRESA}} vende é a forma de pensar estratégia do operador. Hora de execução é insumo comprável; a forma de pensar, não.**
> Escopo que estoura o teto **aciona contratação**, sempre. Método completo, escada de delegação, régua da pessoa excepcional e os três freios: `100-métodos/METODO-GATE-DE-CONTRATACAO.md`.

**O que o §4 acima passa a significar.** Os números de capacidade continuam valendo como **medida**, e deixam de valer como **veto**. Teto estourado não fecha a porta: abre uma decisão de contratação, com custo, receita nomeada e rampa.

| Faixa de delegação | Régua para liberar | Estado |
|---|---|---|
| **D1 · execução técnica** (build, integração, deploy, QA sob spec e gate) | spec + gate de aceite + revisão do operador | **✅ liberada — primeira contratação** |
| **D2 · operação de entrega** | D1 estável + SOP escrito | 🟡 `a calibrar` |
| **D3 · atendimento/CS + back-office** | D2 estável | 🟡 `a calibrar` |
| **D4 · estratégia** (diagnóstico, oferta, precificação, arquitetura, condução de call) | **MRR ≥ `{{META_MRR}}`** **E** (12+ meses de casa **OU** régua da pessoa excepcional), com decisão registrada | 🔴 **fechada** |

**Nunca se delega, em nenhum estágio:** posicionamento · precificação · abrir/fechar nicho · aceitar ou recusar cliente · decisão societária.

**Gatilhos de contratação:**
- **Primário — cobertura de pipeline ≥ 3× a meta do mês** (§3): contrata **antes** de a venda fechar, para a rampa acontecer fora do contrato. ⚠️ assume risco de caixa deliberadamente.
- **Secundário — contrato assinado** cujo escopo estoura o teto: contratação acionada na assinatura, custo lançado no próprio contrato.
- **Defesa — tripwire de 85% por 2 semanas:** 🔴 **aciona contratação. Não pausa venda ativa.**

**Os três freios que substituem o teto de horas:**
1. **Caixa** — PJ por escopo antes de CLT; toda contratação nomeia a receita que a paga (contrato, parcela, data); reserva mínima `a calibrar`.
2. **Pensamento** — a única recusa por capacidade que sobrevive: *a entrega exige delegar estratégia a quem ainda não pode recebê-la*.
3. **Rampa** — 2 a 4 semanas para D1 (`n=0`), com hora do operador consumida em dobro no período. Prazo de proposta que ignora a rampa mente.

**Comprar hora autoriza entregar mais, nunca cobrar menos.** Piso de `{{VALOR_HORA_PISO}}`/h, margem de `{{MARGEM_MINIMA}}` e teto de desconto de 10% seguem intactos.

## 5. Pricing (modelo, pisos e tetos)

> **Fronteira:** esta seção define **quanto** cobramos. **Como a proposta se ancora** — breakeven, payback, curva de gerações, custo da inação, condições de validade, cenários e as 5 condições de recusa — vive em `100-métodos/METODO-ANCORAGEM-DE-PROPOSTA.md`. Os pisos abaixo são a **Âncora 7** daquele método: nenhuma proposta sai sem ser validada contra eles.

> **⭐ Régua de exposição (alcance de carteira): serviço por hora NUNCA é mostrado a cliente.**
> O preço se **decide** por **capacidade geradora de riqueza** — quanto o ativo construído faz o cliente ganhar, e em quanto tempo. O preço se **verifica** pelos pisos desta seção.
>
> | | Decide o preço | Verifica o preço |
> |---|---|---|
> | Olha para | o cliente | nós |
> | Instrumento | breakeven dele, payback, curva de gerações, custo da inação | valor-hora, margem, capacidade, folga de horas |
> | Vive em | proposta, folha do cliente, artifacts | **Âncora 7, e só ali** |
> | Sai da casa? | sim | **nunca** |
>
> **O piso de valor-hora não é revogado por esta régua: ele muda de função.** Deixa de ser método de precificação e passa a ser **checagem interna de viabilidade**. Continua obrigatório e continua podendo vetar um preço; o que ele deixa de ser é a **razão** pela qual o preço é aquele. **Preço decidido por hora confessa que o produto é tempo. O nosso produto é o ativo que sobra depois.**
>
> **Obrigação operacional:** antes de qualquer artefato ir a cliente, varrer por "por hora", "R$/h", "valor-hora" e horas de escopo nossas. Agenda ou horas **do cliente** ficam — costumam ser o núcleo do argumento de valor.

**Modelo:** setup (paga a montagem, antecipa caixa) + recorrência (MRR, paga a operação e financia o produto). Serviço avulso existe só como porta de entrada.

> ### ⭐ NO QUE O PREÇO SE ANCORA
>
> **Preço se ancora na entrega e no retorno provável. Nunca na hora.**
>
> Ancoramos em três coisas: **capacidade real de entrega** · **probabilidade de retorno para o cliente** (receita gerada, ou estrutura viável para o objetivo declarado dele) · **estrutura e método já validados** sobre os quais a entrega se apoia.
>
> **Nunca ancoramos em** horas trabalhadas, esforço percebido, tabela de mercado, o que o cliente pode pagar, ou comparação com salário de contratação.
>
> **Gate de recusa:** não se oferece nada sem probabilidade real de gerar receita ou criar estrutura viável. Sem uma das duas, a proposta não é cara nem barata — **não deveria existir**.
>
> Método completo: `100-métodos/METODO-ANCORAGEM-DE-PROPOSTA.md` §0-bis.

- **Valor-hora de referência interna: `{{VALOR_HORA_PISO}}`/h.** ⚠️ **É gate de viabilidade, não método de precificação.** Nenhuma proposta sai com preço implícito abaixo disso (preço ÷ horas estimadas ≥ piso) — e o motivo tem duas faces: protege a margem **e protege a entrega**. Escopo que não cabe no preço vira entrega menor, e entrega menor destrói a probabilidade de retorno que ancorou o preço. **O teto de horas serve ao cliente antes de servir a nós.** A conta de hora vive na folha interna e **nunca aparece como justificativa de preço para o cliente**.
- **Piso de margem de contribuição: `{{MARGEM_MINIMA}}`** em recorrência (nosso custo é hora + ferramenta; margem protege capacidade). Referência do método: 70%.
- **Comissão de indicação é custo de aquisição (CAC), não custo de hora.** Sai da nossa margem e **não entra na conta do piso por hora**: o piso se confere sobre o preço que o cliente paga. Enquanto o CAC não entra no cálculo do preço, vale o preço de tabela, e o CAC fica registrado por conta para virar a base desse cálculo (o destino natural é o preço passar a pagar a própria aquisição).
- **Desconto:** teto de **10%**, e **somente no setup, nunca no MRR** (recorrência barata é gargalo perpétuo). Acima disso: {{OPERADOR}}. Alternativa preferida a desconto: **reduzir escopo, não preço**.
- **⭐ Desconto por prazo nasce na RENOVAÇÃO, não no contrato longo.** Contrato longo assinado hoje dá desconto sobre trabalho ainda não orçado. **O ciclo 2 não repete a construção do ciclo 1**, e é só isso que autoriza cobrar menos por ele. **O erro que a régua corrige é conceitual: desconto por volume pressupõe que o custo unitário cai com a escala, e em serviço com entrega mensal ele não cai** — o mês 12 consome quase as mesmas horas do mês 6. **Volume sem economia de escala é só desconto.**
- 🔴 **⭐ CAPITAL DE TESTE DE MÍDIA — piso de entrada.** Frente que depende de tráfego frio para validar (funil de VSL e equivalentes) **só abre com capital reservado para 2 a 3 tentativas**, nunca uma. Faixa de benchmark: **`{{VERBA_POR_TENTATIVA}}` por tentativa → 2 a 3× isso de exposição** (referência de mercado: R$ 2.000–3.000 por tentativa). **Reservado significa separado, não previsto.** Razão com número: a assertividade de referência é ~30% por tentativa, logo **uma tentativa isolada tem ~70% de chance de não provar nada** — e o dinheiro sai sem gerar venda nem aprendizado utilizável. **Quem tem capital para uma tentativa não tem capital para a frente: tem para um teste de mensagem.** Se o capital é do cliente, entra nas condições de validade da proposta (Âncora 5). Se é nosso, valida contra o caixa vivo do `STATUS.md`. Método: `100-métodos/METODO-FUNIL-DE-VSL.md` §2.2.
- **⭐ Taxa de meio de pagamento é sempre repassada, nunca absorvida.** Razão: no parcelamento longo a taxa leva uma fatia grande do bruto, e absorvê-la derruba a operação para baixo do piso. **Antes de cotar parcelamento, confirmar qual dos dois modelos a operadora usa** — coeficiente de parcelamento (o comprador paga os juros, recebemos o cheio) ou taxa deduzida do bruto (`bruto = líquido ÷ (1 − taxa)`). Sobre a mesma taxa nominal os dois divergem materialmente, e errar o modelo é sub-recuperar em silêncio.
- **⭐ Garantia de execução: autorizada como padrão. Garantia de resultado: segue vedada.** Formulação canônica: *"Se uma entrega marcada como nossa não sair na data marcada, e o atraso for nosso, você não paga aquele mês."* Incondicional do nosso lado, verificável sem interpretação, obrigação de meio. **Garantia com condição de contrapartida do cliente não vale: ela é lida como letra miúda e não vende.**
- ⭐ **O setup é sempre maior que a parcela mensal.** Se o setup fica abaixo da mensalidade, o preço está afirmando que a montagem vale menos que um mês de manutenção — e não vale: **o setup é o que decide se o resto funciona.** A régua vale também **depois de juros de parcelamento**, que é onde ela costuma quebrar.
  **Quando a régua for violada, corrige-se por acréscimo no setup, nunca por redução da parcela.** Redistribuir empurra a recorrência para baixo do piso, e recorrência barata é gargalo perpétuo. Na prática, a régua costuma revelar **setup subprecificado**, não mensalidade alta.
- **Entrada: mínimo 50% do setup antecipado.** Sem entrada, sem agenda.
- **Inadimplência > 15 dias:** entrega pausada com aviso; > 45 dias: encerramento formal.
- **Reajuste:** preços de tabela revisados a cada 6 meses ou a cada 10 casos entregues no formato (o que vier antes).

**Escada de ofertas vigente (preços-alvo):** ver `30-comercial/oferta.md` §3 (tabela com unit economics). A escada abaixo é o **modelo de catálogo** que o método pressupõe; os nomes das famílias são usados pelos métodos (Mapa da Ordem, Alicerce, Assessoria, CORE), os preços são seus.

> ### ✅ O DIAGNÓSTICO PAGO (Mapa da Ordem) — precificado no piso, sem exceção
>
> | Versão | Preço | Horas | Valor-hora |
> |---|---:|---:|---:|
> | **Núcleo** | `{{TICKET_MAPA_NUCLEO}}` | `a calibrar` | ✅ no piso |
> | **Operação** | a partir de `{{TICKET_MAPA_OPERACAO}}` | `a calibrar` | ✅ no piso |
>
> **Decisão de arquitetura, não de tabela:** o Mapa **não é produto básico de entrada com desconto.** A distinção entre as versões é **amplitude diagnosticada**, não profundidade — o Núcleo fecha a camada que decide (4 pilares + Pivô de Conversão), o Operação acrescenta a que executa e mede (página, funil, conteúdo, tráfego, dados/tracking).
>
> **Em ambas o cliente sai com o mapa E as sugestões de execução.** É isso que sustenta o preço sem exceção: não se vende o apontamento, vende-se o apontamento com o caminho.
>
> **A fronteira que precisa continuar dita:** sugestão de execução não é execução. O Mapa entrega **o que fazer e em que ordem**; a Assessoria é **quem faz junto, toda semana**.

| Oferta | Preço | Função na trajetória |
|---|---|---|
| **Mapa da Ordem · Núcleo** | `{{TICKET_MAPA_NUCLEO}}` — 5 dimensões (4 pilares + Pivô de Conversão) | porta de entrada paga · no piso |
| **Mapa da Ordem · Operação** | a partir de `{{TICKET_MAPA_OPERACAO}}` — 10 dimensões, com tráfego e tracking | diagnóstico completo · no piso |
| **Alicerce** | a partir de `{{TICKET_ALICERCE}}` — 4 pilares, escopo fechado | trilho do ICP B (`ICP.md` §4-bis) · no piso exato |
| Produto de ciclo curto (ex.: site de conversão) | `{{TICKET_SITE}}` (lote fundador → padrão → com 10 casos) | caixa + carteira (Estágio A) |
| Assessoria Base | `{{TICKET_ASSESSORIA}}`/mês (escopo fechado: 1 canal + site + relatório) | construir MRR (Estágio B) |
| Assessoria Completa | `{{TICKET_ASSESSORIA_COMPLETA}}`/mês (funil + tráfego + criativos + conteúdo) | MRR de ticket maior |
| **Assessoria de Marketing Local** | `{{TICKET_ASSESSORIA_LOCAL}}`/mês + verba à parte, mínimo 3 meses (tráfego + artes estáticas + estratégia mensal + roteiro de WhatsApp) · bloco de 3 meses parcelado no cartão, taxa repassada, verba sempre fora | MRR via prospecção presencial · no piso · `METODO-PROSPECCAO-PRESENCIAL-LOCAL.md` §6.3 |
| **Módulo de Automação de Retorno** · degrau seguinte da Assessoria Local | `{{MONTAGEM_RETORNO}}` + `{{MENSAL_RETORNO}}`/mês · com SDR IA: `{{MONTAGEM_RETORNO_SDR}}` + `{{MENSAL_RETORNO_SDR}}`/mês · estrutura (servidor, CRM, automação) e mensagens de API no nome e no cartão do cliente · só a partir do mês 3 · ⟲ **exceção: a trava do mês 3 é dispensada quando a conta já tem base própria de clientes com histórico de compra** (o porquê da trava é a Assessoria Local formar a base primeiro; quem já tem base não precisa esperar) · SDR IA só com roteiro iterado | recompra e LTV da base · `METODO-PROSPECCAO-PRESENCIAL-LOCAL.md` §6.2.1 |
| CORE Essencial | setup `{{SETUP_CORE_ESSENCIAL}}` + `{{MENSAL_CORE_ESSENCIAL}}`/mês | Estágio B→C |
| CORE Avançado | setup + mensal | Estágio C |
| **Motor de Receita** | setup + mensal (teto de horas `a calibrar`) | Assessoria Completa **com diagnóstico de dependências** |
| **CORE Operação + Receita** | setup + mensal (teto de horas `a calibrar`) | **a tese fundadora**: redesenhar a operação a partir da receita pretendida |
| CORE Full | setup + mensal | Estágio C |

> ### As duas linhas de maior valor — e por que existem
>
> **Motor de Receita** — setup: diagnóstico do caminho do dinheiro até onde a receita depende, e a **matriz if-else** (*"para vender X, o processo Y precisa existir"*), entregue ao cliente. Mensal: narrativa, posicionamento, lançamento, páginas, mídia.
> ⚠️ **Fronteira obrigatória na proposta:** entregamos o mapa das dependências de processo; **quem executa é a operação do cliente**, e se as dependências não forem resolvidas **a projeção deixa de valer**. Sem essa cláusula escrita, esta oferta vira promessa incompleta.
>
> **CORE Operação + Receita** — setup: BPMN **AS-IS** do caminho do dinheiro, **mapa de vazamentos**, **TO-BE** com pontos de integração de IA declarados, **TO-RUN** (quem executa, com que gatilho, **e o que fazer na exceção**), matriz if-else e **motor de governança** implantado. Mensal: as duas camadas, mais guarda da governança e direção dos recursos que o cliente já tem.
>
> **O motor de governança tem seis componentes:** fonte única de estado · camadas declaradas (política, processo, estado) · **régua de exceção** · registro de decisão com o descartado · cadência · precedência. **BPMN é o processo; governança é o que faz o processo sobreviver ao contato com a realidade.**
>
> **Nenhuma das duas inclui construção de sistema.** Desenhamos o processo; o cliente ou o dev dele constrói.
> **Nenhuma das duas é contratação.** Não operamos o dia a dia — **construímos a operação que a próxima contratação do cliente vai operar**, e a régua que a mantém coerente. Posicionar como "braço direito" faz sermos medidos contra um salário, e essa comparação se perde sempre.
>
> **Fronteira com a Assessoria:** Assessoria trabalha a receita **sobre a operação que existe**. CORE O+R **redesenha a operação a partir da receita pretendida**. Se o gargalo é processo, é CORE; se é demanda, é Assessoria.
>
> **Os tetos de hora são regra interna, não item de contrato** — as linhas fecham no piso dentro do teto. Estourar é furar o piso. **`n=0` até o primeiro contrato fechado.**

> **Anti-padrão registrado:** mensalidade de Assessoria Base por escopo de agência completa (funil, páginas, criativos, tráfego, conteúdo e tracking) fica **abaixo do valor-hora piso** e compra gargalo. Contratos assim não se repetem: escopo daquele tamanho é Assessoria Completa ou não é.

**Exceção abaixo do piso: só como precedente registrado, nunca como padrão.** A leitura: preço abaixo do piso não compra a objeção que ele pretende comprar — e deixa a dívida de capacidade de qualquer forma. Toda exceção passa pela Âncora 7 e pela §3 do método de ancoragem (condições de recusa), com decisão registrada no rodapé.

## 5-ter. 🔴 ORDEM DE DEPENDÊNCIA DA ENTREGA — urgência corta volume, nunca dependência

**Risco que a régua fecha:** volume de peças com estrutura aprovada em todos os gates e cenas de público inventadas, sem o ICP colhido, custa a conta.

**A cadeia, e ela não tem atalho:**

> **diagnóstico → ICP colhido → oferta e narrativa → copy**

Cada elo é insumo do seguinte. **Pular um elo não acelera a entrega: troca a entrega por uma imitação dela**, com a mesma aparência e sem o conteúdo. Copy sem ICP é achismo com boa estrutura.

**A régua:**

> **Pedido urgente de cliente não altera a ordem de dependência.** Quando a urgência é real, **reduz-se o volume, nunca a dependência.** Uma peça com procedência vale mais que dez sem.

**As três respostas possíveis a "preciso para ontem":**

| Resposta | Veredito |
|---|---|
| Entregar **uma** peça, marcada como rascunho, sobre o único material com procedência | ✅ |
| Dizer que não cabe, **e dizer o que cabe e quando** | ✅ |
| Entregar **o volume completo como se fosse definitivo**, sobre insumo não colhido | 🔴 **proibido.** É a única resposta que não pode dar certo |

**Leitura de risco que vem junto (camada 3 do §11 do kernel).** Cliente com sinais de desconfiança ou de instabilidade de direção, **pedindo entrega urgente antes do diagnóstico, está fazendo um teste de conformidade disfarçado de pedido operacional.** Entregar rápido e errado confirma exatamente o medo dele. **O sinal costuma estar registrado no repositório antes da entrega, e ser lido tarde.**

**Onde isso aparece na operação:** `CLAUDE.md` §6 (réguas transversais) · `10-skills/copywriter-senior-continuum/` (régua de ordem na checklist) · `100-métodos/METODO-ARQUEOLOGIA-DE-ICP.md` §6.

## 6. ICP e abertura de frente

- **Duas frentes comerciais no máximo**, com papéis explícitos (`30-comercial/ICP.md`): frente de caixa e frente de tese.
- **Segmento só é "validado" com n ≥ 3** clientes pagantes recorrentes e playbook escrito. Um contrato = um caso, não um segmento.
- **Abrir nicho novo exige:** segmento atual saturado ou travado + playbook replicável (script + lista + critério de score) + capacidade livre (§4). Decisão: {{OPERADOR}}.
- **Concentração: nenhum cliente pode passar de 40% da receita.** Acima disso, diversificar é prioridade 1 do pipeline.

## 7. Tripwires (param a operação e forçam decisão)

| Sinal | Limite | Ação obrigatória |
|---|---|---|
| Churn | > 3%/mês | CS diagnostica causa antes de qualquer venda nova no segmento |
| TTFV | > 30 dias em 2 clientes seguidos | revisar onboarding (`30-comercial/onboarding.md`) |
| Concentração | > 40% em 1 cliente | diversificação vira prioridade de pipeline |
| Inadimplência | > 10% do MRR | rotina de cobrança diária até normalizar |
| Horas comprometidas | > 85% por 2 semanas | 🔴 **aciona contratação (§4-bis)** — não pausa venda |
| CAC | subindo 2 meses sem LTV acompanhar | rever oferta/canal antes de escalar verba |
| MRR novo | 2 meses abaixo de 50% da meta do plano | revisão estratégica extraordinária (ritual mensal antecipado) |

## 8. 🔴 ⭐ PÚBLICO É SEMPRE ANONIMIZADO

**A régua:** o que qualquer pessoa alcança sem login não identifica quem é ou foi cliente, prospect, parceiro, ex-sócio, funcionário de cliente ou contraparte, nem traz dado deles. **Sem exceção por pressa, por "é só um exemplo" ou por "ninguém vai achar".**

**Por quê:** o nome de quem confiou na casa não é nosso para publicar, e nome com relação comercial é dado pessoal (LGPD). E publicar não se desfaz: o que foi clonado, indexado ou copiado não volta.

| É público | Não é público |
|---|---|
| repositório público **e o histórico inteiro dele** (commit, autor, mensagem, branch, tag) · gist · página no ar, **mesmo fora do menu, com `noindex` ou em endereço adivinhável** · o código de página com login (HTML e JS chegam ao navegador antes da senha) · API aberta do site · PDF, imagem e metadado que sai para público indefinido · material de aula, demonstração aberta, post, story | repositório privado · documento enviado ao próprio cliente, sobre a conta dele · link com código imprevisível, `noindex`, só com dado da conta de quem o recebe · **peça do cliente, em nome dele** (o site dele traz o nome dele; ele é o dono) |

| O que identifica | Como sai |
|---|---|
| nome, apelido, marca, produto, mecanismo com apelido, @, domínio, cidade | rótulo neutro: *uma conta*, *Conta A* |
| sigla ou ID derivado do nome | ID neutro |
| número de caso: preço de contrato, faturamento, volume, data e hora de call | ordem de grandeza, ou some |
| fala literal reconhecível | paráfrase |
| quem nos passou material, curso ou pack pago | *fonte de mercado*. **Autor publicado segue creditado** |
| o operador como pessoa: finanças, família, saúde, vocabulário íntimo, e-mail pessoal | some. O nome na marca dele é escolha dele |
| a casa por dentro: pastas, código de decisão, produto não lançado, banco, servidor, resultado comercial real | molde ou placeholder |

**Antes de publicar, sempre:** `python3 40-operacao-rotinas/ferramentas/varrer-publico.py` (`--repo` antes do push, com o histórico; `--pasta` antes de subir peça; `--url` depois de subir). **Reprovou, não sai.** O dicionário sai das próprias pastas de conta e de um arquivo privado: **lista de nomes de memória não é gate.** O gate não dispensa leitura, porque ele não enxerga caso contado sem nome. Commit em repositório público sai com o e-mail da empresa. Todo repositório público tem o `pre-push` instalado (`--instalar-hook`), e o `--todos` roda toda semana, numa task recorrente.

### Vazou: limpa-se na hora, sem perguntar

🔴 **Nome ou dado de conta em superfície pública não abre decisão: a ordem é esta seção.** A sequência:

1. **Repositório público não se bloqueia:** itera-se removendo o dado, e ele fica fora do ar só o tempo da troca. **Página com o dado sai do ar primeiro, de modo reversível:** bloqueio no servidor, sem apagar.
2. **Limpa e republica.** Em repositório, **`git push --force` não limpa**: o commit antigo segue aberto por SHA e pela aba de atividade. A troca é um ato só: o limpo pronto e conferido primeiro; aí o antigo fica privado, com outro nome, e o público nasce de novo, no mesmo endereço, com um commit só.
3. **Registra** no `STATUS.md`: o que vazou, desde quando, quem pode ter visto.
4. **Dado de terceiro aberto é incidente:** registro em `80-juridico/registros/` e advogado no mesmo dia (LGPD, art. 48).

**O que continua pedindo a palavra de {{OPERADOR}}:** apagar de vez, e tirar do ar peça em uso.

---
*Registro de mudanças: `{{DATA_INSTANCIACAO}}` — instanciado a partir do template Continuum; números calibrados por {{OPERADOR}}: (listar os `{{…}}` preenchidos e os ainda `a calibrar`).*
