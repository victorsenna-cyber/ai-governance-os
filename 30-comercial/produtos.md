# produtos.md — Produtos e Plataforma da {{EMPRESA}}

> ⚠️ MODELO — preencher com os produtos da {{EMPRESA}}; o desenho é o método, o conteúdo é seu.

> O que construímos como ativo de software — distinto de `servicos.md` (o que entregamos com mão de obra + IA).
> Princípio: **a operação financia o produto.** Cada módulo nasce de um processo já entregue a cliente real.

---

## 1. `<Produto principal>`

**O que é:** `<uma frase: para quem e o que resolve>`.

- **Tese de arquitetura:** `<a decisão que todo o resto respeita>`.
- **Forma:** `<como é construído e onde roda>`.
- **Módulos:** `<lista curta; cada um nasce de um processo já entregue em serviço>`.

**Camada de decisão (onde mora o diferencial):**
`Operação → Analytics → BI → Decision Engine → Execução → Feedback`.
O **Decision Engine** transforma alertas de BI em decisões executáveis (ação, SLA, responsável, escala, canal).

**Estado atual:** `<fase em que está o seu produto; o que está em produção e o que não está>`. Regime: nada avança sem comando de tarefa explícito; zero regressão.

> Roadmap de productização: cada item vira módulo vendável a partir do processo validado em serviço.

---

## 2. `<Sistema de agentes, se houver>`

**Recebe comando em linguagem natural, compõe skills e agentes e opera sob gates humanos.**

- **Primitivas:** **Skill** (capacidade reutilizável) · **Agente** (composição de skills com papel) · **Projeto** (trava o "como"/processo).
- **Componentes:** `<runtime, orquestrador, canais>`.
- **Estado:** `<o que está no ar, quantos testes, quais gates; o que está pendente>`.
- **Regime de construção:** o agente planeja e executa sob task (`40-operacao-rotinas/tarefas/README.md`), com a regra de supply-chain de 7 dias para dependências novas.

---

## 3. `<CRM>`

- **Produto:** `<qual, e a licença dele>`. Licença copyleft (AGPL, por exemplo) pede cuidado antes de revender como serviço.
- **Uso atual:** `<interno ou vendido>`.
- **Integração prevista:** funil ↔ CRM via API/webhooks.

---

## 4. Automações

Orquestração da prospecção e do SDR. A automação é **borda de execução**: orquestra, nunca decide.

---

## 5. Sistema financeiro

Modelos de planilha que codificam a lógica financeira real, antes ou ao lado do sistema: INPUTS → RECEITA → CUSTOS → IMPOSTOS → DRE → FLUXO DE CAIXA → DISTRIBUIÇÃO → INDICADORES → PROJEÇÃO. Detalhe em `50-integracoes-dados/` e `45-financeiro/`.

---

## 6. Relação produto × serviço

| Camada | Hoje (serviço) | Amanhã (produto) |
|---|---|---|
| Prospecção/SDR | operado por nós | módulo SDR |
| Follow-up | cadência manual ou assistida | módulo de follow-up |
| Cobrança | processo do cliente | módulo de cobrança e reativação |
| Onboarding | sprints + acompanhamento | módulo de onboarding |
| Decisão | rituais + dashboards | Decision Engine |
| CRM | interno | `<produto, se fizer sentido>` |

---

## 7. Handoffs

← `oferta.md` (como o produto é vendido) · → `servicos.md` (o que opera em volta do produto) · ← `c-level/CTO.skill.md` (arquitetura/roadmap técnico) · ← `heads/head-ti-cybersec.skill.md` (infra/segurança) · → `50-integracoes-dados/` (conectores e fontes).
