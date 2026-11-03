# MÉTODO CONTINUUM — GESTÃO DE TRÁFEGO PAGO

> **Tipo:** método · secundário: política (§2.2, §7.3, §7.5), gate (§1, §3) *(reclassificado 26/09/2026 por auditoria independente de leitura integral; antes: "método-raiz (camada 2 — política)")* · **Criado em:** 2026-07-08 · **Status:** vigente, pendente de calibração com 1º cliente
> **Abrir por momento:** decidir §2.2 · produzir §3–§7 · conferir §1 e §3 *(mapa proposto pela auditoria de 26/09 — conferir no primeiro uso)*
> Fonte única do método de tráfego. Skills que o carregam: `10-skills/gestao-trafego.skill.md` (execução) + `10-skills/heads/head-trafego.skill.md` (persona).
> Cadeia endurecida: **Projeto → Objetivo → Página → Criativo → Campanha → Tracking → Gestão → Relatório.** Nenhuma fase pula gate.
> Precificação, alçadas e capacidade: `00-core/POLITICAS-DE-DECISAO.md` prevalece. Estado por cliente: `clientes/<Cliente>/NN - tráfego pago/`.

---

## 0. Princípios do método (a lógica de 2026)

A realidade dos leilões mudou. O método assume estes fatos e decide a partir deles:

1. **O criativo é a segmentação.** Os sistemas de entrega (Meta Andromeda, Google AI) leem o criativo para decidir a quem entregar. Criativo responde por ~56% do resultado — mais que público, verba e posicionamento somados. Segmentar por interesse detalhado é lutar contra o algoritmo.
2. **Consolidação > fragmentação.** Estruturas com muitas campanhas/conjuntos fatiam o sinal de conversão e matam o aprendizado. Contas consolidadas convertem ~15-17% mais. Regra: o mínimo de campanhas que a verba sustenta com dados densos.
3. **Sinal limpo é pré-requisito, não otimização.** Pixel sozinho está quebrado (ad blockers ~25-30%, iOS/ATT). Pixel + CAPI simultâneos e Event Match Quality ≥ 7 são gate de subida de campanha.
4. **Regras de decisão antes da campanha.** O que é "ganhou", "perdeu" e "escala" é definido por escrito ANTES de gastar o primeiro real. Gestão por sensação é a causa nº 1 de verba queimada.
5. **Matemática reversa do funil.** Toda meta nasce do unit economics do cliente (preço → margem → CPA máximo → verba mínima viável), nunca de benchmark genérico.
6. **Verba pequena tem física própria.** Cliente com verba abaixo do mínimo viável (§2.2) não roda estratégia de conta grande em miniatura — roda a estratégia de verba pequena (§5.3) ou não roda.
7. **Não tratar sintoma como causa.** CPA alto tem 5 causas possíveis — oferta, público-alvo implícito no criativo, criativo, página, tracking — e o diagnóstico segue essa ordem (§7.4). Trocar criativo quando o problema é oferta é atividade, não progresso.
8. **Processo antes de ferramenta.** Automação (regras automáticas, agentes, APIs) só depois do método rodando manualmente por ≥ 1 ciclo completo em ≥ 1 cliente.

---

## 1. GATE DE ENTRADA — o cliente pode entrar?

Nenhum contrato de tráfego é aceito sem passar pelos 5 critérios. Reprovou em 1 → não entra (ou entra condicionado, por alçada do {{OPERADOR}}).

| # | Critério | Régua |
|---|---|---|
| G1 | **Oferta clara e vendável** | O cliente sabe o que vende, para quem e por quanto. Oferta confusa = primeiro consultoria de oferta, depois tráfego. |
| G2 | **Unit economics fecha** | Margem bruta do cliente por venda comporta um CAC realista (CPA máx ≥ CPA plausível do nicho). Se a conta não fecha no papel, não fecha no leilão. |
| G3 | **Verba mínima viável** | Verba mensal ≥ mínimo calculado em §2.2. Abaixo disso, tráfego vira loteria — recusar ou reenquadrar expectativa por escrito. |
| G4 | **Ativo de conversão existe ou será construído** | Página/WhatsApp/funil funcional. Sem destino decente, não sobe campanha (gate da Fase 3). |
| G5 | **Nossa capacidade e preço** | `POLITICAS-DE-DECISAO.md` §4 (régua de capacidade) e §5 (piso valor-hora `{{VALOR_HORA_PISO}}`, margem ≥ `{{MARGEM_MINIMA}}`). Gestão de tráfego entra na escada como parte da **Assessoria Completa (`{{TICKET_ASSESSORIA_COMPLETA}}`/mês)** ou módulo precificado à parte — nunca abaixo do piso. |

**Saída do gate:** `BRIEFING.md` preenchido no workspace do cliente + decisão registrada (aceito / recusado / condicionado).

---

## 2. FASE 1-2 — PROJETO E OBJETIVO (a matemática antes da mídia)

### 2.1 Briefing obrigatório (inputs sem os quais não há plano)

Negócio e oferta (o que vende, ticket, margem bruta, LTV se recorrente) · público comprador real (quem paga, não quem curte) · concorrência direta e como anuncia (Biblioteca de Anúncios) · histórico de mídia (contas, campanhas, resultados, aprendizados) · ativos existentes (página, pixel, listas, criativos, provas sociais) · capacidade de atendimento do cliente (leads gerados precisam ser atendidos — gargalo pós-clique é responsabilidade mapeada) · restrições (compliance do nicho, políticas de anúncio).

### 2.2 Matemática reversa (feita no plano, revisada mensalmente)

Sequência obrigatória, registrada em `PLANO-DE-MIDIA.md`:

1. **Ticket médio × margem bruta = lucro por venda.**
2. **CPA máximo** = lucro por venda × fração aceitável (padrão: ≤ 30% do lucro por venda em aquisição direta; até 100% se LTV comprovado ≥ 3× ticket).
3. **Taxa de conversão da etapa** (página→lead, lead→venda) — usar dado real do cliente; sem dado, usar premissa conservadora e marcar `a calibrar`.
4. **CPL máximo** = CPA máx × conversão lead→venda.
5. **Verba mínima viável/dia** = 10-15× CPA alvo da campanha (referência de saída de aprendizado: ~50 conversões do evento otimizado/semana por conjunto). Se o evento de compra não atinge volume, otimizar para o evento anterior do funil que atinge.
6. **Meta numérica do mês**: verba → leads esperados → vendas esperadas → receita esperada → ROAS/custo por resultado alvo. **Sem essa linha assinada pelo cliente, campanha não sobe.**

### 2.3 Objetivo por estágio da conta

| Estágio | Duração típica | Objetivo | O que NÃO cobrar |
|---|---|---|---|
| **Aprendizado** | semanas 1-2 | sinal limpo + primeiras conversões + validar tracking | CPA no alvo (volatilidade é normal) |
| **Validação** | semanas 3-6 | CPA ≤ alvo em ≥ 1 combinação criativo+página estável | escala |
| **Escala** | mês 2+ | crescer verba mantendo CPA (regras §7.3) | eficiência máxima (escala custa CPM) |

Expectativa contratada com o cliente **por estágio** — protege a relação e o resultado.

---

## 3. FASE 3 — PÁGINA DE VENDAS/CAPTURA (gate estrutural)

- Toda página nova ou reformada segue **`METODO-PAGINA-DE-VENDAS.md`** (via `10-skills/pagina-de-vendas.skill.md`). Copy cruza a árvore de copy do `CLAUDE.md` §6.1.
- **Checklist de aprovação de página para mídia** (reprova em qualquer item → campanha não sobe):
  1. Promessa da página = promessa do anúncio (coerência de mensagem, message match literal no above the fold);
  2. 1 página = 1 oferta = 1 CTA dominante;
  3. Carregamento móvel < 3s (testar; tráfego pago é ~90% mobile);
  4. Prova social real presente;
  5. Formulário/CTA com o mínimo de fricção que a qualificação permite;
  6. Pixel + CAPI disparando os eventos certos na página (validar no Events Manager antes da verba);
  7. Captura de first-party data (e-mail/WhatsApp) em algum ponto do fluxo.
- **Destino WhatsApp** (comum no nosso ICP): mensagem de abertura pré-preenchida qualificadora + processo de atendimento definido (tempo de resposta ≤ 15 min em horário comercial é meta contratada com o cliente) + registro de origem do lead.

---

## 4. FASE 4 — CRIATIVOS (o alvo é a segmentação)

### 4.1 Matriz de criativos (obrigatória antes de produzir)

> ⭐ **Quando o destino é uma VSL (instituído 13/09/2026):** o par a casar **não é anúncio ↔ primeira dobra da página, é anúncio ↔ LEAD da VSL** — a página é só a moldura do player. **A lead é o segundo contato do funil e o ponto de maior variância** (`METODO-FUNIL-DE-VSL.md` §5.1): mesma copy, trocando só a lead, uma versão dá prejuízo e a outra dá lucro.
>
> ⚠️ **O que se casa é a MENSAGEM, não o rosto** *(08/10/2026)*: o fim do anúncio tem que encaixar no que a lead diz no começo; **quem aparece no anúncio não precisa ser o expert da VSL.** Relato de fonte externa, não medido por nós: criativos narrados por outra pessoa que não o expert foram os melhores de ofertas que escalaram. Trocar quem fala é teste de execução legítimo.
>
> **Consequência para a matriz abaixo:** cada ângulo de criativo precisa ter **uma lead correspondente**, e o teste é do par, nunca do criativo isolado. **E a ordem de otimização inverte a intuição: mexe-se no topo — anúncio e lead — antes de qualquer ajuste no meio ou no fim da VSL.**

Preencher `matriz-criativos.md` cruzando:

- **Ângulos** (mín. 4 por oferta): dor · desejo/aspiração · prova/case · objeção invertida · urgência legítima · custo de não agir · comparação com alternativa.
- **Formatos** (mín. 3): imagem estática · vídeo curto (talking head/UGC-like) · carrossel · vídeo demonstração.
- **Hooks** (mín. 3 por ângulo): a primeira linha e os primeiros 3s decidem a **captura**; o **gancho completo** sustenta até o corpo e pode passar disso. Medir captura não é fixar duração. Testar hooks é mais barato que testar conceitos. **Abertura composta:** `100-métodos/METODO-EMPILHAMENTO-DE-HOOKS.md` (vale para peça nova, não exige vencedor).
- ⭐ **Abertura segmentada — a técnica que executa o princípio 1 ("o criativo é a segmentação")** *(08/10/2026)*: o mesmo corpo com aberturas que chamam subpúblicos diferentes (*"se você é X…"* / *"se você é Y…"* — por profissão, momento, região, dor). Com targeting broad, **é o criativo que separa os públicos, e a variação revela o subpúblico de CPA mais barato.** Fonte: relato externo, não medido por nós. Conta como **teste de componente** (abertura), não conceito novo.

**Volume mínimo de lançamento: 8-12 criativos genuinamente distintos** (ângulo diferente ≠ cor diferente — o sistema fingerprinta o criativo; variação superficial é lida como duplicata e compete consigo mesma).

**Campos obrigatórios por linha da matriz (instituídos 20/09/2026):** `ID` · `ID da base` quando for derivado · `tipo de teste` (conceito · componente · combinação) · `componente alterado` · `hipótese em uma frase`.

> **Conceito novo e variação de execução contam em colunas separadas.** Doze variações do mesmo pivô não são doze criativos distintos, e variação com hipótese escrita não é "cor diferente". Derivação de base vencedora roda por `100-métodos/METODO-LATERALIZACAO-DE-CRIATIVOS.md`; redação nova de anúncio DR roda por `100-métodos/METODO-CONSTRUCAO-DE-CRIATIVOS-DR.md`.

### 4.2 Regra de portfólio 70/30

Cada rodada de criativos: ~70% iterações de vencedores (novos hooks/formatos sobre ângulo validado) + ~30% conceitos novos de risco real. Só iterar = teto caindo; só experimentar = conta instável.

🔴 **Esta é a fonte única da proporção** (`METODO-LATERALIZACAO-DE-CRIATIVOS.md` §7 a consome e não a redefine). Ela classifica **produção de criativo**, não distribuição de verba. **Conta sem vencedor não tem 70:** declara ausência de base e roda exploração. Fabricar a parcela de iteração é fingir histórico.

### 4.3 Produção e compliance

- Copy de criativo: `10-skills/copywriter-senior-continuum/` (módulos 03, 04 e 06) + `100-métodos/METODO-CONSTRUCAO-DE-CRIATIVOS-DR.md` quando for anúncio de resposta direta + voz do cliente (skill de voz se existir; senão, amostras no briefing) + `clientes/<cliente>/lexico-icp/`. **Nunca** `voz-operador` para cliente. *(Ponteiro corrigido em 20/09/2026: `copywriting-fable5` e `stop-slop` são legado em `10-skills/_legado/`.)*
- Conformidade com políticas de anúncio do canal ANTES de subir (nicho sensível → checar políticas específicas; reprovação em série machuca a conta).
- **Nomenclatura padrão:** `[cliente]-[ângulo]-[formato]-[hook]-[versão]` (ex.: `contaa-dor-video-h1-v2`). Sem nomenclatura, não há leitura de dados.

### 4.4 Fadiga e reposição

> 🔴 **Hook rate alto e venda baixa pede diagnóstico de mídia primeiro — não presumir que a causa é o gancho. E nenhuma base se classifica como vencedora sem o critério da conta** (`METODO-LATERALIZACAO-DE-CRIATIVOS.md` §4). *(migrado do roteador em 26/09/2026 — era afirmação ÓRFÃ: existia só no `CLAUDE.md` §6, e se perderia na compactação)*


Sinal de fadiga: frequência > 3,5-4,0 **e** CTR caindo ≥ 20% vs. média própria. Ação: pausar criativo e repor da fila. **Fila de reposição: mín. 4 criativos prontos a cada início de mês.** Cadência de refresh: rodada nova a cada 2-4 semanas conforme verba.

**Rota de reposição:** diagnosticar primeiro (§7.4) e, com base elegível e hipótese sobre um componente, derivar por `100-métodos/METODO-LATERALIZACAO-DE-CRIATIVOS.md`. **Troca superficial não resolve fadiga**, e queda de retenção não prova que a causa é o gancho.

---

## 5. FASE 5 — ESTRUTURA DE CAMPANHAS

### 5.1 Regra-mãe (qualquer canal)

**1 campanha por objetivo de conversão. O mínimo de subdivisões que a verba sustenta com dados densos.** Toda subdivisão precisa justificar-se por diferença real de oferta, funil ou economia — nunca por "organização".

### 5.2 Meta Ads (canal padrão do nosso ICP)

- **Estrutura:** 1 campanha por objetivo · 1-3 conjuntos no máximo · **6-20 criativos ativos por conjunto** · targeting broad ou Advantage+ **de público** (restrições mínimas: idade/região quando o negócio exige, ex.: local). Advantage+ de **posicionamento** é proibido (linha abaixo).
- 🔴 ⭐ **Posicionamento: personalizado, só Instagram Feed, Stories e Reels, sempre** *(regra da casa, 14/10/2026, corrigida em 22/10/2026, alçada {{OPERADOR}})*. Todo conjunto de anúncios na Meta sobe com **posicionamento manual** e três caixas marcadas: **Instagram Feed**, **Instagram Stories** e **Instagram Reels** (na API: `publisher_platforms ["instagram"]`, `instagram_positions ["stream","story","reels"]`; sufixo `igfsr` no nome do conjunto). Sai todo o resto: Facebook, Messenger, WhatsApp, Threads, Audience Network e, dentro do Instagram, perfil, Explorar e pesquisa. **Posicionamento Advantage+ (automático) é proibido.**
  - ~~Só Instagram Stories e Reels, feed desmarcado~~ *(vigente de 14/10 a 22/10/2026)*. **Correção de alçada do {{OPERADOR}}, 22/10:** a regra é que entram, sempre, feed, stories e reels, e somente no Instagram; o erro de escrita foi tratar "story/reel" como "uma coisa só". "Story/reel" é **um grupo de arte** (o 9:16), não a lista de posicionamentos.
  - **Em cada anúncio vão as duas artes, e as duas são veiculadas:** a 4:5 no grupo **Feeds** da personalização por posicionamento (é a que aparece no feed do Instagram) e a 9:16 no grupo **Stories e Reels**. Nenhuma é a outra esticada ou cortada. **Anúncio que só tem a 9:16 não sobe em conjunto com feed:** produz-se a 4:5 antes.
  - **Conferência antes de publicar:** no conjunto, a lista de posicionamentos mostra só os três; no anúncio, a prévia do feed mostra a 4:5 inteira, e a de Stories e a de Reels mostram a 9:16 inteira, sem corte de texto na zona livre do topo e da base (§4.3).
  - **Conjunto já no ar fora da regra:** corrigir reinicia o aprendizado, então é decisão do {{OPERADOR}}, registrada no `LOG-DECISOES.md` do cliente. Conjunto novo não tem exceção.
  - *Por quê:* decisão do {{OPERADOR}}. Leitura nossa, a confirmar: concentra a verba onde o nosso ICP consome e onde a arte 9:16 foi feita para caber, e tira a leitura de resultado da média com posicionamentos que não testamos.
- 🔴 ⭐ **Objetivo: campanha para WhatsApp sobe em Engajamento, por prioridade** *(regra da casa, 27/10/2026, alçada {{OPERADOR}})*. Decisão de alçada: toda campanha para WhatsApp tem como prioridade o objetivo de engajamento. Vale para toda campanha cujo resultado é a conversa no WhatsApp, chegue ela direto ou passando por uma página.
  - **WhatsApp direto (clique para WhatsApp):** Engajamento → local da conversão **Apps de mensagem / WhatsApp** → meta **maximizar conversas**. Na API: `OUTCOME_ENGAGEMENT`, `destination_type WHATSAPP`, `optimization_goal CONVERSATIONS`, `promoted_object {page_id}`. Pede a página do cliente com o WhatsApp Business ligado.
  - **Página que leva ao WhatsApp** (sem WhatsApp Business, ou página como ponte): Engajamento → local da conversão **Site** → meta **conversões** no evento **Contact** do pixel, disparado no clique do botão de WhatsApp. Na API: `OUTCOME_ENGAGEMENT`, `destination_type WEBSITE`, `optimization_goal OFFSITE_CONVERSIONS`, `promoted_object {pixel_id, custom_event_type: CONTACT}`. **Nunca otimizar pelo clique ou pela visualização da página:** isso entrega quem passeia, não quem chama.
  - **Ordem, por resultado e por custo** *(decisão de {{OPERADOR}}, 27/10: a prioridade de Engajamento em campanhas para o WhatsApp é por resultados e custos)*: **Engajamento > Leads** e **Engajamento > Vendas (conversão)**. Leads ou Vendas só com o motivo escrito no `LOG-DECISOES.md` do cliente. **Tráfego nunca.**
  - **O objetivo não se troca depois:** a Meta recusa mudar o objetivo de campanha que já tem conjunto (erro `1885073`). Objetivo errado = campanha nova.
  - *Por quê:* **resultado e custo**. Em Engajamento a conversa sai com mais volume e mais barata do que em Leads ou em Vendas. 🟡 **A medir com dado nosso:** custo por conversa em Engajamento contra Leads e Vendas, na primeira conta que rodar mais de um. O número calibra a regra e não a reabre sem dado. *O erro que a regra evita:* subir em Tráfego ou em Leads por volume e ter de refazer a campanha, porque o objetivo não se troca depois.
- 🔴 **Conta herdada: inventário de status antes de criar qualquer coisa**. Ler campanha, conjunto **e** anúncio com `status` e `effective_status`, e não só o gasto. O que não é nosso fica **pausado nos três níveis**, e o inventário é registrado no `LOG-DECISOES.md`. Anúncio ativo sob campanha pausada é bomba-relógio: basta alguém ligar a campanha. *Por quê:* gasto zero não prova nada. Um anúncio pode estar ativo e com verba sob uma campanha pausada, e um registro que só lê o gasto não o enxerga.
- **Não fazer:** empilhar lookalikes/interesses em conjuntos paralelos · duplicar criativos entre conjuntos concorrentes · mais de 3 conjuntos com verba < R$ 300/dia.
- **Teste → escala:** teste em estrutura própria com cap de verba (~50% do normal) e regras de kill (§7.3); vencedores migram/escalam na campanha principal (CBO). Exclusão mútua entre teste e principal quando possível.
- **Local/serviço:** raio geográfico + broad; formulário nativo ou WhatsApp como conversão (WhatsApp: objetivo Engajamento, linha acima); Customer Match/lista de clientes como sinal, não como jaula.

### 5.3 Verba pequena (< R$ 100/dia — realidade frequente do nosso ICP)

- **1 campanha, 1 conjunto, 6-10 criativos.** Zero fragmentação.
- Otimizar para o evento que gera ≥ 30-50 eventos/semana (lead/conversa, não compra, se necessário).
- Janela de decisão mais longa (dados escassos = decisões mais lentas, §7.3 com prazos dobrados).
- Expectativa contratada: verba pequena valida mensagem e gera fluxo, não escala. Dizer isso por escrito.

### 5.4 Google Ads (quando o nicho é demanda ativa)

- Verba < R$ 2.000/mês ou < 15 conversões/mês: **Search pura com correspondência controlada** (evitar PMax — IA sem dados queima verba em aprendizado).
- PMax só com ≥ 30 conversões/mês projetadas na campanha e feed/ativos decentes; asset groups por tema, não "tudo junto".
- Verba diária de referência: ≥ 10× CPA alvo (15-20× encurta aprendizado).

### 5.5 Nomenclatura de campanha (obrigatória)

`[cliente]-[canal]-[objetivo]-[funil]-[data]` · conjuntos: `[público/estrutura]` · anúncios: nomenclatura §4.3. Registrada em `estrutura-campanhas.md` do cliente.

**Campos da conta (14/10/2026):** uma conta pode acrescentar campos à convenção (`[produto]` na campanha quando há mais de uma oferta; `[linha]` de arte no anúncio, depois do hook, quando a peça sai em duas linhas visuais), desde que **sempre na mesma posição, sempre preenchidos e declarados no `estrutura-campanhas.md` dela**. Campo opcional quebra a leitura por posição. Valores fixos da casa: funil `topo · meio · fundo`, data `aaaammdd` do início da veiculação, sem hífen dentro de campo. **Nome não muda depois de o anúncio rodar:** mudança de peça é anúncio novo, com versão nova. Exemplo completo: `90-templates/trafego-cliente/estrutura-campanhas.md`.

---

## 6. FASE 6 — TRACKING (sem sinal, sem verba)

Checklist de subida — **tudo verde antes do primeiro real**:

1. **Pixel + CAPI simultâneos** (Meta) / tag + conversões aprimoradas (Google). EMQ alvo ≥ 7.
2. **Eventos do funil mapeados e testados** no Events Manager (PageView → Lead/Conversa → Compra, com dedupe pixel/CAPI).
3. **Convenção UTM documentada e travada** (padrão: `utm_source=meta|google · utm_medium=paid · utm_campaign=[nomenclatura §5.5] · utm_content=[criativo §4.3]`). Inconsistência de UTM fragmenta a leitura — convenção é lei.
4. **Fonte de verdade fora da plataforma:** planilha/CRM com leads por origem, custo, e resultado comercial (venda/não venda). A plataforma reporta o que ela vê; o caixa do cliente é o juiz.
5. **Atribuição definida por escrito** (janela padrão 7d clique/1d visualização) e mantida estável — mudar janela no meio invalida comparações.
6. Auditoria mensal do Events Manager (sinal degrada em silêncio).

---

## 7. FASE 7 — ROTINA DE GESTÃO (regras, não sensação)

### 7.1 Cadência

| Frequência | Ação | Tempo |
|---|---|---|
| **Diária** (dias úteis) | checagem de anomalia: gasto rodando? reprovações? CPA explodiu (> 2× alvo no dia)? | 10 min |
| **2×/semana** (ter/sex) | decisões kill/scale/manter pelas regras §7.3 + registrar em `LOG-DECISOES.md` | 30-45 min |
| **Semanal** | leitura de funil completo (plataforma + fonte de verdade), fila de criativos, ajuste de plano | 1h |
| **Mensal** | relatório ao cliente (Fase 8) + revisão da matemática §2.2 + auditoria de tracking | 2h |

### 7.2 Disciplina de aprendizado (o que NÃO fazer)

- **Não mexer nas primeiras 72h** de campanha/conjunto novo, salvo kill hard (§7.3).
- **Uma mudança estrutural por vez** — cada edição significativa (verba, otimização, criativo no conjunto) pode resetar aprendizado.
- Verba: **nunca variar mais de ±20% por 48-72h** no mesmo conjunto/campanha.

### 7.3 Regras de decisão (default — calibrar por cliente no plano)

| Situação | Regra | Ação |
|---|---|---|
| **Kill hard** (vale mesmo < 72h) | gastou 3× CPA alvo sem 1 conversão · CTR < 0,5% com ≥ 2.000 impressões · reprovado/limitado | pausar criativo/conjunto |
| **Kill normal** | CPA > 3× alvo por 3 dias corridos (após 72h) | pausar e diagnosticar (§7.4) |
| **Fadiga** | frequência > 3,5-4,0 + CTR −20% vs. média própria | pausar criativo, repor da fila |
| **Vencedor** | CPA ≤ alvo com ≥ 10 conversões acumuladas | iterar por `METODO-LATERALIZACAO-DE-CRIATIVOS.md` (70/30 §4.2) + candidato a escala |
| **Escala** | vencedor estável ≥ 7 dias | +20% de verba a cada 48-72h; monitorar CPA por 72h antes do próximo degrau |
| **Escala horizontal** | vertical saturou (CPA subiu 2 degraus seguidos) | novo criativo/ângulo/canal, não mais verba no mesmo lugar |
| **Verba pequena (§5.3)** | dados escassos | prazos das regras acima **dobrados** |

**Toda decisão dessas é registrada em `LOG-DECISOES.md` (data · o quê · por quê · resultado esperado).** O log é o que transforma gestão em método e alimenta o aprendizado entre clientes.

### 7.4 Ordem de diagnóstico (CPA alto — não tratar sintoma como causa)

1. **Tracking** — o dado é real? (Events Manager + fonte de verdade divergem?)
2. **Oferta** — CTR ok mas ninguém converte em lugar nenhum? O problema não é mídia.
3. **Página/atendimento** — clique caro converte mal? (CTR ok, conversão pós-clique baixa; ou leads bons não atendidos a tempo.)
4. **Criativo** — CTR baixo, frequência ok? Hook/ângulo fraco.
5. **Estrutura/leilão** — tudo acima ok e CPM explodiu? Sazonalidade, concorrência, consolidar estrutura.

### 7.5 Guardrails financeiros

- Cap de gasto mensal da conta = verba contratada (configurar na plataforma, não confiar em disciplina).
- Mudança de verba > 30% do plano mensal: aprovação do cliente por escrito.
- Nosso lado: CAC do cliente subindo 2 meses sem LTV acompanhar → tripwire `POLITICAS` §7 (rever oferta/canal antes de escalar verba).

---

## 8. FASE 8 — RELATÓRIO AO CLIENTE

- **Cadência:** mensal formal + resumo semanal curto (WhatsApp/e-mail, 5 linhas: gasto · resultado · próxima ação).
- **Estrutura do mensal:** (1) meta vs. realizado (a linha assinada em §2.2.6); (2) funil completo com custo por etapa; (3) o que aprendemos (criativos/ângulos vencedores e mortos); (4) decisões tomadas e por quê (extrato do log); (5) plano do próximo ciclo; (6) o que precisamos do cliente.
- **Métricas proibidas como manchete:** impressões, alcance, cliques soltos. Manchete é sempre resultado de negócio (leads qualificados, vendas, custo por resultado, receita).
- Números da plataforma **e** da fonte de verdade, lado a lado, com divergência explicada.
- Documento interno de governança não cruza stop-slop; **relatório de cliente cruza** (`stop-slop.skill.md` — é peça para humano).

---

## 9. COMPLIANCE DE SAÍDA E HANDOFFS

- Output de campanha/criativo/relatório passa por `00-core/COMPLIANCE-DE-OUTPUT.md`.
- **Handoffs:** ← CEO/CRO (oferta, posicionamento, preço) · → Head de Conteúdo (criativos, mensagem) · → Comercial do cliente (leads → atendimento; SLA de resposta é contratado) · → Head Financeiro (cobrança do fee + repasse de verba **sempre na conta do cliente**, nunca na nossa).
- **Verba do cliente roda em ativo do cliente** (BM/conta de anúncios própria, nós como parceiros/gestores). Protege o cliente, protege a nós e preserva o histórico dele.

---

## 10. EVOLUÇÃO DO MÉTODO

- Após cada ciclo mensal de cada cliente: 3 aprendizados registrados no `LOG-DECISOES.md` → candidatos a virar regra aqui.
- Thresholds do §7.3 são **defaults** — calibrados por cliente no `PLANO-DE-MIDIA.md`; quando 3+ clientes calibram o mesmo número, o default muda aqui (decisão registrada no rodapé).
- **Fase 2 (automação):** regras automáticas de plataforma, agentes de leitura via API (Windsor/Meta) e dashboards só entram após ≥ 1 cliente com 1 ciclo completo manual. Processo antes de ferramenta.

---

*Registro de mudanças: 2026-07-08 — criação (pesquisa de práticas 2025-26: consolidação pós-Andromeda, criativo-como-segmentação, Pixel+CAPI, regras de kill/escala; adaptado à nossa escala e ICP). Pendente: calibração com 1º cliente. · 2026-10-27 — §5.2: campanha para WhatsApp sobe em Engajamento, por prioridade (alçada {{OPERADOR}}).*
