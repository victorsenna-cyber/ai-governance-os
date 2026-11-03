# MÉTODO — Kit de Marca

> **Tipo:** método
> **Instituído em:** 18/10/2026 · **Alçada:** {{OPERADOR}} · 🟡 **vigência provisória até o primeiro kit aprovado por um cliente** (`CLAUDE.md` §7.1, item 4). Roteado desde o primeiro dia (REGRA Nº 1).
> **Decisão de alçada ({{OPERADOR}}, 18/10/2026):** o pedido "faça os pilares", para cliente novo ou qualquer outro, envolve também uma análise arquetípica hipotética que entrega um kit completo: fontes/tipografia, cores, arquétipo dominante e os demais, no molde da identidade da casa, em `945-branding/`.
> **Nome:** *kit de marca*, não *mídia kit*. No mercado, mídia kit é o material de audiência para patrocinador (alcance, público, preço de publi), e cliente influenciador entenderia errado.
> **Carrega:** `100-métodos/ARQUETIPOS-DE-MARCA.md` (framework) · `100-métodos/METODO-PRANCHA-DE-ESCOLHA.md` (a escolha) · `90-templates/kit-de-marca/` (blueprint e gerador) · motor de render da casa em `945-branding/01 - identidade visual/sistema/`.
> **Caso de origem:** a identidade da casa (pasta `945-branding/`).

---

## 0. Por que existe

Os pilares dizem **para quem, o quê e por quê**. Não dizem **como a marca aparece**. Sem isso, cada peça da conta escolhe cor e fonte pelo gosto do dia, e o público lê uma marca diferente a cada post. **A pessoa decide em menos de um segundo, pelo que vê, antes de ler** (Dilts: o ambiente é o primeiro nível percebido). Se o ambiente imprime um arquétipo e a fala imprime outro, a fala chega desmentida.

## 1. 🔴 Quando roda

**Junto com os pilares, sempre.** O pedido *"faça os pilares"* entrega dois artefatos: `PILARES.md` (o teste, `METODO-TESTE-DE-PILARES.md`) **e** o kit de marca. **Ordem: pilares primeiro**, porque o kit lê ICP e promessa de lá.

Também roda: conta nova (etapa do `METODO-TRILHO-DE-CONTA-NOVA.md`), pedido de identidade visual, e antes do primeiro criativo visual de uma conta que ainda não tem kit.

## 2. 🔴 Pré-condição

| Insumo | Sem ele |
|---|---|
| `PILARES.md` da conta | o kit não sabe para quem fala. **Roda os pilares antes** |
| **falas literais da própria expert**, com fonte (call, áudio, legenda, transcrição) | a leitura arquetípica sai marcada **hipótese fraca**, e o kit não vai para o cliente sem essa marca |
| o ativo visual atual (site, perfil, logo), se existir | o kit ignora o custo de troca e propõe ruptura sem saber |

## 3. As etapas

| # | Etapa | Saída | Quem |
|---:|---|---|---|
| 1 | **Dossiê de fatos:** quem é e o que vende, 15 a 25 falas literais da expert, 8 a 15 do público, identidade visual atual (hex, fontes, imagens), restrições de tom, lacunas. Tudo com caminho e linha | `dossie-marca.md` (rascunho, fora do repo ou em `_trabalho/`) | subagente `sonnet` |
| 2 | **Leitura arquetípica** (`ARQUETIPOS-DE-MARCA.md`): dominante, da escrita, da borda e sombra. Pessoa × entrega quando houver operação. **Três falas literais para o dominante**; os descartados com o porquê | `KIT-DE-MARCA.md` §1–2 | **Opus** |
| 3 | **Teste da peça:** uma pergunta, derivada do dominante, que toda peça da conta precisa responder | `KIT-DE-MARCA.md` §2 | Opus |
| 4 | **Níveis de Dilts**, de propósito a ambiente: o que já existe na conta e o que falta | `KIT-DE-MARCA.md` §3 | Opus |
| 5 | **Direção:** as cinco perguntas (`10-skills/ui-ux-designer-senior-continuum/referencias/00-direcao-de-arte.md`): quem vê e em que estado, sensação, extremo, o que nunca faz, elemento memorável | `KIT-DE-MARCA.md` §4 | Opus |
| 6 | **Ambiente:** paleta nos nove tokens do motor, **2 a 4 combinações tipográficas** livres (Google Fonts; nunca Inter), paletas alternativas se a cor estiver em aberto, tipos de criativo (do catálogo do motor: N1–N3, P1–P2, B1, C1, D1, ou só os que servem), ambiente de gravação, lista de veto, gate visual de quatro itens | `kit.json` + `KIT-DE-MARCA.md` §5–8 | Opus |
| 7 | **Continuidade com o ativo:** o que o kit mantém do que já existe, o que muda e por quê. **A propriedade do ativo é da cliente, a estrutura é nossa (REGRA Nº 0).** Mudança em ativo no ar sai como recomendação, com custo de troca | `KIT-DE-MARCA.md` §9 | Opus |
| 8 | **Peças com conteúdo real:** 4 a 8 peças, uma por tipo escolhido, texto da própria conta com `_procedencia` | `kit.json` → `pecas` | Opus (subagente pode montar o JSON) |
| 9 | **Gerar:** `python3 90-templates/kit-de-marca/gerar_kit.py "<conta>/<pasta de design>/branding/01 - identidade visual/kit.json"` | `tokens.css`, `saida/`, `prancha-teste.html` + `.png`, `kit.html` + `.png` | ferramenta |
| 10 | **Gate a olho** no PNG (§6), nunca no código | correções no `kit.json` | Opus |
| 11 | **Envio e escolha:** prancha e kit vão como PNG ou PDF, com a nossa recomendação na mensagem (`METODO-PRANCHA-DE-ESCOLHA.md` §4.5). A escolha da cliente entra **literal** no `DECISOES.md` da conta | a frase dela, com data | cliente |
| 12 | **Kit vigente:** os tokens da escolha viram o padrão no `kit.json`, o kit muda de 🟡 para ✅ e ganha uma linha no `ARQUETIPOS-DE-MARCA.md` §4 | kit ✅ | nós |

**Onde mora:** `branding/` dentro da pasta de design da conta (ex.: `05 - design/branding/`; conta sem pasta de design: `branding/` na raiz dela), com `01 - identidade visual/` (o kit) e `02 - posicionamento/` (ponteiro para pilares e narrativa da conta, sem duplicar). Mesma forma da `945-branding/` da casa.

## 4. 🔴 Alçada (REGRA Nº 0)

| Decide | Quem |
|---|---|
| arquétipos, teste da peça, direção, o leque de paletas e tipografias, a lista de veto | **nós.** É estrutura, e perguntar à cliente qual arquétipo ela é devolve o produto sem entregar |
| entre as opções do leque, qual ela prefere | **a cliente**, pela prancha |
| objeção (a cliente diz que aquilo não é ela) | **objeção de congruência**: volta à leitura, resposta por escrito. Nunca vira "escolha o que quiser" |

## 5. Estado e medição

**Todo kit nasce 🟡 hipótese, `n=0`.** O arquétipo vira dado quando o registro de peças da conta ganha as colunas `Arquétipo` e `Linha` (como o `REGISTRO.md` de peças do perfil do {{OPERADOR}}, em `950-marketing/conteudo-perfil/`) e, com três peças por linha publicadas, mostra qual salva, compartilha e gera conversa.

## 6. 🔴 Gate — reprova sozinho

- **dominante sem três falas literais** da própria expert, e o kit não marcado como hipótese fraca;
- **arquétipo do público ou do nicho** lido como o da expert (`ARQUETIPOS-DE-MARCA.md` §2);
- cor ou tipografia **sem justificativa no arquétipo** (gosto não é critério);
- **Inter**, ou fonte paga sem substituta livre declarada;
- kit **sem lista de veto** ou **sem teste da peça**;
- peça do kit com texto **sem procedência**;
- tokens definitivos **sem a escolha literal** da cliente no `DECISOES.md`;
- **pilares entregues sem kit** quando o pedido foi "faça os pilares".

## 7. Fora do escopo

**Logo e naming.** O kit dá a direção do logo (arquétipo, paleta, tipografia, o que nunca faz); o desenho fica com designer. **Foto profissional:** o kit diz a luz, o fundo e a roupa; a produção não é nossa.

## 8. Validação (§9)

Aumenta o valor do G0 sem custo de hora proporcional: o dossiê roda em subagente, o render no motor que já existe, e o Opus gasta a hora na leitura. No ICP B (Alicerce) a conta constrói do zero e precisa disso de qualquer forma; no ICP A, pode virar adicional cobrado.

---
*Base: `945-branding/` (caso de origem) · `CLAUDE.md` §8, REGRA Nº 0.*
