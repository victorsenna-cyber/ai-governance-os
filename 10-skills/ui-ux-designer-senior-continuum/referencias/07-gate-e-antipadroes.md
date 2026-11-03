> Módulo de referência. Carregar antes de entregar e em toda crítica de layout.

# PARTE 7 · Gate visual

## 7.1 Os 9 passes (detalhe)

1. **Direção.** A direção está declarada por escrito? Ela é reconhecível na tela? Rode o teste do esqueleto: remova marca e texto, e veja se o que sobra tem personalidade. Rode o teste do concorrente: um concorrente poderia assinar isto? Se sim, reprova.
2. **Sistema.** Varrer valores de cor, espaço, tipo, raio e elevação. Cada valor solto é um achado, com o elemento citado. Sistema com furo não é sistema, é sugestão.
3. **Hierarquia.** Apertar os olhos e listar o que salta, em ordem. A sequência conta a história certa? Dois elementos com o mesmo peso disputando é achado.
4. **Clímax.** Contar os pontos de contraste máximo. Se há mais de um, não há nenhum. Conferir que o único coincide com o momento de decisão.
5. **Estados.** Percorrer cada elemento interativo contra a matriz de estados. Foco ausente reprova sozinho.
6. **Acessibilidade.** Tabela de contraste preenchida, teclado percorrido, zoom a 200%, semântica conferida, movimento reduzido respeitado. Achado crítico reprova sozinho.
7. **Mobile.** Re-hierarquizado e testado em aparelho real. Título em no máximo três linhas, ação alcançável, tabela virou pilha com o item certo em cima.
8. **Movimento e performance.** Nada essencial depende de script. Durações dentro da faixa. Nenhum deslocamento de layout durante a leitura. Imagens dimensionadas e fontes que não bloqueiam.
9. **Integridade.** Zero placeholder, zero texto simulado, zero imagem provisória, zero imagem de banco genérica. Spec anexada. A copy é a aprovada, sem edição do designer.

## 7.2 Score visual

| Dimensão | Pergunta | Nota |
|---|---|---|
| Intenção | dá para dizer a direção em 3 segundos? | |
| Hierarquia | o olho vai para onde a decisão está? | |
| Clímax | o pico visual coincide com o pico de decisão? | |
| Consistência | tudo vem do sistema? | |
| Acessibilidade | teclado, contraste, zoom, semântica | |
| Acabamento | espaçamento, alinhamento óptico, estados, detalhe | |

**Abaixo de 42/60, revisar. Nota 4 ou menos em Acessibilidade reprova sozinha.**

## 7.3 Formato do achado

Auditor e crítico devolvem defeito localizado, com o elemento citado e a direção da correção. **Nunca o valor pronto, nunca o redesenho.** Só o designer de tela altera pixel.

| # | Elemento | O que está errado | Qual regra | Severidade | Direção |
|---|---|---|---|---|---|

## 7.4 Anti-padrões de design

Nenhum passa no gate.

**De direção**
1. Direção não declarada: o design foi acontecendo.
2. Direção que existe só na primeira tela e evapora depois.
3. Duas direções misturadas na mesma página.
4. Estética da moda aplicada sem relação com o que a marca vende.

**De sistema**
5. Valor solto de cor, espaço ou tipo espalhado pela tela.
6. Cinco pesos de fonte e três famílias.
7. Raios misturados sem escala.
8. Sombra difusa idêntica em tudo, sem sistema de elevação.
9. Paleta de seis cores em pesos iguais.

**De hierarquia e composição**
10. Tudo com o mesmo peso: nada salta, o olho não sabe para onde ir.
11. Ênfase empilhada: negrito, maior, colorido e caixa alta ao mesmo tempo.
12. Dois clímax visuais, ou nenhum.
13. Três blocos seguidos com o mesmo fundo, altura e composição.
14. Densidade por acidente de conteúdo, não por decisão.
15. Espaçamento que agrupa errado: mais respiro entre título e seu texto do que entre seções.
16. Meia tela vazia por estética, sem função de hierarquia.

**De conteúdo visual**
17. Imagem de banco genérica, imagem sintética como fotografia, ilustração vetorial padrão de pessoas.
18. Um ícone decorativo por item de lista.
19. Emoji usado como ícone.
20. Elemento de marca que virou o prato em vez do tempero.

**De interação**
21. Contorno de foco removido.
22. Bloco clicável que não é botão nem link.
23. Componente entregue sem estado de erro, carregando ou vazio.
24. Rótulo que vive só dentro do campo e some ao digitar.
25. Alvo de toque pequeno demais, ou colado no vizinho.

**De movimento e performance**
26. Conteúdo da primeira tela que depende de script para existir.
27. Animação acima de um segundo no caminho crítico.
28. Deslocamento de layout enquanto a pessoa lê.
29. Movimento reduzido ignorado.
30. Mídia com som automático.

**De integridade**
31. Placeholder ou texto simulado no ar.
32. Designer editando copy aprovada para caber no layout.
33. Entrega sem spec, "porque o código está lá".

---
