# MÉTODO — ANÁLISE DIÁRIA DE CAMPANHA (coleta → análise → implementação)

> **Tipo:** método · secundário: trilho (três tasks encadeadas) e gate (§8)
> **Origem:** casa de origem do template · **Alçada:** {{OPERADOR}} · o estágio 2 é N5, não N4 · **Estado:** 🟡 **provisório** — gradua com 1 conta × 10 dias úteis rodando os três estágios sem retrabalho do {{OPERADOR}}
> **Roda dentro de:** `METODO-TRAFEGO-PAGO.md` §7 (cadência, disciplina, regras de decisão, ordem de diagnóstico) · `METODO-ITERACAO-DE-CPA.md` (equação, amostra mínima, CPA como juiz) · operação por tasks (`40-operacao-rotinas/tarefas/README.md`, níveis N0–N5) · escada de autonomia (`ferramentas/autonomia.py`)
> **Onde mora o que produz:** `clientes/<Cliente>/NN - tráfego pago/diario/` (molde em `90-templates/trafego-cliente/diario/`)

---

## 1. O princípio — três modelos, três verbos, um arquivo cada

A gestão diária do `METODO-TRAFEGO-PAGO.md` §7.1 ("checagem de anomalia, 10 min") era feita de cabeça, no Gerenciador, e não deixava rastro. **Este método a transforma em três atos separados por quem os faz e por quanto custam:**

| Estágio | Verbo | Nível | Modelo | Escreve | Nunca faz |
|---|---|---|---|---|---|
| **1 · Coleta** | **cita** | N2 (N0 quando automatizar) | Haiku | `diario/AAAA-MM-DD.md` — os números, por campanha → conjunto → anúncio, com fonte e hora | interpretar, comparar com meta, sugerir, tocar na plataforma |
| **2 · Análise** | **decide** | **N5** | Fable 5.1 | `diario/AAAA-MM-DD-ANALISE.md` (a leitura: estado por item, diagnóstico, o que não se faz) **e `diario/AAAA-MM-DD-BRIEFING.md` (o briefing de otimização: as ordens executáveis)** | coletar dado, executar na plataforma, inventar número que o diário não tem |
| **3 · Implementação** | **executa** | N3 (N4 se a ordem exigir julgamento) | Sonnet | a mudança na plataforma + linha no `LOG-DECISOES.md` + `BRIEFING.md` §4 · **lê só o briefing** | mudança fora da ordem escrita, ordem sem aprovação quando a alçada exige, decidir |

**Por que separar:** quem coleta não pode decidir (o número chega limpo, sem leitura embutida); quem decide não pode coletar (o modelo caro não gasta janela copiando tabela); quem executa não pode decidir (a mudança na conta do cliente é sempre rastreável a uma ordem escrita). **A fronteira entre os três é o arquivo.** Estágio que não deixou arquivo não aconteceu.

**O que este método NÃO é:** não cria criativo (ESCRITA), não muda oferta nem público-alvo da matriz (REGRA Nº 0, decisão da análise que vira task própria), não substitui a leitura semanal de funil nem o relatório mensal (§7.1 e §8 do método-mãe). Ele é a **camada diária**: anomalia, kill, fadiga, escala, aprendizado.

---

## 2. Estágio 1 — COLETA (Haiku cita, não lê)

### 2.1 Insumos

- **Hoje (manual):** os números que o {{OPERADOR}} cola ou o Gerenciador aberto na sessão (MCP da Meta: `ads_get_ad_entities` com insights do dia e acumulado, nos três níveis). O coletor é um **subagente `haiku`** da sessão, com o contrato do §6.1.
- **Depois (automático):** um script N0, `coletar-campanha.py` *(a construir)*, lendo a Marketing API com o token guardado em arquivo local, fora do repositório (o mesmo do `painel-resultado/servir.py`) e gravando o mesmo arquivo. Haiku fica só para conferir e completar a fonte de verdade. **Promover o coletor a N0 não muda o arquivo nem os estágios 2 e 3.**
- **Fonte de verdade** (vendas, conversas etiquetadas `vendeu`): vem do {{OPERADOR}} ou do cliente; quando não vier, o campo fica `—` e é dito. **Nunca se inventa venda.**

### 2.2 Saída: `diario/AAAA-MM-DD.md`

Um arquivo por dia por conta, no molde de `90-templates/trafego-cliente/diario/AAAA-MM-DD.md`. Tabela por nível (campanha · conjunto · anúncio), com `id`, status efetivo, gasto do dia e acumulado, impressões, frequência, CTR, CPM, cliques no link, resultado (conversas iniciadas, ou compras na campanha de site), custo por resultado, **dias desde a última edição** (o que decide se está em aprendizado), e, no rodapé, a fonte de verdade do dia e as mudanças das últimas 72h lidas do `LOG-DECISOES.md`.

**Réguas do coletor:**
- Todo número com **fonte e hora** (`Gerenciador 29/10 08h10`, `{{OPERADOR}}, WhatsApp 29/10 08h30`).
- Campo sem dado é `—`, nunca zero. Zero é um número.
- **Nada de adjetivo, comparação ou seta.** "CTR caiu" é análise. "CTR 0,8%" é coleta.
- Se a plataforma e a fonte de verdade divergem, as duas entram lado a lado; a divergência é **registrada**, não explicada.
- Dado de cliente (`C`): **nunca em N1**. Fica no repo do cliente.

---

## 3. Estágio 2 — ANÁLISE (Fable decide, por regra e não por sensação)

### 3.1 Carga, nesta ordem

1. `diario/AAAA-MM-DD.md` de hoje **e os últimos 7 diários** (sem a série, não há tendência; com menos de 3 diários, a análise diz "série curta" e só aplica kill hard).
2. `PLANO-DE-MIDIA.md` da conta — **CPA alvo, verba/dia, thresholds calibrados** (§7.3 do método-mãe é default; o plano prevalece). 🔴 **O plano tem que ser do canal em que a campanha roda** (numa conta, o plano carregado era de um canal e a campanha rodava em outro). Plano de outro canal, ou com status *"nada criado"* enquanto há campanha ativa, **para a análise**: antes se corrige o plano (ARVORE-CONTA, régua de captura), depois se analisa.
3. `LOG-DECISOES.md` — o que já foi tentado, o que está em janela de 72h, a hipótese aberta do ciclo (`METODO-ITERACAO-DE-CPA.md` §6: uma por alavanca).
4. `painel.json` — a série acumulada e a faixa de confiança da taxa.
5. `estrutura-campanhas.md` e `matriz-criativos.md` — para saber **qual hipótese cada anúncio testa** (criativo sem hipótese escrita é veto do método-mãe; aqui ele vira "não analisável").

### 3.2 O que a análise faz, na ordem

1. **Estado de cada item:** `aprendizado` (< 72h desde a última edição; dobrado em verba pequena, §5.3) · `lendo` · `vencedor` · `fadiga` · `kill hard` · `kill normal` · `escalar` · `manter` — **pela tabela §7.3 do método-mãe, com o número que disparou a regra escrito ao lado.** Item em aprendizado só recebe kill hard.
2. **Anomalia da conta:** gasto rodando? reprovação? CPA do dia > 2× alvo? saldo e cap mensal (§7.5)? Isto é a "checagem de 10 min" do §7.1, agora escrita.
3. **Ordem de diagnóstico quando o CPA está alto** (§7.4): tracking → oferta → página/atendimento → criativo → estrutura. **A análise nomeia em que degrau parou e por quê**, e não pula para "troca o criativo".
4. **CPA como juiz** (`METODO-ITERACAO-DE-CPA.md` §6): mudança que melhorou a alavanca e piorou o CPA é reprovada, mesmo que pareça vitória.
5. **Amostra mínima** (§7 do CPA): custo por conversa só com ≥ 7 dias fora do aprendizado; taxa só com ≥ 30 conversas etiquetadas; com menos de 5 vendas, verba se decide pelo **piso** da faixa do painel.
6. **Briefing de otimização** (`AAAA-MM-DD-BRIEFING.md`, o único arquivo que o Sonnet lê): uma linha por mudança — `id` da entidade · ação (pausar / ativar / verba de X para Y / repor criativo da fila) · regra que a justifica · resultado esperado em número e data · **classe de alçada** (§5). **No máximo uma mudança estrutural por conta por dia** (§7.2); verba nunca ±20% em menos de 48–72h.
7. **O que NÃO se faz hoje**, com o motivo (em aprendizado · amostra curta · hipótese do ciclo ainda aberta). Esta seção é obrigatória e normalmente é a maior.
8. **Aprendizado do dia** para o `LOG-DECISOES.md` e, quando bate gatilho (criativo ≥ 7 dias com CPA ≤ meta), a entrada no `30-comercial/swipe-file/` (§11.5 do kernel) — **na mesma tarefa**.

### 3.3 Saída: `diario/AAAA-MM-DD-ANALISE.md` (a leitura) + `diario/AAAA-MM-DD-BRIEFING.md` (o briefing de otimização)

Moldes em `90-templates/trafego-cliente/diario/`. A análise guarda o porquê; o briefing guarda o quê, em que ordem, por qual via, com qual prova e o que não tocar. **Toda ordem cita o número e a regra.** Ordem sem número é opinião, e opinião não se implementa. **Teste do briefing:** se o Sonnet precisar abrir a análise ou o diário para executar, o briefing está incompleto e volta para o Fable.

**Nunca:** número que não está em nenhum diário · "vamos testar um criativo novo" como ordem (isso é task de ESCRITA, e a análise a **abre**, não a executa) · mudar dois itens da mesma alavanca no mesmo ciclo · ler item em aprendizado como kill normal.

---

## 4. Estágio 3 — IMPLEMENTAÇÃO (Sonnet executa a ordem, só a ordem)

### 4.1 Pré-condição

`BRIEFING.md` do dia existe, tem o §1 (ordens) preenchido, e **cada ordem está `aprovada`** segundo a classe de alçada do §5 (automática ou pelo {{OPERADOR}}). Sem isto a task vai para `decisao/` e vira cartão em `DECISOES-PENDENTES.md`, não para a plataforma.

### 4.2 Execução

- **Na sessão:** MCP da Meta (`ads_update_entity` para status e verba; `ads_create_ad` para repor criativo já produzido). **Em task agendada:** o script da conta em `NN - tráfego pago/scripts/` (padrão da casa) — o executor escreve o script a partir da ordem, roda, **e lê de volta o status nos três níveis** (campanha, conjunto, anúncio) antes de dizer "feito". Status não conferido não é feito.
- **Uma ordem de cada vez, na ordem da análise.** Falhou uma, para, registra, não improvisa a próxima.
- **Nada além da ordem.** Viu algo errado na conta que a análise não viu? Registra no `BRIEFING.md` §4 como achado e **não mexe**. Vai para a análise de amanhã (ou para o Opus hoje, se for kill hard).

### 4.3 Registro, no mesmo ato

1. `LOG-DECISOES.md` da conta: `data · o quê (id) · por quê (regra + número) · resultado esperado (número + data) · resultado medido: —` — o campo medido é preenchido pela análise do dia marcado.
2. `BRIEFING.md` §4 *Implementado*: cada ordem com hora, status lido de volta e divergência, se houve.
3. `painel.json`: só se a verba/dia mudou (campo `verbaDia`), pelo painel ou à mão; a leitura do dia o painel faz sozinho.
4. `PAINEL.md` da conta: frontmatter tocado se o estado mudou (`ARVORE-CONTA.md`).

---

## 5. Alçada — o que roda sozinho e o que espera o {{OPERADOR}}

A escada `autonomia.py` (A0–A3) vale por **tipo de decisão**, e este método declara os seus:

| `tipo_decisao` | O que é | Nível de partida | Por quê |
|---|---|---|---|
| `kill_hard_campanha` | pausar item que bateu kill hard (§7.3: 3× CPA sem conversão · CTR < 0,5% com ≥ 2.000 impressões · reprovado) | **A2** — executa e avisa, janela de veto de 24h | perda em curso, reversível em um clique (reativar), regra numérica sem interpretação. *(Proposta do sistema, 29/10; o {{OPERADOR}} confirma ou rebaixa para A1)* |
| `kill_normal_campanha` | pausar após 72h com CPA > 3× alvo por 3 dias | A1 — o sistema ordena, o {{OPERADOR}} aprova | envolve a ordem de diagnóstico §7.4; pode ser tracking, não mídia |
| `fadiga_reposicao` | pausar criativo fatigado e repor **da fila já produzida** | A1 | mexe em criativo; a fila precisa existir |
| `escala_verba` | +20% em vencedor estável ≥ 7 dias, dentro do cap mensal | A1 | é dinheiro do cliente; sobe para A2 só com histórico |
| `verba_fora_do_plano` | mudança > 30% do plano mensal | **nunca sozinho**: aprovação do cliente por escrito (§7.5) | contrato |
| `criativo_novo`, `publico_novo`, `oferta` | hipótese nova | **não é deste método**: a análise abre task em ESCRITA / NEGÓCIO | REGRA Nº 0 e Nº 2 |

**Na fase manual (hoje):** o {{OPERADOR}} é a aprovação de tudo que está em A1; ele lê o `BRIEFING.md` §1 e diz *"implementa"* (todas) ou nomeia as ordens. **Na fase automática:** a análise grava `aprovada: sim` nas ordens A2+, e as A1 esperam no cartão de decisão; o despachante só lança a implementação com ordem aprovada.

---

## 6. Contratos — o que cada executor recebe (copiar literalmente)

> Todo contrato começa com a cerca: *"Você opera dentro do repositório da {{EMPRESA}}, na conta `<Cliente>`. Escreve em UM arquivo. Não envia nada a ninguém. Dado de cliente fica no repo."*

### 6.1 Coleta (haiku)

> Leia `clientes/<Cliente>/NN - tráfego pago/diario/README.md` e o molde `90-templates/trafego-cliente/diario/AAAA-MM-DD.md`. Com os dados abaixo [ou: com `ads_get_ad_entities` da conta `act_<id>`, insights de hoje e acumulados, níveis campanha, conjunto e anúncio], escreva `diario/<hoje>.md` preenchendo todas as colunas. Fonte e hora em todo número. Campo sem dado é `—`. **Não interprete, não compare, não sugira, não use adjetivo nem seta.** Leia `LOG-DECISOES.md` e copie, no rodapé, as entradas dos últimos 3 dias, literais. Saída: só o arquivo.

### 6.2 Análise (fable · `claude-fable-5-1`)

> Carregue, nesta ordem: `diario/<hoje>.md` e os 7 diários anteriores · `PLANO-DE-MIDIA.md` (CPA alvo, thresholds) · `LOG-DECISOES.md` · `painel.json` · `estrutura-campanhas.md` · `matriz-criativos.md` · `100-métodos/METODO-TRAFEGO-PAGO.md` §7 · `100-métodos/METODO-ITERACAO-DE-CPA.md` §6–§7. Escreva dois arquivos, pelos moldes: `diario/<hoje>-ANALISE.md` (estado de cada item com o número que disparou a regra; anomalia da conta; degrau do diagnóstico §7.4 quando o CPA está alto; decisões em resumo; o que NÃO se faz hoje e por quê; aprendizado para o log) e `diario/<hoje>-BRIEFING.md`, o briefing de otimização que o Sonnet executa sem abrir mais nada: ordens na ordem de execução, cada uma com `id`, nível, ação exata, de → para, regra + número, resultado esperado em número e data, `tipo_decisao`, alçada e `aprovada`; a via de execução e a prova de cada ordem; a lista explícita do que não tocar. Máximo uma mudança estrutural na conta. Nenhum número que não esteja num diário. Não execute nada. Se precisar de criativo ou público novo, escreva a task em `40-operacao-rotinas/tarefas/fila/` (árvore ESCRITA ou NEGÓCIO) e cite o id na análise.

### 6.3 Implementação (sonnet)

> Leia `diario/<hoje>-BRIEFING.md`, e só ele. Execute **só** as ordens do §1 marcadas `aprovada: sim`, uma de cada vez, na ordem [na sessão: MCP da Meta; agendado: script em `NN - tráfego pago/scripts/`]. Depois de cada uma, leia de volta o status nos três níveis e registre. Falhou: pare, registre, não improvise. Escreva a linha no `LOG-DECISOES.md` (data · o quê · por quê · resultado esperado) e o §4 do `BRIEFING.md` (hora, status lido, divergência). Achado fora das ordens vai para o §4 como achado, **sem mexer**. Não decida nada.

---

## 7. Operação por tasks — os três modelos

Em `40-operacao-rotinas/tarefas/modelos/`: `analise-campanha-1-coleta.md` (N2, diária, `conta: <Cliente>`), `analise-campanha-2-analise.md` (N5, `depende_de` a coleta; ⚠️ provar que o modelo da análise roda fora de sessão antes de agendar, `PROTOCOLO-MULTI-MODELO.md` §1-quater — até provar, a análise agendada roda em sessão), `analise-campanha-3-implementacao.md` (N3, `depende_de` a análise, só roda com ordem aprovada). **Para pôr uma conta no ar:** copiar os três para `fila/`, trocar `<Cliente>`, `NN`, `act_<id>` e os ids; `recorrencia: diaria`. **Por padrão, nenhuma conta nasce na fila:** a coleta depende de dado colado ou de MCP na sessão, e `claude -p` não tem o MCP da Meta — o despachante só a sustenta quando o `coletar-campanha.py` (N0) existir. Até lá, o protocolo roda **na sessão**, pelo §6, com os mesmos arquivos: a análise é a própria sessão do Fable, sem subagente.

**Horário de referência:** coleta depois das 08h (o dia anterior fechou na plataforma), análise na sequência, implementação até as 12h. Dias úteis (§7.1); fim de semana só coleta, salvo kill hard.

---

## 8. GATE

- [ ] O diário do dia existe, com fonte e hora em todo número, sem adjetivo?
- [ ] A análise carregou os 7 diários anteriores (ou declarou "série curta")?
- [ ] Toda ordem tem `id`, regra, número que disparou, resultado esperado com data e `tipo_decisao`?
- [ ] Item em aprendizado só recebeu kill hard?
- [ ] No máximo uma mudança estrutural na conta hoje?
- [ ] "O que NÃO se faz" está escrito, com motivo?
- [ ] Cada ordem executada tem linha no `LOG-DECISOES.md` e status lido de volta nos três níveis?
- [ ] Nenhuma mudança na plataforma sem ordem escrita e aprovada?
- [ ] O briefing bastou sozinho (o Sonnet não precisou abrir a análise nem o diário)?

**🔴 Reprova sozinho:** mudança na plataforma **sem ordem escrita no `BRIEFING.md` do dia** · Sonnet executando a partir da análise ou do diário, e não do briefing · ordem A1 executada **sem aprovação do {{OPERADOR}}** · coleta com interpretação, comparação ou número sem fonte · análise com número que não está em nenhum diário · item em aprendizado (< 72h) tratado como kill normal · ordem executada **sem linha no `LOG-DECISOES.md`** · dado de cliente coletado em N1 · criativo ou público novo "implementado" por este método (é task de ESCRITA / NEGÓCIO).

---

## 9. Evolução

- Primeira conta real: a que tiver campanha no ar e `painel.json` com série (o primeiro uso de uma mudança de gate nunca é um cliente, mas este método **não muda gate existente**, ele materializa o §7.1 que já valia).
- Após 10 dias úteis: medir tokens por estágio (`medir-tokens.py`), tempo do {{OPERADOR}} na aprovação, ordens revertidas. Se `kill_hard_campanha` não teve veto em 10 decisões, pede A3; se `escala_verba` acertou ≥ 90% em 10, pede A2.
- O `coletar-campanha.py` (N0) é a próxima peça; nasce em `40-operacao-rotinas/ferramentas/`, reutiliza o token e o `insights` do `painel-resultado/servir.py`, e grava o mesmo `diario/AAAA-MM-DD.md`.

---
*Regra da casa (três modelos, três estágios, arquivo no repo do cliente). A análise passou do Opus para o Fable, e a saída do estágio 2 virou dois arquivos: o Sonnet lê só o briefing.*
