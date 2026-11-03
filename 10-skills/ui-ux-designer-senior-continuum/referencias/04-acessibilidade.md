> Módulo de referência. Carregar sempre. Acessibilidade é restrição de projeto, não camada final.

# PARTE 4 · Acessibilidade (padrão AA)

> **Acessibilidade não é caridade nem burocracia: é a diferença entre uma pessoa comprar e não conseguir comprar.** A maior parte do ganho vem de duas coisas: contraste e teclado. Comece por elas.

## 4.1 Os critérios que mais aparecem

**Perceptível**
- Todo conteúdo não textual com significado tem alternativa em texto. Imagem decorativa é marcada como decorativa, não descrita.
- Informação e estrutura são transmitidas semanticamente, não só visualmente. Título é título de verdade, lista é lista de verdade.
- **Contraste de texto:** mínimo 4,5 para 1 no texto normal, 3 para 1 no texto grande (a partir de 24, ou 19 em negrito).
- **Contraste de elemento:** mínimo 3 para 1 em borda de campo, ícone com significado, limite de componente e indicador de estado.
- **Cor nunca é o único portador de informação.** Erro em vermelho e nada mais é invisível para parte do público, e some sob sol forte em qualquer tela.

**Operável**
- Toda funcionalidade alcançável por teclado, sem armadilha: entra e sai de qualquer região.
- Ordem de foco lógica, seguindo a ordem visual.
- Indicador de foco visível, com contraste próprio contra o fundo.
- Alvo de toque de no mínimo 44 por 44, com folga entre alvos vizinhos.
- Nada pisca acima de três vezes por segundo.
- Movimento decorativo respeita a preferência de movimento reduzido do sistema.

**Compreensível**
- Nada muda de contexto sozinho quando um elemento recebe foco.
- Erro identificado com texto que descreve o problema E como resolver.
- Todo campo tem rótulo ou instrução associada de forma programática.
- Idioma da página declarado.

**Robusto**
- Todo componente de interface tem nome, papel e valor acessíveis. Botão feito de uma caixa clicável sem papel semântico não existe para quem usa leitor de tela.

## 4.2 Como testar (na ordem, do mais barato ao mais caro)

1. **Contraste.** Conferir cada par de texto e fundo, e cada elemento de interface, contra a régua. Fazer isso na definição dos tokens, não no fim.
2. **Só teclado.** Guardar o mouse. Percorrer a página inteira com tabulação: dá para chegar em tudo, o foco é visível, e a ordem faz sentido?
3. **Zoom a 200%.** O layout quebra, corta conteúdo ou obriga a rolar na horizontal?
4. **Leitor de tela.** Percorrer os pontos principais e ouvir como cada elemento é anunciado.
5. **Verificação automatizada.** Pega cerca de um terço dos problemas. É o começo, nunca o fim.
6. **Aparelho real, sob sol.** O teste que ninguém faz e que reprova mais paleta de baixo contraste que qualquer ferramenta.

## 4.3 Os oito erros que mais aparecem

1. Contraste insuficiente, quase sempre em texto secundário cinza-claro e em microcopy.
2. Contorno de foco removido para "ficar limpo".
3. Campo sem rótulo associado, com rótulo vivendo só como texto interno.
4. Elemento clicável que não é botão nem link, invisível para tecnologia assistiva.
5. Imagem com significado sem alternativa em texto.
6. Armadilha de foco em sobreposição: entra e não sai com teclado.
7. Mídia que começa sozinha, com som, sem controle.
8. Cor como único sinal de estado.

## 4.4 Formato do achado

O auditor devolve achado localizado, nunca correção pronta.

| # | Elemento | Problema | Critério | Severidade | Direção da correção |
|---|---|---|---|---|---|
| 1 | [elemento citado] | [o que acontece] | [contraste, teclado, rótulo...] | crítico / maior / menor | [o que precisa mudar, não o valor exato] |

**Severidade:**
- **Crítico** — impede alguém de completar a ação. Reprova a entrega sozinho.
- **Maior** — dificulta de forma relevante. Corrige antes de publicar.
- **Menor** — polimento. Entra na fila.

## 4.5 Tabela de contraste (anexo obrigatório da spec)

| Elemento | Frente | Fundo | Razão | Exigido | Passa |
|---|---|---|---|---|---|
| Texto de corpo | | | | 4,5:1 | |
| Texto secundário | | | | 4,5:1 | |
| Microcopy sob a ação | | | | 4,5:1 | |
| Rótulo da ação principal | | | | 4,5:1 | |
| Borda de campo | | | | 3:1 | |
| Anel de foco | | | | 3:1 | |
| Ícone com significado | | | | 3:1 | |

**Microcopy é o campeão de falha de contraste** justamente porque é pequeno e cinza, e é ele que carrega a última objeção antes do clique. Conferir sempre.

---
