# Modelo · Dashboard Vidro

> **Tipo:** blueprint · **Status:** 🟡 provisório (sai para ✅ com o primeiro caso real no ar) · **Rota:** `00-core/roteador/ARVORE-ESCRITA.md` (interface de painel) e `90-templates/direcoes-de-interface/README.md` (direção **D**)
> **Fonte:** uma referência em vídeo ("Glassy Dashboard", seis telas) trazida pelo operador. **Forma modelada, código nosso**: nada do código da referência foi copiado.

## O que é

Painel de gestão em **vidro fosco sobre foto de ambiente**: casca translúcida grande, trilho de ícones à esquerda, cartões de vidro que sobem 4 px no hover, um único azul de destaque (anel, barra em foco, chave ligada) e todo o resto em branco com transparência. É calmo, premium, de dono de empresa olhando o negócio; não é sala de controle.

Um arquivo, sem build: `dashboard.html` (estrutura, estilo e lógica) + `dados.js` (os números da conta). Abre em `file://`, publica em qualquer hospedagem estática.

## As cinco telas

| Tela | O que mostra | De onde vem o número |
|---|---|---|
| **Visão geral** | abas no topo · equipe · meta do período em anel · receita com curva e seletor Hoje/Semana/Mês · novos leads · aprovação com "arraste para aprovar" · vendas em barras com a barra em foco · 4 indicadores com chave · gravação de call com onda | digitado em `visao_geral` |
| **Relatórios** | esqueleto de carregamento (0,7 s) e três leituras: vendas no ano, negócios por etapa, clientes por status | **calculado** das outras telas |
| **Funil** | 4 KPIs · filtro por responsável · busca · quadro por etapa, **arrastável** | KPIs **calculados** dos cartões (aberto, ponderado pela probabilidade da etapa, taxa de ganho, ticket médio) |
| **Clientes** | 4 KPIs · filtro por status com contagem · busca · tabela ordenável · **exportar CSV** | KPIs **calculados** das linhas |
| **Produtos** | 4 KPIs · filtro por categoria · grade com orbe colorido, preço, vendas, chave "à venda" | KPIs **calculados** dos itens |

Cada tela só aparece se o bloco de dados dela existir em `dados.js`. Rótulo, ícone, título e subtítulo de cada tela se trocam em `secoes`: "Produtos" pode virar "Peças", "Funil" pode virar "Orçamentos".

## Tokens

| Token | Valor | Uso |
|---|---|---|
| `--acento` | `#3B82F6` (troca por `marca.acento`) | anel, barra em foco, chave ligada, badge, onda ouvida |
| `--vidro` / `--vidro-2` / `--vidro-forte` | branco a 7,5 % / 12 % / 20 % | cartão / hover e ícone / item ativo |
| `--borda` / `--borda-2` | branco a 12 % / 22 % | contorno do vidro / hover |
| `--texto` / `-2` / `-3` | `#F6F5F3` a 100 / 66 / 40 % | valor / rótulo / legenda |
| `--ok` `--ruim` `--aviso` | `#4ADE80` `#F87171` `#FBBF24` | variação e status, só em pílula pequena |
| raios | casca 34 · cartão 22 · interno 14 · pílula 99 | |
| fonte | **Outfit** 300–600 (Google Fonts), queda para system-ui | |
| desfoque | casca 42 px · cartão 22 px | `backdrop-filter` |
| movimento | `cubic-bezier(.2,.8,.2,1)`, entrada em cascata de 45 ms, hover −4 px | `prefers-reduced-motion` desliga |

**Fundo:** `marca.fundo` com a url de uma foto de ambiente (sala, pátio, loja do cliente) põe a foto atrás do vidro. Vazio, o fundo é gerado em CSS (luz quente embaixo, luminárias). **A foto é o que faz o vidro parecer vidro**: em conta com foto própria, use a dela.

## Como instanciar numa conta

1. Copiar `dashboard.html` para a pasta da conta (`clientes/<Conta>/NN - web design/<painel>/` ou a pasta do sistema dela).
2. Copiar `dados-exemplo.js` como **`dados.js`** ao lado e trocar os valores. Sem `dados.js`, a página abre com o exemplo, e é assim que se percebe que a instância está incompleta.
3. **Regra Nº 0, lacuna de fato:** número que a conta não tem não se inventa. Bloco sem dado sai de `secoes` ou fica marcado como exemplo no próprio rótulo.
4. Foto de ambiente da conta em `marca.fundo`; cor da marca em `marca.acento` só se ela tiver contraste sobre o vidro (azul, verde, laranja vivos funcionam; cor escura some).
5. Conferir no Chrome em 1440 × 1000 e em 390 × 844 (no celular o trilho vira barra fixa embaixo).

**Dado que a conta ainda não tem** (o caso comum na fase 1): campo `null` aparece como **"—"**, nunca como zero; funil sem negócio mostra KPI "—" e o aviso de `funil.aguardando`; meta sem realizado mostra o alvo e `meta.aguardando`; produto com `preco: null` mostra `preco_nota` ("a confirmar"). Bloco de texto para o que ainda não tem número: `visao_geral.listas` (título, itens com `rotulo`, `nota`, `estado` e `tom` = ativo · teste · lead · perdido). Marcação de fonte da casa: `fontes.<tela>` vira o rodapé "fonte: … · atualizado em …"; indicador aceita `nota`.

**Ligar a dado vivo:** `dados.js` é o contrato. Quem gera o painel (script do repo, Supabase, planilha) escreve `window.DADOS = {...}` no mesmo formato; a página não muda.

## Veto

- Número inventado numa instância de cliente reprova (Regra Nº 0).
- Segundo acento além do `--acento` reprova: cor só em pílula de status e no orbe de produto.
- Texto escuro sobre vidro, ou acento escuro que some no fundo, reprova.
- Instância sem conferência em largura de celular não está pronta.

## Arquivos

- `dashboard.html` — o modelo inteiro.
- `dados-exemplo.js` — empresa fictícia, todos os blocos preenchidos, comentado.
- `prancha/` — prints das cinco telas, para mostrar antes de instanciar.
