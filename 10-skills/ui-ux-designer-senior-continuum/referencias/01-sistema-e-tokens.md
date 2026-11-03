> Módulo de referência. Carregar ao montar o sistema, no modo direção.

# PARTE 1 · Sistema e tokens

**Regra-mãe do módulo: todo valor visível na tela vem de um token nomeado.** Valor solto no meio do desenho ou do código é dívida: no dia da revisão ninguém sabe se aquele espaço de 22 é intencional ou acidente.

## 1.1 Tipografia

**Escolher duas famílias, no máximo três.** Uma de display com caráter, uma de leitura confiável, e opcionalmente uma monoespaçada para números e códigos. Fonte é a assinatura mais barata da marca.

**Escala.** Usar uma razão fixa e ficar nela. Razões que funcionam: 1,2 para interfaces densas, 1,25 para páginas equilibradas, 1,333 ou 1,5 para páginas com títulos dramáticos. Definir os degraus e nomeá-los por função, nunca por tamanho.

```
--txt-micro     legenda, microcopy sob botão
--txt-corpo-p   nota, rodapé
--txt-corpo     leitura padrão
--txt-corpo-g   subtítulo de bloco, primeiro parágrafo
--txt-titulo-p  título de card, pergunta de acordeão
--txt-titulo    título de bloco
--txt-display   título de abertura e de clímax
```

**Regras que valem sempre:**
- Corpo de leitura entre 16 e 20 no celular. Abaixo de 16 o navegador dá zoom sozinho em alguns aparelhos, e o layout quebra.
- Altura de linha entre 1,4 e 1,7 para leitura; entre 1,05 e 1,2 para display. Título com altura de linha de corpo parece frouxo.
- Largura de coluna entre 45 e 75 caracteres. Acima disso o olho perde a linha de volta.
- Entreletra negativa só em display grande. Caixa alta pequena pede entreletra positiva.
- Números que se comparam em coluna usam variante tabular. Preço que dança de largura entre planos lê como desleixo.
- Dois pesos por família bastam para quase tudo. Cinco pesos é indecisão documentada.

## 1.2 Cor

Nomear por função, nunca por aparência. `--cor-acento` sobrevive a uma troca de marca; `--azul-claro-2` não.

```
Marca:      --cor-marca · --cor-marca-forte · --cor-marca-suave
Superfície: --sup-base · --sup-elevada · --sup-densa · --sup-invertida
Texto:      --txt-forte · --txt-medio · --txt-suave · --txt-sobre-inverso
Acento:     --cor-acento (raro, só onde importa) · --cor-acento-hover
Sinal:      --sinal-ok · --sinal-atencao · --sinal-erro · --sinal-info
Borda:      --borda-sutil · --borda-media · --borda-forte
```

**Regras:**
- **Dominância, não equilíbrio.** Uma cor ocupa a maior parte, uma apoia, o acento aparece em menos de 5% da área. Acento em tudo é acento em nada.
- **O acento pertence à ação.** Se o botão principal e três outros elementos usam o mesmo acento, o botão perde.
- **Superfície invertida é recurso escasso.** Reservar para o clímax. Uma página com quatro faixas escuras não tem clímax.
- **Sinal não é decoração.** Vermelho é erro; usar vermelho como cor de marca queima o vocabulário de erro para sempre.
- Todo par de texto e fundo é conferido contra a régua de contraste antes de virar token, não depois (módulo 04).

## 1.3 Espaçamento e grade

**Uma escala, baseada em uma unidade.** Base 4 ou 8. Os degraus são multiplicações, e nada fora deles.

```
--e-1 = 4    --e-2 = 8    --e-3 = 12   --e-4 = 16
--e-5 = 24   --e-6 = 32   --e-7 = 48   --e-8 = 64
--e-9 = 96   --e-10 = 128
```

**Regras:**
- **Proximidade é significado.** O espaço entre um título e seu parágrafo é sempre menor que o espaço entre esse parágrafo e o próximo título. Quando isso se inverte, o leitor agrupa errado, e nenhuma cor conserta.
- **Espaço entre blocos vem dos degraus grandes** (7 a 10); espaço dentro de componente vem dos pequenos (1 a 5). Misturar as duas escalas é o que faz uma tela parecer montada e não desenhada.
- **Grade:** 12 colunas no desktop com medianiz de um degrau da escala; 4 colunas no celular. Largura máxima de conteúdo de leitura entre 640 e 760; largura máxima de bloco largo entre 1120 e 1280.
- **Alinhamento óptico vence alinhamento matemático.** Ícone, aspas e formas redondas precisam de ajuste manual para parecerem alinhados.

## 1.4 Forma, borda e elevação

- **Raio:** uma escala pequena, tipicamente três degraus mais o zero. Um raio único aplicado a tudo é a assinatura de montagem; nenhum raio é uma decisão legítima; raios aleatórios é descuido.
- **Borda:** definir os três pesos e usar borda em vez de sombra sempre que a direção for técnica, editorial ou brutalista.
- **Elevação:** sombra é um sistema de altura, com três a quatro níveis, cada um com uma função declarada (repouso, sobreposição, foco, modal). Sombra difusa igual em tudo é ruído.
- **Regra da profundidade:** em uma tela, no máximo dois níveis de elevação convivendo. Três já é confusão espacial.

## 1.5 Nomeação e manutenção

- Nome por **função**, não por aparência ou valor.
- Duas camadas: tokens primitivos (a paleta e a escala cruas) e tokens semânticos (o que cada um significa na interface). O desenho e o código usam só a camada semântica.
- **Auditoria do sistema:** varrer periodicamente por valor solto, nome inconsistente e componente sem documentação. Uma tabela de cobertura vale mais que uma opinião: quantos valores de cor, espaço e tipo estão fora de token, e onde.

## 1.6 O que o modo direção entrega para quem escreve

Além dos tokens, a direção devolve à skill de copy uma coisa que ela não tem como adivinhar: **quanto cabe.**

```
LIMITES POR BLOCO
Sobretítulo:        até N caracteres, 1 linha
Título de abertura: até N caracteres, no máximo 2 linhas no celular
Subtítulo:          até N caracteres, 2 a 3 linhas
Título de bloco:    até N caracteres, 1 a 2 linhas
Item de lista:      até N caracteres, 1 linha no desktop
Rótulo de botão:    até N caracteres, 1 linha sempre
Microcopy de botão: até N caracteres, 1 linha
```

Os números saem da escala tipográfica escolhida e da largura da grade, medidos, não estimados. Sem esta tabela, a copy volta do redator com títulos que quebram em quatro linhas no celular, e alguém acaba editando texto aprovado no meio do desenho. É assim que a promessa muda sem ninguém decidir que ela mudaria.

---
