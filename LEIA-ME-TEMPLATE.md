# LEIA-ME — como instanciar este template

> Este repositório é o **template do repositório de governança Continuum**: a arquitetura completa (kernel, três camadas, sete árvores, taxonomia, métodos tipados, skills, blueprints, gates mecanizados, operação por tasks, rastro e sincronia git) de uma operação real, **sem dado pessoal, sem cliente e sem regra que só valia para a casa de origem**. O que ficou é o que decide.
> **Apague este arquivo quando a instanciação terminar.** Ele não faz parte da carga (`CLAUDE.md` §3).

---

## 1. O que é o quê

| Camada | O que você recebe | O que você faz |
|---|---|---|
| **Kernel** (`CLAUDE.md`) | papel, carga, roteador, regras permanentes, validação financeira, rastro | troca os placeholders; não apaga regra sem registrar a decisão |
| **Identidade** (`00-core/`) | princípio, cultura, manifesto, modos, compliance, taxonomia, protocolo multi-modelo, as 7 árvores | `CULTURA.md` §0 e §9 e `PROJECT.md` recebem a sua operação |
| **Política** (`00-core/POLITICAS-DE-DECISAO.md`, `30-comercial/`) | as réguas com o porquê; os números como `{{…}}` | calibra os números no dia 1; o que não sabe fica `a calibrar` |
| **Estado** (`STATUS.md`, `60-planos/`, `40-operacao-rotinas/`) | esqueletos com a forma certa | preenche e **mantém**: estado velho com cara de fonte é pior que não ter |
| **Métodos** (`100-métodos/`) | 40 artefatos tipados, anonimizados, íntegros | lê pela árvore, nunca "de cabeça"; método novo segue a REGRA Nº 1 |
| **Skills** (`10-skills/`, `.claude/agents/`) | portáteis, personas, jurídico, agentes de VSL, leitor sintético | `voz-operador.skill.md` é esqueleto: a sua voz entra pela extração de linguagem |
| **Ferramentas** (`40-operacao-rotinas/ferramentas/`) | verificador de propagação, sincronia git (também dos repositórios vivos de cliente), renomeação de conta, foto da operação, gate do que é público, medição de tokens, despachante, transcrição, captura, painéis | liga só o que vai usar; cada uma tem README |

## 2. Placeholders

Rode `python3 40-operacao-rotinas/ferramentas/instanciar-template.py --listar` para ver todos os `{{…}}` com arquivo e linha, e `--definir CHAVE=valor` para substituir em todo o repositório. Os principais:

| Placeholder | O que é | Onde pesa |
|---|---|---|
| `{{EMPRESA}}` | nome da sua empresa | kernel, personas, contratos |
| `{{OPERADOR}}` | quem detém a alçada (nome) | kernel, políticas, alçadas, registros |
| `{{DOMINIO}}` · `{{EMAIL}}` | domínio e e-mail da operação | painéis, workflows, contratos |
| `{{BANCO}}` · `{{BANCO_DOMINIO}}` | o banco das notificações | rotina `financas-gmail` |
| `{{META_MRR}}` · `{{MRR_ESTAGIO_B}}` · `{{MRR_ESTAGIO_C}}` · `{{DATA_HORIZONTE}}` | norte e gates de estágio | `POLITICAS` §2, personas, gate de contratação |
| `{{MOTOR_DE_CAIXA}}` | o produto de ciclo curto que paga o mês | `POLITICAS` §2, `STATUS` |
| `{{VALOR_HORA_PISO}}` · `{{MARGEM_MINIMA}}` · `{{TETO_DESPESA}}` · `{{TETO_HORAS_MES}}` · `{{HORAS_ENTREGA_SEMANA}}` | pisos e tetos | `POLITICAS` §1, §4, §5 e todo método que ancora proposta |
| `{{TICKET_MAPA_NUCLEO}}` · `{{TICKET_MAPA_OPERACAO}}` · `{{TICKET_ALICERCE}}` · `{{TICKET_SITE}}` · `{{TICKET_ASSESSORIA}}` · `{{TICKET_ASSESSORIA_COMPLETA}}` · `{{TICKET_ASSESSORIA_LOCAL}}` · `{{SETUP_CORE_ESSENCIAL}}` · `{{MENSAL_CORE_ESSENCIAL}}` · `{{MONTAGEM_RETORNO}}` · `{{MENSAL_RETORNO}}` · `{{MONTAGEM_RETORNO_SDR}}` · `{{MENSAL_RETORNO_SDR}}` | a escada de ofertas | `POLITICAS` §5, `oferta.md`, `ICP.md` §4-bis, métodos de diagnóstico e prospecção |
| `{{VERBA_POR_TENTATIVA}}` | capital de teste de mídia por tentativa | `POLITICAS` §5, funil de VSL |
| `{{META_SITES_MES}}` | meta de sites por mês, se usar a frente de sites | `30-comercial/prospeccao-sites/README.md` |
| `{{SUPABASE_URL}}` · `{{SUPABASE_ANON_KEY}}` · `{{HOSTINGER_CONTA}}` · `{{HASH_DO_TOKEN}}` | integrações opcionais dos painéis | `980-web-design/painel-*/config.js`, `980-web-design/painel-*/.hostinger/site.json`, `980-web-design/painel-financeiro/supabase/001-painel-financas.sql`, `.github/workflows/` |
| `{{DATA_INSTANCIACAO}}` · `{{DATA}}` · `{{MES_ANO}}` | datas | `STATUS`, rodapés |

**Regra:** placeholder que você não sabe preencher vira `a calibrar`, nunca palpite. Campo inventado contamina toda peça produzida depois.

## 2-bis. Qual kernel a sua ferramenta lê

| Ferramenta | Lê | O que fazer |
|---|---|---|
| Claude Code | `CLAUDE.md` | nada; `AGENTS.md` é réplica mantida pelo `sincronizar.py` |
| Codex, GPT e outras que leem `AGENTS.md` | `AGENTS.md` | nada; é o mesmo kernel com outro nome — o Codex opera como agente principal (CEO) |
| Dois agentes (um principal, um executor na antessala) | principal: `CLAUDE.md` ou `AGENTS.md` · executor: `AGENTS-EXEC.md` | renomear `AGENTS-EXEC.md` para o nome que o executor lê, se for o caso |

O roteiro de entrevista para popular o repositório com o contexto da empresa está no `README.md`.

**macOS ou Linux:** comece por `40-operacao-rotinas/ferramentas/macos/README.md` e rode `./40-operacao-rotinas/ferramentas/macos/instalar-mac.sh`. Toda a documentação usa `python3`; o que era só Windows (agendador, `.bat`, atalho, caminho do Chrome) tem equivalente lá. **Para gerar PDF:** `python3 -m pip install pymupdf` (o `gerar_pdf.py` confere o PDF com ele).

## 3. O dia 1, em ordem

1. **`CLAUDE.md` §1** — confirme a realidade operacional (uma pessoa, 100%). Se tiver sócio ou equipe, corrija aqui, em `STATUS.md` §4 e em `POLITICAS` §1 **no mesmo ato** — e nada vale sem instrumento escrito (`80-juridico/POLITICAS-JURIDICAS.md` §1).
2. **`PROJECT.md` e `SCOPE.md`** — identidade, dimensões, o vocabulário de trabalho do operador (`CLAUDE.md` §5.1 lê daqui).
3. **`00-core/POLITICAS-DE-DECISAO.md`** — todos os `{{…}}`. Os números são seus; as réguas não.
4. **`30-comercial/ICP.md`, `oferta.md`, `servicos.md`, `produtos.md`, `onboarding.md`** — o desenho é o método; preencha com a sua oferta. O que não tem dado fica `n=0`, escrito assim.
5. **`STATUS.md`** — §1 a §6. A tabela §7 (registro de métodos) já vem preenchida: ela é o que o verificador confere.
6. **`80-juridico/DADOS-DO-CONTRATADO.md`** — sua qualificação; os contratos puxam daqui.
7. **`10-skills/voz-operador.skill.md`** — fica esqueleto até a primeira call destilada (eixo 13 de `METODO-DESTILACAO-DE-CALLS.md`). Não invente a própria voz.
8. **`945-branding/01 - identidade visual/IDENTIDADE-VISUAL.md`** — quando houver marca decidida; antes disso, `ARQUETIPOS-DE-MARCA.md` + `METODO-KIT-DE-MARCA.md`.
9. **Git:** `git init`, remoto **privado** (repositório público só depois de ler `POLITICAS` §8: copie `ferramentas/varrer-publico.exemplo.txt` para `varrer-publico.txt`, preencha, e rode `varrer-publico.py --instalar-hook`; sem dicionário o gate recusa), e `.claude/settings.json` já chama `sincronizar.py` ao abrir e ao fechar a sessão (`CLAUDE.md` §11.6). Sem remoto, rode `sincronizar.py --sem-push`.
10. **Feche:** `python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py` em ✅. Depois, **o primeiro pedido real pelo roteador** — e registre no `STATUS.md` o que o repositório não soube responder. É assim que ele passa a ser seu.

## 4. O que ficou de fora, de propósito

- Toda conta de cliente (`clientes/` vem só com o molde), prospects, parceiros, registros jurídicos e societários, finanças reais, extratos, áudios, transcrições, peças publicadas, site, referências de página e de criativo (imagens), livros de terceiros.
- A skill de voz preenchida da casa de origem e o material linguístico que a alimenta.
- A "tela" de apresentação da prospecção presencial e o treino (carregam a marca de origem): o método descreve as telas; você constrói as suas.
- Os registros de auditoria e verificação que instituíram regras (a lição de cada um está no método que ela mudou).
- As referências internas da casa de origem: caminhos de pasta e procedência de material não público. **Autoria pública fica creditada** (livros, autores, vídeos abertos).
- O histórico de regras (`_legado/`) e os ponteiros de caminho antigo: o template nasce sem nenhum. O histórico é o `git log`; `_legado/` só nasce quando uma substituição precisar do porquê legível (`CLAUDE.md` §7.1, item 3).

## 5. O que nunca mudar sem registrar

As REGRAS Nº 0, 1 e 2 (`CLAUDE.md` §8), a régua-mãe do §9, a saída mínima do §10 e o rastro do §11. Elas não são preferência da casa de origem: são o que fez o repositório funcionar como memória e como mecanismo de carga. Mudar é legítimo; **mudar sem registrar, no `STATUS.md` e no rodapé do arquivo, não.**

## 6. Os casos anonimizados

Vários métodos trazem "o caso que instituiu a regra" como narrativa genérica ("uma conta de assessoria em que…"). Onde um mesmo caso é citado várias vezes num arquivo, ele aparece como rótulo estável (`Conta A`, `Conta B`…). **Leia cada caso pelo raciocínio, não pelos detalhes** — a régua que nasceu deles é verificável pelo porquê que acompanha cada uma. Quando a sua operação produzir o próprio caso, substitua.

## 7. Versões

- **03/11/2026.** Três métodos novos, todos 🟡 e roteados: `METODO-ANALISE-DIARIA-DE-CAMPANHA`, `METODO-DESENHO-DE-PRODUTO` e `METODO-RELATORIO-DA-OPERACAO`, com moldes em `90-templates/`. Agente novo: `leitor-sintetico`. Eixo 14 na destilação de calls (o que a outra parte já ouviu de nós). Duas regras novas no kernel: captura propaga (§6) e repositório vivo de cliente (§11.6), com as ferramentas em `90-templates/repo-cliente/ferramentas/`. PDF: capa medida pela página, fontes estáticas, `gerar_pdf.py` que reprova Type3, fita cortada e página em branco, e exemplares para ver cada linha. Ferramentas novas: `renomear-conta.py` e `foto-da-operacao.py`. Consertos: o `verificar-propagacao.py` passou a conferir de verdade se o `AGENTS.md` é réplica do `CLAUDE.md`, e os dois painéis ganharam a faixa de navegação e o `.hostinger/site.json` que o `publicar.py` exige.
- **03/11/2026, segunda passada.** Revisão de anonimização. `produtos.md` e `termos-places-icp.md` viraram moldes de verdade. Régua nova, `POLITICAS` §8: público é sempre anonimizado, com `varrer-publico.py` como gate. Os exemplos (`kit-modelo.json`, `pdf-dashboard-trafego/exemplo.json`, `pecas-demo.json`) são inteiramente fictícios. O motor de peças (`945-branding/01 - identidade visual/sistema/`), do qual o gerador de kit depende, passa a vir no template, em valores neutros.
- **28/10/2026.** Primeira versão.

## 8. Como popular este repositório com o contexto da empresa — roteiro de entrevista para a IA

> **Para o agente (Claude, Codex ou outro) que abre este repositório pela primeira vez numa empresa nova.** O repositório vem com a arquitetura e os métodos; o que falta é o **fato** da empresa. Este roteiro diz **o que perguntar, em que ordem, onde cada resposta vai e o que nunca se inventa.** Rode-o como uma entrevista: um bloco por sessão, respostas registradas **literalmente** (entre aspas, com data), e cada bloco fechado com o arquivo escrito e lido de volta para quem respondeu.

### As quatro regras da entrevista

1. **Pergunta só o que é FATO.** Preço, capacidade, prova, o que entrega, palavra do público, quem decide, quanto tem em caixa. **Estrutura — promessa, mecanismo, narrativa, ordem dos argumentos, recorte de público — é decisão do agente, feita a partir dos fatos** (`CLAUDE.md` §8, REGRA Nº 0). Perguntar estrutura ao dono é erro de método.
2. **O que ele não sabe vira `a calibrar` ou `n=0`, escrito assim.** Nunca palpite, nunca "deve ser uns". Campo inventado contamina toda peça produzida depois.
3. **Registra literal, decide depois.** A fala do dono entra entre aspas, com data. A leitura do agente vem separada e marcada como leitura (`CLAUDE.md` §11.2).
4. **Um bloco por vez, e o arquivo nasce no fim do bloco.** Entrevista inteira sem arquivo é conversa que se perde no fim da sessão.

### Bloco 0 — quem opera (10 min) → `CLAUDE.md` §1, `STATUS.md` §4, `POLITICAS` §1

- Nome da empresa e de quem detém a alçada. Há sócio? Qual a participação e **existe instrumento assinado**? Se não existe: registrar *"acordo verbal — não oponível"* e abrir pendência em `80-juridico/societario/`.
- Quem executa, quantas pessoas, quantas horas de entrega por semana **cada uma** (de verdade, não de intenção; se não sabe, `a calibrar` e medir em duas semanas).
- Que ferramenta de IA opera o repositório (Claude Code, Codex, outra) e quem é o **dono nomeado do registro** (nome, não cargo). Sem dono, o repo congela em 30 dias.
- Rodar: `python3 40-operacao-rotinas/ferramentas/instanciar-template.py --definir EMPRESA="…" OPERADOR="…"`.

### Bloco 1 — a empresa (20 min) → `PROJECT.md`, `SCOPE.md`, `00-core/CULTURA.md` §0 e §9

- O que a empresa vende, para quem, há quanto tempo, e **o que já vendeu de fato** (clientes pagantes, quantos, por quanto).
- Constituição: CNPJ, cidade, banco por onde o dinheiro passa (empresa e pessoal são a mesma conta?).
- O vocabulário próprio do dono: termos, modelos e referências que ele usa sem explicar (vão para `PROJECT.md` §1; o agente passa a usá-los como língua de trabalho).
- De onde vem a cultura dele (o fundamento que o move) e **como a marca aparece** quando aparece (arquétipo dominante e secundários — se não souber, fica para o Bloco 7).
- Stack: CRM, automação, site, onde publica, o que paga por mês em ferramenta.

### Bloco 2 — os números que decidem (30 min) → `00-core/POLITICAS-DE-DECISAO.md`

Perguntar **um a um**, na ordem do arquivo, e escrever a resposta no lugar do `{{…}}`:
- Norte: qual MRR, até quando. Os gates de estágio (`MRR_ESTAGIO_B`, `MRR_ESTAGIO_C`): o agente propõe a partir do norte; o dono confirma.
- Teto de despesa que exige decisão explícita. Horas de entrega por semana. Teto de horas por mês.
- Piso de valor-hora e margem mínima: **se o dono nunca calculou, o agente calcula a partir do custo fixo mensal ÷ horas de entrega, mostra a conta e pergunta se aceita** — e marca `[estimado]`.
- Verba de teste de mídia por tentativa (só se houver tráfego frio).
- Tudo o que ele responder "não sei" fica `a calibrar` e entra no `STATUS.md` §6.

### Bloco 3 — quem compra (30 min) → `30-comercial/ICP.md`

- Os últimos 5 clientes que pagaram: segmento, faturamento aproximado, **por que canal chegaram** (indicação, frio, inbound), ticket, o que compraram, o que travava a operação deles antes.
- Os últimos 5 que **não** fecharam: o que disseram, literalmente.
- O canal em que o cliente opera (WhatsApp, e-mail, balcão) — pré-requisito de acoplagem.
- Quem o dono **não** quer atender, e por quê.
- Com isso o agente escreve §2 (primário, com `n`), §2.1 (canal, com o dado), §4 (anti-ICP) e deixa §3 (expansão) vazio até haver caso. **O score do §5 não se pergunta: o agente aplica aos 10 nomes e mostra o resultado.**

### Bloco 4 — o que se vende e por quanto (30 min) → `30-comercial/oferta.md`, `servicos.md`, `produtos.md`, `POLITICAS` §5

- Lista do que ele vende hoje: nome, o que entrega, prazo, preço (setup e mensal, separados), **quantas vezes vendeu cada um**.
- O que ele gostaria de vender e nunca vendeu (vai para o roadmap, marcado `n=0`, nunca para a escada vigente).
- Capacidade por oferta: quantas horas cada entrega consome, **em construção e em operação** (duas fases, `POLITICAS` §4-ter). Se não mediu, `[estimado por analogia]`.
- O agente monta a escada (§3 da oferta) nos degraus do método — diagnóstico pago, construção, recorrência, maior valor — **e é ele quem decide em que degrau cada oferta cai**. O dono objeta congruência; não decide estrutura.

### Bloco 5 — como se vende e se entrega (20 min) → `30-comercial/onboarding.md`, `prospeccao-*/`, `40-operacao-rotinas/RITUAIS.md`, `GESTAO-DO-TEMPO.md`

- Como um cliente entra hoje, passo a passo, do primeiro contato ao primeiro pagamento. Onde trava.
- O que acontece na primeira semana depois de fechar (o onboarding real, não o desejado).
- O dia padrão do dono: a que horas prospecta, entrega, atende; o que sempre engole o quê.
- Metas semanais que ele já persegue (conversas, propostas, fechamentos) — ou `a calibrar`.

### Bloco 6 — dinheiro e papel (20 min) → `45-financeiro/`, `940-operador/FINANCAS.md`, `80-juridico/DADOS-DO-CONTRATADO.md`, `80-juridico/registros/`

- Caixa hoje, custo fixo mensal, passivo, **a obrigação dura mais próxima** (data, valor, origem do dinheiro).
- Qualificação para contrato (nome completo, CPF/CNPJ, endereço, e-mail, Pix) — direto para `DADOS-DO-CONTRATADO.md`.
- Relação ativa sem instrumento escrito (cliente, parceiro, fornecedor, sócio)? Cada uma vira pendência jurídica com data.
- Conflito ou cobrança em aberto? Abre registro em `80-juridico/registros/` no padrão das 4 camadas.

### Bloco 7 — voz e marca (quando houver material) → `10-skills/voz-operador.skill.md`, `945-branding/`

- **Não se pergunta "como é a sua voz".** Pede-se material: 2 a 3 calls gravadas, 20 mensagens de WhatsApp enviadas, textos publicados. A voz se **mede** pela `100-métodos/Método de extração de linguagem/`; sem corpus, a skill fica esqueleto e as peças saem na voz neutra do método.
- Marca: logo, cores e fontes existentes; referências visuais que ele admira. O arquétipo sai de `100-métodos/ARQUETIPOS-DE-MARCA.md`, proposto pelo agente.

### Bloco 8 — as contas (uma sessão por cliente ativo) → `clientes/<Cliente>/`

Para cada cliente ativo: criar a pasta pelo molde (`clientes/README.md`), rodar o `PEDIDO-UNICO.md` e registrar `STATUS.md` + `DECISOES.md` com o que já foi decidido e **o que foi descartado**. Toda call gravada é destilada, nunca resumida.

### Fechamento da entrevista

- `STATUS.md` §1 a §6 preenchidos; §7 já vem pronto.
- `python3 40-operacao-rotinas/ferramentas/instanciar-template.py --listar` com zero placeholders obrigatórios (os de preço podem ficar `a calibrar`, escritos assim).
- `python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py` em ✅.
- Uma entrada no topo do `STATUS.md`: *"repositório instanciado em DD/MM/AAAA; pendências de calibração: …"*.
- **O primeiro pedido real roteado pelo `CLAUDE.md`/`AGENTS.md` §6** — e o que o repositório não soube responder vira a próxima pergunta. É assim que ele passa a ser da empresa.

---
