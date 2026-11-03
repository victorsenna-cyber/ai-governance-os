# onboarding.md — Onboarding Orquestrado (Comercial → Entrega)

> ⚠️ MODELO — preencher com a oferta da {{EMPRESA}}; o desenho é o método, os valores são seus.

> A ponte entre o "sim" e o primeiro valor. Ativação **automática e estruturada** pós-venda, com TTFV curto e churn reduzido.
> Princípio: **não separar venda de entrega.** O cliente não pode esfriar entre assinar e ver valor.
> **Responsável de processo: {{OPERADOR}}.** Detalhe de skill em `heads/head-onboarding-orquestrado.skill.md`.

---

## 1. Por que existe

O ponto onde mais se perde receita não é a venda — é o vácuo logo depois dela. Cliente que assina e não é ativado vira churn antes do primeiro valor. Onboarding Orquestrado fecha esse vácuo.

> Proibido: onboarding manual desestruturado · ausência de TTFV · depender do cliente para avançar · acompanhamento passivo.

---

## 2. Fluxo (8 etapas obrigatórias)

1. **Ativação automática** do onboarding logo após a venda (gatilho no fechamento).
2. **Captura de dados** — contrato + acordos + expectativas registradas.
3. **Plano de sucesso** — first value esperado e prazo (TTFV). ⚠️ O plano de sucesso **não nasce aqui.** Ver §2.1.
4. **Responsáveis** definidos dos dois lados (cliente + nossa operação).
5. **Execução guiada** por etapas (kickoff → setup → ativação).
6. **Monitoramento** — ativação, TTFV, risco de churn, adoção.
7. **Alertas automáticos** (WhatsApp / sistema) quando algo trava.
8. **Insights de causa e efeito** — por que ativou / por que travou.

### 2.1 ⭐ O plano de sucesso é feito ANTES da venda

**Colocar o plano de sucesso como etapa pós-venda é o erro clássico.**

**O plano de sucesso é construído antes da call de vendas e apresentado nela.** Ele existe em duas versões, e as duas são o mesmo documento em momentos diferentes:

| Momento | Versão | O que ele faz | Estado dos números |
|---|---|---|---|
| **Antes da venda** | **esboço** | mostra o caminho, o first value, as fases e quem entrega o quê. **É peça de venda e de decisão** | estimativa, com a premissa declarada ao lado |
| **No kickoff** | **refeito** | volta com os insumos que só existem do lado do cliente e vira compromisso | número real, data travada |

**Por que a ordem é essa, e não a inversa:** o cliente decide comprando um caminho, não uma lista de entregáveis. Quem só monta o plano depois do "sim" vende promessa e depois descobre o que prometeu. **E o vácuo que o §1 nomeia começa antes da assinatura, não depois.**

**O que o esboço obriga a ter, e é o que o torna peça de venda honesta:**

1. **First value nomeado e mensurável**, com data (TTFV). Não "resultado em breve".
2. **Responsáveis dos dois lados, com nome e data por entrega.** A coluna do cliente é o que mostra onde trava se ele parar.
3. **Gates entre fases**, em métrica medida e nunca em mês de calendário.
4. **A fronteira do que não se promete**, escrita.

**O que o kickoff acrescenta:** faturamento e números reais · listas e bases · materiais existentes · acessos técnicos · nomes da equipe do cliente. **As estimativas viram números e as datas viram compromisso.**

### 2.1-bis ⭐ De onde vem o esboço

**O esboço do plano de sucesso não se escreve do zero.** Ele é derivado do **Mapa da Ordem** (`100-métodos/METODO-DIAGNOSTICO-DE-OPERACAO.md`):

| Do diagnóstico | Vira no plano de sucesso |
|---|---|
| §6 · a primeira alavanca já paga | **o first value, com data (TTFV)** |
| §7 · a ordem de execução | **as fases, e o gate entre elas** |
| §8 · o que não foi apurado | **a coluna do cliente** — o que trava se ele não entregar |
| §9 · o que fica fora, com preço | **a fronteira do que não se promete** |

**Por que isso fecha um buraco:** antes, o esboço era montado a partir da call de vendas, e call de vendas nem sempre produz número. **O diagnóstico produz número por construção** — é o que ele é. Com ele, o plano de sucesso deixa de ser estimativa apresentada como caminho e passa a ser o caminho que o próprio cliente já viu descrito e pagou para ver.

> **Régua:** proposta comercial e plano de sucesso não são dois documentos concorrentes. A proposta ancora a **economia** (7 âncoras, `100-métodos/METODO-ANCORAGEM-DE-PROPOSTA.md`); o plano de sucesso ancora a **execução**. Vão juntos na mesma call, e o plano aponta para a proposta quando o cliente quiser ver a conta inteira.

**Par de peças:** um HTML da economia (`conta-<cliente>.html`) e um da execução (`plano-sucesso-<cliente>.html`), gerados na pasta da conta.

---

## 3. Kickoff (primeira semana)

- **Refazer o plano de sucesso** com os insumos do cliente (§2.1). É a primeira tarefa do kickoff, não a última.
- Confirmar que o cliente **entendeu o que foi vendido** (alinhar expectativa × escopo).
- Definir **first value** concreto e mensurável (ex.: primeira reunião agendada pelo SDR; primeiro relatório de pipeline; primeira campanha no ar).
- Mapear onde está o risco: **expectativa · setup · adoção · valor percebido**.
- Travar responsáveis e cadência (alinhamentos quinzenais como padrão).

---

## 4. Métricas (KPIs)

- **TTFV** (time-to-first-value) — meta **< 30 dias**.
- **Taxa de ativação** — % de clientes que atingem o first value.
- **Adoção inicial** — uso real do que foi entregue.
- **% de onboardings com plano de sucesso** formalizado.
- **Alertas resolvidos** / tempo de resolução.
- **Health score** inicial (entra em CS — `heads/head-customer-success.skill.md`).

---

## 5. Modelo de execução (sprints)

Onboarding roda em **sprints** quando o serviço exige construção (ex.: assessoria de marketing):

- **Sprint 1 — Estrutura:** infraestrutura estratégica (ICP/prontidão, arquitetura da oferta, funil, protocolo de qualificação, sistema de conteúdo, cockpit operacional).
- **Sprint 2 — Identidade/Operação:** identidade operacional, anti-posicionamento, jornada do cliente, ritualização. Onboarding orquestrado pode entrar como bônus.

Para serviços de prospecção/SDR, o onboarding é mais curto: setup técnico → primeira leva de leads → calibração → primeira reunião.

---

## 6. Sistema e integrações

- **ClickUp** — tarefas e etapas do onboarding.
- **n8n** — gatilhos e alertas automáticos.
- **WhatsApp** — comunicação e alertas ao cliente/operação.
- **Supabase** — dados de ativação/TTFV.
- Detalhe de conexão em `50-integracoes-dados/`.

---

## 7. Handoffs

← `c-level/CRO.skill.md` (passagem de bastão da venda) · ← `oferta.md` / `servicos.md` (o que foi vendido) · → `heads/head-customer-success.skill.md` (cliente ativado → retenção/expansão) · → `c-level/COO.skill.md` (entrega) · → `iteracao.md` (loop de melhoria).

---
*Registro: **o plano de sucesso é pré-venda, não pós-venda** (§2.1): esboço construído antes e apresentado na call de vendas, refeito no kickoff com os insumos do cliente. A etapa 3 do §2 é o momento em que ele é **confirmado**, não criado. A regra evita prometer em call um plano que só seria construído depois do fechamento.*
