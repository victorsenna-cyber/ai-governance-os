# Governança {{EMPRESA}}

Centro de comando da {{EMPRESA}}. Esta pasta governa cultura, estratégia, tática e operação como um sistema único.
**Comece sempre pelo `CLAUDE.md`** — ele define que você opera como CEO da {{EMPRESA}}.
**Primeira vez aqui?** `LEIA-ME-TEMPLATE.md` (e apague-o quando terminar).

---

## Como usar

1. Abrir `CLAUDE.md` → assume o papel de CEO e as regras permanentes.
2. Rotear o pedido para uma das sete árvores (`CLAUDE.md` §6 → `00-core/roteador/`).
3. Carregar na ordem do processo: `framework → trilho → método → blueprint → política → gate`.
4. Consultar o estado (`STATUS.md`) e o contexto da conta (`clientes/<cliente>/`).
5. Entregar decisão + direção + ação + impacto; registrar (`CLAUDE.md` §11); fechar com `verificar-propagacao.py` e `sincronizar.py`.

---

## Mapa de pastas

| Pasta | O que contém |
|---|---|
| `00-core/` | DNA da empresa: princípio, cultura, manifesto, políticas de decisão (os números), modos de resposta, critérios, compliance de output, KPIs, protocolo multi-modelo, taxonomia de artefatos e `roteador/` (as 7 árvores). |
| `10-skills/` | Skills portáteis (copy, página, ui-ux), personas (C-level, heads), jurídico, métodos não portados e a voz do operador. |
| `100-métodos/` | Os artefatos de conhecimento, tipados: frameworks, trilhos, métodos, políticas, gates. |
| `20-projeto-escopo/` | Detalhamento por dimensão (fonte: `PROJECT.md`/`SCOPE.md`). |
| `30-comercial/` | Só processo comercial da casa: ICP, oferta, produtos, serviços, onboarding, prospecção, swipe file, benchmark. Nada de cliente aqui. |
| `40-operacao-rotinas/` | Rituais, gestão do tempo, operação por tasks, medição de tokens, rito de integração da antessala e as `ferramentas/` (Windows, macOS e Linux; Mac começa em `ferramentas/macos/`). |
| `45-financeiro/` | Lançamentos da empresa e extratos classificados (fonte do painel *Caixa*). |
| `50-integracoes-dados/` | Estado dos sistemas (CRM, automações), escrito pelo sistema. |
| `60-planos/` | Plano de 90 dias e metas vigentes. |
| `70-metodologias-chave/` | Biblioteca de referência (PDFs, fora do git). |
| `80-juridico/` | Políticas jurídicas, templates de contrato, registros de caso, societário, dados do contratado. |
| `90-templates/` | Blueprints: repo de cliente, conta nova, léxico de ICP, benchmark de VSL, diagnóstico, PDFs, prancha, kit de marca, tráfego, desenho de produto, relatório da operação. |
| `900-oficina/` | Oficina das skills e agentes (edita-se aqui, publica-se em `10-skills/` e `.claude/agents/`). |
| `940-operador/` | O que é pessoal do operador e precisa estar no sistema (finanças pessoais). |
| `945-branding/` · `950-marketing/` · `960-referências criativos/` · `980-web-design/` | Marca, peças de marketing, referências de criativo, páginas e painéis nossos. |
| `clientes/` · `parceiros/` | Uma pasta por cliente e por parceiro; o molde em `clientes/README.md`. |
| `execução Codex/` | A antessala de um executor externo; nada aqui é canônico antes do rito. |
| `Padrão Linguístico - Operador/` | Fonte da voz do operador (corpus falado). |

---

## Documentos raiz

- `CLAUDE.md` — comportamento e papel de CEO (autoritativo), lido por Claude Code.
- `AGENTS.md` — **o mesmo kernel, para quem usa Codex, GPT ou outra ferramenta que lê `AGENTS.md`**: réplica do `CLAUDE.md`, só o nome muda; `sincronizar.py` mantém os dois iguais. Com ele, o Codex opera como agente principal (CEO).
- `AGENTS-EXEC.md` — o contrato do **segundo** agente (executor na antessala `execução Codex/`), se a operação tiver dois. Quem usa um agente só ignora este arquivo.
- `STATUS.md` — estado vivo, fonte única de fato atual.
- `PROJECT.md` — tudo sobre a {{EMPRESA}} · `SCOPE.md` — escopo de atuação.
- `MAPA-DO-REPO.md` — o grafo de funcionamento (o README diz o que existe; o mapa, o que acontece depois).
- Nenhum método mora na raiz: todos vivem em `100-métodos/`.

---

## Como popular este repositório com o contexto da empresa — roteiro de entrevista para a IA

> **Para o agente (Claude, Codex ou outro) que abre este repositório pela primeira vez numa empresa nova.** O repositório vem com a arquitetura e os métodos; o que falta é o **fato** da empresa. Este roteiro diz **o que perguntar, em que ordem, onde cada resposta vai e o que nunca se inventa.** Rode-o como uma entrevista: um bloco por sessão, respostas registradas **literalmente** (entre aspas, com data), e cada bloco fechado com o arquivo escrito e lido de volta para quem respondeu.

### As quatro regras da entrevista

1. **Pergunta só o que é FATO.** Preço, capacidade, prova, o que entrega, palavra do público, quem decide, quanto tem em caixa. **Estrutura — promessa, mecanismo, narrativa, ordem dos argumentos, recorte de público — é decisão do agente, feita a partir dos fatos** (`CLAUDE.md` §8, REGRA Nº 0). Perguntar estrutura ao dono é erro de método.
2. **O que ele não sabe vira `a calibrar` ou `n=0`, escrito assim.** Nunca palpite, nunca "deve ser uns". Campo inventado contamina toda peça produzida depois.
3. **Registra literal, decide depois.** A fala do dono entra entre aspas, com data. A leitura do agente vem separada e marcada como leitura (`CLAUDE.md` §11.2).
4. **Um bloco por vez, e o arquivo nasce no fim do bloco.** Entrevista inteira sem arquivo é conversa que se perde no fim da sessão.

### Bloco 0 — quem opera (10 min) → `CLAUDE.md` §1, `STATUS.md` §4, `POLITICAS` §1

- Nome da empresa e de quem detém a alçada. Há sócio? Qual a participação e **existe instrumento assinado**? Se não existe: registrar *"acordo verbal — não oponível"* e abrir pendência em `80-juridico/societario/`.
- Quem executa, quantas pessoas, quantas horas de entrega por semana **cada uma** (de verdade, não de intenção; se não sabe, `a calibrar` e medir em duas semanas).
- Que ferramenta de IA opera o repositório (Claude Code, Codex, outra) e quem é o **dono nomeado do registro** (nome, não cargo). Sem dono, o repo congela em 30 dias.
- Rodar: `python3 40-operacao-rotinas/ferramentas/instanciar-template.py --definir EMPRESA="…" OPERADOR="…"`.

### Bloco 1 — a empresa (20 min) → `PROJECT.md`, `SCOPE.md`, `00-core/CULTURA.md` §0 e §9

- O que a empresa vende, para quem, há quanto tempo, e **o que já vendeu de fato** (clientes pagantes, quantos, por quanto).
- Constituição: CNPJ, cidade, banco por onde o dinheiro passa (empresa e pessoal são a mesma conta?).
- O vocabulário próprio do dono: termos, modelos e referências que ele usa sem explicar (vão para `PROJECT.md` §1; o agente passa a usá-los como língua de trabalho).
- De onde vem a cultura dele (o fundamento que o move) e **como a marca aparece** quando aparece (arquétipo dominante e secundários — se não souber, fica para o Bloco 7).
- Stack: CRM, automação, site, onde publica, o que paga por mês em ferramenta.

### Bloco 2 — os números que decidem (30 min) → `00-core/POLITICAS-DE-DECISAO.md`

Perguntar **um a um**, na ordem do arquivo, e escrever a resposta no lugar do `{{…}}`:
- Norte: qual MRR, até quando. Os gates de estágio (`MRR_ESTAGIO_B`, `MRR_ESTAGIO_C`): o agente propõe a partir do norte; o dono confirma.
- Teto de despesa que exige decisão explícita. Horas de entrega por semana. Teto de horas por mês.
- Piso de valor-hora e margem mínima: **se o dono nunca calculou, o agente calcula a partir do custo fixo mensal ÷ horas de entrega, mostra a conta e pergunta se aceita** — e marca `[estimado]`.
- Verba de teste de mídia por tentativa (só se houver tráfego frio).
- Tudo o que ele responder "não sei" fica `a calibrar` e entra no `STATUS.md` §6.

### Bloco 3 — quem compra (30 min) → `30-comercial/ICP.md`

- Os últimos 5 clientes que pagaram: segmento, faturamento aproximado, **por que canal chegaram** (indicação, frio, inbound), ticket, o que compraram, o que travava a operação deles antes.
- Os últimos 5 que **não** fecharam: o que disseram, literalmente.
- O canal em que o cliente opera (WhatsApp, e-mail, balcão) — pré-requisito de acoplagem.
- Quem o dono **não** quer atender, e por quê.
- Com isso o agente escreve §2 (primário, com `n`), §2.1 (canal, com o dado), §4 (anti-ICP) e deixa §3 (expansão) vazio até haver caso. **O score do §5 não se pergunta: o agente aplica aos 10 nomes e mostra o resultado.**

### Bloco 4 — o que se vende e por quanto (30 min) → `30-comercial/oferta.md`, `servicos.md`, `produtos.md`, `POLITICAS` §5

- Lista do que ele vende hoje: nome, o que entrega, prazo, preço (setup e mensal, separados), **quantas vezes vendeu cada um**.
- O que ele gostaria de vender e nunca vendeu (vai para o roadmap, marcado `n=0`, nunca para a escada vigente).
- Capacidade por oferta: quantas horas cada entrega consome, **em construção e em operação** (duas fases, `POLITICAS` §4-ter). Se não mediu, `[estimado por analogia]`.
- O agente monta a escada (§3 da oferta) nos degraus do método — diagnóstico pago, construção, recorrência, maior valor — **e é ele quem decide em que degrau cada oferta cai**. O dono objeta congruência; não decide estrutura.

### Bloco 5 — como se vende e se entrega (20 min) → `30-comercial/onboarding.md`, `prospeccao-*/`, `40-operacao-rotinas/RITUAIS.md`, `GESTAO-DO-TEMPO.md`

- Como um cliente entra hoje, passo a passo, do primeiro contato ao primeiro pagamento. Onde trava.
- O que acontece na primeira semana depois de fechar (o onboarding real, não o desejado).
- O dia padrão do dono: a que horas prospecta, entrega, atende; o que sempre engole o quê.
- Metas semanais que ele já persegue (conversas, propostas, fechamentos) — ou `a calibrar`.

### Bloco 6 — dinheiro e papel (20 min) → `45-financeiro/`, `940-operador/FINANCAS.md`, `80-juridico/DADOS-DO-CONTRATADO.md`, `80-juridico/registros/`

- Caixa hoje, custo fixo mensal, passivo, **a obrigação dura mais próxima** (data, valor, origem do dinheiro).
- Qualificação para contrato (nome completo, CPF/CNPJ, endereço, e-mail, Pix) — direto para `DADOS-DO-CONTRATADO.md`.
- Relação ativa sem instrumento escrito (cliente, parceiro, fornecedor, sócio)? Cada uma vira pendência jurídica com data.
- Conflito ou cobrança em aberto? Abre registro em `80-juridico/registros/` no padrão das 4 camadas.

### Bloco 7 — voz e marca (quando houver material) → `10-skills/voz-operador.skill.md`, `945-branding/`

- **Não se pergunta "como é a sua voz".** Pede-se material: 2 a 3 calls gravadas, 20 mensagens de WhatsApp enviadas, textos publicados. A voz se **mede** pela `100-métodos/Método de extração de linguagem/`; sem corpus, a skill fica esqueleto e as peças saem na voz neutra do método.
- Marca: logo, cores e fontes existentes; referências visuais que ele admira. O arquétipo sai de `100-métodos/ARQUETIPOS-DE-MARCA.md`, proposto pelo agente.

### Bloco 8 — as contas (uma sessão por cliente ativo) → `clientes/<Cliente>/`

Para cada cliente ativo: criar a pasta pelo molde (`clientes/README.md`), rodar o `PEDIDO-UNICO.md` e registrar `STATUS.md` + `DECISOES.md` com o que já foi decidido e **o que foi descartado**. Toda call gravada é destilada, nunca resumida.

### Fechamento da entrevista

- `STATUS.md` §1 a §6 preenchidos; §7 já vem pronto.
- `python3 40-operacao-rotinas/ferramentas/instanciar-template.py --listar` com zero placeholders obrigatórios (os de preço podem ficar `a calibrar`, escritos assim).
- `python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py` em ✅.
- Uma entrada no topo do `STATUS.md`: *"repositório instanciado em DD/MM/AAAA; pendências de calibração: …"*.
- **O primeiro pedido real roteado pelo `CLAUDE.md`/`AGENTS.md` §6** — e o que o repositório não soube responder vira a próxima pergunta. É assim que ele passa a ser da empresa.

---

## Estado

| Item | Status |
|---|---|
| Arquitetura e métodos | ✅ vêm prontos do template |
| Placeholders `{{…}}` | 🟡 a preencher (`LEIA-ME-TEMPLATE.md` §2) |
| Políticas e ICP | 🟡 a calibrar com evidência |
| Primeiro pedido real roteado | ⏳ pendente |
