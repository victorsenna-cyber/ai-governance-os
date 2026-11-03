# ÁRVORE — CONTA

> **Tipo:** trilho · **Instituído:** 26/09/2026 (onda 5 da auditoria de roteamento de 26/09/2026) · **Alçada:** {{OPERADOR}}
> **Carrega-se quando:** o pedido é sobre **abrir ou destravar a conta de um cliente** — conta nova, pilares, alçada fato × estrutura, repo de cliente, cliente nominal. **E sempre que a ESCRITA manda voltar para cá** porque a pré-condição dela não foi atendida.
> **Réguas transversais** (§8 REGRAS Nº 0, 1, 2 · procedência · ordem) **valem aqui e não se repetem.**

---

## 1. Pré-condição

🔴 **O estado da conta foi lido INTEIRO: `clientes/<cliente>/STATUS.md` + `clientes/<cliente>/execução Codex/` (antessala).** Pacote isolado é proposta, nunca estado — mas decidir sem ter lido a antessala é decidir sobre metade (o que muda a conta pode estar na antessala, não no estado). Se há pacote não promovido → **CASA primeiro** (rito de integração).

## 2. O processo desta árvore

| Tipo | O que se carrega |
|---|---|
| **framework** | `100-métodos/METODO-ESTIMATIVA-DE-CARGA.md` — **o gargalo de conta é latência, não produção** · `100-métodos/ARQUETIPOS-DE-MARCA.md` (a leitura do kit de marca) |
| **trilho** | 🔴 `100-métodos/METODO-TRILHO-DE-CONTA-NOVA.md` — quatro atos, dez etapas, **pedido único no dia 0** |
| **método** | `100-métodos/METODO-ARQUEOLOGIA-DE-ICP.md` · `100-métodos/METODO-DESTILACAO-DE-CALLS.md` · `100-métodos/METODO-KIT-DE-MARCA.md` |
| **blueprint** | `90-templates/conta-nova/` (`PAINEL.md`, `PEDIDO-UNICO.md`) · `90-templates/lexico-icp/` · `90-templates/repo-cliente/` · `90-templates/kit-de-marca/` |
| **política** | `100-métodos/METODO-ALCADA-DE-ESTRUTURA.md` (**REGRA Nº 0**: fato se pergunta, estrutura se decide) |
| **gate** | 🔴 `100-métodos/METODO-TESTE-DE-PILARES.md` — **P1 ou P4 reprovando bloqueia a ESCRITA** |

⭐ **Esta árvore é o que torna a pré-condição da ESCRITA verificável:** ela produz `clientes/<cliente>/PILARES.md` e `clientes/<cliente>/lexico-icp/`. Sem os dois, não há peça para cliente — **inclusive sob urgência.**

## 3. Linhas — sinal → carga → veto

| Sinais | Carga, na ordem do processo | 🔴 Veto |
|---|---|---|
| cliente novo, conta nova, "por onde eu começo", montar a estrutura do zero, ordem das etapas, conta travada sem saber em que etapa | `100-métodos/METODO-TRILHO-DE-CONTA-NOVA.md` *(trilho)* → `90-templates/conta-nova/` *(blueprint)* → opera em `clientes/<cliente>/PAINEL.md` | etapa com duas entradas · pendência sem "o que destrava" · pedido ao cliente contendo lacuna de ESTRUTURA |
| "a conta não anda e ninguém sabe por quê", pilares, **"faça os pilares"**, coerência, "para quem é mesmo?", divergência proposta × registro, depois de pivô, antes de página ou VSL | `100-métodos/METODO-TESTE-DE-PILARES.md` *(gate)* → `clientes/<cliente>/PILARES.md` → 🔴 **e na mesma entrega o kit de marca** (linha abaixo) | 🔴 **P1 ou P4 reprovando bloqueia produção de copy** — o mecanismo que custou uma conta, com roteiros aprovados no gate de forma e ICP que nunca rodou · **pilares entregues sem kit de marca** |
| **kit de marca**, "mídia kit", arquétipo da cliente, identidade visual da conta, cores e fontes da cliente, "como a marca dela aparece", conta sem kit antes do primeiro criativo visual *(instituído 18/10/2026)* | `100-métodos/ARQUETIPOS-DE-MARCA.md` *(framework)* → `100-métodos/METODO-KIT-DE-MARCA.md` *(método — 🟡 provisório)* → `90-templates/kit-de-marca/` *(blueprint + `gerar_kit.py`)* → `100-métodos/METODO-PRANCHA-DE-ESCOLHA.md` (a escolha) → `clientes/<cliente>/<pasta de design>/branding/` | dominante sem três falas literais da expert · arquétipo do público ou do nicho lido como o dela · cor ou fonte sem porquê no arquétipo · tokens definitivos sem escolha literal no `DECISOES.md` |
| "pergunto ou decido?", cliente escolhendo entre versões, cliente pedindo mudança de copy, "o que você prefere?", brief com campo vazio, elicitação | `100-métodos/METODO-ALCADA-DE-ESTRUTURA.md` *(política — REGRA Nº 0)* | estrutura devolvida como pergunta · **objeção de congruência sem resposta escrita** (alterar do nosso jeito ou explicar por que não) · propriedade do ativo tratada como autoria da estrutura |
| repo para o cliente, cérebro da operação, kernel para a equipe dele, entregar mais que documento | `100-métodos/METODO-DIRECT-RESPONSE.md` §4.2 → `90-templates/repo-cliente/` *(blueprint; §3-bis: o repo vivo, onde mora e como sincroniza)* + `30-comercial/oferta.md` §7-bis · repo já entregue: `clientes/<Cliente>/entregaveis/repositorios.json` + `CLAUDE.md` §11.6 | framework ou método nosso no repo dele · sem as 3 condições (agente que carrega, dono nomeado, primeira peça conosco) · **repo como concessão em negociação parada por preço** |
| cliente nominal, projeto de cliente, voz, produto, página, campanha ou entrega específica | `clientes/<cliente>/AGENTS.md` (se existir) + `clientes/<cliente>/CLAUDE.md` + fontes do kernel dele · **lista viva de contas: a pasta `clientes/` e o `STATUS.md`** | usar cópia homônima fora de `clientes/` como fonte |
| 🔴 **qualquer tarefa que altera o `STATUS.md` de uma conta** — registro de conversa, decisão, pagamento, entrega, mudança de fase *(instituído 28/10/2026, painel de projetos)* | no mesmo ato, o frontmatter de `clientes/<Conta>/PAINEL.md`: `atualizado:`, `fase`, `proximo_marco`, `marco_prazo`, `marco_dono`, `marcos:` (só os abertos, até 6, inline) e `contrato`/`recebido` quando mudam · esquema no `980-web-design/painel-projetos/README.md` · conferir com `python3 40-operacao-rotinas/ferramentas/painel-projetos.py --verificar` | 🔴 **`STATUS.md` alterado sem o frontmatter do `PAINEL.md`** (o painel mostra *"STATUS mais novo que o painel há N dias"* e a conta fica amarela) · marco fechado que continua em `marcos:` · saúde ou cor escrita no frontmatter · `PAINEL.md` novo sem frontmatter |

| 🔴 **fato novo em captura do OpenWA ou em transcrito de sessão** — mensagem do cliente, decisão do {{OPERADOR}} no chat, mudança de canal, pagamento, bloqueio de plataforma *(instituído 30/10/2026, alçada {{OPERADOR}})* | ler a captura dos últimos 7 dias da conta **antes** de qualquer análise ou peça; propagar o fato, no mesmo ato, para **todo** arquivo que ele muda: `DECISOES.md` (adendo ⟲ com data e fala literal), `STATUS.md` §1 e §5, `PAINEL.md`, e, em mídia, `PLANO-DE-MIDIA.md` + `estrutura-campanhas.md` + `BRIEFING.md` + `LOG-DECISOES.md` | fato de captura registrado só no arquivo do pedido · plano de mídia de canal que não é o que roda · `STATUS.md` §1 contradizendo o §5 · análise diária carregando plano de outro canal |

## 4. Desempate interno

- **"O estado da conta parece velho"** → CASA primeiro (antessala do Codex), depois esta árvore.
- **Montar o `lexico-icp/`** → o método é da LEITURA (arqueologia); a obrigação de tê-lo antes da peça é desta árvore.
- **Precedência dentro da conta:** política da Governança → `DECISOES.md` do cliente → método → artefato (`CLAUDE.md` §6.2).

---
*Linhas migradas do roteador v1 (R02, R20, R21, R37, R49).*
