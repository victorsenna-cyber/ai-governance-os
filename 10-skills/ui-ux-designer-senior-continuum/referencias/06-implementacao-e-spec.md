> Módulo de referência. Carregar ao entregar. Spec é sempre obrigatória; código é sob demanda.

# PARTE 6 · Implementação e entrega

## 6.1 A spec (obrigatória, mesmo quando há código)

A spec existe porque o código muda de mão e a intenção não pode morrer no caminho. Formato por bloco:

```
BLOCO:            [identificador do bloco na estrutura recebida]
INTENÇÃO:         [o porquê emocional recebido de quem faz a física]
VOLTAGEM / PESO:  [número recebido -> tratamento visual escolhido]
COMPOSIÇÃO:       [centralizada, assimétrica, duas colunas, densidade]
SUPERFÍCIE:       [token de fundo, textura, o que muda em relação ao bloco anterior]
TIPOGRAFIA:       [degraus usados, por elemento]
ESPAÇAMENTO:      [degraus, interno e externo]
COMPONENTES:      [quais, em que variante e tamanho]
ESTADOS:          [o que precisa existir além do repouso]
LIMITE DE TEXTO:  [caracteres por elemento, medido]
MOBILE:           [o que muda de ordem, tamanho ou composição]
MOVIMENTO:        [o que anima, quanto tempo, com que função]
ACESSIBILIDADE:   [pares de contraste, ordem de foco, papéis semânticos]
```

Anexos da spec: tabela de tokens, tabela de contraste (módulo 04, §4.5), e a ficha de cada componente novo.

## 6.2 Quando há código

**Marcação semântica antes de qualquer estilo.** Cabeçalho, seções, listas, botões e links de verdade. Um bloco clicável que não é botão não existe para tecnologia assistiva e não funciona no teclado.

- Um `h1` por página. Hierarquia de títulos sem pular nível. A ordem dos títulos é o índice que o leitor de tela usa para navegar.
- Botão para ação, link para navegação. Trocar os dois quebra teclado e expectativa.
- Formulário com rótulo associado ao campo, agrupamento quando faz sentido, e mensagem de erro ligada ao campo.
- Região principal, navegação e rodapé marcadas, para quem navega por regiões.
- Idioma declarado.

**Estilo a partir dos tokens.** Todos os valores como variáveis, em uma camada semântica. Nenhum valor solto no meio do estilo: valor solto é o que impede trocar a marca depois sem reescrever tudo.

**Do celular para cima.** Escrever o estilo base para a tela pequena e adicionar nos pontos de quebra. O caminho inverso produz páginas que funcionam bem no monitor de quem desenhou e mal onde a maioria decide.

**Pontos de quebra por conteúdo, não por aparelho.** O ponto de quebra fica onde a linha começa a ficar longa demais ou o bloco começa a apertar, e isso se descobre esticando a janela, não consultando uma lista de tamanhos de telefone.

**O que nunca fazer no código:**
- Remover o contorno de foco sem colocar outro.
- Depender de script para o conteúdo da primeira tela existir.
- Fixar altura em bloco de texto, que quebra em outro idioma ou com fonte ampliada.
- Usar unidade fixa em tudo: tamanho de fonte e espaçamento respeitam a preferência de quem usa.
- Deixar imagem sem dimensão declarada.
- Guardar dado sensível no navegador, ou depender de armazenamento local para o conteúdo aparecer.

## 6.3 Antes de entregar

- [ ] Rodou com script desligado: o conteúdo principal está lá.
- [ ] Rodou só no teclado: chegou em tudo, o foco é visível, saiu de todas as sobreposições.
- [ ] Zoom a 200%: nada corta, nada rola na horizontal.
- [ ] Aparelho real, não emulador.
- [ ] Rede lenta simulada: o valor aparece antes da fonte bonita.
- [ ] Nenhum texto simulado, nenhum placeholder, nenhuma imagem provisória.
- [ ] O texto é exatamente o aprovado. Ajuste de tamanho de bloco é pedido a quem escreve, nunca resolvido editando a copy.

## 6.4 Handoff

Quem recebe precisa de quatro coisas, e só de quatro:
1. A spec por bloco.
2. Os tokens, com nome e valor.
3. Os componentes novos documentados, com estados.
4. A lista do que ficou em aberto, com a pergunta pronta para quem decide.

**Handoff sem estados é retrabalho garantido.** A pergunta "e como fica quando dá erro?" chega sempre, e chega tarde.

---
