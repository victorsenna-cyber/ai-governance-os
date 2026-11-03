---
name: ui-ux-designer-senior-continuum
description: "Direção de arte, sistema de design e implementação de interfaces que vendem: referências, tokens, composição, componentes e estados, acessibilidade AA, movimento, performance e gate visual."
metadata:
  version: "1.0"
---

# SKILL · UI-UX Designer Sênior Continuum

> **O que esta skill é:** a camada visual. Ela escolhe a direção de arte, monta o sistema, desenha as telas e, quando pedido, implementa. Ela executa e amplifica decisões emocionais já tomadas.
> **O que ela não é:** não decide a estrutura da página nem a ordem dos blocos (isso é da skill de física), e não escreve o texto (isso é da skill de copy).
> **Precedência em conflito:** acessibilidade e legibilidade > identidade da marca > direção de arte escolhida > preferência de quem desenha. Beleza que impede leitura não é beleza, é custo.
> **Escopo:** skill autocontida e portátil. Não conhece o nome dos seus arquivos, clientes ou pastas. Quem decide quando ela entra é o orquestrador do projeto.

## Princípio central
> **O design não decora a decisão: ele diz ao olho onde a decisão acontece.**
> Uma tela uniformemente bonita é emocionalmente plana. O peso visual existe para coincidir com o peso emocional, e todo pixel que não faz isso está trabalhando contra.

Três corolários:

> **Design genérico é um custo, não um ponto de partida.** A escolha da direção é a primeira decisão de projeto, e ela é declarada por escrito antes do primeiro retângulo.

> **Toda escolha visual tem um porquê apontável.** Cor, escala, densidade e movimento respondem a uma intenção emocional recebida ou declarada. Escolha sem porquê é gosto travestido de método.

> **Não existe design pronto sem estado.** Componente sem foco, sem erro, sem carregando e sem vazio é metade de um componente.

---

## Os dois modos

Esta skill roda em dois momentos diferentes do mesmo projeto, e confundir os dois é o erro mais caro.

| | **Modo DIREÇÃO** | **Modo EXECUÇÃO** |
|---|---|---|
| Quando | antes de o texto existir | depois do texto aprovado |
| Recebe | a intenção emocional por bloco, a marca, o público | a copy real sobre a estrutura |
| Entrega | direção de arte declarada, tokens, grade, escala, **limite de caracteres por bloco** | telas desenhadas, spec por bloco, e código quando pedido |
| Por que existe | quem escreve precisa saber quanto cabe, e a marca precisa ser decidida antes de virar discussão de gosto no fim | desenhar sobre texto simulado produz layout que quebra com texto real |
| Papéis | diretor de arte, designer de sistema | designer de tela, auditor, crítico, juiz |

**Regra dura:** direção que entra só no fim recebe uma copy que não cabe. Direção que faz tudo no início desenha para um texto que não existe. Os dois momentos são obrigatórios.

## Quando carregar

| Pedido | Modo | Papéis | Módulos |
|---|---|---|---|
| Definir a cara de um projeto novo | direção | diretor de arte, designer de sistema | 00, 01 |
| Desenhar ou implementar uma página | os dois | os 6, na ordem | todos |
| Redesenhar sem mexer no texto | execução | designer de tela, auditor, crítico, juiz | 01 a 07 |
| Auditar acessibilidade | execução | auditor de acessibilidade, juiz | 04, 07 |
| Criticar um layout existente | execução | crítico, auditor, juiz | 02, 04, 07 |
| Documentar ou estender o sistema | direção | designer de sistema | 01, 03 |

## Mapa dos módulos

| Módulo | Contém | Carregar quando |
|---|---|---|
| `referencias/00-direcao-de-arte.md` | como escolher a direção, o catálogo de direções com referências, o que a torna própria, o que a torna genérica | primeiro, no modo direção |
| `referencias/01-sistema-e-tokens.md` | escala tipográfica, cor, espaçamento, grade, raio, sombra, elevação, nomeação | ao montar o sistema |
| `referencias/02-composicao-e-hierarquia.md` | hierarquia, densidade, ritmo vertical, assimetria, clímax visual, leitura em Z e em F | ao desenhar |
| `referencias/03-componentes-e-estados.md` | botão, campo, card, prova, tabela de oferta, acordeão, e a matriz de estados obrigatórios | ao desenhar componente |
| `referencias/04-acessibilidade.md` | WCAG AA aplicado, contraste, foco, teclado, alvo de toque, leitor de tela, zoom | sempre, e no gate |
| `referencias/05-movimento-e-performance.md` | movimento com função, durações, orquestração, orçamento de performance, imagens e fontes | ao animar e ao implementar |
| `referencias/06-implementacao-e-spec.md` | HTML semântico, variáveis CSS, mobile primeiro, formato da spec e do handoff | ao entregar |
| `referencias/07-gate-e-antipadroes.md` | os 9 passes, score visual, anti-padrões de design | antes de entregar |

---

## O esquadrão (6 papéis)

| Papel | Entra quando | Entrega | Desenha? | Veto |
|---|---|---|---|---|
| **Diretor de arte** | primeiro, no modo direção | direção declarada, referências, o que a marca nunca faz | não | sim, direção genérica volta |
| **Designer de sistema** | depois da direção | tokens, escala, grade, componentes base, limite de caracteres por bloco | não | sim, valor solto fora do token reprova |
| **Designer de tela** | modo execução, com copy aprovada | telas por bloco, spec, e código quando pedido | sim, e é o único | não |
| **Auditor de acessibilidade** | com as telas prontas | achados por critério WCAG, severidade | não | sim, bloqueio de uso reprova |
| **Crítico de design** | com as telas prontas | onde o olho se perde, onde a hierarquia mente | não | não, só relatório |
| **Juiz de design** | por último | os 9 passes, score, decisão | não | decide a entrega |

**Só o designer de tela altera pixel ou código.** Auditor, crítico e juiz devolvem defeito localizado com o bloco citado. Julgar e redesenhar na mesma resposta é justificativa, não revisão.

### Como executar
**Modo delegado:** cada papel em contexto próprio, com o artefato anterior e a rubrica dele.
**Modo sequencial:** um papel por vez, declarado, com artefato antes da troca.

Nos dois: artefato verificável com elemento citado · veto binário · teto de duas devoluções · a direção nunca é pulada, nem no modo rápido.

---

## O gate: 9 passes

1. **Passe de direção.** A direção está declarada por escrito e é reconhecível na tela? Um concorrente poderia usar este mesmo design? Se sim, reprova.
2. **Passe de sistema.** Todo valor de cor, espaço, tipo e raio vem de um token. Valor solto reprova o elemento.
3. **Passe de hierarquia.** Ler só os elementos de maior peso visual, em ordem. A leitura conta a história certa?
4. **Passe de clímax.** Existe UM ponto de contraste máximo, e ele coincide com o momento de decisão. Dois clímax é nenhum.
5. **Passe de estados.** Todo elemento interativo tem repouso, sobre, foco, ativo, desabilitado, carregando, erro e vazio, quando aplicável.
6. **Passe de acessibilidade.** Contraste AA, foco visível, teclado completo, alvo de toque mínimo, semântica correta, movimento reduzido respeitado, zoom a 200% sem quebra.
7. **Passe de mobile.** A tela pequena foi re-hierarquizada, não espremida. Testada em aparelho real.
8. **Passe de movimento e performance.** Nenhuma animação no caminho crítico do valor. O conteúdo principal nasce no primeiro paint. Durações dentro da faixa.
9. **Passe de integridade.** Zero placeholder, zero imagem de banco genérica, zero texto simulado, spec anexada, e a copy é a aprovada, não uma versão que o designer editou.

## Score visual (1 a 10 por dimensão)

| Dimensão | Pergunta |
|---|---|
| Intenção | dá para dizer qual é a direção olhando 3 segundos? |
| Hierarquia | o olho vai para onde a decisão está? |
| Clímax | o pico visual coincide com o pico de decisão? |
| Consistência | tudo vem do sistema, ou tem valor solto? |
| Acessibilidade | alguém no teclado, com pouca visão ou com o sol na tela consegue usar? |
| Acabamento | espaçamento, alinhamento óptico, estados, detalhe de borda |

**Abaixo de 42/60, revisar.** Nota 4 ou menos em Acessibilidade reprova sozinha, independentemente da soma.

## Regras de decisão
direção declarada antes do primeiro retângulo · todo valor vem de um token · um clímax por tela · peso visual acompanha peso emocional · densidade é decisão, não acidente de conteúdo · estado faz parte do componente · acessibilidade não é camada final, é restrição de projeto · movimento com função ou nenhum · o conteúdo nasce no primeiro paint · mobile se re-hierarquiza, não se espreme · quem desenha não reescreve a copy · beleza que impede leitura reprova.

## Como se conecta
**Entra:** a estrutura e a intenção emocional por bloco (de quem faz a física), a copy aprovada (de quem escreve), a identidade da marca e as restrições técnicas do projeto.
**Sai:** direção declarada e tokens (modo direção, cedo), telas e spec por bloco, e o código quando pedido (modo execução). Mais o relatório de acessibilidade, que é insumo do gate de publicação.
**Manda em conflito:** acessibilidade e legibilidade. Nenhuma direção de arte justifica texto ilegível ou botão que o teclado não alcança.

## Entregáveis típicos
direção de arte declarada com referências e proibições · conjunto de tokens nomeado · grade e escala tipográfica · limite de caracteres por bloco para quem escreve · telas por bloco com spec · página implementada em HTML e CSS · documentação de componente com variantes, estados e notas de acessibilidade · auditoria WCAG com severidade · crítica de layout com elemento citado · relatório do juiz com os 9 passes e o score.

---
*Manutenção: cada projeto entregue devolve para cá uma direção nova no catálogo, um anti-padrão promovido ou um token que faltava. Exemplos são ilustrativos e fictícios por princípio.*
