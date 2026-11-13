# direcoes-de-interface · as cinco direções de tecnologia para painel, app e sistema de cliente

> **Tipo:** blueprint · ✅ vigente (as três primeiras direções); D e E, ver abaixo.
> **Quando entra:** toda tela de produto digital nossa ou de cliente — painel, app, PWA, tela de conexão, sistema de gestão — **no degrau 5 (cara) do `100-métodos/METODO-DESENHO-DE-PRODUTO.md`**, pela skill `10-skills/ui-ux-designer-senior-continuum/` em modo direção. Rota: `00-core/roteador/ARVORE-ESCRITA.md` (linha de direção de arte e tela).
> **O que resolve:** o cliente precisa *ver* que é tecnologia na primeira olhada. Começar destas direções evita a média genérica e evita errar a leitura do público (o caso abaixo).

## As cinco

| | Direção | Cara | Serve quando | Trai quando |
|---|---|---|---|---|
| **A** | **Sala de controle** | escuro de instrumento, grade fina no fundo, número em fonte de código (JetBrains Mono), luz ciano tirada da cor da marca, LEDs de status com brilho | dono que quer *sentir* controle; uso noturno; operação com muito estado (entregas, tarefas, alertas) | uso longo ao sol, sem tema claro; público que se intimida com painel |
| **B** | **Vidro petróleo** | fintech premium: a cor da marca vira luz de fundo, cartões de vidro por cima (o vidro se justifica porque há luz atrás), cantos macios, ação em verde-água | produto que vende sofisticação; dinheiro e finanças; app de consumo | tela densa de operação; aparelho fraco (o desfoque pesa) |
| **C** | **Engenharia** | papel de pontos, cor da marca como base do destaque, azul elétrico na ação, número em fonte de engenharia (IBM Plex Mono) | leitura no sol, mesa, tabela, o administrativo; o tema claro de quem escolheu A | marca que precisa de calor ou de emoção |
| **D** | **Vidro fosco** | casca translúcida sobre **foto de ambiente** desfocada, cartões de vidro neutros que sobem no hover, um só azul de destaque, Outfit | painel do dono olhando o negócio (receita, meta, funil, clientes, produtos); quem quer calma e acabamento premium | operação densa e noturna (aí é A); aparelho fraco; conta sem foto de ambiente boa |
| **E** | **Grafite** | preto em camadas de carvão sob uma luz difusa que vem de cima à direita; cartão de canto largo (18 px) com borda quase invisível; **todo controle em pílula**; número em display técnica (Space Grotesk, tabular, zero cortado) e palavra em Instrument Sans; **um acento só, que é também a cor de "atenção"** (preenchimento = ação ou seleção; ponto com palavra = estado), vermelho só para ruim e verde só para bom; a seleção se faz **na própria visualização** (régua de dias, barra acesa, nó ativo) | painel de quem olha dinheiro e decide: caixa, DRE, fluxo, receita, funil; um número-herói por tela com a composição dele e a ação ao lado; escuro por padrão com claro derivado | operação densa de instrumento, com muito estado por linha (aí é A); marca cujo acento não passa em contraste com texto escuro por cima; tela sem um número que mande nas outras |

**E já vem como sistema completo de tokens e componentes** (nos dois temas, com o contraste conferido por script): o molde é a folha de estilo do painel financeiro da própria casa. Modelada de uma referência trazida pelo operador; código nosso. **Desvio da regra comum:** a marcação de fonte sai na família dos números, não em mono (duas famílias só).

**E · caso de tela: o cartão de decisão em duas camadas.** A aba de decisões do painel mostra a **face** do cartão (pergunta grande, "em jogo", faixa de números, opções como botão inteiro com rótulo e efeito, e o porquê e a premissa **dentro** da opção recomendada, que mantém a regra da direção: borda âmbar e selo, nunca botão primário) e guarda o **lastro** atrás de um botão fantasma; depois do clique o cartão recolhe numa linha com "Desfazer". Só tokens e componentes do sistema, nenhum token novo. Molde do conteúdo: `40-operacao-rotinas/tarefas/modelos/cartao-decisao.md`. 🟡 até a medição de leitura do resultado.

**Vetos da E:** segundo acento reprova · âmbar de acento e âmbar de aviso em tons diferentes reprova · texto sobre a cor de marca do acento reprova · número sem dataset declarado reprova · cartão tracejado sem ação por trás reprova · mais de um botão primário por tela (fora de fila) reprova · tela sem print em 390×844, escuro e claro, não está pronta.

**D já vem como painel completo, não só direção:** `90-templates/dashboard-vidro/` (cinco telas, dados num `dados.js`, KPIs calculados). Modelado de uma referência em vídeo; código nosso.

**Comum a todas, e é o que as torna da casa:** todo número sai com a **marcação de fonte** (de onde veio e quando, em mono, com um ponto de cor), um **destaque por tela** (o número que pede decisão, com a única ação forte), **status com palavra** (nunca só cor), **LED na linha** e **indicador com minigráfico**.

## Arquivos

| Arquivo | O que é |
|---|---|
| `direcoes.html` | a mesma tela *Hoje* nas três direções, lado a lado, com dados fictícios. **É a prancha de escolha** para mostrar ao operador ou ao cliente |

**Os tokens de verdade nascem no repositório do cliente**, na instância (`<repo do cliente>/…/design/tokens.css`, `componentes.css`, `tema.js`), com troca de tema e de modo na tela e contraste AA conferido em cada combinação.

## Como instanciar

1. Abrir `direcoes.html`, trocar a cor da marca pela do cliente (lida da logo) e mostrar. O operador escolhe: **uma padrão e, se quiser, uma segunda como troca**.
2. Criar `tokens.css`, `componentes.css` e `tema.js` na pasta de design do repo do cliente a partir da direção escolhida e trocar o bloco de cores de marca e destaque.
3. Conferir contraste dos pares de texto nos modos escolhidos (texto ≥ 4,5:1; campo ≥ 3:1). O botão de ação dentro do destaque usa um acento próprio (`--acento-destaque`): o acento comum costuma falhar sobre o fundo do destaque.
4. Prancha do cliente com as telas reais dele e o seletor de tema; README de design no repo dele, roteado no kernel dele.

## Caso 0 · um sistema de gestão de cliente

**Escolha:** uma direção escura como padrão, com claro, e uma segunda direção como opção de troca de tema, também com claro e escuro → **A padrão (escuro), C como troca, os dois com claro e escuro.**

**Descartada no mesmo dia, e o porquê (régua):** a primeira direção foi **brutalismo de material** (concreto, borda grossa, canto vivo, letra de placa), tirada do mundo do produto do cliente. A leitura dele: parecia tema de alto contraste, e ele precisava ver que era tecnologia. **O erro foi de leitura do público:** desenhou-se para o mundo do produto e não para o que o cliente comprou (um sistema). **Régua:** a cara de um sistema de gestão fala da tecnologia que o cliente contratou, não do material que ele fabrica. A ideia que sobreviveu da descartada: a marcação de fonte em todo número.
