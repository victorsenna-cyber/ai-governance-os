> Módulo de referência. Carregar ao animar e ao implementar.

# PARTE 5 · Movimento e performance

## 5.1 Movimento com função, ou nenhum

Cada efeito custa: peso, processamento, bateria e, no pior caso, o valor da primeira tela. Movimento entra quando faz uma destas quatro coisas:

1. **Guia o olho** para onde a próxima decisão acontece.
2. **Explica uma relação** entre dois estados: de onde veio, para onde foi.
3. **Confirma uma ação** com resposta imediata ao toque.
4. **Dá peso ao clímax**, uma vez só, no momento da decisão.

Se o efeito não faz nenhuma das quatro, ele é atrito com aparência de capricho. Corta.

## 5.2 Faixas de duração

| Tipo | Faixa | Nota |
|---|---|---|
| Resposta ao toque | 80 a 120ms | precisa parecer instantâneo |
| Micro-interação: sobre, foco, alternância | 150 a 250ms | |
| Transição de estado: abrir, fechar, expandir | 250 a 400ms | |
| Revelação de bloco na rolagem | 400 a 700ms | com deslocamento pequeno, de 8 a 24 |
| Sequência orquestrada de entrada | até 900ms no total | atraso entre itens de 40 a 80ms |

**Nada acima de um segundo no caminho crítico.** Movimento que atrasa a leitura do valor é o pior tipo de bonito.

**Curvas:** saída rápida e chegada suave para coisas que entram; o inverso para coisas que saem. Curva linear só para movimento contínuo e mecânico.

## 5.3 Orquestração de entrada

Uma sequência bem feita na chegada da página vale mais que vinte micro-interações espalhadas. Regras:

- **Máximo três grupos** entrando em sequência. Mais que isso vira espera.
- Os elementos entram **na ordem de leitura**, nunca em ordem aleatória ou de "efeito".
- **A ação principal entra por último e chega inteira.** Botão que ainda está aparecendo quando a pessoa já quer clicar é frustração pura.
- **Um gesto assinado, repetido com disciplina**, cria identidade. Cinco gestos diferentes criam ruído.

## 5.4 A regra do primeiro paint

> **O valor da primeira tela nunca depende de script.** Texto, ação e a informação essencial nascem visíveis. Animação é revelação progressiva do que já está lá, nunca a condição para que exista.

Consequência prática: se a técnica escolhida esconde o conteúdo até que o script decida mostrar, e o script falha ou atrasa, a página entregou uma tela em branco. Elemento que entra por movimento começa visível e é animado a partir daí, não o contrário.

## 5.5 Preferência de movimento reduzido

Parte das pessoas sente náusea ou desconforto com movimento na tela, e o sistema operacional já avisa isso. Respeitar não é opcional.

- Movimento decorativo: desligar.
- Movimento funcional (confirmação, mudança de estado): reduzir para uma transição curta de opacidade.
- **Nunca desligar tudo a ponto de o conteúdo sumir.** Se o elemento aparecia por animação, com movimento reduzido ele simplesmente está lá.

## 5.6 Orçamento de performance

- **A primeira tela completa em poucos segundos em rede móvel comum.** Esse é o alvo, e ele governa as escolhas abaixo.
- **Imagens:** dimensionadas para o espaço real, formato moderno, com largura e altura declaradas para não empurrar o layout quando carregam. Carregamento adiado para tudo que está abaixo da primeira tela, nunca para o que está dentro dela.
- **Fontes:** poucos arquivos, subconjunto de caracteres, exibição com fonte substituta enquanto carrega. Fonte que bloqueia a renderização é a causa mais comum de tela em branco em rede lenta.
- **Deslocamento de layout:** reservar espaço para tudo que chega depois. Elemento que empurra o conteúdo enquanto a pessoa lê é atrito puro, e cliques errados.
- **Vídeo:** nunca com som automático. Silencioso, curto e em laço é tolerado fora do caminho crítico de leitura. Qualquer vídeo com fala espera o clique, e vem com legenda, porque a maioria assiste sem som.
- **Miniatura de vídeo é uma mini-tela:** rosto real e uma frase específica de curiosidade. Miniatura genérica é uma porta desperdiçada.
- **Terceiros:** cada script externo é peso e risco. O que não é essencial carrega depois, ou não carrega.

---
