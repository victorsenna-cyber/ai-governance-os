# ÁRVORE — ESCRITA

> **Tipo:** trilho · **Instituído:** 26/09/2026 (onda 5 da auditoria de roteamento de 26/09/2026) · **Alçada:** {{OPERADOR}}
> **Carrega-se quando:** o pedido é **produzir uma peça** — copy, página, VSL, anúncio, proposta, roteiro, conteúdo, mecanismo, pivô.
> **Réguas transversais** (§8 REGRAS Nº 0, 1, 2 · procedência · ordem) **valem aqui e não se repetem.** Esta árvore também guarda, íntegros, a **árvore de copy** (§5) e o **circuito de página** (§6) que moravam no `CLAUDE.md`.

---

## 1. 🔴 Pré-condição — o portão que um caso real pediu

> **Peça para o PÚBLICO de um cliente — copy, página, VSL, anúncio, roteiro, conteúdo — só se escreve se a árvore CONTA já passou:**
> - `clientes/<cliente>/PILARES.md` existe **sem P1 nem P4 reprovando**; **e**
> - `clientes/<cliente>/lexico-icp/` tem **ao menos uma fonte de grau `D`**.
>
> **Senão, o pedido vai para `ARVORE-CONTA.md` — inclusive sob urgência.** Urgência reduz volume, nunca dependência.
>
> ⚠️ **Escopo, corrigido no replay de 26/09:** documento **para o próprio cliente** — proposta, PDF de estrutura, relatório, devolutiva — **não passa por este portão**, porque não fala com o público dele. **Mas pilar reprovando é declarado DENTRO do documento**, na seção do que falta (nosso × seu): empacotar uma divergência sem nomeá-la a transforma em entrega. *(A primeira versão do portão dizia "peça para cliente" e travaria toda proposta — achado de auditoria independente ao testar o portão num documento para o próprio cliente.)*
>
> **Peça NOSSA** ({{EMPRESA}}): `30-comercial/ICP.md` + o léxico do nosso ICP em `30-comercial/`.
> **Proposta:** as âncoras vêm da árvore **NEGÓCIO** antes da peça.
> **VSL:** as três referências **escaladas** vêm da árvore **LEITURA** antes do roteiro.

*Por que é portão e não aviso:* uma rodada de roteiros passou em todos os gates com cenas de ICP inventadas. **Rodou-se o método e o gate; pulou-se a etapa anterior. E o gate aprovou, porque conferia a forma da própria etapa.** Gate não substitui etapa anterior.

## 2. O processo desta árvore

| Tipo | O que se carrega |
|---|---|
| **framework** | `100-métodos/METODO-DIRECT-RESPONSE.md` (tronco) · `100-métodos/METODO-ESTRUTURA-INVISIVEL.md` · `100-métodos/METODO-PONTOS-LOGICOS.md` · `100-métodos/METODO-PIVO-DE-CONVERSAO.md` |
| **trilho** | o **circuito de página** (§6 abaixo) · as fases do `100-métodos/METODO-FUNIL-DE-VSL.md` · a **árvore de copy** (§5 abaixo) |
| **método** | `10-skills/copywriter-senior-continuum/` · `100-métodos/METODO-PRODUCAO-VSL-POR-AGENTES.md` · `100-métodos/METODO-CONSTRUCAO-DE-CRIATIVOS-DR.md` · `100-métodos/METODO-EMPILHAMENTO-DE-HOOKS.md` · `100-métodos/METODO-LATERALIZACAO-DE-CRIATIVOS.md` · `100-métodos/METODO-MECANISMO-E-ONE-BELIEF.md` · `100-métodos/METODO-ANCORAGEM-DE-PROPOSTA.md` |
| **blueprint** | templates do método em uso · `clientes/<cliente>/lexico-icp/` como insumo |
| **política** | **REGRA Nº 0** (estrutura é nossa) · **REGRA Nº 2** (escala) · voz aplicável (do cliente; `voz-operador` só em peça nossa) · `00-core/POLITICAS-DE-DECISAO.md` para preço |
| **gate** | os **11 passes** da skill de copy · anti-slop (módulo 04) · `100-métodos/METODO-GATE-DE-CONGRUENCIA.md` |

## 3. Linhas — sinal → carga → veto

| Sinais | Carga, na ordem do processo | 🔴 Veto |
|---|---|---|
| proposta comercial de qualquer tipo, orçamento, cotação, precificar projeto, renovação, reajuste, "quanto cobrar de X" | **NEGÓCIO antes** → `100-métodos/METODO-ANCORAGEM-DE-PROPOSTA.md` *(método — 7 âncoras, 6 gates A–F, 5 recusas; Âncora 1-bis e Régua 4)* → circuito §6 → anti-slop · formal/contrato: + JURÍDICO | âncora não preenchida nem declarada faltante · **sem bloco de onboarding** · `n` inventado onde é `n=0` · **denominador de produto único** (o denominador é a empresa) · **processo da negociação dentro do documento** — vai na mensagem |
| página de vendas, landing, dobras, CRO de página, "criar uma página para X" | **circuito §6** — entrada sempre pelo `10-skills/gerador-web-designer-senior-continuum/` | sem brief de 9 campos, nada avança · qualquer P0 reprova a publicação |
| direção de arte, design de tela, tokens, acessibilidade, implementação de interface | `10-skills/ui-ux-designer-senior-continuum/` — **etapas 2 e 4 do circuito §6** (modo direção ou execução) · **tela de produto digital** (app, PWA, painel, guia, SaaS): **NEGÓCIO antes**, `100-métodos/METODO-DESENHO-DE-PRODUTO.md` degraus 1 a 4; a skill entra no degrau 5 *(01/11/2026)* | direção genérica · clímax fora da decisão · 🔴 **tela de produto sem os degraus 1 a 4 do desenho de produto escritos** |
| VSL, vídeo de vendas, funil de VSL, vender para público frio, perpétuo, roteiro de vídeo de vendas | 🔴 **antes: VSL é o formato ESCALADO neste nicho?** (REGRA Nº 2) → **LEITURA** (3 VSLs escaladas via `METODO-DESTILACAO-DE-VSL`) → `100-métodos/METODO-FUNIL-DE-VSL.md` *(método — 5 blocos, escrita de trás para frente)* → **escrita do roteiro: `100-métodos/METODO-PRODUCAO-VSL-POR-AGENTES.md` *(método — 6 geradores, 6 auditores e juiz em `.claude/agents/vsl-*`; esqueleto aprovado antes do texto; auditores em contexto próprio; ✅ vigente, roda no Claude Code CLI)*** → circuito §6 → **edição com imagens ilustrativas → OPERAÇÃO: `40-operacao-rotinas/ferramentas/video-por-codigo/README.md`** *(aviso de 20/10: motor HyperFrames + biblioteca de 703 prompts)* | pilares P1/P4 reprovando · **peça gravada sem o laudo do A7** (compreensão do ouvinte frio por tempo + coerência global; `40-operacao-rotinas/ferramentas/tempo-vsl.py`) · **rodada fechada sem a composição da VSL** (§4.4 do método; `40-operacao-rotinas/ferramentas/composicao-vsl.py`) · **capital para 2–3 tentativas não reservado** · ativos mínimos ausentes · **roteiro escrito e auditado no mesmo contexto** |
| anúncio de resposta direta (destino quiz, VSL, página ou conversa), "escreve o anúncio", mecanismo do problema e da solução, CTA com valor | `100-métodos/METODO-CONSTRUCAO-DE-CRIATIVOS-DR.md` *(método)* + `100-métodos/METODO-PONTOS-LOGICOS.md` (mecanismo) + skill de copy (00–04; +06 vídeo; +08 reenquadre) + voz + léxico · com mídia: `METODO-TRAFEGO-PAGO.md` §4 | **anúncio não abre o circuito de página** salvo destino a criar ou refazer · 🔴 *(12/10)* texto longo que carrega a venda: **deleção na tese, no mecanismo ou na oferta** e **colchete de fato aberto na mídia** (§4.2-bis do método) · 🟡 vigência provisória |
| empilhar ganchos, abertura composta, "quantos hooks tem esse vídeo", auditar sequência de abertura | `100-métodos/METODO-EMPILHAMENTO-DE-HOOKS.md` *(método)* + skill 03–04 + léxico · vale para peça nova · derivar de vencedor chama lateralização | dividir a frase em três linhas não é empilhar |
| lateralizar anúncio, variação de vencedor, "faz mais versões desse que vende", renovar criativo validado | `100-métodos/METODO-LATERALIZACAO-DE-CRIATIVOS.md` *(método)* + evidência da base + `METODO-TRAFEGO-PAGO.md` §4.2 e §7.3 | **sem base com resultado documentado é exploração**, e se chama assim |
| roteiro de vídeo curto, Reels, gancho/hook orgânico, carrossel, "por que meu vídeo não performa", **"não sei o que postar", "travei na hora de gravar"** | skill de copy **módulo 06** (**§11.1-bis: escolher o SENTIMENTO antes do assunto** — curiosidade · surpresa · identificação · aprendizado · tensão) + voz + `lexico-icp/` · com mídia: tráfego §4 | 🔴 **identificação é bloco de espelho: o sentimento mais fácil de fabricar** · sentimento não declarado antes do assunto |
| conteúdo, narrativa, linha editorial | `10-skills/heads/head-conteudo.skill.md` *(persona — decide)* → skill de copy módulo 06 *(executa)* | — |
| **apresentar opções visuais para escolha**: identidade visual de cliente, tipografia, paleta, linha de criativo, direção de página, "monta as opções pro cliente escolher", prancha *(instituído 18/10/2026)* | `100-métodos/METODO-PRANCHA-DE-ESCOLHA.md` *(método — 🟡 provisório)* → direção (`ui-ux-designer-senior-continuum` modo direção) → leitura de referências em lote → `945-branding/01 - identidade visual/sistema/render.py` com `tokens.css` da conta → `90-templates/prancha-de-escolha/gerar_prancha.py` → escolha literal no `DECISOES.md` da conta | opção que não assinaríamos · mais de uma variável por linha · texto sem procedência · escolha não registrada literal |
| **arte de peça do perfil do {{OPERADOR}}**: story, post, carrossel, capa de reel, estático, "monta a arte", "cria o criativo", cor, fonte, identidade visual, branding *(instituído 18/10/2026)* | texto pela linha de cima (módulo 06 ou resposta direta) → `945-branding/01 - identidade visual/IDENTIDADE-VISUAL.md` *(blueprint: escolher o tipo N1–D1)* → `sistema/render.py` → gate visual §7 → linha no registro de peças publicadas de `950-marketing/conteudo-perfil/` com `Arquétipo` e `Linha` · **peça de cliente não usa a identidade do {{OPERADOR}}: usa o kit da conta** (linha abaixo) |
| **arte de peça de cliente**: criativo visual, estático, story, carrossel para o público de uma conta *(instituído 18/10/2026)* | `clientes/<cliente>/<pasta de design>/branding/01 - identidade visual/KIT-DE-MARCA.md` + `kit.json` → o mesmo motor (`945-branding/01 - identidade visual/sistema/render.py`, que lê o kit da conta) → gate visual do kit (§8 dele) · **conta sem kit: ARVORE-CONTA, linha do kit de marca, antes** | criativo visual de conta **sem kit de marca** · item da lista de veto do kit · peça sem `_procedencia` · **dois pontos de luz** · item da lista de veto (azul, roxo, dourado metálico, condensada com cor de alarme) |
| **criativo modelado de uma referência** da `960-referências criativos/` ("faz uma versão dela", "modela desse", "igual a essa referência") *(instituído 18/10/2026, alçada {{OPERADOR}})* | `960-referências criativos/LEIA-ME-MODELAGEM.md` *(regra)* → medir a referência no pixel e escalar → montar → comparação lado a lado salva em `referencias/` do lote · cor da conta decidida no planejamento | 🔴 **proporção, composição ou elemento diferente da referência sem aprovação do {{OPERADOR}} ou sem sinalização escrita na entrega** · mecanismo da referência perdido (copiou o estilo, não o que faz funcionar) · texto na moldura de um formato "print" · foto real simulada em desenho |
| peça (anúncio, página, VSL, roteiro, proposta) que toca **assunto regulado**: saúde, dependência química, medicamento, alimento, crédito e investimento, promessa de resultado, dado pessoal, internação *(instituído 22/10/2026)* | antes de publicar: `80-juridico/FONTE-LEGISLACAO.md` → a norma do tema no acervo de legislação indicado lá · **CONAR e as políticas de anúncio da Meta e do Google não estão no acervo:** conferir por fora | afirmação legal sem norma apontável · termo que a lei veda para aquele tipo de serviço (a norma apontada por artigo, não o termo de memória) |
| pontos lógicos, tese de marketing, "o argumento não fecha", cadeia de raciocínio, mecanismo da VSL, "por que a pessoa deve acreditar" | `100-métodos/METODO-PONTOS-LOGICOS.md` *(framework — 3 padrões, dose 5–8)* → `100-métodos/METODO-MECANISMO-E-ONE-BELIEF.md` (o **destino** da cadeia) | elo que não derruba o seguinte · **conclusão escrita na peça** · cadeia sem destino · aplicar a conteúdo de topo |
| nomear mecanismo, apelido, one belief, crença central, "qual é a tese", batizar a oferta | `100-métodos/METODO-MECANISMO-E-ONE-BELIEF.md` *(método)* | apelido **sem mecanismo construído** · Nova Oportunidade igual ao apelido · **apelido variado — sinônimo desancora** |
| estrutura invisível, "estrutura dentro da estrutura", elementos da copy, modelar × copiar, ordem dos argumentos | `100-métodos/METODO-ESTRUTURA-INVISIVEL.md` *(framework)* → skill de copy **módulo 09** | texto transposto da referência · dose fora de ±15% · modelar sequência em peça de degrau 3 |
| pivô, "onde a peça vira", E · Mas · Por isso, peça que só acumula acordos | `100-métodos/METODO-PIVO-DE-CONVERSAO.md` *(framework)* → skill de copy passe 3 | pivô não apontável por linha |

## 4. Desempate interno

- 🔴 **Onde a peça de cliente é salva (25/10/2026, alçada {{OPERADOR}}):** página, site e quiz do cliente → `clientes/<Cliente>/NN - web design/` (e a config de publicação junto) · plano e scripts de campanha → `clientes/<Cliente>/NN - tráfego pago/`. Nunca em `30-comercial/`.
- **"Criativo"** sem mais nada: mídia (campanha, CPA) → OPERAÇÃO · redação do anúncio → linha de resposta direta · conteúdo orgânico → módulo 06. **Conteúdo orgânico não entra em resposta direta por conter a palavra "criativo".**
- **"Hook"**: anúncio → empilhamento · Reels/orgânico → módulo 06.
- **Criativo que cansou** → OPERAÇÃO primeiro (diagnóstico de mídia); só com base vencedora documentada volta para cá (lateralização).
- **Mecanismo:** montar o argumento → pontos lógicos · dar nome → mecanismo e one belief. **Nunca nomear antes de montar.**

---

## 5. ÁRVORE DE COPY — combinações obrigatórias *(movida íntegra do `CLAUDE.md` §6.1 em 26/09/2026)*

**Skill-mãe de escrita: `10-skills/copywriter-senior-continuum/` (v3.2, 28/10/2026).** Ela é autocontida, portátil e genérica por decisão: absorve régua da linguagem, camada de nuance (Schwartz, coreografia de tensão e objeções, copy↔visual), gate anti-slop, o pivô **E · Mas · Por isso** e o método de conteúdo e roteiro. **Todo roteamento vive aqui, nunca dentro da skill.** Fonte instalável na oficina de skills (`900-…/`); edita-se lá e publica-se em `10-skills/`.

Legado, em `10-skills/_legado/` (fonte histórica, leitura, nunca carregar): `copywriting-fable5` · `copywriting-avancado` · `stop-slop` · `criativos-video` · `pagina-de-vendas` · `METODO-PAGINA-DE-VENDAS-v2.0`. Os caminhos antigos continuam existindo como ponteiros, para referência velha aterrissar na explicação e não em erro.

Todo pedido de escrita segue esta combinação — sem exceção:

- **Página de vendas / landing** → não é pedido de copy, é pedido de circuito. Ver **§6.3**. A skill de copy entra como etapa 3, nunca como porta de entrada.
- **Peça-mestra (página, VSL, sequência de lançamento, campanha)** → mesma combinação, esquadrão completo (9 papéis) e gate dos 10 passes.
- **Bastidor, story, legenda ou mensagem sobre o nosso trabalho, e-mail de atualização, relatório para cliente** *(28/10/2026, v3.2)* → `10-skills/copywriter-senior-continuum/` (módulos 02, 04, **10**) + voz de quem assina. **Sinal:** o pedido mostra algo que fizemos (print, tela, resultado). **Carga:** a imagem ou o fato, depois a skill. 🔴 **Veto:** primeira linha que responde "e daí?" (moldura de tempo, anúncio do assunto, nome antes do efeito, descrição da imagem) reprova sozinha, inclusive em legenda de uma linha. Peça do perfil do {{OPERADOR}} vai para `950-marketing/conteudo-perfil/` e entra no registro de peças quando publicada.
- **Anúncio, hook, e-mail** → `10-skills/copywriter-senior-continuum/` (módulos 00, 02, 03, 04) + voz aplicável. 🔴 **Nomear mecanismo saiu daqui em 20/09/2026: é `100-métodos/METODO-MECANISMO-E-ONE-BELIEF.md`** — a skill nunca teve régua de nomeação, e o pedido caía num lugar que não sabia respondê-lo. **Adicionar o módulo 08** quando o comprador se orgulha da própria competência ou o mercado já ouviu a promessa.
- **Conteúdo, roteiro de vídeo curto, carrossel, linha editorial** → `10-skills/copywriter-senior-continuum/` (+ módulos **01** e 06) + voz aplicável + **`clientes/<cliente>/lexico-icp/`**. 🔴 **Antes do primeiro roteiro:** preencher o **brief mínimo de conteúdo** — campos 2 (ICP e léxico), 5 (provas), 6 (origem do tráfego) e 8 (voz) do brief de 9 campos, com a regra do campo vazio valendo igual (*"campo vazio vira pergunta ao dono da oferta, nunca invenção"*). **Campo 2 vazio PARA a produção.** O **arqueólogo** entra no esquadrão e o **módulo 01** é carregado: cena, fala de ICP e léxico entram com fonte apontada e grau de procedência, ou a peça não sai.

> 🔴 **As duas réguas que esta linha existe para sustentar**:
>
> **1. Procedência.** Nenhuma cena, dor, objeção ou fala de ICP entra numa peça sem fonte rastreável. O teste é de dez segundos: apontar **quem disse aquilo e onde**. Se a resposta for *"é plausível"*, a cena sai.
>
> 🔴 ⭐ **3. Alçada (instituída 15/09/2026).** A regra do campo vazio vale para **lacuna de fato** — e os quatro campos do brief mínimo acima (2, 5, 6, 8) são todos de fato, por isso ela se aplica inteira aqui. **Ela não vale para lacuna de estrutura:** promessa, mecanismo, narrativa, headline, gancho, ordem de elemento e recorte de público **se decidem, nunca se perguntam.** Ver `METODO-ALCADA-DE-ESTRUTURA.md` e a REGRA Nº 0 do §8.
>
> **2. Ordem.** **Pedido urgente de cliente não altera a ordem de dependência da entrega.** Copy depende de ICP, ICP depende de diagnóstico. Quando a urgência é real, **reduz-se o volume, nunca a dependência**: uma peça com procedência vale mais que dez sem. **Esta régua é de conduta — nenhum gate de skill opera sobre material que não foi colhido.**
- **Criativo de tráfego para cliente** → matriz do `METODO-TRAFEGO-PAGO.md` §4 + `10-skills/copywriter-senior-continuum/` (módulos 03, 04, 06, com o ajuste de mídia paga) + voz do cliente. **Nunca** `voz-operador`.
- 🔴 ⭐ **Anúncio de resposta direta (destino quiz, VSL, página ou conversa) — instituído 20/09/2026** → `100-métodos/METODO-CONSTRUCAO-DE-CRIATIVOS-DR.md` + skill de copy (módulos 00, 01, 02, 03 e 04; **+ 06** para execução em vídeo; **+ 08** no gatilho de reenquadre) + voz e `clientes/<cliente>/lexico-icp/`. Abertura composta chama `METODO-EMPILHAMENTO-DE-HOOKS.md`, **inclusive em peça nova**; derivação de vencedor chama `METODO-LATERALIZACAO-DE-CRIATIVOS.md`. **Conteúdo orgânico não entra aqui por conter a palavra "criativo":** Reels, carrossel e linha editorial seguem no módulo 06. Os vetos de procedência, a REGRA Nº 0 e o bloqueio por P1/P4 valem inteiros. 🔴 **As mudanças de 20/09 nos módulos 03 e 06 e os três métodos estão em vigência provisória:** carregam e valem para executar agora, e só viram definitivos com o `.zip` regerado, depois da verificação em caso real.
- **Prospecção/venda na voz do {{OPERADOR}}** → `METODO-ABORDAGEM-FRIA.md` + `voz-operador.skill.md` (**duas camadas — ficha de assinatura de metamodelo e gate prescritivo; governa também a FALA, com checklist pré-call**) + `10-skills/copywriter-senior-continuum/` (gate, módulos **01** e 04). 🔴 **Instituído 10/09/2026:** mensagem fria é feita de bloco de espelho (*"você provavelmente já tentou…"*, *"o que costuma acontecer com quem…"*), e **é a peça em que mais inventamos, porque o prospect ainda não falou conosco.** O passe 11 vale aqui igual: **a cena vem do banco de léxico do NOSSO ICP** (`30-comercial/`), ou a mensagem descreve o que observamos no site e no perfil dele — fato verificável — em vez de afirmar o que ele sente.
- **Peça para um terceiro falar (cliente, futuro vendedor)** → estrutura do método + voz da pessoa. **Nunca** `voz-operador`.
- **Peça que define um resultado** (página, oferta, plano estratégico, diagnóstica) → adicionar `geracao-de-resultados.skill.md` (PNL + cocriação): promessa no positivo, evidência/prova, específica, na identidade do público. Quando o público tem uma linguagem de cocriação própria, usá-la como ponte nativa (autoria, nunca culpa).
- **Qualquer copy voltada a humano** cruza o gate anti-slop (módulo 04) antes de sair. Documento interno de governança não cruza (tom neutro-claro).
- 🔴 ⭐ **`100-métodos/METODO-PONTOS-LOGICOS.md` (13/09/2026, autoria de João Campos) — obrigatório em todo bloco de mecanismo, tese ou argumentação.** **Cadeia, não lista.** O gate é o **teste de encadeamento**: remova o elo N, e se o elo N+1 ainda se sustenta, não era cadeia. **A conclusão não se escreve** — os elos se põem e o último passo fica com o leitor. ⚠️ **E o limite ético é de forma indistinguível: a técnica funciona porque a conclusão parece própria; se os elos forem verdadeiros ela É própria, e se algum for falso vira manipulação.** É o que torna o gate de procedência inegociável aqui.
- ⭐ **Camada transversal, instituída 13/09/2026 — `100-métodos/METODO-ESTRUTURA-INVISIVEL.md`.** **A unidade de trabalho da escrita deixa de ser o parágrafo e passa a ser o ELEMENTO.** Revisar deixa de ser ler e passa a ser **contar**: a sequência está completa e na ordem? **E o pivô ganha instrumento — ele é uma transição nomeada, uma posição na sequência, não uma qualidade difusa do texto.** 🔴 ⭐ **Publicado na skill em 20/09/2026 como módulo 09** (a propagação estava declarada como prioridade alta desde 13/09 e não tinha sido feita — sete dias em que o método sabia medir e a skill não sabia o que fazer com a medição). **O passe 3 do gate passa a apontar o elemento `transição` que carrega o "Mas".** 🟡 Vigência provisória até caso real. Aplica-se a toda peça de conversão; **não se aplica a peça de reenquadre de categoria (módulo 08), onde quebrar a sequência é o argumento.**
- **Regra de saída (vale para toda peça):** o pivô **E · Mas · Por isso** precisa caber em uma frase e ser apontável por linha. Peça que é só acúmulo de acordos ("E, e, e") não sai.
- 🔴 ⭐ **Proposta comercial (instituído 17/09/2026, alçada {{OPERADOR}}).** Proposta **não é documento, é peça de conversão**, e segue esta árvore como qualquer página: circuito §6.3 + skill de copy + gate anti-slop + `METODO-ANCORAGEM-DE-PROPOSTA.md` §0-ter. **Três réguas:** (1) arquitetura de conversão obrigatória, com curva de tensão e custo da inação antes do preço; (2) **o onboarding é parte vendida** — bloco que responde o que acontece nas primeiras 48h, o que o cliente entrega, como recebe, qual a cadência e **quanto tempo dele consome**, que é a pergunta que ninguém faz em voz alta; (3) **pressuposição nunca vira afirmação** — varredura frase a frase, e o que se depreende sai ou vira leitura declarada. **Bloco de onboarding ausente reprova a proposta inteira.**

---

## 6. CIRCUITO DE PÁGINA DE VENDAS *(movido íntegro do `CLAUDE.md` §6.3 em 26/09/2026)*

"Criar uma página de vendas para X" não carrega uma skill: **abre um circuito de três skills, em cinco etapas.** Este bloco é a única coisa que precisa estar aqui; a classificação, os gates e os papéis vivem dentro das skills, que são genéricas e portáteis.

**A entrada é sempre o gerador.** Nunca começar pela copy nem pelo design. O `10-skills/gerador-web-designer-senior-continuum/` classifica o pedido em 4 eixos antes de existir qualquer dobra: **ticket** (baixo, médio, alto, medido pelo tipo de decisão que exige, não pelo valor) · **modelo de entrega** (infoproduto, serviço feito para o cliente, negócio local, assinatura, software) · **ato de conversão** (compra direta, conversa por mensagem, agendamento, aplicação) · **temperatura e consciência**. Não existe skill de roteamento separada: a classificação é o módulo 00 do gerador.

| # | Etapa | Skill | Entrega | Veto |
|---|---|---|---|---|
| 1 | **Física** | `10-skills/gerador-web-designer-senior-continuum/` | classificação, brief de 9 campos, esqueleto dobra a dobra, curva numerada, extrato de crença, briefing visual por bloco | sem brief, nada avança |
| 2 | **Direção visual** | `10-skills/ui-ux-designer-senior-continuum/` (modo direção) | direção de arte declarada, tokens, grade, escala, **limite de caracteres por bloco** | direção genérica volta |
| 3 | **Escrita** | `10-skills/copywriter-senior-continuum/` | copy final por bloco, com pivô, régua e intenção visual | copy sem pivô volta |
| 4 | **Execução visual** | `10-skills/ui-ux-designer-senior-continuum/` (modo execução) | telas, spec por bloco, código quando pedido | clímax fora da decisão volta |
| 5 | **Gate** | gerador, papel do juiz | veredito de publicação, consolidando os três gates | qualquer P0 reprova |

**Por que a ui-ux entra duas vezes.** Antes, para dar restrição: quem escreve precisa saber quantos caracteres cabem num título e se a marca aceita bloco escuro. Depois, porque desenhar sobre texto real é diferente de desenhar sobre texto simulado. Direção só no fim recebe copy que não cabe; direção só no início desenha para um texto que ainda não existe.

**Fronteiras que não se cruzam:** quem faz a física não escreve a frase nem escolhe a fonte · quem escreve não muda a ordem das dobras · quem desenha não reescreve a copy nem move o clímax. Violação volta para o dono do artefato, não se resolve no lugar.

**Quando o circuito encolhe:** auditar página existente roda 1 e 5 · trocar a oferta roda 1 parcial, 3 e 5 · refazer só o visual roda 2, 4 e 5 · decidir se vale ter página para na etapa 1. **Nunca encolhem:** a classificação, o brief e o gate.

**Combinações obrigatórias que o circuito herda:** voz do cliente na etapa 3 (nunca `voz-operador` em peça de cliente) · par anúncio↔primeira dobra com `METODO-TRAFEGO-PAGO.md` §4 quando há mídia paga · preço e capacidade validados contra `00-core/POLITICAS-DE-DECISAO.md` · garantia condicional espelhada em contrato (`80-juridico/`) · peça que define resultado adiciona `geracao-de-resultados.skill.md`.

---
*Linhas migradas do roteador v1 (R10, R15–R17, R19, R23, R24, R28, R33, R38–R40) e do ponto cego roteado em 26/09 (pivô). §5 e §6 são cópia literal das seções 6.1 e 6.3 do `CLAUDE.md` de 26/09, feita por script..*
