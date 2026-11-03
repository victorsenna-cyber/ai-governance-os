# oferta.md — Arquitetura de Oferta da {{EMPRESA}}

> ⚠️ MODELO — preencher com a oferta da {{EMPRESA}}; o desenho é o método, os valores são seus.

> Como empacotamos e vendemos valor. Define a oferta âncora, a escada de ofertas (CORE), preços de referência e a lógica de ancoragem.
> Princípio: **serviço valida, produto escala.** Cada oferta entrega ordem operacional — não execução isolada.

---

## 1. Promessa central

> **Organizamos vendas, cobrança, operação, clientes e dados em uma única lógica de crescimento — para a receita parar de escapar entre as áreas.**

Categoria: **Revenue & Operations OS**. Não é agência, não é ferramenta solta, não é automação genérica.
Frase-âncora institucional: `{{FRASE_ANCORA}}` *(a frase que resume a promessa da {{EMPRESA}} em uma linha; escreva a sua)*.

---

## 2. Oferta âncora atual (Fase 01 — Serviço Recorrente + Setup)

**Máquina de Receita Previsível + Onboarding Orquestrado**, com **Agente de IA (SDR) no WhatsApp** como ponta visível de valor.

Estrutura de cobrança em duas partes:

- **Setup (pagamento único):** monta a estrutura — diagnóstico, pipeline, scripts, SDR AI, scraping de leads, integração WhatsApp, dashboards.
- **Recorrência mensal (MRR):** opera, calibra e expande — prospecção contínua, follow-up, rituais de pipeline, suporte e iteração.

> Lógica: o **setup antecipa caixa** e paga a montagem; a **recorrência** gera previsibilidade e financia o produto ({{EMPRESA}} OS).

---

## 3. Escada de ofertas (linha CORE)

> **Precedência de preço:** os números que **decidem** vivem em `00-core/POLITICAS-DE-DECISAO.md` §5 (pisos, tetos de desconto, alçadas). Os valores citados aqui são **referência de arquitetura de oferta**, não fonte de preço. **Em qualquer divergência, vale POLÍTICAS.**

Três níveis. O score do ICP (`ICP.md` §5) define o ponto de entrada.

### ⭐ Degrau 0 — Mapa da Ordem *(porta de entrada paga)*

**A distinção entre as versões é amplitude diagnosticada, não profundidade. Nenhuma é "básica", e nas duas o cliente sai com o mapa E as sugestões de execução.**

| Versão | Amplitude | Produção | Preço |
|---|---|---:|---:|
| **Núcleo** | **5 dimensões**: ICP, promessa, oferta, narrativa e **Pivô de Conversão** · 7 dias · devolutiva 45 min | ~8h | **{{TICKET_MAPA_NUCLEO}}** |
| **Operação** | **10 dimensões**: as 5 do Núcleo + página, funil, conteúdo, **tráfego pago e dados/tracking** · 14 dias · devolutiva 90 min | ~20h | **a partir de {{TICKET_MAPA_OPERACAO}}** |

**Abatimento:** integral no setup se a Assessoria fechar em até 15 dias da devolutiva. O Núcleo abate no Operação dentro de 60 dias.

> **A fronteira que precisa ser dita na devolutiva:** o Mapa entrega **o que fazer e em que ordem**. A Assessoria é **quem faz junto, toda semana.** Sugestão de execução não é execução.

> **Régua: nenhuma proposta de Assessoria sai sem diagnóstico rodado** — pago como Degrau 0, ou coberto por fase de descoberta já executada e registrada no repositório. **Proposta sem diagnóstico é `n=0` e se escreve assim.**

### ⭐ Trilho do ICP B — Assessoria Estratégica · Alicerce

| | |
|---|---:|
| Escopo fechado: os **4 pilares** (ICP, promessa, oferta, narrativa), testados em conversa real | **a partir de {{TICKET_ALICERCE}}** |
| Fora, com degrau nomeado: página ({{TICKET_SITE}}) · funil · campanha inicial (a orçar) | |
| Gate de saída: oferta levada a **10 conversas reais**, com respostas registradas | |

**Ver `ICP.md` §4-bis.** Não confundir trilhos: Mapa da Ordem é para quem já fatura; Alicerce para quem ainda não.

### Linha CORE

| Oferta | Setup (ref.) | MRR (ref.) | O que inclui |
|---|---|---|---|
| **CORE Essencial** | {{PRECO_CORE_ESSENCIAL_SETUP}} | {{PRECO_CORE_ESSENCIAL_MRR}} | Scraping de leads + **SDR AI no WhatsApp** + follow-up estruturado. Ativa pipeline sobre base existente. |
| **CORE Avançado** | {{PRECO_CORE_AVANCADO_SETUP}} | {{PRECO_CORE_AVANCADO_MRR}} | Tudo do Essencial + **pipeline/forecast**, rituais comerciais, dashboard de leads/MRR. |
| **CORE Full / Padrão** | {{PRECO_CORE_FULL_SETUP}} | {{PRECO_CORE_FULL_MRR}} | Tudo do Avançado + **WhatsApp integrado**, estruturação comercial completa, scraping ampliado, onboarding orquestrado. |

**Ofertas de porta de entrada (score 40–59 ou caixa imediato):**

- **Estruturação Comercial avulsa:** setup ~**{{PRECO_ESTRUTURACAO_AVULSA}}** (+ {{PRECO_SDR_AI}} SDR AI). Monta o Sistema Comercial Mínimo Viável em ~4 semanas.
- **Dashboard de Leads (HTML):** entregável rápido de valor, abre conversa para CORE.

**Faixa de referência consolidada:** Agente IA + estruturação comercial = **{{FAIXA_MENSAL_AGENTE_IA}}/mês**; pacotes setoriais ("<Setor> que Vende") **a partir de {{PRECO_PACOTE_SETORIAL_MENSAL}}/mês**.

### ⭐ Pacote setorial — modelo: **OPERAÇÃO COM VÁRIAS UNIDADES** (`n=0`)

Exemplo de como se instancia um pacote setorial a partir da escada, sem inventar preço novo. **Não é preço novo — é o CORE Essencial e o CORE Full instanciados para operação com várias unidades.** Substitua o setor, o mecanismo e os nós pelos do seu pacote.

**Mecanismo nomeado: `<nome do mecanismo>`** — três nós, um por vazamento da operação (ex.: primeiro contato · recontato · reativação da base). Nomear o mecanismo, e não a categoria, é o que tira a oferta da prateleira de "agente de IA para WhatsApp", onde a comparação só tem preço.

| | Etapa 1 · por unidade | Etapa 2 · rede |
|---|---|---|
| Instancia | CORE Essencial | CORE Full |
| Unidade 1 | {{PRECO_LOJA1_SETUP}} setup + {{PRECO_LOJA1_MRR}}/mês | rede até `<N>` unidades: {{PRECO_REDE_SETUP}} + {{PRECO_REDE_MRR}}/mês |
| Unidade adicional | {{PRECO_LOJA_ADICIONAL_SETUP}} + {{PRECO_LOJA_ADICIONAL_MRR}}/mês | + {{PRECO_LOJA_ADICIONAL_REDE_MRR}}/mês |

> ⚠️ Os valores seguem **`POLITICAS` §5**, não a tabela do §3 deste arquivo: se os dois divergirem, **vale POLITICAS**. Alinhe a tabela do §3 a ela assim que preencher os preços.

**Três regras que este pacote institui e que valem para qualquer conta multi-unidade:**
1. **Unidade adicional é incremento de configuração, nunca projeto novo** (custa uma fração do setup e do mensal da primeira). É o que prova que construímos sistema e não serviço — e é o que faz a terceira unidade caber.
2. **O preço da Etapa 2 vai publicado dentro da proposta da Etapa 1**, com gate medido e crédito de migração sobre parte do setup. Escada com preço guardado vira negociação do zero na segunda venda.
3. 🔴 **Teto de volume obrigatório.** Esta família de oferta tem **custo variável por unidade de uso** (mensageria + inferência): MRR liso e ilimitado corrói a margem exatamente quando o cliente cresce. Faixa incluída + excedente por conversa, revistos periodicamente sobre o realizado.

**Setores adjacentes onde o mesmo pacote se aplica sem redesenho:** franquias de varejo com tráfego pago para WhatsApp, clínicas com várias unidades, escolas e academias com matrícula por unidade.

---

### ⭐ Frente — FUNIL DE VSL *(`n=0`)*

**Construção de funil de aquisição em público frio:** produto de entrada + roteiro de VSL + página + anúncios + estrutura de teste de lead. Método: `100-métodos/METODO-FUNIL-DE-VSL.md`.

🔴 **Preço e escopo NÃO definidos — e não se inventam aqui.** A frente está aberta como capacidade, não como produto de catálogo. Antes de ir a qualquer cliente:

| # | Pendência | Por quê |
|---|---|---|
| 1 | **Faixa de preço** derivada da curva de carga (`POLITICAS` §4-ter) | construção é fase pesada, operação é leve — **preço único aqui tende a fechar com valor-hora muito abaixo do piso** |
| 2 | **Quem paga a mídia** | se o capital de teste é do cliente, entra nas condições de validade (Âncora 5). Se é nosso, vira custo e muda o preço |
| 3 | **Trilho de ICP** | serve ao **ICP A** (já fatura, tem capital de teste) — ⚠️ **o ICP B quase sempre reprova no gate de caixa**, e vender a ele seria o loop de verba que a régua-mãe existe para impedir |

**Enquanto as três não fecharem: `n=0`, e é assim que se escreve em qualquer proposta.**

## 4. Ofertas de serviço complementares (cross/upsell)

Validadas em entrega real — empacotar conforme dor do cliente (detalhe em `servicos.md`):

- **Assessoria de Marketing e Crescimento** — funil completo + tráfego pago (Meta Ads) + criativos + conteúdo + tracking. Referência de contrato: **{{PRECO_ASSESSORIA_TOTAL}} / 6 meses** ({{TICKET_ASSESSORIA}}/mês), obrigação de meio. Pode incluir garantia de performance (meta de referência 1,5× investimento).
- **Tráfego Pago** (Google / Meta) — aquisição qualificada acoplada ao funil.
- **Conteúdo / Autoridade** — linha editorial de 4 camadas, carrosséis, posicionamento.
- **Sites de Conversão / Web Design** — para nichos premium (ex.: um serviço local de ticket alto).

> Regra: complementares **não se vendem soltos** ao não-ICP. Só entram quando há (ou haverá) estrutura comercial que os sustente.

---

## 5. Lógica de ancoragem e venda

Método: *"Venda é engenharia de decisão"* — o cliente **conclui**, não é convencido. Sequência (sistema de vendas v3.0):

Frame → Diagnóstico → Quantificação → **Dor financeira** → Quebra de ilusão → Visão de futuro → Método → Oferta → **Ancoragem** → Decisão.

Axiomas de ancoragem:

- *"Sem número, não há decisão."* — toda proposta quantifica a receita que escapa hoje.
- *"Sem dor financeira, não há urgência."* — ancorar o preço contra a perda atual, não contra concorrente.
- Ancorar **CORE Full primeiro**, descer para Avançado/Essencial conforme score e caixa.
- Preferir **entrada antecipada (50%+ do setup)** — alavanca de caixa e compromisso.

---

## 6. O que NÃO ofertamos

- Execução isolada sem estrutura ("só tráfego", "só bot", "só automação").
- Promessa de resultado sem capacidade de entrega.
- Desconto que quebra margem sem autorização (decisão do CEO).
- Sofisticação (módulo/IA avançada) antes de operação estável no cliente.

---

## 7. Roadmap de oferta (serviço → produto)

1. **Fase 01 — Serviço Recorrente + Setup** (posição atual): caixa imediato + recorrência; cliente vira fonte de dados.
2. **Fase 02 — Productização:** transformar o que fazemos manualmente em **módulos vendáveis** (Follow-up AI, Cobrança/Reativação, Onboarding Orquestrado, BI Executivo, Decision Engine).
3. **Fase 03 — SaaS Modular + Enterprise:** assinatura a partir dos processos validados; contratos de maior ticket. *A operação financia o produto.*

---

## 7-bis. 🔴 ⭐ INVENTÁRIO DONE FOR YOU — a tarefa aberta que o método de DR cria

> **`100-métodos/METODO-DIRECT-RESPONSE.md` §4 instituiu o Done For You como princípio de produto.** `METODO-ANCORAGEM-DE-PROPOSTA.md` §0-ter régua 2-bis instituiu que **o bloco de onboarding de toda proposta se responde com inventário de ativo, não com estimativa de hora.**
>
> 🔴 **O inventário começa vazio, e o preenchimento é seu.** Enquanto não existir, toda proposta continua respondendo *"quanto tempo do cliente isso consome"* por estimativa — **que é exatamente o que a régua proíbe.**

**A tabela a preencher, uma linha por entrega da escada do §3:**

| Entrega | O que o cliente recebe PRONTO hoje | Degrau (0–4) | Já existe, ou se refaz por cliente? | O que subiria de degrau com uma construção única |
|---|---|---|---|---|
| *(preencha uma linha por entrega da escada do §3; ex.: repo de cliente, páginas, criativos, tracking)* | | | | |

**As três perguntas que classificam cada linha** (§4.3 do método de DR): remove uma etapa que ele teria de executar? · **é repetível sem customização?** · ele consegue usar sem nos perguntar nada?

🔴 **A coluna que decide é a terceira.** Item que se refaz do zero a cada cliente **não é DFY — é serviço, e precisa estar no preço como serviço.** É o mecanismo que derruba o valor-hora abaixo do piso: entrega tratada como ativo sendo paga como ativo, e executada como operação.

⚠️ **E o inventário tem valor comercial imediato, não só de higiene:** cada item no degrau 3 é uma linha que a proposta pode escrever como fato — *"você recebe X pronto"* — em vez de promessa. **Sem o inventário, escrevemos promessa porque não sabemos o que temos.**

---

## 8. Handoffs

← `ICP.md` (a quem ofertar) · → `produtos.md` (o que é o produto/OS) · → `servicos.md` (como entregamos) · → `onboarding.md` (o que acontece após o "sim") · ← `c-level/CFO.skill.md` (viabilidade de preço/margem) · ← `c-level/CEO.skill.md` (aprovação de exceção comercial).

---
