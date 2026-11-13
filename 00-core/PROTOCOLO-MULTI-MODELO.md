# PROTOCOLO MULTI-MODELO — quem executa o quê, com que contexto

> **Tipo:** política (camada 2) · **Criado:** 2026-07-08 (Fable 5) · Vale para TODOS os projetos.
> Princípio: **inteligência cara decide e trava; inteligência barata executa contrato.** Um modelo executor nunca decide o que um método já decidiu; se o contrato não cobre, ele PARA e registra a dúvida no log do projeto, nunca improvisa. **O destino da dúvida é a sessão principal, nunca o {{OPERADOR}}:** o subagente devolve achado, recomendação e classe do ato (R ou L1–L7, `CLAUDE.md` §5.2), e quem decide e fala com o operador é a sessão principal (mecanismo opcional: `gate-fecho.py` no hook `SubagentStop` devolve o relatório que endereçar o operador).

## 1. Roteamento por ferramenta

| Ferramenta | Usar para | Nunca usar para |
|---|---|---|
| **Agente principal (modelo forte)** | decisões novas · métodos e skills · estrutura e arquitetura de peça · **copy** · auditoria de peça-mestra · registro no repo (`CLAUDE.md` §11) · desbloqueio quando executor travar | builds longos de front, edição mecânica, ler pastas grandes |
| **Agente de build (modelo médio, com ferramentas)** | build de código e scripts · iteração com preview · automações | decidir oferta/preço/copy de venda (vem do plano) |
| **Executor externo (segundo agente, se houver)** | ⭐ **execução visual — etapa 4 do circuito de página** (`CLAUDE.md` §6.3): HTML/CSS/JS, responsivo, estados, animação, performance, Lighthouse · refino de código já aprovado · **revisão cruzada técnica** · paralelismo com o Claude | decidir ordem de dobras · **tocar em uma palavra de copy** · qualquer coisa canônica · registro no repo |
| **Ferramenta de imagem** | geração/edição de imagem (criativos estáticos a partir da copy pronta + direção de design) · variações de volume sobre matriz travada | qualquer coisa canônica (métodos, decisões, oferta) |
| **Assistente de código gratuito** | edição mecânica: propagar data/preço, renomear, formatar, mover arquivo, checklist | qualquer escolha com 2 opções válidas |

> 🔴 **O executor externo, se houver, opera em ISOLAMENTO DE ESCRITA.** Ele só escreve em pastas `execução Codex/`; todo o resto da Governança é leitura. **Consequência: a saída dele nunca é estado — é proposta**, e precisa do `40-operacao-rotinas/RITO-INTEGRACAO-CODEX.md` para virar canônico. ⚠️ **Isso muda a economia da delegação: cada tarefa dada a ele gera uma tarefa de integração.** Vale a pena em trabalho volumoso e verificável; **não vale em ajuste pequeno, onde o custo de integrar supera o de fazer.**

**Revisão cruzada barata:** o que um agente cria, outro audita contra o contrato. **Quem julga não reescreve** — o auditor aponta defeito localizado por linha e devolve ao dono do artefato. (Mesma regra do esquadrão de copy; autoauditoria não pega o que revisão cruzada pega.)

### 1-bis. ⭐ DONO POR ETAPA DO CIRCUITO DE PÁGINA (regra da casa)

O circuito de `CLAUDE.md` §6.3 já tem cinco etapas. **A divisão de ferramenta é por etapa, não por "quem é melhor".**

| # | Etapa | Skill | **Dono** | Por quê |
|---|---|---|---|---|
| 1 | **Física** | gerador | **Claude** | classificação, brief de 9 campos, esqueleto, curva — é decisão, não execução |
| 2 | **Direção visual** | ui-ux (direção) | **Claude** | tokens, grade, **limite de caracteres por bloco** — é restrição que o executor vai obedecer |
| 3 | **Escrita** | copywriter | **Claude** | pivô, régua, gate anti-slop, voz do cliente |
| 4 | ⭐ **Execução visual** | ui-ux (execução) | **Codex** | é exatamente "front guiado": insumo travado, saída verificável |
| 5 | **Gate** | juiz | **Claude** decide · **Codex** roda a parte técnica | veredito é decisão; medição é execução |

> **A etapa 4 é a única que muda de dono, e é onde o Codex é melhor que nós.** As três primeiras produzem o briefing de que ele precisa: **a qualidade da etapa 4 é função direta da 1, 2 e 3.** Codex mal briefado não é Codex ruim — é contrato ausente.

### 1-ter. 🔴 Por que um executor "não segue o repo com maestria" — e não é falha dele

**Diagnóstico.** Três causas estruturais, todas nossas:

1. **`CLAUDE.md` declara "você opera como CEO" e concede autoridade de decisão** — o oposto exato do que o §Princípio deste protocolo exige de um executor. Mandar o executor ler o kernel inteiro **autoriza** o improviso que se queria proibir.
2. **`CLAUDE.md` §6 é um roteador denso de intenção→skill.** Numa tarefa de front, ~95% é irrelevante. Ruído de contexto em executor produz exatamente o sintoma observado.
3. **O §2 deste protocolo já dizia a resposta e ninguém aplicou:** *"se o executor precisa de mais de 5 arquivos, o contrato está mal feito"*. Um contrato de executor que manda ler 6 arquivos antes de começar, e o `CLAUDE.md` sozinho aponta para dezenas.

**A correção: o kernel do principal (`CLAUDE.md`, replicado em `AGENTS.md`) e o contrato do executor (`AGENTS-EXEC.md`) são complementares, não redundantes.**

| Arquivo | Governa | Contém |
|---|---|---|
| **`CLAUDE.md`** | o agente que **decide** | autoridade, roteador, método, registro |
| **`AGENTS-EXEC.md`** | o agente que **executa** | contrato, fronteiras, lista do proibido, gate de fecho. **Diz explicitamente para NÃO ler o `CLAUDE.md`** |

**É a divisão que as duas ferramentas já fazem por convenção de nome** — só não estava sendo usada. Template de contrato por tarefa: `90-templates/CONTRATO-EXECUTOR.md`.

### 1-quater. ⭐ NÍVEIS N0–N5 DA OPERAÇÃO POR TASKS

Toda task agendada declara `nivel_minimo` e `escada`: **N0** script (sem LLM) · **N1** gratuito via FreeLLMAPI, **só dado `P`/`I`** · **N2** Haiku (mecânico) · **N3** Sonnet (checklist, rascunho, inventário) · **N4** Opus (decidir, copy, diagnóstico, revisar amostra; Ruflo só como worker externo com `swarm: sim`) · **N5** Fable 5.1 (o raro e caro — plano de iteração, auditoria de peça-mestra, passada global do juiz, decisão que cruza áreas, revisar amostra do N4; nunca por padrão). Nunca abaixo do piso; orçamento batido = adia ou vira cartão de decisão (molde `40-operacao-rotinas/tarefas/modelos/cartao-decisao.md`). Tabela completa e esquema: `40-operacao-rotinas/tarefas/README.md` §2–§3. Despachante: `40-operacao-rotinas/ferramentas/despachar.py`. 🔴 **Gate de contexto:** peça com carga de sessão (hook, skill, MCP, plugin) só entra com a carga fixa medida antes e depois (`medir-contexto.py`); **o teto de carga fixa por sessão é parâmetro da operação** (cada operação mede a sua carga e fixa o seu teto). `medir-contexto.py --teto <N>` é o gate.

**As peças do roteamento de modelo, e o que cada uma impede.** O nível diz *quem* executa; estas peças garantem que a divisão aconteça sem depender de alguém lembrar dela (`CLAUDE.md` §8, REGRA Nº 1):

| Peça | Onde | O que faz | Sem ela |
|---|---|---|---|
| **Níveis N0–N5** | `40-operacao-rotinas/tarefas/README.md` §2–§3 (`nivel_minimo`, `escada`) | cada task declara o piso e até onde pode subir; o despachante tenta do mais barato para cima, nunca abaixo do piso | o modelo caro vira padrão e a janela acaba no trabalho mecânico |
| **Despachante** | `40-operacao-rotinas/ferramentas/despachar.py` (N0, sem LLM) | lê `tarefas/fila/`, ordena por prioridade e prazo, confere dependência, janela e orçamento, e lança um worker por task no nível mais barato permitido; passos e tempo por nível têm teto (a task sobrescreve com `max_turns:` e `timeout_min:`); estado é a pasta (`fila → executando → revisao · entregue · falhou · decisao`); trava em `tarefas/.lock`; três falhas seguidas param a rodada; `--dry-run` mostra tudo sem executar | task agendada roda no modelo que a sessão estiver usando, ou não roda |
| **Agendador** | o do sistema: Windows por `ferramentas/despachar-agendado.vbs` (sem janela); macOS por `ferramentas/macos/` | uma rodada do despachante a cada intervalo fixo, sem sessão aberta | a operação por tasks só anda quando há alguém na frente da tela |
| **Orçamento** | `40-operacao-rotinas/tokens/ORCAMENTO.json` + `tarefas/log/GASTO.jsonl` | teto semanal calibrado pelo `medir-tokens.py --calibrar` e a divisão operador · agendado · folga; o despachante soma o que o agendado já gastou e só lança a task cuja `estimativa_tokens` cabe; N0 e N1 não contam | o agendado come a janela de quem trabalha na sessão |
| **PAUSA** | arquivo `40-operacao-rotinas/tarefas/PAUSA` | com ele presente, o despachante não lança nada; apagar o arquivo devolve a operação | não há freio de emergência que não seja desligar a máquina |
| **Painel do despachante** | `40-operacao-rotinas/ferramentas/despachante_painel.py` | a fila, os níveis e o que o despachante faria agora, lidos do repo com as mesmas regras do `despachar.py`, para a tela do sistema | o estado do agendado só se vê abrindo pastas |
| **Varredor** | `.claude/agents/varredor.md` (modelo barato fixo no cabeçalho, só lê) | o subagente da sessão para varrer pastas, buscar, contar, ler transcrito, captura ou `.jsonl` e rodar conferências; devolve achado com caminho, linha e citação literal, e não decide nem edita | o modelo caro gasta a janela lendo o que um modelo barato leria |
| **Gate de delegação** | `40-operacao-rotinas/ferramentas/gate-delegacao.py`, hooks `UserPromptSubmit` e `PreToolUse` | na sessão do modelo caro, nega na 1ª chamada a leitura de captura, transcrito, `.jsonl` e a execução das ferramentas de captura e conferência, e nega a leitura mecânica genérica a partir da 6ª no mesmo turno (`GATE_DELEGACAO_LIMITE`); subagente, modelo barato, sessão na nuvem e `GATE_DELEGACAO=0` passam; cada bloqueio vai para `tokens/GATE-DELEGACAO.jsonl` | a regra de delegação existe no texto e não pega na hora |
| **Gate de contexto** | `40-operacao-rotinas/ferramentas/medir-contexto.py --teto <N>` | mede a carga fixa da sessão antes e depois de toda peça com hook, skill, MCP ou plugin | cada peça nova encarece todas as sessões em silêncio |

### 1-quater-bis. ⭐ "Manda o modelo mais forte decidir": o barato junta, o forte decide

Quando o {{OPERADOR}} manda o modelo mais forte (N5) decidir ou analisar algo, **a sessão não decide nem resume por ele:** (1) o `varredor` junta os insumos em caminhos e linhas, sem leitura própria; (2) a fonte primária que o modelo forte precisa ler ele mesmo (call, transcrito) vai **apontada, nunca resumida**; (3) abre-se a task N5 (`nivel_minimo: N5`) ou passa-se o dossiê à sessão dele; (4) a decisão volta como cartão (molde `40-operacao-rotinas/tarefas/modelos/cartao-decisao.md`) ou como regra, pelo modelo forte. A sessão que juntou não antecipa a decisão no fecho. *(Resumo feito pelo modelo do meio é exatamente o filtro que o operador quis tirar do caminho.)*

### 1-quinquies. 🔴 Quem paga o modelo: conversa com cliente = chave de API; assinatura = só o que o operador ordena

**Todo modelo que conversa com cliente** (um atendente, um agente no grupo da conta) roda pela **chave de API própria da operação**, com `claude -p --bare` ou equivalente, que só aceita a chave de API e nunca lê o login da assinatura. **Sem chave, não responde e não cai para a assinatura.** A **assinatura pessoal** do operador fica para o que ele ordena: as sessões dele e as tasks que nascem delas. E o prompt de quem conversa com cliente **não carrega o kernel**: leva só o prompt de atendimento e o contexto enxuto da conta, para o custo por conversa ficar baixo. *(Assinatura é de uso do titular; atender terceiros por ela mistura custo, cota e termos de uso.)*

## 2. Anatomia de contrato (o que todo executor recebe)

Toda tarefa delegada aponta, nesta ordem: (1) **arquivo-contrato** (plano/método específico, ex.: `PLANO-PAGINA-<conta>.md`), (2) **fontes canônicas** (DECISOES/OFERTA do projeto), (3) **skills a carregar** (máx. 3), (4) **saída esperada + gate**, (5) **o que é proibido decidir**. Prompt curto que aponta > prompt longo que explica. Se o executor precisa de mais de 5 arquivos, o contrato está mal feito: voltar ao Fable.

## 3. Regra de diretório (economia de contexto)

Padrão obrigatório em toda pasta de projeto:

1. **`CLAUDE.md` da pasta = mapa de carga**: tabela "tipo de tarefa → arquivos mínimos". Executor lê o CLAUDE.md e SÓ os arquivos da linha.
2. **`_arquivo/` em toda pasta**: o que é histórico sai da raiz. Raiz limpa = contexto barato. Nada em `_arquivo/` é fonte.
3. **Camada de decisão separada de camada de asset**: markdown leve (decisões, planos, logs) em pastas que os modelos leem; binários pesados (vídeo, pptx, node_modules, transcrição íntegra) em pastas marcadas **"não ler — abrir só se for o objeto da tarefa"**.
4. **Transcrições e fontes brutas nunca se releem**: minerar 1 vez → `SINTESE-*.md` assinada → executores leem só a síntese.
5. **Precedência declarada no topo de cada CLAUDE.md** (o que vence em conflito), para o executor não "resolver" divergência sozinho.

## 4. Ciclo de operação semanal

Fable (ou o modelo mais forte disponível): 30 min/semana — lê `STATUS.md` + logs de decisões dos projetos ativos → atualiza contratos → fila de tarefas com ferramenta dona. Executores: consomem a fila. Tudo que executor aprende (CPA real, criativo vencedor, bug) entra no log do projeto, nunca solto em chat.

## 5. Janela de tokens e ritmo diário (handoff)

Este protocolo diz **qual ferramenta** para cada tarefa. **Quando** rodar cada peso de tarefa e como racionar a janela de uso é orientação que cada operação ajusta ao seu plano e às suas contas: conhecer o limite de cada ferramenta (janela de tokens, recarga, cota semanal do executor externo) e **agendar o trabalho pesado para quando a janela está cheia**. Regra que amarra os dois: **task pesada → bloco de menor interrupção, com a janela cheia; executor externo de cota semanal (Codex) só em tarefa planejada, nunca improvisada.**

---
*Regra-mãe: processo antes de ferramenta; contrato antes de execução; log antes de memória. Se este protocolo conflitar com um método-raiz, o método vence.*
