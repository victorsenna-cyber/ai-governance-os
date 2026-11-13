# MÉTODO — GATE DE CONGRUÊNCIA

> **Tipo:** gate · secundário: índice (§3), framework (§1) *(reclassificado por auditoria independente de leitura integral; antes: "método-raiz (camada 2)")* · **Origem:** casa de origem do template · **Alçada:** {{OPERADOR}}
> 🟡 **VIGENTE PARA EXECUTAR, VERIFICAÇÃO EM CASO REAL PENDENTE.** Roteado desde o primeiro dia (REGRA Nº 1).
> **O que é:** o auditor que checa o output **contra os métodos que a requisição carregou**, ponto a ponto.
> **Por que existe:** temos 20+ métodos, cada um com gate próprio, **e nenhum deles audita o conjunto.** Um pedido simples carrega cinco métodos e **nada verifica que a resposta honrou os cinco.**

---

## 1. 🔴 O DIAGNÓSTICO — o que existe hoje, e o que não existe

**A pergunta que originou este método: todo output bate contra um auditor que checa congruência ponto a ponto? A resposta honesta, na origem, era NÃO.**

### O que já existe ✅

| Instrumento | Cobre |
|---|---|
| `copywriter-senior-continuum` — juiz, 11 passes, veto binário | **peça de copy voltada a humano** |
| `gerador-web-designer-senior-continuum` — juiz de publicação | **página** |
| **7** métodos com gate de saída declarado + **3** com gate sob outro nome (`O GATE`, `VERIFICAR`, gate de passagem) | **o artefato daquele método** |
| `00-core/COMPLIANCE-DE-OUTPUT.md` | modo, camada de ver, classe de PDF |

### 🔴 Os cinco buracos

| # | Buraco | Consequência |
|---:|---|---|
| **1** | 🔴 **Nenhum gate audita ENTRE métodos.** Cada um checa o próprio artefato contra as próprias regras. **Os gates não sabem que os outros existem** | carga de cinco métodos, cinco gates isolados, **zero verificação do conjunto** |
| **2** | 🔴 **Output que não é peça não cruza gate nenhum.** Análise, diagnóstico, recomendação, registro, resposta de conversa — **e é a maior parte do que se produz aqui** | o gate de copy só pega copy. O resto sai sem rede |
| **3** | 🔴 **Ninguém declara o que carregou.** Sem a lista, **não existe "ponto a ponto" possível** — o auditor não sabe contra o quê | é o buraco que impede fechar os outros quatro |
| **4** | **A autoauditoria é do mesmo contexto que produziu.** A skill manda não escrever e auditar na mesma resposta — **é convenção, não mecanismo** | auditoria colada na escrita vira justificativa |
| **5** | ⚠️ **22 dos 32 arquivos de `100-métodos/` não têm gate de nenhum tipo** — parte é registro, auditoria datada e ponteiro, que não produzem output; o resto é dívida | carregar um deles não produz verificação nenhuma |

> **O buraco 3 é a chave, e é por onde este método começa.** Auditoria ponto a ponto exige **declarar contra que pontos.**

---

## 2. ⭐ AS DUAS PEÇAS QUE TORNAM O GATE BARATO

**Um auditor que relê cinco métodos inteiros a cada resposta é um auditor que ninguém roda.** Duas decisões de desenho resolvem isso:

### 2.1 A DECLARAÇÃO DE CARGA

**Toda resposta de peso fecha declarando o que carregou.** Três a seis linhas, **no fecho e nunca na abertura** — abertura vira preâmbulo, e preâmbulo é ruído que o leitor paga.

```
Carregado: METODO-X (§3) · METODO-Y · skill Z (módulos 01, 04)
Decidiu: X deu a ordem · Y deu a dose · Z deu a régua de linguagem
Contradição: nenhuma  /  X e Y divergiram em __; venceu X por __
Desvio declarado: nenhum  /  __
```

### 2.2 ⭐ A RÉGUA DE VETO — uma linha por método

> **Cada método declara UMA coisa que reprova sozinho. O auditor checa essas linhas, não os métodos.**

**É isto que faz o gate custar segundos em vez de minutos:** cinco métodos carregados viram **cinco perguntas binárias**, não cinco leituras.

---

## 3. 🔴 A TABELA DE VETOS — o índice que o auditor usa

**Uma linha por método. É o instrumento inteiro.**

| Método / regra | 🔴 O que reprova sozinho |
|---|---|
| **Sistema da operação — áreas Operação e Comercial** *(🟡)* | prospect vivo sem `PAINEL.md` · aceite sem conta aberta e sem `onb_d0` · número na tela que não sai de um `.md` (valor, previsão, taxa com `n` escondido) · contrato pago à vista contado como receita recorrente · agente da Fase B ligado antes do gate à mão |
| **Cartão de decisão em duas camadas (face e lastro)** · `40-operacao-rotinas/tarefas/modelos/cartao-decisao.md` · `40-operacao-rotinas/ferramentas/decisoes_cartao.py --lint` *(🟡)* | **V-DEC-1** cartão aberto no formato antigo (sem "Em jogo") · **V-DEC-2** campo da face acima do teto (pergunta 90, em jogo 160, rótulo 60, efeito 150, recomendação 200, supondo 140) ou face acima de 1.200 caracteres · **V-DEC-3** código da casa na face (crase, asterisco, id, caminho, nome de arquivo, sigla de nível, data relativa) · **V-DEC-4** recomendação sem porquê, sem "Supondo", ou opção sem a linha do que o clique dispara · **V-DEC-5** prazo que não é data nem "sem prazo", ou cabeçalho sem `aberta:` · **V-DEC-6** cartão de dinheiro sem "Números" · cartão resolvido parado em Abertas |
| **Esteira de produção de entregáveis** · `entregaveis.py --verificar` *(🟡)* | **V-ENT-1** promessa nossa (eixo 15 da destilação, classe `promessa_nossa` da captura) sem task `tipo: entregavel` com fonte apontando para ela · **V-ENT-2** task pronta sem arquivo em `saida`, fora de `clientes/<Conta>/entregaveis/` ou sem linha no README da conta · **V-ENT-3** task entregue sem `enviado_em` ou sem linha no `STATUS.md` da conta · **V-ENT-4** marco do `PAINEL.md` com dono {{OPERADOR}} que é verbo de produção (mandar, enviar, escrever, montar, gerar, PDF, mensagem) e sem `task:` *(aviso; o CEO decide pela `--triagem`)* · **V-ENT-5** pronto depois do prometido sem `## Ajuste de expectativa` · **V-ENT-6** `enviado_em` escrito por rotina, subagente ou task (só o clique do {{OPERADOR}} no painel ou a ordem literal dele na sessão) |
| **`METODO-DECISAO-DE-OFERTA`** *(🟡)* · inventário `30-comercial/INVENTARIO-DE-CAPACIDADES.md` | **oferta recomendada sem dor de fonte D ou O apontável** (indicador ou leitura nossa é hipótese de entrada, não recomendação) · **produto que exige operador sem operador nomeado** · produto escolhido pela ferramenta pedida e não pela dor · combo com peça fora do catálogo tratado como catálogo · recomendação sem descartado ou sem gatilho de troca · preço escrito no inventário ou fora da fonte canônica do produto · hipótese de entrada registrada como recomendação · `inventario-capacidades.py` ≠ ✅ · recomendação de oferta decidida sozinha enquanto `oferta_catalogo` estiver em A1 |
| **`METODO-ONBOARDING-ORQUESTRADO`** *(🟡)* | conta em entrega sem `onb_d0` no `PAINEL.md` · passagem de bastão e kickoff na mesma reunião · primeiro valor registrado sem fala do cliente com data e fonte · revisão com oferta de venda na pauta · alerta automático enviado ao cliente · prazo ou peso mudado no método sem a mesma mudança em `onboarding_regras.py`, ou o inverso |
| **`CLAUDE.md` §8 · REGRA Nº 0** | estrutura de conversão devolvida ao cliente como pergunta — promessa, mecanismo, narrativa, headline, gancho, ordem de elemento, recorte de público |
| **`CLAUDE.md` §8 · REGRA Nº 1** | método, skill ou módulo criado **sem roteamento na mesma tarefa** |
| **`CLAUDE.md` §10** | saída que é só análise — **sem decisão, direção, ação e impacto** |
| **`CLAUDE.md` §11.3** | conversa externa relevante encerrada **sem registro no repo** |
| **`CLAUDE.md` §11.6** *(15/10)* | tarefa encerrada com trabalho **fora da `main` do GitHub** · conflito resolvido **descartando uma versão** sem registro · rebase ou force-push na `main` · *(30/10)* **repo de cliente fora do clone vivo da pasta dele** (cópia congelada, clone solto, edição direta no GitHub, push à mão) · repo de cliente sem linha no `entregaveis/repositorios.json` ou fora do `.gitignore` · dado sensível publicado no repo do cliente |
| **`POLITICAS-DE-DECISAO.md` §8 · público anonimizado** | **nome, sigla ou fato de cliente, prospect, parceiro, ex-sócio ou contraparte no que se alcança sem login, histórico de repositório incluído** · publicação sem `varrer-publico.py` em ✅ · lista de nomes de memória no lugar do dicionário das pastas · `git push --force` tratado como limpeza · dado de terceiro aberto sem registro em `80-juridico/registros/` e advogado no mesmo dia |
| **`ARVORE-CONTA.md` · painel de projetos** *(28/10)* | `STATUS.md` de conta alterado **sem o frontmatter do `PAINEL.md`** no mesmo ato · estado da conta decidido pelo painel e não pelo `STATUS.md` · dado corrigido no Supabase ou no site · `painel-projetos.py --verificar` ≠ ✅ ao fechar tarefa de conta |
| **`ARVORE-ESCRITA.md` §7 · retorno atrasado** | mensagem a cliente, prospect ou parceiro com 3+ dias sem resposta nossa (ou entrega fora do prazo dito) que **abre sem desculpa, sem a falha real de processo nomeada, sem o "mas" da melhoria ou sem o mini bônus** · falha inventada onde não há falha apontável · "correria" ou "agenda cheia" como falha · bônus que é **dinheiro, desconto ou escopo novo** · enviada sem o ✅ do {{OPERADOR}} |
| **`CLAUDE.md` §11.5** | peça que bateu gatilho de performance e **não entrou no swipe file na mesma tarefa** |
| 🔴 **`CLAUDE.md` §8 · REGRA Nº 2 — ESCALA** *(22/09)* | **promessa, oferta, lead ou arquitetura de funil/VSL sem referência ESCALADA registrada** (estado + sinal **+ fonte da evidência** — biblioteca, fonte de confiança da casa ou número público; ausência na biblioteca sozinha não reprova, desde 25/09) · **espaço vazio usado como estrutura principal** · peça de teste apresentada como estrutura principal da conta |
| `METODO-ARQUEOLOGIA-DE-ICP` | cena, dor ou fala de grau **`I` em bloco de espelho** · fonte não apontável em dez segundos · 🔴 **crença-alvo do lead com uma fonte só ou tirada do fecho de um caso isolado** (§6-quater, 18/10) |
| `METODO-TESTE-DE-PILARES` | **P1 ou P4 reprovando** → bloqueia produção de copy |
| `METODO-ALCADA-DE-ESTRUTURA` | lacuna de **estrutura** tratada como pergunta ao cliente |
| `METODO-PONTOS-LOGICOS` | elo cuja remoção **não derruba o seguinte** · **conclusão escrita na peça** · cadeia **sem destino** declarado |
| `METODO-MECANISMO-E-ONE-BELIEF` | apelido **sem mecanismo construído** · Nova Oportunidade **igual** ao apelido · apelido **variado** em vez de repetido idêntico |
| `METODO-ESTRUTURA-INVISIVEL` | **texto transposto** da referência · dose fora de ±15% · modelar sequência em peça de **degrau 3** |
| `METODO-BENCHMARKING` | referência **sem estado de escala registrado** (escalado / em escala / testando + o sinal) · referência "testando" usada como base · fala de concorrente usada como grau `D` |
| `METODO-DESTILACAO-DE-VSL` | bloco **"o que não se sabe pela peça"** ausente · eixo 9 não marcado `R` |
| `METODO-DESTILACAO-DE-CALLS` | citação **sem timestamp** · propagação não feita **na mesma tarefa** · 🔴 **transcrição de áudio fora da pasta do áudio, com outro nome ou editada** (regra de transcrição, 18/10 → `METODO-TRANSCRICAO-DE-AUDIO`) · **eixo 14 ausente em call de venda ou diagnóstico** · **proposta escrita que contradiz o que ele já ouviu de nós sem declarar a correção** *(29/10)* |
| `METODO-TRANSCRICAO-DE-AUDIO` *(18/10 · 21/10)* | 🔴 **transcrição refeita** quando já existia na conta · transcrição **sem pedido** do {{OPERADOR}} · transcrição **fora da pasta do áudio**, com **outro nome**, em **`.txt`** ou **editada** · **README da pasta não atualizado** depois de transcrever · transcrição em **serviço de nuvem sem ok do {{OPERADOR}}** ou sem o serviço no cabeçalho |
| `METODO-FUNIL-DE-VSL` | qualquer um dos **três gates de entrada** aberto: pilares, caixa reservado, ativos mínimos |
| `METODO-PRODUCAO-VSL-POR-AGENTES` *(02/10)* | roteiro de VSL **escrito e auditado no mesmo contexto** com subagentes disponíveis · bloco aprovado **sem os seis relatórios** · auditor que **reescreve** · texto **antes do esqueleto aprovado** · bloco seguindo com defeito de **procedência** ou **promessa acima do teto** · *(16/10, revisão 1)* **G1 com lacuna de fato aberta ou estrutura-base sem função e tempo** · **rodada acima do orçamento sem reporte** · **juiz que reabre decisão do dono** · *(16/10)* **peça gravada sem o laudo do A7 (compreensão e coerência) ou com veto dele aberto** — veículo não dito até 1:00, público não dito até 1:30, produto revelado só na oferta, afirmação de prazo/disponibilidade falsa, crítica ao que a expert vende · *(16/10)* **rodada fechada sem a composição da VSL** (`COMPOSICAO-VSL.md` + `.pdf`: 2 páginas de estrutura + 1 de função, §4.4) |
| `METODO-ANCORAGEM-DE-PROPOSTA` | âncora não preenchida **nem declarada faltante** · **bloco de onboarding ausente** · `n` inventado onde é `n=0` · 🔴 **denominador de produto único ou percentual de margem em peça que vai ao cliente** (gate interno exportado) · **recorrência proposta antes de existir denominador de empresa** |
| `METODO-CAMADA-DE-VER` | artefato que **pede decisão**, ou processo com 3+ passos e bifurcação, **sem diagrama que abre o documento** |
| `METODO-DIRECT-RESPONSE` | promessa **sem prova** que a pague · DFY **refeito por cliente** vendido a preço de produto |
| `METODO-GERACAO-DE-RESULTADOS` | resultado no **negativo**, sem evidência, ou não específico |
| `METODO-ESTIMATIVA-DE-CARGA` | **hora nossa em documento que sai da casa** · multiplicador de produção aplicado a **colheita ou latência** |
| `METODO-EDICAO-DE-VIDEO-CURTO` *(15/10 · 🟡)* | render final **sem roteiro de corte aprovado pelo {{OPERADOR}}** · legenda publicada **sem conferência de nome próprio** · fonte do WhatsApp usada como original · áudio fora de **−14 LUFS ±1** · trecho que fere a **régua de tom** (§3 do método) |
| `METODO-KIT-DE-MARCA` *(18/10 · 🟡)* | dominante **sem três falas literais** da expert e o kit não marcado hipótese fraca · cor ou tipografia **sem porquê no arquétipo** · Inter · kit **sem veto ou sem teste da peça** · peça do kit sem procedência · tokens definitivos **sem escolha literal** no `DECISOES.md` · **pilares entregues sem kit** quando o pedido foi "faça os pilares" |
| `ARQUETIPOS-DE-MARCA` *(18/10 · 🟡)* | **arquétipo do público ou do nicho** lido como o da expert · **estética atual** lida como identidade · aspiração ("quero ser vista como") lida como fato · coluna de ambiente citada como Mark e Pearson (é heurística da casa) |
| `METODO-PRANCHA-DE-ESCOLHA` *(18/10 · 🟡)* | opção na prancha **que não passou no gate visual** (que não assinaríamos) · **mais de uma variável** mudando entre as opções de uma linha · texto **sem procedência** · escolha do cliente **não registrada literal** no `DECISOES.md` antes de virar token |
| `METODO-TRAFEGO-PAGO` | criativo **sem hipótese escrita** · linha de matriz sem os campos obrigatórios · *(14/10)* **conjunto Meta com posicionamento automático ou fora de Instagram Feed + Stories + Reels** *(feed entra)* · **anúncio sem as duas artes** (4:5 no feed, 9:16 em Stories e Reels) · *(27/10)* **campanha para WhatsApp fora do objetivo Engajamento (Leads, Vendas) sem motivo escrito no `LOG-DECISOES.md`** · **campanha para WhatsApp em Tráfego** · **campanha para WhatsApp otimizada por clique ou visualização de página** · **conta herdada sem inventário de status nos três níveis** |
| `METODO-TRILHO-DE-CONTA-NOVA` | etapa com **duas entradas** · pendência **sem "o que destrava"** · pedido ao cliente contendo lacuna de estrutura |
| `copywriter-senior-continuum` | os **11 passes**; piso que vale sempre: **1 (diagnóstico) · 3 (pivô) · 10 (proibições) · 11 (procedência do espelho)** · *(28/10, v3.2)* **no passe 10, abertura em contexto reprova sozinha em qualquer formato** (módulo 10, teste "e daí?") · *(12/10)* no passe 7, **informação cortada junto com o enchimento** reprova (módulo 04) |
| — módulo 06 | **sentimento não declarado antes do assunto** (§11.1-bis) |
| `gerador-web-designer` | **sem brief, nada avança** · qualquer P0 reprova a publicação |
| 🔴 `00-core/TAXONOMIA-DE-ARTEFATOS` *(26/09)* | artefato de conhecimento criado **sem `Tipo:` do vocabulário** (seis tipos + registro, ponteiro, índice) · híbrido de 3+ tipos **sem a linha `Abrir por momento`** · 🔴 **etapa do PROCESSO pulada** — peça produzida (método/blueprint) sem o framework e o trilho que a precedem, **inclusive sob urgência** (§4.2) |
| `90-templates/repo-cliente` *(23/09)* | **framework ou método nosso** dentro do repo do cliente · repo prometido em proposta **sem as três condições respondidas** (agente que carrega, dono nomeado, primeira peça conosco) · repo oferecido como **concessão em negociação parada por preço** |
| 🔴 `verificar-propagacao.py` *(26/09)* | tarefa que criou ou alterou artefato encerrada **com resultado diferente de ✅** — ou **sem ter rodado o verificador** |
| `METODO-ABORDAGEM-FRIA` *(27/09 — extraída do gate do próprio arquivo)* | produto, feature ou preço citado na 1ª mensagem · número inventado sem hipótese explícita ou incerteza admitida · cena simulada sem dado real |
| `METODO-ITERACAO-DE-CPA` *(19/10 · 🟡)* | **CPA prometido ao cliente** em fala, proposta ou contrato · campanha no ar **sem etiqueta de venda** · mudança mantida que melhorou a alavanca e **piorou o CPA** · duas mudanças na mesma alavanca no mesmo ciclo · decisão de roteiro sobre amostra curta |
| `METODO-ANALISE-DIARIA-DE-CAMPANHA` *(29/10 · 🟡)* | mudança na plataforma **sem ordem escrita no `BRIEFING.md` do dia** · Sonnet executando pela análise ou pelo diário e não pelo briefing · ordem A1 executada **sem aprovação do {{OPERADOR}}** · coleta com interpretação, comparação ou número sem fonte · análise com número que não está em nenhum diário · item em aprendizado (< 72h) tratado como kill normal · ordem executada **sem linha no `LOG-DECISOES.md`** · dado de cliente coletado em N1 · criativo ou público novo "implementado" por este método |
| `METODO-RELATORIO-DA-OPERACAO` *(31/10 · 🟡)* | **número, valor, hora, data, código ou citação fora da foto da operação** · relatório **enviado sem ✅** do `verificar_relatorio.py` · **contornar o verificador** (número por extenso, aspas que não são citação) · fonte não lida **sem a linha "Não li"** · item em "Precisa de você" **que não está em `precisa_de_voce` da foto** |
| `METODO-DESENHO-DE-PRODUTO` *(01/11 · 🟡)* | **tela, token ou protótipo antes dos degraus 1 a 4 escritos** · job **sem três falas** de pessoas diferentes não marcado hipótese fraca · funcionalidade **sem job apontável** ("a referência tem") · fluxo com **mais de 5 toques** ou sem métrica · direção que **um concorrente poderia usar** · **protótipo com máquina ligada** (banco, pagamento, integração) · degrau 7 **sem 5 pessoas por ator**, ou com amiga próxima de quem decide · produto de cliente com degraus 1 a 3 **não vendidos antes** · porquê com "plataforma", "solução" ou "conectar" · **laudo do `leitor-sintetico` contado como validação**, ou persona dele **sem fala `D`** por trás, ou laudo com nota ou "aprovado" |
| `METODO-PROSPECCAO-PRESENCIAL-LOCAL` *(19/10 · 🟡)* | porta **sem fato observado** na pré-visita · preço oferecido antes de ser pedido na porta · pitch **sem concordância do dono com a causa em voz alta** · **número financeiro do dono pedido antes do pivô, ou dado do cliente nas telas 1 a 4** *(20/10)* · breakeven sobre ticket · visita ou reunião **sem linha no registro** · roteiro trocado **sem a fase que quebrou** identificada · projeção pelo anúncio **sem fonte do CPA ou sem margem de risco** · tela 6 (o plano) com **mais de uma carta `desenhamos` por mês** ou **`degrau seguinte` no preço** · ganho do simulador usado como promessa · **parcelamento oferecido com a conta sem fechar** · verba de anúncio recebida por nós · **módulo de automação vendido antes do mês 3 ou SDR IA sem roteiro iterado** · **mensagem da API Oficial paga por nós** |
| `METODO-CONSTRUCAO-DE-CRIATIVOS-DR` *(27/09 — extraída do gate do próprio arquivo)* | banco de léxico ausente — a escrita não começa · prova com pessoa, prazo ou resultado inventados · destino inexistente liberado para mídia · 🔴 *(12/10, §4.2-bis)* **tese, mecanismo ou oferta com substantivo ou verbo que não responde o quê, quem, quando e como** · **peça com colchete de fato aberto liberada para mídia** · promessa de resultado sem prova documentada |
| `METODO-EMPILHAMENTO-DE-HOOKS` *(27/09 — extraída do gate do próprio arquivo)* | divisão tipográfica contada como vários hooks · grupo e elemento contados em dobro · expectativa aberta sem resposta localizada no corpo |
| `METODO-LATERALIZACAO-DE-CRIATIVOS` *(27/09 — extraída do gate do próprio arquivo)* | exploração sem base vencedora apresentada como lateralização validada · resultado inconclusivo apresentado como decisão · significância declarada sem cálculo |
| `METODO-GATE-DE-CONTRATACAO` *(27/09 — extraída do gate do próprio arquivo)* | entrega que exige delegar estratégia (D4) antes do piso — **recusa, o único veto que resta** · delegação de estratégia com MRR abaixo de `{{META_MRR}}` |
| `METODO-SALESFORCE-INBOUND` *(27/09 — extraída do gate do próprio arquivo)* | sem régua de veto declarada — candidato a gate (buraco 5). *Framework de referência: não declara critério que reprove um output nosso* |
| `METODO-ALICERCE` *(27/09 — extraída do gate do próprio arquivo)* | passagem a ICP A sem a oferta levada a 10 conversas reais registradas · promessa de faturamento em qualquer artefato · cliente que exige garantia de faturamento |
| `METODO-DIAGNOSTICO-DE-OPERACAO` *(27/09 — extraída do gate do próprio arquivo)* | mais de três dimensões vermelhas no documento · palavra da lista banida (vazamento, erro, falha, problema grave, auditoria…) · Mapa vendido ao ICP B |
| `METODO-PIVO-DE-CONVERSAO` *(27/09 — extraída do gate do próprio arquivo)* | pivô não apontável no ativo · mais de um pivô na mesma peça · causa apontada diferente da que a oferta resolve |
| **Autonomia por default** (`CLAUDE.md`, seção de autonomia) | resposta que termina oferecendo ato reversível em vez de tê-lo feito · defeito achado no caminho e não corrigido nem registrado · relatório de subagente que endereça o {{OPERADOR}} · ato da lista fechada feito sem a palavra dele · kernel alterado sem `backup-governanca.py --marco` antes |
| **Delegação por custo** (`CLAUDE.md` §8, agente `.claude/agents/varredor.md`) | varredura, busca, contagem ou conferência mecânica feita pelo modelo caro na sessão · `varredor` que edita, decide, recomenda ou parafraseia o literal · **pacote externo de agentes instalado sem `model:` no cabeçalho, ou que soma descrição à carga fixa sem medir (`medir-contexto.py`)** |
| `MATRIZ-LEITURA-CONTEUDO` *(27/09 — extraída do gate do próprio arquivo)* | amostra abaixo de 10 peças tratada como diagnóstico · leitura contra benchmark externo em vez da mediana do próprio perfil · mais de uma variável alterada por lote |

⚠️ **Método carregado que não está nesta tabela entra com o gate que ele próprio declarar.** Se não declara nenhum, **isso se registra na declaração de carga** — e é candidato a ganhar gate (buraco 5).

---

## 4. O GATILHO — o que cruza o gate, e o que não

🔴 **Gate em toda resposta mataria a operação.** Ele é proporcional:

| Cruza o gate | Não cruza |
|---|---|
| **peça que vai a humano** — copy, proposta, mensagem, roteiro, página | resposta de conversa, pergunta, confirmação |
| **artefato que vira arquivo** no repositório | rascunho descartável |
| **output que decide** — diagnóstico, recomendação, veredito, plano | levantamento sem conclusão |
| **qualquer coisa que sai da casa** | nota interna de trabalho |
| **resposta que carregou 3 ou mais métodos** | resposta com 1 método |

---

## 5. OS CINCO PASSES

**Rodados depois do output fechado, lendo o output como texto — nunca como intenção.**

### P0 · Proporcionalidade da carga

> **O pedido exigia esses métodos, ou foram carregados por precaução?**

🔴 **Método que não produziu nenhuma decisão visível no output não deveria ter sido carregado.** E a declaração de carga torna isso verificável: se a linha *"decidiu"* não tem nada a escrever sobre um método, ele sobrou.

⚠️ **Carga excessiva não é zelo.** Dilui, atrasa e **aumenta a superfície de contradição** — cada método a mais é uma chance a mais de dois mandarem coisas opostas.

### P1 · Carga declarada

- [ ] O que foi carregado **está escrito**?
- [ ] O roteador (`§6`) mandaria este pedido para **esses** métodos? Se não, ou o roteamento está errado, ou a carga está.

### P2 · Veto, ponto a ponto

**Para cada método carregado: a régua de veto dele (§3) foi honrada, e dá para apontar ONDE?**

| Método | Régua de veto | Cumprida? | Onde, no output |
|---|---|:---:|---|
| | | ✅ / 🔴 | linha, bloco ou seção |

🔴 **"Cumprida" sem a coluna "onde" preenchida não conta.** É a mesma régua do passe 11 da skill de copy: apontar, não afirmar.

### P3 · Contradição entre métodos

> **É o passe que só existe porque há muitos métodos — e o que nenhum gate de formato faz.**

**Dois métodos carregados mandaram coisas opostas?** Se sim:

- [ ] A contradição está **nomeada**?
- [ ] Qual venceu, e **por qual precedência**? (`CLAUDE.md` §3: kernel > políticas > skill dominante > artefato de área · fato comercial: `ICP.md` · estado: `STATUS.md` · data mais recente)
- [ ] A divergência foi **sinalizada ao usuário**, como o §3 manda?

⚠️ **Contradição resolvida em silêncio é o pior resultado possível:** o output fica coerente e ninguém descobre que uma regra foi atropelada.

### P4 · Lastro

> **O output afirma alguma coisa que nenhum método, nenhum artefato e nenhum dado sustenta?**

- [ ] Todo número tem fonte ou marcação `[benchmark]` / `n=0`
- [ ] Toda cena ou fala tem grau
- [ ] Toda afirmação sobre a conta tem origem no repositório
- [ ] **Nada foi preenchido com plausível**

🔴 **É o passe anti-alucinação, e é o único que vale mesmo quando só um método foi carregado.**

---

## 6. OS TRÊS VEREDITOS

| Veredito | Quando | O que acontece |
|---|---|---|
| ✅ **PASSA** | os cinco passes limpos | entrega |
| ⚠️ **PASSA COM DESVIO DECLARADO** | uma régua não pôde ser cumprida, **e o motivo está escrito no output** | entrega **com o desvio visível ao usuário**, nunca em nota de rodapé |
| 🔴 **REPROVA** | régua de veto violada em silêncio · contradição não nomeada · afirmação sem lastro | **volta. Não se entrega declarando depois** |

> 🔴 **A diferença entre "passa com desvio" e "reprova" é uma só: o desvio foi declarado ANTES de alguém perguntar.** Desvio declarado é informação; desvio descoberto é erro.

---

## 7. A SEPARAÇÃO DE PAPEL

**Quem produz não audita na mesma passada.**

| Ambiente | Como rodar |
|---|---|
| **Com subagentes** | o auditor roda em contexto próprio, recebendo **o output e a tabela de vetos** — e nada do raciocínio de quem produziu |
| **Sessão única** | rodar como **passe declarado**, depois do output fechado, **lendo o texto e não a intenção** |

⚠️ **Em sessão única a separação é imperfeita e isso se assume.** O que a torna útil mesmo assim é a tabela: **checar uma lista externa é diferente de reler o próprio raciocínio.**

---

## 8. O QUE ESTE GATE NÃO FAZ

- **Não substitui os gates de formato.** Os 11 passes da copy, o juiz de publicação e os gates de método continuam onde estão. **Este audita o conjunto; aqueles auditam o artefato.**
- **Não julga qualidade.** Congruência não é excelência. Peça congruente e morta continua morta — isso é o gate anti-slop.
- **Não relê os métodos.** Lê a tabela de vetos. **Se a régua de um método mudar, muda a linha na tabela** — e isso é parte da alteração, não do depois.
- **Não vira preâmbulo.** A declaração de carga fecha a resposta.

---

## 9. 🔴 A OBRIGAÇÃO QUE ISTO CRIA NOS OUTROS MÉTODOS

> **Todo método novo declara, na criação, a sua régua de veto — a linha que reprova sozinho — e a linha entra na tabela §3 na mesma tarefa.**

**É o ato 5 da REGRA Nº 1**, e pela mesma razão dos outros quatro: régua que não está na tabela não é checada, e método com gate que ninguém roda é método sem gate.

⚠️ **Os 22 arquivos sem gate** (§1, buraco 5) ficam como dívida nomeada. **Alguns não precisam de gate** — registro, auditoria datada e ponteiro não produzem output. **Os que precisam ganham na próxima vez que forem tocados.**

---

## 10. A FORMA CURTA

> **Muitos métodos por requisição não é o problema. O problema é ninguém declarar quais, e nada checar o conjunto.**
>
> **Declara-se a carga no fecho. Cada método tem UMA régua que reprova sozinho. O auditor checa essas linhas — não os métodos.**
> **Contradição resolvida em silêncio reprova. Desvio declarado passa.**
> **E método que não decidiu nada no output não deveria ter sido carregado.**

---
*Regra da casa, a partir da pergunta de se todo output era auditado ponto a ponto — **e a resposta honesta era não.** Gate de saída de output: `00-core/COMPLIANCE-DE-OUTPUT.md`. Precedência em conflito: `CLAUDE.md` §3. 🟡 Verificação em caso real pendente.*
