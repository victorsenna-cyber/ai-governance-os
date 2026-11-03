# STATUS.md — Estado Vivo da {{EMPRESA}}

> **Regra de posteridade: toda data neste arquivo leva o ano** (formato DD/MM/AAAA). Este documento será lido daqui a anos.
> **Como se escreve aqui:** as entradas novas entram **no topo**, acima desta linha, como citação de uma linha de abertura em negrito (`> **🟢/🟡/🔴 Área — DD/MM/AAAA · O QUE ACONTECEU, EM UMA FRASE.** detalhe…`). Emoji: 🟢 fechado/positivo · 🟡 em andamento · 🔴 risco ou decisão pendente · ⭐ regra nova. Toda entrada diz **o fato, a decisão, o descartado e o próximo passo com dono** (`CLAUDE.md` §11). O que só existe na conversa não existe.
> **Como se lê:** pelo topo — as entradas dos últimos 30 dias e as §1–§5. O §6 e os registros antigos por `grep`, nunca o arquivo inteiro. Bloco cuja data mais recente tem mais de 60 dias vai para `40-operacao-rotinas/rotinas/STATUS-HISTORICO-<ano>.md`, com ponteiro de uma linha.

> **⭐ Casa — {{DATA_INSTANCIACAO}} · REPOSITÓRIO INSTANCIADO A PARTIR DO TEMPLATE CONTINUUM.** Placeholders preenchidos conforme `LEIA-ME-TEMPLATE.md`. Pendências de calibração do dia 1 listadas no §6. Próximo passo: `{{OPERADOR}}` roda o primeiro pedido real pelo roteador (`CLAUDE.md` §6) e registra aqui o que o repositório não soube responder.

---

## 1. Snapshot executivo

| Indicador | Valor | Fonte / nota |
|---|---|---|
| **Caixa disponível** | `a calibrar` | `45-financeiro/LANCAMENTOS-EMPRESA.md` · painel *Caixa* |
| **MRR com termo** | `a calibrar` | só contrato com instrumento assinado conta |
| Receita recorrente sem termo | `a calibrar` | não é MRR; é risco |
| Vendas acumuladas (ano) | `a calibrar` | |
| **Burn mensal** | `a calibrar` | custo fixo da operação + ferramentas |
| Passivo total conhecido | `a calibrar` | |
| **Obrigação dura mais próxima** | `a calibrar` | data e valor; a origem do recurso se escreve ao lado |
| Clientes recorrentes ativos | 0 | com termo |
| Estágio da trajetória | **A — Caixa** | `00-core/POLITICAS-DE-DECISAO.md` §2 |
| Janela de blitzscaling | **Fechada** | previsibilidade §3 não atendida |

## 2. Metas vigentes ({{MES_ANO}})

| Meta do mês | Alvo | Status |
|---|---|---|
| `{{MOTOR_DE_CAIXA}}` vendidos | `{{META_MES_CAIXA}}` | 0 |
| Conversas novas de prospecção | `{{META_CONVERSAS_SEMANA}}`/semana | 0 |
| 1º contrato de recorrência (MRR) | 1 × `{{TICKET_ASSESSORIA}}`/mês até `{{DATA}}` | 0/1 |

**Meta do trimestre:** MRR novo ≥ `{{MRR_ESTAGIO_B}}` (abre o gate do Estágio B). Detalhe: `60-planos/PLANO-90-DIAS.md`.

## 3. Pipeline (atualizar toda segunda)

| Etapa | Qtde | Valor potencial |
|---|---|---|
| Conversas abertas | 0 | — |
| Propostas enviadas | 0 | — |
| Fechado no mês | 0 | — |
| Clientes entregues (elegíveis para recorrência) | 0 | — |

Pipeline coverage alvo: ≥ 3× a meta do mês (`POLITICAS` §3). Hoje: **sem cobertura — prioridade nº 1 é volume de prospecção.**

## 4. Capacidade

| Pessoa | Disponibilidade de entrega | Papel atual |
|---|---|---|
| **{{OPERADOR}}** | `{{HORAS_ENTREGA_SEMANA}}` h/semana de entrega (`a calibrar` na 1ª semana: medir, não presumir) | **tudo.** Prospecção · fechamento · entrega · onboarding · jurídico · construção do sistema |

- Teto de comprometimento: 70% das horas de entrega (`POLITICAS` §4). Horas comprometidas hoje: `a calibrar`.
- Onboardings simultâneos: 0/3.
- **Proteção obrigatória:** 1 período de recuperação semanal (mínimo meio dia). Burnout do operador é o maior risco operacional único de uma operação de uma pessoa.
- Tripwire ativo? Não.

## 5. Frentes ativas

| Frente | Status | Dono |
|---|---|---|
| Motor de caixa (`{{MOTOR_DE_CAIXA}}`) | **ativa — prioridade 1** | {{OPERADOR}} |
| Prospecção | a abrir: canal, lista, script e critério de score (`30-comercial/ICP.md` §2.1, `METODO-ABORDAGEM-FRIA.md`) | {{OPERADOR}} |
| Conversão carteira → recorrência | inicia a cada entrega | {{OPERADOR}} |
| Jurídico (contratos + registros) | `80-juridico/` instalado; templates de contrato a revisar por advogado (gate de caixa) | {{OPERADOR}} |
| Casa (o próprio repositório) | instanciado; `verificar-propagacao.py` em ✅ | {{OPERADOR}} |

## 6. Pendências de calibração

1. **Horas de entrega reais por semana** — medir nas duas primeiras semanas (`POLITICAS` §4).
2. **Preços e pisos** — preencher todos os `{{…}}` de `00-core/POLITICAS-DE-DECISAO.md` §5 e de `30-comercial/oferta.md`.
3. **ICP** — `30-comercial/ICP.md` §2 com o segmento de tração e o canal que de fato converte (`n` real, nunca desejo).
4. **Voz do operador** — `10-skills/voz-operador.skill.md` a partir da primeira destilação de call (eixo 13).
5. **Identidade visual** — `945-branding/01 - identidade visual/IDENTIDADE-VISUAL.md`.
6. **Integrações opcionais** — painel financeiro e de projetos (Supabase + Action), captura de WhatsApp, transcrição local: só ligar o que a operação vai usar.

---

## 7. Registro de métodos vigentes (gate de propagação)

> O `40-operacao-rotinas/ferramentas/verificar-propagacao.py` confere que todo artefato de `100-métodos/` tem registro neste arquivo. **Método novo entra nesta tabela na mesma tarefa em que nasce** (`CLAUDE.md` §8, REGRA Nº 1, ato 4).

| Artefato | Tipo | Estado no template |
|---|---|---|
| `ARQUETIPOS-DE-MARCA` | framework | 🟡 provisório até o primeiro kit aprovado por um cliente |
| `MATRIZ-LEITURA-CONTEUDO` | framework | ✅ vigente |
| `METODO-ABORDAGEM-FRIA` | método | ✅ vigente |
| `METODO-ALCADA-DE-ESTRUTURA` | política | ✅ vigente (REGRA Nº 0) |
| `METODO-ALICERCE` | método | ✅ vigente |
| `METODO-ANALISE-DIARIA-DE-CAMPANHA` | método | 🟡 provisório até 1 conta rodar 10 dias úteis sem retrabalho |
| `METODO-ANCORAGEM-DE-PROPOSTA` | método | ✅ vigente |
| `METODO-ARQUEOLOGIA-DE-ICP` | método | ✅ vigente |
| `METODO-BENCHMARKING` | método | ✅ vigente |
| `METODO-CAMADA-DE-VER` | framework | ✅ vigente |
| `METODO-CONSTRUCAO-DE-CRIATIVOS-DR` | método | ✅ vigente |
| `METODO-DESENHO-DE-PRODUTO` | método | 🟡 provisório até o primeiro produto chegar ao degrau 7 |
| `METODO-DESTILACAO-DE-CALLS` | método | ✅ vigente |
| `METODO-DESTILACAO-DE-VSL` | método | 🟡 vigente para executar, verificação em caso real pendente |
| `METODO-DIAGNOSTICO-DE-OPERACAO` | método | ✅ vigente (o G0 pago) |
| `METODO-DIRECT-RESPONSE` | framework | ✅ vigente (tronco da família DR) |
| `METODO-EDICAO-DE-VIDEO-CURTO` | método | 🟡 provisório até o primeiro vídeo real |
| `METODO-EMPILHAMENTO-DE-HOOKS` | método | ✅ vigente |
| `METODO-ESTIMATIVA-DE-CARGA` | framework | ✅ vigente |
| `METODO-ESTRUTURA-INVISIVEL` | framework | ✅ vigente |
| `METODO-FUNIL-DE-VSL` | método | ✅ vigente |
| `METODO-GATE-DE-CONGRUENCIA` | gate | ✅ vigente (tabela de vetos §3) |
| `METODO-GATE-DE-CONTRATACAO` | política | ✅ vigente |
| `METODO-GERACAO-DE-RESULTADOS` | framework | ✅ vigente (régua-mãe do §9) |
| `METODO-ITERACAO-DE-CPA` | método | 🟡 provisório, `n=0` |
| `METODO-KIT-DE-MARCA` | método | 🟡 provisório até o primeiro kit aprovado |
| `METODO-LATERALIZACAO-DE-CRIATIVOS` | método | ✅ vigente |
| `METODO-MECANISMO-E-ONE-BELIEF` | método | 🟡 vigente para executar, verificação em caso real pendente |
| `METODO-PAGINA-DE-VENDAS` | ponteiro | → skills de página |
| `METODO-PIVO-DE-CONVERSAO` | framework | ✅ vigente |
| `METODO-PONTOS-LOGICOS` | framework | ✅ vigente |
| `METODO-PRANCHA-DE-ESCOLHA` | método | 🟡 provisório até a primeira prancha apresentada |
| `METODO-PRODUCAO-VSL-POR-AGENTES` | método | ✅ vigente (agentes em `.claude/agents/vsl-*`) |
| `METODO-PROSPECCAO-PRESENCIAL-LOCAL` | método | 🟡 provisório, `n=0` |
| `METODO-RELATORIO-DA-OPERACAO` | método | 🟡 provisório até o primeiro relatório real |
| `METODO-SALESFORCE-INBOUND` | framework | ✅ referência |
| `METODO-TESTE-DE-PILARES` | gate | ✅ vigente |
| `METODO-TRAFEGO-PAGO` | método | ✅ vigente |
| `METODO-TRANSCRICAO-DE-AUDIO` | método | ✅ vigente |
| `METODO-TRILHO-DE-CONTA-NOVA` | trilho | 🟡 vigente para executar, verificação em caso real pendente |

*🟡 provisório gradua a confiança, nunca adia o roteamento (`CLAUDE.md` §7.1, itens 4 e 5). O primeiro caso real de cada um é registrado aqui, com data.*
