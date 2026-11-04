# SKILL — Extração de Linguagem (operacional do MEL v3)

> **Fonte completa:** `100-métodos/Método de extração de linguagem/METODOLOGIA CONTINUUM DE EXTRAÇÃO DE LINGUAGEM.md`
> **Quando carregar:** todo pedido de perfil linguístico, skill de voz, mapa de comunicação, "extrai a voz de X", ou auditoria de copy contra voz.
> **v3:** adiciona a **Camada 2.5 — Padrões de Linguagem** (metamodelo/Milton, critérios+valores+equivalência complexa, atos de fala+pressuposições, submodalidades+prosódia-transe). Representacional, raciocínio, ensino, método e taxonomia **já eram v2** — rodar sempre, não pular.

## Sequência obrigatória

1. **Corpus:** listar fontes e classificar (espontânea / ensinando / vendendo / escrita / assistida-IA). Assistida-IA = referência de marca, não evidência de voz.
2. **Filtrar** mecanicamente só as falas da pessoa (regex pelo prefixo do falante).
3. **Camada 1 — Superfície** (sempre): tom · vocabulário-assinatura · metáforas · ritmo/prosódia · rituais de abertura/fechamento · evitações · intensidade.
4. **Camada 2 — Percepção/raciocínio:**
   - **VAK+D quantificado** (sempre): contar predicados por sistema (script), descontar verbos neutros de fala e muletas, reportar **% + n + sequência típica** (ex.: C→V→D).
   - **Metaprogramas com %** (se houver fala de decisão): busca/afastamento · referência int/ext · chunk · opções/procedimentos · match/mismatch.
   - **Arquitetura de raciocínio** (sempre): gatilho de entrada → forma (linear/espiral/associativa) → conectores → digressão+retorno → tipo de inferência → fechamento.
   - **Marcadores somáticos** (se declarados) · **Submodalidades** (sempre): brilho/cor/distância (V), volume/ritmo/tom (A), calor/pressão/textura/local no corpo (C) — o "volume" dentro do sistema, base da direção de arte.
5. **Camada 2.5 — Padrões de linguagem (v3):**
   - **Metamodelo** (sempre): generalizações · apagações (nominalizações, comparativos sem referente) · distorções (leitura mental, causa-efeito).
   - **Milton Model** (se houver fala de indução/ensino/transe): pressuposições, causa-efeito suave, "e" encadeador, vagueza artful. Cruzar com prosódia-transe.
   - **Critérios + hierarquia de valores** (sempre): palavras-critério contadas + ordem de prioridade quando colidem → eixos da promessa e filtro de público.
   - **Equivalência complexa + crenças** (sempre que houver crença operante): os X=Y e os "se…então" que ela trata como óbvios. Nunca contrariar núcleo.
   - **Atos de fala + pressuposições** (sempre): o que ela *faz* ao falar (comanda/convida/pede/promete/declara) → gramática do CTA; o que pressupõe como já-verdadeiro → pressuposições da copy.
   - **Prosódia-transe** (se houver indução): onde acelera/suspende/repete/baixa para mover estado → curva de cadência das dobras.
6. **Camada 3 — Universo/transmissão** (módulos conforme corpus): cosmologia operativa · taxonomia+ontologia simbólica · extração de método (com **lacunas**) · arquitetura de ensino · código de objeções · matriz de identidade narrativa.
7. **Saídas:** Perfil Linguístico → Mapa de Comunicação (presente ao cliente) → Skill de voz (1–2 págs) → protocolo de auditoria.

## Regras duras

- **≥3 citações literais por estrutura** — senão `sinal fraco — não afirmar`.
- Percentual **só por contagem** (reportar n e ajustes). Nunca por impressão. Vale também para critérios (2.5.3).
- Módulo sem corpus = `não observável neste corpus`. Não deduzir.
- Voz ≠ tema: descontar vocabulário de assunto do VAK.
- Sistema (2.1) ≠ submodalidade (2.5): canal vs. volume — não confundir.
- Milton/atos de fala: usar os **da pessoa**, nunca os de copywriter genérico.
- Não contrariar equivalência-núcleo (2.5.4) nem cosmologia (3.1) para "vender melhor".
- Skill de voz resultante entra na árvore de copy do CLAUDE.md §6.1 (+ o gate anti-slop, `10-skills/copywriter-senior-continuum/referencias/04-gate-antislop.md`, sempre).

## Auditoria de copy contra o perfil (gate de saída)

- grep termos proibidos = 0
- 1ª dobra abre no sistema representacional dominante e segue a sequência da pessoa
- **submodalidades da pessoa presentes na direção de arte** (o que ela vê brilhante/próximo/quente é o que a página torna assim)
- conectores e ritmo dela presentes (≥1 assinatura por seção); cadência das dobras segue a curva de estado dela
- **CTA no ato de fala dominante** (convite ≠ comando-direto ≠ declaração)
- **pressuposições no lugar de argumentos** onde ela pressuporia; **nenhuma equivalência-núcleo ou cosmologia contrariada**
- entidades simbólicas na fase/nível certo da ontologia
- objeções tratadas no código dela (não no genérico)
- persona narrativa certa para a seção
