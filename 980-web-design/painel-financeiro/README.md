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

Seletor **Tudo · Pessoal · Empresa** e o seletor de mês no topo.

## O site e o artefato

O painel nasceu como um artefato do tipo Dashboard no claude.ai (**Finanças {{EMPRESA}}**). O código passou a ser nosso e a fonte é o repositório: `artefato/index.html` é editado aqui; o artefato do claude.ai fica como legado, sem ser espelhado. O nome da pasta ficou (`montar.py` e `publicar.py` leem esse caminho).

| Arquivo | O que é |
|---|---|
| `artefato/index.html` | o layout das seis telas. Tokens e componentes moram só no `sistema.css`/`sistema.js` |
| `artefato/datasets/*.sql` | as oito consultas da RPC `painel_dados` |
| `casca.html` | a página do site em volta: entrada, barra lateral e topo montados pelo `sistema.js`, `#dash-root` e o botão sair |
| `sistema.css` · `sistema.js` | os tokens (paleta escura e clara), a casca (barra lateral, topo) e os componentes `sis-*` que o Caixa e o Projetos dividem; o `sistema.js` põe `data-theme` no `<html>` antes da página desenhar |
| `runtime.js` · `runtime.css` | o objeto `dash` (dados, filtro Tudo/Pessoal/Empresa, aba no endereço), o recuo da página e a entrada: **e-mail e senha**; o link por e-mail é só para o primeiro acesso ou senha esquecida, e quem entra por ele sem senha criada cai na tela de criar senha (marca `senha_definida` no `user_metadata`); `shouldCreateUser: false`, ninguém se cadastra pela tela; *trocar senha* no menu da conta |
| `simbolo.png` · `favicon.ico` · `favicon-32.png` · `apple-touch-icon.png` | o símbolo, sem fundo (22 px na barra lateral) e o favicon |
| `montar.py` | gera `index.html` (casca + artefato) e `supabase/004-painel-dados.sql` (as oito consultas numa função `public.painel_dados()`, `security invoker`: o RLS das tabelas decide quem lê; `anon` não executa) |

**Fontes:** Instrument Sans (palavra) e Space Grotesk (número, tabular). As fontes *Anthropic Sans* e *Anthropic Serif* do tipo Dashboard não podem ser hospedadas e não são usadas.

**Regra de design:** o painel não leva headlines grandes (`h2.cx-title`) nas abas; só o rótulo pequeno de cada aba.

**Navegação:** as seis telas são itens do grupo **Caixa** da barra lateral (no celular, a fita de pílulas sob o topo). Seletor **Tudo · Pessoal · Empresa** e seletor de mês no topo. **Busca:** **Ctrl+K** (⌘K no Mac), **/** fora de campo de texto, ou a pílula no centro do topo abrem a paleta (`sistema.js`): leva às telas das duas páginas e acha contraparte (abre Lançamentos já filtrado), conta, decisão e ficha do Comercial (abrem no Projetos). Casa sem acento e sem caixa; ↑ ↓ andam, Enter abre, Esc fecha. `?busca=<contraparte>` na URL abre Lançamentos filtrado (é por onde a busca do Projetos chega aqui). Teclas numéricas não existem: o teclado navega por Tab.

**Direção Grafite:** preto em camadas de carvão sob luz difusa, um acento só, âmbar, que é também a cor de "atenção"; nenhum azul (as séries do gráfico são cinza claro e âmbar); cartão 18 px, bloco interno 12 px, controle em pílula; botões de 34 px de altura e 104 px de largura mínima; versão clara em cinza, derivada dos mesmos tokens; o escuro é o padrão em todo aparelho. A barra lateral tem grupos por intenção (Visão · Agir · Contas · Automação · Caixa), montada pelo `sistema.js` do mesmo mapa nas duas páginas, recolhível, gaveta no celular.

**O que mudou na tela:** a Visão tem herói com fôlego ("cobre N meses de saídas"), quatro KPIs com minigráfico, o gráfico do saldo com régua de dias (clique, toque e teclado; abre no dia do menor saldo), "Vence em 7 dias" que filtra a Agenda, "Para onde foi" em fluxo de três colunas (nó de categoria abre Lançamentos filtrado), o resultado do mês com o mapa de calor das saídas, e o primeiro alerta do Conferir no pé da barra lateral. DRE tem herói, fluxo e barras por mês; Fluxo, barras por semana com o previsto listrado; A pagar e A receber, cartões; as tabelas viram lista no celular. Saída é neutra com sinal; vermelho só para ruim.

**Contadores cruzados:** o `runtime.js` lê, além do `painel_dados`, o `projetos_estado` e a fila `mensagens_fila` (as mesmas leituras do Projetos, mesma sessão e mesma RLS), e a barra lateral mostra os contadores das duas páginas pelas mesmas funções do `sistema.js`: Decisões, Mensagens, Projetos, Onboarding, Entregáveis e A pagar (vencidas). Leitura que falha some com o contador; nunca um zero inventado. O aviso do pé da barra lateral mostra o alerta **mais grave**: crítico (caixa negativo, contas vencidas) antes de atenção.

**Teste local:** cópia em pasta temporária com os datasets embutidos, aberta por `file://`; nada de exemplo vai ao ar.

**Artefato mudou?** Editar `artefato/index.html`, `python3 montar.py`, aplicar o SQL no Supabase, publicar.

## Extrato, cartão e mês

Tudo entra no sistema, inclusive o detalhamento dos gastos.

- **Fontes do leitor:** os `.csv` de `45-financeiro/extratos/` (cada movimento da conta {{BANCO}}, classificado por `extratos/CLASSIFICACAO.md`) e, se houver, as compras pessoais no cartão compartilhado de terceiro (`940-operador/cartao-compartilhado/CARTAO-COMPARTILHADO.md`). Movimento do extrato igual (dia, sentido, valor) a uma linha dos `.md` sai: vale a do `.md`.
- **Campo `meio`** em `financas_lancamentos` (`supabase/005-meio.sql`): `conta` ou `cartão de terceiro`. Caixa, projeção e semanas só somam `conta`; DRE e categorias somam tudo. Vale em `kpis`, `projecao`, `resumo_projecao`, `semanas` e `lancamentos` (coluna nova), no site e no artefato.
- **Seletor de mês** no topo, guardado por aba: Lançamentos abre no mês corrente, as outras em *Todos os meses*. Visão: *Para onde foi* e a agenda · DRE: a linha do mês e as categorias dele · Fluxo: as semanas que tocam o mês · A pagar/A receber: o vencimento. Com um mês escolhido, as categorias saem somadas dos lançamentos daquele mês; em *Todos os meses*, da consulta `categorias`.
- **Divisão por mês** (linha com o total do mês) em Lançamentos, A pagar e A receber.
- Limite conhecido: uma despesa recorrente que chega agrupada, com o vencimento da 1ª parcela, não aparece num mês futuro.

## Publicar na Hostinger

São onze arquivos estáticos (`index.html`, `sistema.css`, `sistema.js`, `simbolo.png`, `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `runtime.css`, `runtime.js`, `config.js`, `.htaccess`; lista em `publicar.py`), na raiz do domínio. `.hostinger/site.json` guarda o destino: `financeiro.{{DOMINIO}}` (estático, conta `{{HOSTINGER_CONTA}}`). Se um WordPress ocupar o subdomínio, só o substitua com autorização do {{OPERADOR}}.

**Uma vez só, no Supabase** (Authentication → URL Configuration): pôr a URL do site em *Site URL* e em *Redirect URLs*. Sem isso, o link do e-mail volta para o endereço padrão e o login não fecha.

**Uma vez só, no Supabase — porta fechada:** Authentication → Sign In / Providers → **Allow new users to sign up: desligado**. O `shouldCreateUser: false` do site só vale para quem usa a tela; a API pública aceita cadastro direto, e com o cadastro aberto qualquer pessoa cria conta e dispara e-mail pelo projeto. Com ele desligado, link e recuperação de senha só chegam a quem já existe (**só o {{OPERADOR}}**; apague qualquer outra conta de teste. Confira com a API: ela deve responder `signup_disabled`). **Quem lê o dado** continua sendo decidido pelo RLS, pela tabela `financas_privado.leitores` (só `{{EMAIL}}`): conta que entra e não está ali vê o painel vazio.

## Uma vez só, no GitHub

Settings → Secrets and variables → Actions → **New repository secret** `FINANCAS_SYNC_TOKEN` (o valor é gerado na criação da função de sincronização e entregue ao {{OPERADOR}}; não fica no repo). Sem ele o Action roda, avisa e não atualiza.

## Publicar

`python3 publicar.py` sobe os onze arquivos da lista `ARQUIVOS` para a raiz de `financeiro.{{DOMINIO}}` pela API da Hostinger (token em `~/.continuum/hostinger-token.txt`; conta e domínio em `.hostinger/site.json`); `python3 publicar.py --conferir` compara byte a byte.

**Projetos no topo:** a barra lateral dos dois painéis lista Projetos antes de Caixa, e o domínio abre no Projetos: o `.htaccess` da raiz manda `/` para `/projetos/` (302). **O Caixa mora em `/index.html`**, e é para lá que o link da barra aponta.

**Símbolo e favicon:** tirados do símbolo da marca (transparente), sobem na raiz pelo `publicar.py` e servem também o `/projetos/`. O `--conferir` pode acusar diferença nos PNG porque o CDN da Hostinger os reempacota; compare os pixels.

**Ordem:** publicar o Caixa antes do Projetos (o `sistema.css` e o `sistema.js` moram na raiz e o Projetos os lê).
