# ÁRVORE — NEGÓCIO

> **Tipo:** trilho · **Origem:** casa de origem do template · **Alçada:** {{OPERADOR}}
> **Carrega-se quando:** o nível 1 do `CLAUDE.md` §6 aponta para cá. **O pedido é sobre decidir o negócio** — ICP, oferta, promessa, preço, caixa, contratação, G0, prospecção e venda nossa, resposta direta e escala.
> **Réguas transversais** (§8 REGRAS Nº 0, 1, 2 · procedência · ordem) **valem aqui e não se repetem.**

---

## 1. Pré-condição

Nenhuma de entrada. ⚠️ **Mas esta árvore é INSUMO de outras:** proposta (ESCRITA) exige as âncoras daqui antes; conta nova (CONTA) exige o G0 daqui antes.

## 2. O processo desta árvore

| Tipo | O que se carrega |
|---|---|
| **framework** | `100-métodos/METODO-DIRECT-RESPONSE.md` (40/40/20 · §2-bis escala · §4 DFY) · `100-métodos/METODO-GERACAO-DE-RESULTADOS.md` |
| **trilho** | `CLAUDE.md` §9.1 — `G0 → âncoras → folha interna → veredito → proposta` |
| **método** | `100-métodos/METODO-DECISAO-DE-OFERTA.md` (o que propor a quem, 🟡) · `100-métodos/METODO-DIAGNOSTICO-DE-OPERACAO.md` (ICP A) · `100-métodos/METODO-ALICERCE.md` (ICP B) · `100-métodos/METODO-ABORDAGEM-FRIA.md` |
| **blueprint** | `90-templates/diagnostico-operacao/` |
| **política** | `00-core/POLITICAS-DE-DECISAO.md` · `30-comercial/ICP.md` · `30-comercial/oferta.md` · `100-métodos/METODO-GATE-DE-CONTRATACAO.md` |
| **gate** | `100-métodos/METODO-GATE-DE-CONGRUENCIA.md` — **confere a etapa E a existência das anteriores** |

## 3. Linhas — sinal → carga → veto

| Sinais | Carga, na ordem do processo | 🔴 Veto |
|---|---|---|
| ICP, oferta, posicionamento, modelo de negócio, abrir/fechar nicho | `10-skills/c-level/CEO.skill.md` *(persona)* → `30-comercial/ICP.md` + `30-comercial/oferta.md` *(política)* | fato comercial: `ICP.md` prevalece |
| pipeline, vendas, fechamento, forecast, receita previsível | `10-skills/c-level/CRO.skill.md` → `30-comercial/` | — |
| **funil, pipeline, "o que está para fechar", proposta esfriando, ficha do prospect, aceite, área Comercial do sistema** | ficha `30-comercial/assessoria-prospects/<pasta>/PAINEL.md` (molde `90-templates/prospect/PAINEL.md`: etapa contato → g0 → âncoras → proposta → aceite · perdido, produto, valor, recorrência, validade, próximo passo, checklist de Embarque) → leitor `40-operacao-rotinas/ferramentas/comercial_regras.py` → área **Comercial** do sistema (`980-web-design/painel-projetos/`); o **aceite** marcado no sistema grava a data e abre a task "Abrir a conta" (`40-operacao-rotinas/ferramentas/acoes_do_painel.py`), que vira o `onb_d0` do `100-métodos/METODO-ONBOARDING-ORQUESTRADO.md` | prospect vivo sem ficha · proposta sem a checklist de Embarque (jornada, primeiro valor datado, esboço do plano) · aceite sem conta aberta no mesmo dia · previsão com valor que não está na ficha |
| **"o que oferecer a esta pessoa", qual produto, combo, "que oferta eu levo para a call", indicação que chegou, necessidade que a pessoa expressou, "dá para vender X a ela?", produto que não existe** | `100-métodos/METODO-DECISAO-DE-OFERTA.md` *(método, 🟡 provisório · passo 0 para cliente ativo: já é escopo? · procedência → dor → produto → quem opera → trilho e ordem → viabilidade → capacidade e caixa → registro)* → `30-comercial/INVENTARIO-DE-CAPACIDADES.md` *(o que podemos oferecer: camada 1 = catálogo apontando para o preço do `POLITICAS` §5, camada 2 = o que já entregamos e não é produto; conferido por `40-operacao-rotinas/ferramentas/inventario-capacidades.py`)* → ficha da pessoa (`PAINEL.md`: `dor`, `dor_fonte`, `oferta_recomendada`, `oferta_gatilho`, `dor_sem_produto`) → `autonomia.py --registrar <id> oferta_catalogo … --ficha <pasta>` · **escada:** `oferta_catalogo` em **A1** (o agente recomenda, o {{OPERADOR}} escolhe no cartão) até 10 acertos; produto novo e preço fora da tabela são `produto_novo` e `oferta_preco`, sempre A1 · depois: âncoras pela linha de proposta | 🔴 oferta recomendada sobre dor só de indicador ou leitura nossa · produto que exige operador sem operador nomeado · produto pela ferramenta pedida, não pela dor · combo com peça fora do catálogo tratado como catálogo · sem descartado ou sem gatilho de troca |
| prospecção fria, abordagem, script de WhatsApp, follow-up, qualificação | `100-métodos/METODO-ABORDAGEM-FRIA.md` *(método — abrir por momento)* + `30-comercial/prospeccao-sites/` + `voz-operador.skill.md` | 🔴 **mensagem fria é bloco de espelho e é onde mais se inventa:** cena vem do léxico do NOSSO ICP ou do que se observa no site/perfil dele — nunca do que "ele deve sentir" |
| **prospecção presencial, visita, porta a porta, negócio local, comércio do bairro, reunião presencial, apresentação na tela, assessoria de marketing local, tráfego + artes estáticas** | `100-métodos/METODO-PROSPECCAO-PRESENCIAL-LOCAL.md` *(método, 🟡 provisório · abrir por momento)* → `METODO-PIVO-DE-CONVERSAO.md` + `voz-operador.skill.md` → registro em `30-comercial/prospeccao-local/` | 🔴 porta **sem fato observado na calçada** · preço oferecido antes de ser pedido · pitch **sem o dono concordar com a causa em voz alta** · breakeven sobre ticket · visita sem linha no registro |
| inbound, SDR estruturado | `100-métodos/METODO-SALESFORCE-INBOUND.md` *(framework)* + `10-skills/c-level/CRO.skill.md` | — |
| caixa, margem, DRE, runway, precificação | `10-skills/c-level/CFO.skill.md` → `00-core/POLITICAS-DE-DECISAO.md` *(política)* | validar contra piso e teto, nunca contra intuição |
| resposta direta, branding × venda, 40/40/20, "entregar pronto", DFY, **"isso já está escalado?", qual promessa, qual oferta, modelar oferta** | `100-métodos/METODO-DIRECT-RESPONSE.md` *(framework — §2-bis REGRA DA ESCALA · §4 DFY)* | promessa/oferta/lead/arquitetura **sem referência escalada** (estado + sinal + fonte) · DFY refeito por cliente vendido a preço de produto |
| resultado, meta, plano estratégico, diagnóstica, oferta bem formulada, cocriação, reenquadre | `10-skills/geracao-de-resultados.skill.md` → `100-métodos/METODO-GERACAO-DE-RESULTADOS.md` *(framework)* · combina com ESCRITA em página e oferta | resultado no negativo, sem evidência ou não específico |
| contratar, delegar, "não tenho hora", capacidade estourada, tripwire de horas, avaliar candidato | `100-métodos/METODO-GATE-DE-CONTRATACAO.md` *(política)* + `POLITICAS-DE-DECISAO.md` §4-bis | **nunca recusar venda por teto de horas — aciona contratação** · estratégia delegada antes do piso D4 |
| **Mapa da Ordem**, diagnóstico pago, G0 de quem **já fatura** (ICP A), ler a operação antes de propor | `100-métodos/METODO-DIAGNOSTICO-DE-OPERACAO.md` *(método)* → `90-templates/diagnostico-operacao/` *(blueprint)* → `POLITICAS-DE-DECISAO.md` · §9.1 | **Mapa nunca vendido ao ICP B**, nem com desconto |
| **treinamento, formação, "quero o repo completo", licença do repositório, "me manda treinamento"** | a oferta de formação da casa, se houver (registrada em `30-comercial/`) *(política, ✅ desde 16/10)* → `30-comercial/ARQUITETURA-DE-CAMADAS-E-CATALOGO.md` → termo: `80-juridico/contratos/TEMPLATE-TERMO-FORMACAO-REPOSITORIO.md` | 🔴 **instanciar o repositório do aluno por ele** (isso é o Repo de Governança) · turma começar sem template pronto ou sem termo assinado · turma com menos de 5 alunos |
| cliente que constrói **do zero** (ICP B), "não tem nada ainda", G0 de quem não fatura | `100-métodos/METODO-ALICERCE.md` *(método)* · §9.1 | fora dos 4 pilares · segundo cliente simultâneo |
| **criar um produto digital** (site de produto, app, PWA, painel, guia, SaaS, marketplace, ferramenta com usuário), nosso ou de cliente; "como vai ser o produto", "por onde começo o app", UX, jobs, protótipo, "está aéreo" *(regra da casa)* | `100-métodos/METODO-DESENHO-DE-PRODUTO.md` *(método, 🟡 provisório · sete degraus: por quê → para quem → o quê → fluxo → cara → protótipo → prova)* → moldes em `90-templates/desenho-de-produto/` → degrau 5: `ARQUETIPOS-DE-MARCA` + `METODO-KIT-DE-MARCA` + `10-skills/ui-ux-designer-senior-continuum/` (modo direção) → degrau 4-bis e antes do 7: `.claude/agents/leitor-sintetico.md` (ensaio na pele do ator, só de fala `D`; aponta, nunca aprova) → degrau 6 no ar: OPERAÇÃO · **pré-condição:** kernel de negócio (quem paga, quanto) e mecanismo de receita desenhados; **cliente:** degraus 1 a 3 vendidos e ancorados antes (`METODO-ANCORAGEM-DE-PROPOSTA.md`) · entregáveis em `<projeto>/NN - web design/` | 🔴 **tela, token ou protótipo antes dos degraus 1 a 4 escritos** · job sem três falas não marcado hipótese fraca · funcionalidade sem job ("a referência tem") · **protótipo com máquina ligada** (banco, pagamento, integração) · degrau 7 sem 5 pessoas por ator · produto de cliente com degraus 1 a 3 não vendidos antes |

## 4. Desempate interno

- **"Capacidade estourada"** → linha de contratação, não a do COO (OPERAÇÃO): falta de hora é decisão de negócio.
- **"Qual oferta usar para esta VSL"** → esta árvore primeiro (escala), depois ESCRITA (a peça).
- **Proposta** → as âncoras começam aqui; a peça termina em ESCRITA.

---
*Linhas migradas do roteador v1 (R05–R09, R35, R45, R48) e dos pontos cegos roteados em 26/09 (Mapa da Ordem, Alicerce).
