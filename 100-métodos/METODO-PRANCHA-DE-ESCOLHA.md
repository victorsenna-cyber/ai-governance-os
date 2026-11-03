# MÉTODO — Prancha de Escolha

> **Tipo:** método
> **Instituído em:** 18/10/2026 · **Alçada:** {{OPERADOR}} · 🟡 **vigência provisória até a primeira prancha apresentada a um cliente** (`CLAUDE.md` §7.1, item 4). Roteado desde o primeiro dia (REGRA Nº 1).
> **Gatilho:** decisão de alçada de {{OPERADOR}} (18/10/2026), a partir da prancha de teste da própria identidade: esse tipo de prancha passa a ser o padrão para criarmos para clientes e apresentarmos para escolha.
> **Aplica-se a:** toda decisão visual em que alguém escolhe entre opções: identidade de marca, tipografia, paleta, linha de criativo, direção de página. Cliente primeiro; vale também para o {{OPERADOR}}.
> **Ferramentas:** gerador da prancha em `90-templates/prancha-de-escolha/` · renderizador das opções, o motor em `945-branding/01 - identidade visual/sistema/` (`render.py`, aceita tokens de cliente).
> **Caso que originou:** a identidade visual da própria casa (prancha de referências, prancha de teste, escolha do {{OPERADOR}} registrada em `IDENTIDADE-VISUAL.md`, na `945-branding/`).

---

## 0. Por que existe

Pedir ao cliente "qual estilo você prefere" devolve a ele uma decisão sem instrumento, e ele escolhe pelo que já viu. Mostrar uma peça só obriga a acertar de primeira. **A prancha resolve as duas coisas: o cliente vê as opções lado a lado, com o conteúdo dele, e escolhe por olho em minutos.** A resposta pode vir em uma única mensagem.

## 1. 🔴 A régua que concilia com a REGRA Nº 0

A estrutura de conversão é nossa (`CLAUDE.md` §8, REGRA Nº 0). A prancha não devolve essa decisão ao cliente:

> **Nós definimos o leque. O cliente escolhe dentro dele.** Toda opção que entra na prancha já passou no nosso gate. **Nunca se apresenta uma opção que não assinaríamos.**

- O ativo é dele (marca, perfil); o gosto entre opções equivalentes é dele. **Quem decide se uma opção converte somos nós, antes da prancha.**
- Objeção do cliente a todas as opções é **objeção de congruência**: volta ao diagnóstico, com resposta por escrito. Nunca vira "ele escolhe o que quiser".

## 2. As duas pranchas

| Prancha | O que mostra | Quando |
|---|---|---|
| **De referências** | as finalistas da leitura de referências, agrupadas por tipo de criativo, com **o que modelar** e **o que mudar** em cada uma | quando há referência (do cliente ou levantada por nós) |
| **De teste** | **as mesmas peças renderizadas** em cada opção (tipografia, paleta, linha), com o conteúdo real do cliente | sempre, antes de fechar a identidade |

## 3. O procedimento

| # | Etapa | Saída | Quem |
|---:|---|---|---|
| 1 | **Direção escrita** (as cinco perguntas, `10-skills/ui-ux-designer-senior-continuum/referencias/00-direcao-de-arte.md`) a partir do arquétipo da conta | um parágrafo de direção | nós |
| 2 | **Leitura das referências** em lotes de ~45 por subagente: uma linha por imagem, nota 0–3 contra a direção, o que mudar | `LEITURA-REFERENCIAS-<data>.md` na conta | subagentes (`sonnet`) |
| 3 | **Conferência a olho** das finalistas pelo Opus; corrigir nota quando o subagente errou, e registrar a correção | finalistas confirmadas | nós |
| 4 | **Prancha de referências** | `prancha-referencias.html` | nós, pelo gerador |
| 5 | **Tokens provisórios** da conta (`tokens.css` próprio, copiado do sistema e ajustado) | `tokens.css` da conta | nós |
| 6 | **Render das opções:** a mesma peça, com conteúdo real e procedência, em cada opção. **Uma variável por linha da prancha** | PNGs | nós, pelo renderizador (`render.py`) |
| 7 | **Prancha de teste** | `prancha-teste.html` (+ PNG ou PDF para enviar) | nós, pelo gerador |
| 8 | **Escolha do cliente, literal**, registrada no `DECISOES.md` da conta | a frase dele, com data | cliente |
| 9 | **Tokens definitivos + documento de identidade** da conta | `IDENTIDADE-VISUAL.md` da conta | nós |

**Envio ao cliente:** a prancha vai como imagem ou PDF (renderizada pelo Chrome, `--png` no gerador). O HTML é de uso interno.

## 4. As regras de composição

1. **Uma variável por linha.** Se a linha compara tipografias, cor, texto e tipo de peça ficam iguais. Duas variáveis mudando juntas tornam a escolha ilegível.
2. **Conteúdo real, com procedência.** Nada de *lorem ipsum* nem frase inventada: o texto sai de peça, call ou fonte da conta (`_procedencia` no JSON).
3. **De 2 a 4 opções por decisão.** Uma é imposição; cinco ou mais viram cardápio.
4. **Legenda curta e técnica** em cada opção: o que muda, em uma linha. A prancha não argumenta.
5. **A recomendação nossa vai fora da prancha**, na mensagem. A prancha mostra; a mensagem recomenda.
6. **A escolha pode ser múltipla.** Duas opções podem valer ao mesmo tempo, conforme a composição. Isso vira regra de uso no documento de identidade, não "empate".

## 5. 🔴 Gate — reprova sozinho

- opção na prancha que **não passou no gate visual** da casa (ou seja, que não assinaríamos);
- **mais de uma variável mudando** entre as opções de uma mesma linha;
- texto **sem procedência**;
- **escolha do cliente não registrada literalmente** no `DECISOES.md` da conta antes de virar token.

---
*Base: `945-branding/` (caso de origem) · `CLAUDE.md` §8, REGRA Nº 0 · `10-skills/ui-ux-designer-senior-continuum/`.*
