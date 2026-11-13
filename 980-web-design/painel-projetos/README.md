# painel-projetos — Projetos · {{EMPRESA}}

> Alçada: {{OPERADOR}}. Painel para ver os projetos e o andamento deles no dia a dia: prazos, o que resta entregar, o que precisa de decisão. Mesma base do dashboard e do sistema financeiro.
> 🟡 **Provisório** até a 1ª semana de uso com os frontmatters de cada conta mantidos pela regra da `ARVORE-CONTA.md`.

## Como o dado anda

```
clientes/<Conta>/PAINEL.md (frontmatter) · STATUS.md (datas) · 01 - contexto/OpenWA/ (datas nos nomes)
40-operacao-rotinas/tarefas/*/T-*.md · tarefas/DECISOES-PENDENTES.md · 45-financeiro/LANCAMENTOS-EMPRESA.md
   └→ push na main (sincronizar.py, ao abrir e fechar toda sessão)
       └→ GitHub Action projetos-painel → ferramentas/painel-projetos.py --publicar
            └→ Supabase <projeto-supabase>, tabela projetos_estado (um documento JSON; mesmo token e leitores do financeiro)
                 └→ https://financeiro.{{DOMINIO}}/projetos/  (estático, mesmo login do Caixa)
```

- **Fonte única é o `.md`.** O Supabase é cópia reescrita a cada push. **Nunca se edita dado no Supabase nem no site.**
- **Leitor:** `40-operacao-rotinas/ferramentas/painel-projetos.py` (regras de leitura e de saúde no cabeçalho dele). `--json` dá o estado a qualquer sessão em uma chamada N0; `--verificar` é o gate (sai 1 se algum painel está inválido ou defasado > 3 dias do STATUS).
- **Ponte:** `.github/workflows/projetos-painel.yml` — a cada push na `main` que mexa em `PAINEL.md`, `STATUS.md`, OpenWA, tasks, cartões ou *A receber*; e uma vez por noite, logo após a meia-noite no seu fuso (os contadores de dias andam sem push).
- **Banco:** `supabase/006-projetos.sql` — tabela `projetos_estado`, função `sincronizar_projetos(token, payload)` (mesmo hash do `FINANCAS_SYNC_TOKEN`), RLS pela mesma `financas_privado.leitores`.
- **Site:** `index.html` (página própria, sem artefato: CSS e JS inline, só o supabase-js de fora) + `config.js` (chave publicável, igual ao financeiro) + `.htaccess`. Mora em `/projetos/` do domínio do Caixa de propósito: **mesma origem, mesma sessão** — quem já entrou no financeiro entra aqui sem senha. `publicar.py` sobe os arquivos pela API da Hostinger (token em `~/.continuum/hostinger-token.txt`); `publicar.py --conferir` compara byte a byte.

## As três áreas

A barra lateral tem grupos por intenção e as telas desta página moram em `#operacao`, `#hoje`, `#decisoes`, `#mensagens`, `#prazos`, `#agenda`, `#projetos`, `#onboarding`, `#entregaveis`, `#comercial`, `#despachante`. O domínio abre na **Operação**.

- **Operação:** aviso único (saudável · atenção · crítica) com o motivo e o ato · caixa estimado e quantos meses de saída ele cobre (do Caixa, `painel_dados`) · a receber vencido · receita **recorrente** contratada × recebida no mês e **projeto** recebido no mês (contrato pago à vista é projeto) · pipeline ponderado · em onboarding · saúde média · TTFV · ativação · alertas críticos e de atenção · funil e onboarding em resumo.
- **Comercial:** funil das fichas `30-comercial/assessoria-prospects/<pasta>/PAINEL.md` e das contas em proposta (molde `90-templates/prospect/`), "o que fazer agora", previsão ponderada por mês, fichas com a checklist de Embarque e os botões **Mover** e **Registrar aceite** (alvo `prospect` em `painel_acoes`, `supabase/010-comercial.sql`; a VPS aplica e abre a task "Abrir a conta"). Leitor: `40-operacao-rotinas/ferramentas/comercial_regras.py`.
- **Projetos:** as cinco abas de sempre; o Hoje ganhou o bloco Comercial e o cartão da conta mostra a saúde do onboarding.

## O que o painel mostra

| Aba | Conteúdo |
|---|---|
| **Hoje** | vencidos · próximos 7 dias (marcos, tasks com prazo, decisões com prazo, *A receber*) · decisões abertas · contas sem toque há mais de 7 dias · *A receber* em aberto · marcos sem data · painéis a corrigir |
| **Projetos** | um cartão por conta: saúde · fase · projeto · próximo marco com prazo e dono · motivos da cor · risco · marcos abertos · tasks da operação · decisões · contrato, recebido, a receber · último registro, último WhatsApp, data do painel · caminhos dos arquivos (clique copia) |
| **Decisões** | os cartões abertos de `DECISOES-PENDENTES.md`: contexto, A/B/C, recomendação, autonomia, prazo. **A letra é um botão** (aqui e na lista de *Hoje*), com campo de ajuste opcional: o clique grava em `decisoes_escolhas` no Supabase, e até a VPS levar dá para trocar ou desfazer (seção *Decisões pelo clique*) |
| **Prazos** | linha do tempo por dia: vencidos dos últimos 60 dias e os próximos 45, com os quatro tipos de prazo etiquetados |
| **Onboarding** | o `100-métodos/METODO-ONBOARDING-ORQUESTRADO.md` em tela: em onboarding, em embarque, TTFV mediano, % com primeiro valor, alertas, revisões em 14 dias · **O que fazer agora** (cada alerta com o porquê, a página do livro e o ato mínimo) · **Jornada** em Kanban pelas seis etapas · **Por conta**: a régua do D0 à revisão, a saúde 0–100 com os critérios abertos, a fala do primeiro valor, o que o cliente deve. Calculado no repo por `40-operacao-rotinas/ferramentas/onboarding_regras.py` a partir dos campos `onb_*` do `PAINEL.md`; a página só desenha |

Filtro **Ativas · Todas · uma conta** no topo (nas telas de fila e de conta; some na Operação e no Comercial). Não há teclas numéricas: o teclado navega por Tab e pela busca (**Ctrl+K**, ⌘K, ou **/**). Conta `pausada`, `encerrada` ou `arquivada` só aparece em *Todas*.

## Decisões pelo clique

O operador clica na letra da decisão em vez de voltar à sessão com o id e mandar a letra.

```
clique na letra → rpc escolher_decisao (só leitor de financas_privado.leitores) → public.decisoes_escolhas
  → VPS, contexto.service, a cada 2 min: 40-operacao-rotinas/ferramentas/decisoes-do-painel.py
       → decisoes_pendentes(token) → propagar-decisoes.py (cartão para "Decididas", DECISOES.md da conta, autonomia.py)
       → sincronizar.py (commit "decisões do painel: <ids>" e publicação na main) → decisoes_marcar(token, ids, commit)
  → Action projetos-painel republica o estado (o cartão sai de Decisões) · o PC recebe na próxima sincronia
```

- **Banco:** `supabase/007-decisoes.sql` (tabela, quatro funções, coluna `decisoes_token_sha256` em `financas_privado.config`). O token da ponte não é o do Action: está em `~/.continuum/decisoes-token.txt` (PC) e em `DECISOES_TOKEN` no `/srv/ordens/.env` (VPS).
- **Trocar a letra** vale até a VPS carimbar `propagado_em`; depois disso, mudar é decisão nova, na sessão.
- **Botão enviar.** O campo opcional é uma caixa de texto com **enviar** (ou Ctrl+Enter): com letra já escolhida, reenvia a letra com o texto; **sem letra, grava `escolha = 'LIVRE'`**, a resposta livre, e o `propagar-decisoes.py` a leva como *"resposta livre do operador (sem letra)"*. A resposta livre pede o `supabase/009-resposta-livre.sql`; sem ele, o sistema avisa e a letra + texto segue funcionando.
- **Registro:** `40-operacao-rotinas/tarefas/log/DECISOES-DO-PAINEL.md`, uma linha por escolha propagada.
- **Rótulo × pasta:** o cartão diz o nome da conta; o `propagar-decisoes.py` resolve para a pasta da conta (pasta igual, apelido, `conta:` do `PAINEL.md`, primeiro nome) e **nunca cria pasta**; sem pasta, vai para `DECISOES-CASA.md` com aviso.
- **Cartão visto:** `supabase/015-decisoes-vistas.sql` registra quando o cartão entrou na área visível e quando o lastro abriu, para separar "não viu" de "viu e não decidiu". A tela funciona igual sem esta tabela.

## Resolver o que venceu

Projeto vencido que já não faz sentido precisa de uma saída: descartar, ou acrescentar uma nota.

- **Onde:** botão **resolver** em todo marco e task das listas de *Hoje* (vencido, próximos 7 dias, sem data) e dos cartões de *Projetos* (próximo marco, marcos, tasks); botão **conta** no cabeçalho do cartão.
- **O quê:** **Feito · Descartar · Nova data** (marco e task) ou **Mudar fase** (conta: `pausada`, `encerrada`, `arquivada` saem de *Ativas*), com nota opcional; ou **Só a nota**. A ação nova sobre o mesmo alvo substitui a que ainda não foi; até a VPS aplicar, dá para desfazer.
- **Caminho:** `registrar_acao` → `public.painel_acoes` (`supabase/008-acoes.sql`, mesmo token da ponte) → `decisoes-do-painel.py` na VPS → **`40-operacao-rotinas/ferramentas/acoes_do_painel.py`** aplica: linha de `marcos:` sai ou muda de prazo no frontmatter do `PAINEL.md` (o próximo marco passa ao aberto mais perto), task vai para `tarefas/entregue/` com `estado: entregue|descartada`, `fase:` muda, `atualizado:` de hoje · a nota entra **literal** no `STATUS.md` da conta, seção *Registro do sistema*, com a fonte e a data · linha em `tarefas/log/ACOES-DO-SISTEMA.md` → publicação na `main` → carimbo. Alvo que não se acha volta como erro (🔴 no sistema, com o motivo) e não é tentado de novo.

## Mensagens pelo clique

A aba **Mensagens** espelha a fila do mensageiro (`public.mensagens_fila`, `supabase/011-mensagens.sql`): o que espera ✅ aparece ali, o clique grava em `mensagens_escolhas`, e a VPS lê o pendente, aplica o campo (literal ou ajuste), aprova na fila e carimba. O envio sai no ritmo da fila do mensageiro (janela, tetos, intervalo). **Descartar** pede um segundo clique antes de gravar. A fila mora no mensageiro; aqui é espelho para o clique.

## Enviar o entregável pelo WhatsApp

- **Onde:** botão **WhatsApp** de cada versão da mensagem no cartão da aba *Entregáveis* (Prontos). Abre um popup: **Para** (as conversas da conta no mapa da Evolution, com a privada do destinatário marcada; ou outro número), **sai pelo número** (automação para clientes e parceiros, pessoal para prospect), **o texto que vai** (editável), o **anexo** (o PDF da pasta; sem PDF vai só o texto) e **Cancelar · Confirmar envio**. O clique confirmado é o ✅ do operador sobre aquele texto e é ordem de envio: fura a janela horária, nunca os tetos nem o intervalo.
- **Caminho:** `pedir_envio_entregavel` → `public.entregaveis_envios` (`supabase/012-envio-entregavel.sql`, mesmo token da ponte) → `decisoes-do-painel.py` na VPS → **`40-operacao-rotinas/ferramentas/entregaveis_do_painel.py`**: confere a task em `revisao/` com `estado: pronto`, lê o PDF do clone (só sob `<conta>/entregaveis/`, até 15 MB), resolve o `@lid` pelo mapa da Evolution, põe na fila do mensageiro já aprovado pelo painel e chama `/agora` → o mensageiro manda pelo `sendMedia` da Evolution (texto como legenda; acima de 1.000 caracteres, o texto vai antes e o PDF depois) → quando sai, a task vai para `entregue/` com `enviado_por: painel` (o mesmo caminho do botão **Enviado**) e o cartão mostra ✅. Falha volta com o erro no cartão. Até a VPS pegar (~2 min), dá para desfazer.
- **Payload:** `entregaveis.py` põe em cada pronto `destinos` (jid, nome, tipo), `destino_padrao` e `anexo`; o Action lê `evolution/mapa.json`.

## Entregáveis: progresso e rascunhos

- **Por conta:** chips no topo da aba (ou o seletor de conta). Com conta escolhida, aparece o resumo (andamento %, em produção, prontos, enviados, atrasados) e o formulário **Novo entregável**.
- **Progresso:** barra de cinco etapas por cartão, Prometido · Produzindo · Com você · Pronto · Enviado, lida da pasta-estado da task (`entregaveis.py`, `_etapa`); vermelho quando passou do prazo prometido.
- **Rascunhos:** em cada cartão, "Rascunhos · adicionar". Grava em `public.entregaveis_rascunhos` (**`supabase/013-rascunhos.sql`, rodar uma vez no SQL Editor**); a VPS, na passada do `decisoes-do-painel.py`, chama `40-operacao-rotinas/ferramentas/rascunhos_do_painel.py`, que põe o texto literal no `RASCUNHOS.md` da pasta do entregável e na linha `insumos:` da task. **Peça pronta que recebe rascunho volta para `fila/`** e a esteira da nuvem a refaz; enviada só registra. Sem task, o rascunho abre um entregável novo pelo `entregaveis.py`. Rascunho não substitui o anterior; desfaz-se enquanto não foi ao repo. Testes: `rascunhos_do_painel.py --testar`.

## Sistema: barra lateral, tema e direção Grafite

A casca é a mesma do Caixa, montada pelo `sistema.js` (`aside.sis[data-sis-nav][data-sis-pagina="projetos"]`): grupos **Visão** (Operação) · **Agir** (Hoje, Decisões, Mensagens, Prazos, Agenda) · **Contas** (Projetos, Onboarding, Entregáveis, Comercial) · **Automação** (Despachante) · **Caixa** (as seis do Caixa). Tokens e casca moram em `../painel-financeiro/sistema.css` e `sistema.js`, publicados na raiz pelo `publicar.py` do Caixa e lidos aqui por `../sistema.*`. **Publicar o Caixa antes do Projetos.** O tema claro/escuro fica no aparelho.

A direção **Grafite** é **troca de pele e de composição, nunca de dado:** login, RLS, RPCs, Supabase e `painel-projetos.py` não mudam, e os cliques que gravam (letra, resposta livre, desfazer, resolver com feito, nova data e fase, mensagem enviar e descartar, mover etapa, registrar aceite, envio pelo WhatsApp, Enviado, rascunho, novo entregável) têm os mesmos nomes e argumentos de RPC que antes.

- **Topo:** trilha, busca, filtros, marcação "gerado DD/MM HH:MM" (âmbar se o payload tem mais de 1 dia), tema e menu da conta (trocar senha, sair). No celular: gaveta e fita de pílulas do grupo. Fontes Instrument Sans (palavra) e Space Grotesk (número); nenhuma serifa, nenhum azul.
- **Operação:** aviso (crítica · atenção · saudável, até três motivos, o ato e o **único botão primário** da tela) · herói **Receita recorrente contratada** · fontes de receita, um cartão por conta · cartões de caixa, a receber vencido, pipeline, onboarding, saúde média, TTFV, ativação e prazos em 6 semanas (mapa de calor; o dia clicado abre Prazos nele) · funil e onboarding em barras, **acesa a etapa que tem alerta vermelho** · alertas críticos · atenção (recolhida) · escuta.
- **Comercial:** herói pipeline ponderado · "o que fazer agora" (vermelhos primeiro) · previsão em barras por mês ("n pequeno: leitura, não promessa") · funil em kanban · fichas com Mover etapa e Registrar aceite. A taxa de ganho não vai para a tela (n pequeno).
- **Hoje, Projetos, Decisões, Mensagens, Prazos, Onboarding, Entregáveis:** cartões na pele nova; em Decisões a opção escolhida ganha o véu âmbar e ✓, e **Enviar** é o primário do cartão; Prazos tem mapa de calor de 14 dias atrás a 41 à frente; Onboarding mostra a régua do método como passos ligados e os seis critérios de saúde em medidores; Entregáveis tem o único cartão tracejado do sistema, "Novo entregável", e o botão **WhatsApp** abre um `<dialog>` (Esc fecha; no celular, folha de baixo).
- **Busca:** **Ctrl+K**, ⌘K, **/** ou a pílula do topo: as telas, as contas (abre Projetos filtrado), as decisões, as fichas do Comercial e as contrapartes do Caixa (abre Lançamentos filtrado). `?conta=`, `?dec=` e `?ficha=` na URL abrem a tela já no item.
- **Contadores da barra lateral:** os mesmos nas duas páginas, pelas mesmas funções do `sistema.js`: Decisões, Mensagens (âmbar, esperando ✅), Projetos, Onboarding (vermelho, alertas), Entregáveis (prontos) e A pagar (vermelho, vencidas, do `painel_dados`). Leitura que falha some com o contador. O aviso do pé é o estado da Operação, **o mais grave primeiro**.

## Despachante

Item próprio na barra lateral, grupo **Automação**, em `#despachante`; contador vermelho = tasks que falharam.

- **Dado:** `payload.despachante`, montado por **`40-operacao-rotinas/ferramentas/despachante_painel.py`**, que o `painel-projetos.py` importa. As regras não se repetem: a ordem, os motivos de bloqueio, a escada, o orçamento e o gasto da semana vêm do próprio `despachar.py`. O módulo só traduz o motivo para português ("espera T-… ficar pronta", "agendada para …", "aguardando sua decisão"). O Action lê também `tokens/ORCAMENTO.json` (sparse-checkout).
- **Tela:** aviso (ligado · pausado · sem rodada recente há mais de 6 h) · estado, última rodada, **próxima rodada prevista**, % da parte agendada da semana, prontas para rodar, aguardando decisão · **Na fila, prontas** na ordem do despachante · Aguardando decisão · Falhou · Na fila, paradas (com o motivo) · Em revisão e Entregues nos últimos 7 dias (recolhidas) · **Orçamento da semana** por origem · **Últimas rodadas** (de `log/RODADA-*.md`, com tokens e duração casados no `GASTO.jsonl`) · **Da rotina na nuvem** (tasks `tipo: entregavel`, recolhida, separada).
- **Limite:** a tela mostra o estado do último push. A rodada que não executou nada só chega aqui na sincronia seguinte; o despachante local não roda com o computador desligado.

## Agenda

Item **Agenda** no grupo **Agir** da barra lateral, em `#agenda`: o Google Calendar do operador, para criar, editar e excluir eventos pela tela e pelo repo.

```
tela Agenda (sessão Supabase do leitor) ─┐
agenda.py do repo (token da ponte) ──────┼→ Edge Function agenda ─→ Google Calendar API, primary de {{EMAIL}}
sessão do Claude (MCP Google Calendar) ──┼───────────────────────→ (o mesmo calendário, direto)
Action agenda-pdfs (FINANCAS_SYNC_TOKEN) ┘→ bucket privado calls-pdf ← a tela abre o PDF por URL assinada de 10 min
```

- **Tela:** a semana em kanban, segunda a domingo, navegável (← Hoje →); hoje com a borda âmbar; no celular, uma coluna por tela com rolagem lateral. **Arrastar o cartão para outro dia** muda a data e mantém hora e duração (mouse: arrasta; celular: toque longo e arrasta); a mudança aparece na hora e volta atrás se o Google recusar. Clique (ou Enter) abre a edição; **+ evento** e **Novo evento** criam. Modal: título, dia, início e fim, dia todo, gerar link do Meet, descrição, local ou link, convidados, e "mandar convite ou aviso por e-mail" (desmarcado por padrão: convite é mensagem a terceiro). **Excluir** pede a confirmação dentro do modal. No cartão: o link da call (Meet do próprio evento, ou Zoom, Meet ou Teams achado no local ou na descrição) e **PDF** quando há folha.
- **PDF da call:** a função casa a folha com o evento por, nesta ordem, o caminho ou o nome do arquivo escrito na descrição, a pasta `00 - roteiros calls/<AAAA-MM-DD - …>` escrita na descrição, ou a data do evento + o primeiro nome da conta no título. O PDF fica no bucket **privado** `calls-pdf` (chave `p/<sha1 do caminho>.pdf`, sem política: só a função lê) e abre por URL assinada de 10 min. Quem sobe: `.github/workflows/agenda-pdfs.yml` → `40-operacao-rotinas/ferramentas/agenda_pdfs.py`, a cada push em `clientes/*/00 - roteiros calls/**` ou `parceiros/*/00 - roteiros calls/**` (só o que mudou, pelo sha256; o que saiu do repo sai do bucket).
- **Função:** `supabase/functions/agenda/index.ts` (ações `estado`, `listar`, `criar`, `editar`, `mover`, `excluir`, `pdf_url`, `conectar`, `oauth_trocar`, `pdf_indice`, `pdf_subir`). Quem entra: sessão de e-mail em `financas_privado.leitores` (a tela), o token da ponte (`agenda.py`) ou o `FINANCAS_SYNC_TOKEN` (só as ações de PDF). Se o projeto assina as sessões com ES256, o "Verify JWT" do gateway rejeita a sessão: a página manda a chave publicável em `apikey` e `Authorization` e a sessão em `x-sessao`, que a função confere (`auth.getUser` + `financas_pode_ler`). Teste local, sem rede: `node supabase/functions/agenda/testar.mjs` (Google, Supabase e Storage falsos).
- **Banco:** `supabase/014-agenda.sql`: `financas_privado.agenda_google` (cliente OAuth e refresh token; esquema não exposto, lido só pela função com a chave de serviço), o *state* do OAuth (15 min, uso único) e o bucket `calls-pdf`.
- **Google:** cliente OAuth num projeto Google Cloud do operador, Calendar API ligada, escopo `calendar.events`, redirecionamento para `https://financeiro.{{DOMINIO}}/projetos/` (a página recebe `?code=&state=` e chama `oauth_trocar`). Enquanto não está conectado, a tela mostra o cartão **Conectar a agenda do Google** com os passos e os campos do cliente.
- **Pelo repo:** `40-operacao-rotinas/ferramentas/agenda.py` (`estado`, `listar`, `criar --com-meet`, `editar`, `mover <id> --dia`, `excluir <id> --sim`, `pdf "<caminho>"`). Qual caminho usar, quando: `00-core/roteador/ARVORE-OPERACAO.md`.

## A camada de máquina da conta (frontmatter do `PAINEL.md`)

```yaml
---
conta: Conta A
fase: construir            # prospecto · proposta · fundar · construir · operar · pausada · encerrada · arquivada
projeto: <projeto principal> (principal) · <projeto secundário> (secundário)
proximo_marco: <o próximo marco, em uma frase>
marco_prazo: AAAA-MM-DD
marco_dono: {{OPERADOR}}
contrato: 0                # valor contratado, em reais
recebido: 0                # valor já recebido, em reais
risco: <o risco aberto da conta, em uma frase>
atualizado: AAAA-MM-DD
marcos:
  - { o_que: <marco 1>, prazo: AAAA-MM-DD, dono: {{OPERADOR}}, duro: nao }
  - { o_que: <marco 2>, prazo: AAAA-MM-DD, dono: {{OPERADOR}}, duro: sim }
---
```

- Só `chave: valor` e a lista `marcos:` com itens inline `{ }` (sem vírgula dentro de `o_que`). Sem PyYAML de propósito.
- 🔴 **Regra de manutenção (`ARVORE-CONTA.md`):** toda tarefa que mexe no `STATUS.md` de uma conta atualiza `atualizado:`, `proximo_marco`, `marco_prazo` e `marcos:` no mesmo ato. O painel cobra quando falta (*"STATUS mais novo que o painel há N dias"*).
- **Saúde é calculada** (cabeçalho do script): 🔴 prazo vencido, a receber vencido, decisão vencida, sem toque > 14 dias em `construir`/`operar`, frontmatter inválido · 🟡 prazo em até 7 dias, sem toque > 7, defasagem > 3 dias, contrato vazio além de `proposta` · 🟢 o resto. Ninguém escreve a cor.
- Para criar os frontmatters das contas existentes, um subagente lê o `STATUS.md` §5 e o `DECISOES.md` de cada conta e propõe o bloco; as dúvidas de cada um vão para o `STATUS.md` da casa e são do {{OPERADOR}}.

## Uma vez só

- **Supabase:** rodar `supabase/006-projetos.sql` no SQL Editor do projeto `<projeto-supabase>` (depois do `001` do financeiro), e os demais em ordem conforme o que for usar: `007` decisões, `008` ações, `009` resposta livre, `010` comercial, `011` mensagens, `012` envio do entregável, `013` rascunhos, `014` agenda, `015` cartão visto. Sem o `006` o Action fica vermelho (`sincronizar_projetos` não existe); sem o `012`, o botão WhatsApp abre o popup com o aviso e não envia.
- **Supabase, Redirect URLs:** `https://financeiro.{{DOMINIO}}/projetos/` para o link por e-mail voltar aqui. Sem isso o link cai na raiz do Caixa, já logado, e `/projetos/` abre sem senha na mesma sessão.
- **GitHub:** nada. O secret `FINANCAS_SYNC_TOKEN` já existe e é o mesmo.
- **Agenda:** conectar o Google pelo cartão da própria tela Agenda.

## Rotina

- Task N0 diária `painel-projetos-verificar` (antes do `brief-diario`): `painel-projetos.py --verificar --json 40-operacao-rotinas/rotinas/PAINEL-PROJETOS.json`. O brief lê esse JSON em vez de todas as entradas do `STATUS.md`.
- Mudou `index.html`, `config.js` ou `.htaccess`: `python3 publicar.py` e depois `python3 publicar.py --conferir`.
