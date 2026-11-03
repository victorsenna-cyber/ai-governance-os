# painel-financeiro — Caixa · {{EMPRESA}}

> Alçada: {{OPERADOR}}. Painel de finanças pessoais e da empresa (dashboard, DRE, fluxo de caixa, contas a pagar e a receber), sincronizado com os dados do repo no GitHub e publicável na Hostinger.
> 🟡 **Provisório** até a 1ª semana com a rotina `financas-gmail` lançando e o painel conferido contra o app do {{BANCO}}.

## Como o dado anda

```
e-mail {{BANCO}} → rotina financas-gmail (modelo barato) ─┐
conversa (WhatsApp, call) → sessão: compromisso, dívida,├→ .md no repo → push na main (sincronizar.py)
  crédito a receber, pagamento confirmado ───────────────┘
  → GitHub Action financas-painel → Supabase (<projeto-supabase>, tabelas financas_*) → este site, em tempo real
```

- **Fonte única continua sendo o `.md`:** `940-operador/FINANCAS.md` (finanças pessoais do operador) e `45-financeiro/LANCAMENTOS-EMPRESA.md`. O Supabase é cópia de leitura, reescrita inteira a cada sincronização. **Nunca se edita dado no Supabase.**
- **Leitor:** `40-operacao-rotinas/ferramentas/financas-painel.py` (regras de leitura no cabeçalho dele).
- **Ponte:** `.github/workflows/financas-painel.yml` — a cada push na `main` que mexa nas finanças, e uma vez por noite, logo após a meia-noite no seu fuso (as diárias projetadas andam um dia).
- **Escrita no banco:** só pela função `sincronizar_financas(token, payload)`, que confere o hash do token guardado em `financas_privado.config`.
- **Leitura:** só usuário autenticado cujo e-mail está em `financas_privado.leitores` (inicialmente, só o {{OPERADOR}}).

## O que o painel mostra

| Aba | Conteúdo |
|---|---|
| Visão | caixa estimado (conferido + o que foi registrado depois), vencido, a pagar em 30 dias, a receber, saída do mês, projeção de 30 dias, agenda, saídas por categoria, o que conferir |
| DRE | por mês, regime de caixa: receita bruta, custos por categoria, resultado, margem — empresa (ou pessoal, no seletor) |
| Fluxo de caixa | saldo dia a dia, registrado e projetado (conservador: paga o vencido, não conta o atrasado a receber) e a tabela por semana |
| A pagar · A receber | contas abertas, com situação, prazo real e certeza |
| Lançamentos | extrato com busca |

Seletor **Tudo · Pessoal · Empresa** no topo; **⌘K** abre a paleta; **1 a 6** trocam de aba.

## O site é o artefato

O painel nasceu como um artefato do tipo Dashboard no claude.ai (**Finanças {{EMPRESA}}**) e o site publica **exatamente o código do artefato**, não uma reescrita: marcação, CSS, scripts e consultas iguais. O que muda é só a casca em volta.

| Arquivo | O que é |
|---|---|
| `artefato/index.html` | a página do artefato, **byte a byte**. Não se edita aqui sem editar lá |
| `artefato/datasets/*.sql` | as oito consultas do artefato, sem alteração |
| `casca.html` | a página do site em volta: entrada, `#dash-root` e o botão sair |
| `runtime.js` · `runtime.css` | o que o claude.ai dá ao artefato e fora dele não existe: o objeto `dash` (dados, filtro Tudo/Pessoal/Empresa, aba no endereço), as cores e medidas do tema escuro do tipo Dashboard, o esqueleto de carregamento, a entrada: **e-mail e senha**; o link por e-mail é só para o primeiro acesso ou senha esquecida, e quem entra por ele sem senha criada cai na tela de criar senha (marca `senha_definida` no `user_metadata`); `shouldCreateUser: false`, ninguém se cadastra pela tela; *trocar senha* no rodapé |
| `montar.py` | gera `index.html` (casca + artefato) e `supabase/004-painel-dados.sql` (as oito consultas numa função `public.painel_dados()`, `security invoker`: o RLS das tabelas decide quem lê; `anon` não executa) |

**O que não vem igual, e por quê:** as fontes *Anthropic Sans* e *Anthropic Serif* são da Anthropic e não podem ser hospedadas; o site usa a mesma pilha do tipo, com *Source Serif 4* no lugar da serifa e a fonte do sistema no lugar da sans. O resto é o código do artefato.

**Regra de design:** o painel não leva headlines grandes (`h2.cx-title`) nas abas; só o rótulo pequeno de cada aba. Mesma regra no artefato e no site.

**Artefato mudou?** Copiar de novo `files/index.html` e os `datasets/*` para `artefato/`, `python3 montar.py`, aplicar o SQL no Supabase, publicar.

## Extrato, cartão e mês

Tudo entra no sistema, inclusive o detalhamento dos gastos.

- **Fontes do leitor:** os `.csv` de `45-financeiro/extratos/` (cada movimento da conta {{BANCO}}, classificado por `extratos/CLASSIFICACAO.md`) e, se houver, as compras pessoais no cartão compartilhado de terceiro (`940-operador/cartao-compartilhado/CARTAO-COMPARTILHADO.md`). Movimento do extrato igual (dia, sentido, valor) a uma linha dos `.md` sai: vale a do `.md`.
- **Campo `meio`** em `financas_lancamentos` (`supabase/005-meio.sql`): `conta` ou `cartão de terceiro`. Caixa, projeção e semanas só somam `conta`; DRE e categorias somam tudo. Vale em `kpis`, `projecao`, `resumo_projecao`, `semanas` e `lancamentos` (coluna nova), no site e no artefato.
- **Seletor de mês** no topo, guardado por aba: Lançamentos abre no mês corrente, as outras em *Todos os meses*. Visão: *Para onde foi* e a agenda · DRE: a linha do mês e as categorias dele · Fluxo: as semanas que tocam o mês · A pagar/A receber: o vencimento. Com um mês escolhido, as categorias saem somadas dos lançamentos daquele mês; em *Todos os meses*, da consulta `categorias`.
- **Divisão por mês** (linha com o total do mês) em Lançamentos, A pagar e A receber.
- Limite conhecido: uma despesa recorrente que chega agrupada, com o vencimento da 1ª parcela, não aparece num mês futuro.

## Publicar na Hostinger

São cinco arquivos estáticos (`index.html`, `runtime.css`, `runtime.js`, `config.js`, `.htaccess`), na raiz do zip, sem pasta dentro. `.hostinger/site.json` guarda o destino: `financeiro.{{DOMINIO}}` (estático, conta `{{HOSTINGER_CONTA}}`). Se um WordPress ocupar o subdomínio, só o substitua com autorização do {{OPERADOR}}.

**Uma vez só, no Supabase** (Authentication → URL Configuration): pôr a URL do site em *Site URL* e em *Redirect URLs*. Sem isso, o link do e-mail volta para o endereço padrão e o login não fecha.

**Uma vez só, no Supabase — porta fechada:** Authentication → Sign In / Providers → **Allow new users to sign up: desligado**. O `shouldCreateUser: false` do site só vale para quem usa a tela; a API pública aceita cadastro direto, e com o cadastro aberto qualquer pessoa cria conta e dispara e-mail pelo projeto. Com ele desligado, link e recuperação de senha só chegam a quem já existe (**só o {{OPERADOR}}**; apague qualquer outra conta de teste. Confira com a API: ela deve responder `signup_disabled`). **Quem lê o dado** continua sendo decidido pelo RLS, pela tabela `financas_privado.leitores` (só `{{EMAIL}}`): conta que entra e não está ali vê o painel vazio.

## Uma vez só, no GitHub

Settings → Secrets and variables → Actions → **New repository secret** `FINANCAS_SYNC_TOKEN` (o valor é gerado na criação da função de sincronização e entregue ao {{OPERADOR}}; não fica no repo). Sem ele o Action roda, avisa e não atualiza.

## Publicar

`python3 publicar.py` sobe `index.html`, `runtime.css`, `runtime.js`, `config.js` e `.htaccess` para a raiz de `financeiro.{{DOMINIO}}` pela API da Hostinger (token em `~/.continuum/hostinger-token.txt`; conta e domínio em `.hostinger/site.json`); `python3 publicar.py --conferir` compara byte a byte. A faixa `.sistema` ({{EMPRESA}} · Caixa · Projetos) no topo do painel é a primeira peça do "um sistema só" com o painel de projetos; mora em `casca.html` e `runtime.css`, e `montar.py` a leva ao `index.html`.
