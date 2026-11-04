# MAPA DO REPO — como a {{EMPRESA}} decide, roteia, produz e registra

> **Tipo:** índice · camada 3 · **Alçada:** {{OPERADOR}}
> **Método aplicado:** `100-métodos/METODO-CAMADA-DE-VER.md` — arquitetura do §7-bis (o mapa inteiro primeiro, uma seção por caixa depois), gramática do §2, formato Mermaid do §4.
> **Este `.md` é a fonte.** Uma versão visual (Mermaid em HTML) pode ser gerada dele; não vem no template.
> **Complementa o `README.md`**, que é índice de arquivos. Este é o grafo de funcionamento: o README diz *o que existe*, este diz *o que acontece depois*.

---

## 0. O MAPA INTEIRO

**Um pedido entra por cima e sai por baixo, e o que sai volta a alimentar o que entra.**

```mermaid
flowchart TD
    P([Pedido chega]) --> C[1 · CARGA<br/>o que se lê sempre]
    C --> R[2 · ROTEADOR<br/>pedido vira árvore]
    R --> A{3 · ALÇADA<br/>é fato ou estrutura?}
    A -- "FATO<br/>dado do negócio dele" --> PG[Perguntar ao dono<br/>vazio PARA a produção]
    PG --> A
    A -- "ESTRUTURA<br/>como vender" --> X{4 · EXECUÇÃO<br/>decide ou executa?}
    X -- "decide" --> CIR[5 · CIRCUITO<br/>produção da peça]
    X -- "executa" --> ANT[Antessala do executor isolado<br/>proposta, nunca estado]
    ANT --> CIR
    CIR --> G{6 · GATES<br/>passa nos vetos?}
    G -- "Ainda não" --> CIR
    G -- "Sim" --> RG[7 · ENTREGA<br/>E REGISTRO]
    RG --> ST[(ESTADO VIVO<br/>STATUS + STATUS-CODEX)]
    ST --> C
```

> ## ⭐ Tudo que vem depois é o detalhe de uma destas sete caixas.

**As três coisas que este desenho diz e nenhum texto do repo dizia junto:**

| # | O que o grafo mostra |
|---:|---|
| **1** | 🔴 **A alçada vem ANTES da produção, não durante.** O losango 3 é a `REGRA Nº 0`, e ele está no caminho — não é uma checagem que se faz depois de escrever |
| **2** | **Há dois loops, e são os dois lugares onde o trabalho volta:** gate que reprova devolve à produção · pacote do Codex que não passa no rito **fica na antessala** |
| **3** | ⭐ **O ciclo fecha.** O registro alimenta o estado, e o estado é o que se carrega no próximo pedido. **Registro que não acontece quebra o círculo — e o próximo pedido começa cego** |

---

## 1 · CARGA — o que se lê antes de qualquer coisa

> ⚠️ **Esta seção não tem diagrama, e a ausência é o método funcionando.** Carga e precedência são **acervo**, não processo — `METODO-CAMADA-DE-VER.md` §6: *"não há fluxo, é acervo"*. Forçar um grafo aqui produziria o modo de falha 3, lista vertical fingindo de fluxograma.

**Carga obrigatória, toda sessão:**

| Arquivo | Camada | O que dá |
|---|---|---|
| `CLAUDE.md` | — | autoridade, roteador, método, regra de registro |
| `00-core/*` | **Identidade** | princípio, cultura, e as **políticas que têm os números** |
| `STATUS.md` | **Estado** | o que É |
| 🔴 `execução Codex/STATUS-CODEX.md` | **Estado** | o que está **na antessala** (só se você usa um executor isolado) |
| 1 skill dominante | — | escolhida no roteador (§2 abaixo) |

> 🔴 **Estado = os dois arquivos, sempre que a operação usa um executor.** Ler o canônico sem a antessala dá retrato incompleto **e sem aviso** — o trabalho existe, está pronto, e o estado não o menciona. Sintoma típico: entrega pronta na antessala, estado da conta sem registrá-la.

🔴 ⭐ **Ordem de carga por tipo — o PROCESSO** (`00-core/TAXONOMIA-DE-ARTEFATOS.md` §4.2): `framework → trilho → método → blueprint → política → gate`. **Pular etapa é o erro clássico:** um gate de forma pode aprovar uma peça sem que a etapa anterior — por exemplo, o ICP — tenha rodado. **Gate não substitui etapa anterior.**

**Precedência em conflito:** `CLAUDE.md` → `POLITICAS-DE-DECISAO.md` → skill dominante → artefato de área.
**Exceções que invertem:** fato comercial → `30-comercial/ICP.md` · estado atual → `STATUS.md`.
🔴 **Pacote em `execução Codex/` nunca prevalece sobre canônico, por mais recente que seja.**

---

## 2 · ROTEADOR — como um pedido vira método carregado

**O `CLAUDE.md` §6 roteia por SETE ÁRVORES, cada uma com arquivo próprio em `00-core/roteador/` e a linha do PROCESSO preenchida. A ESCRITA tem portão — peça para cliente só entra com a CONTA passada.**

```mermaid
flowchart TD
    S([Pedido]) --> F{Que árvore?}
    F -- "decidir o negócio" --> NE[NEGÓCIO]
    F -- "abrir ou destravar conta" --> CO[CONTA]
    F -- "ler o que existe" --> LE[LEITURA]
    F -- "produzir peça" --> ES{ESCRITA<br/>conta já passou?}
    F -- "executar e entregar" --> OP[OPERAÇÃO]
    F -- "o próprio repo" --> CA[CASA]
    F -- "contrato e risco" --> JU[JURÍDICO]
    ES -- "Ainda não" --> CP[CONTA primeiro<br/>pilares e léxico]
    CP --> ES
    ES -- "Sim" --> PR[Processo da árvore<br/>tipos em ordem]
    NE --> PR
    CO --> PR
    LE --> PR
    OP --> PR
    CA --> PR
    JU --> PR
```

### 2.1 A família que mais cresceu — escrever para vender

**Ela tem tronco**, para que os métodos irmãos não fiquem soltos.

```mermaid
flowchart TD
    T[TRONCO<br/>METODO-DIRECT-RESPONSE] --> B1[FUNIL-DE-VSL<br/>um formato]
    T --> B2[BENCHMARKING<br/>uma prática]
    T --> B3[ESTRUTURA-INVISIVEL<br/>uma teoria]
    T --> B4[PONTOS-LOGICOS<br/>uma técnica]
    T --> B5[MECANISMO E ONE BELIEF<br/>o destino da cadeia]
    T --> B6[CONSTRUCAO-DE-CRIATIVOS-DR<br/>+ hooks + lateralização]
    B1 --> SK[skill de copy<br/>escreve a frase]
    B2 --> SK
    B3 --> SK
    B4 --> SK
    B5 --> SK
    B6 --> SK
```

> **A regra de precedência dentro da família, e ela resolve quase todo conflito:** **em conflito, vence o método de FORMATO** — ele conhece a física do canal. **Mas formato não revoga princípio:** se aplicar um formato parece exigir violar a fronteira de margem do DFY ou a régua de prova, o errado é a aplicação.

### 2.2 As três regras de leitura do `10-skills/`

| Tipo | Regra |
|---|---|
| **Ponteiro** (`# PONTEIRO —`) | 🔴 **nunca é fonte.** Seguir para onde ele aponta |
| **Legado** (`_legado/`) | 🔴 **nunca se carrega.** Serve para entender por que uma regra existe |
| **Portátil / persona / método** | fonte ativa |

> 🔴 **`REGRA Nº 1` do §8: nunca se ativa método na mão.** Se aplicar um método depende de alguém **lembrar** de carregá-lo, ele não está em produção — está guardado. **O roteador é o único mecanismo de carga que existe.**

---

## 3 · ALÇADA — o losango mais importante da casa

**`REGRA Nº 0`, instituída depois de uma conta perder a alçada da estrutura.**

```mermaid
flowchart TD
    L([Lacuna no brief]) --> Q{É um dado sobre o negócio dele,<br/>ou uma decisão sobre como vender?}

    Q -- "DADO<br/>preço, capacidade, prova,<br/>palavra do público" --> F[Perguntar. Obrigatório.<br/>🔴 Campo vazio PARA a produção]
    Q -- "DECISÃO<br/>promessa, mecanismo, narrativa,<br/>headline, ordem, recorte" --> D[Decidir. Obrigatório.<br/>🔴 Perguntar é erro de método]

    D --> O{Cliente objeta<br/>congruência?}
    O -- "Sim" --> R[Alterar do nosso jeito<br/>OU explicar por escrito]
    R --> D
    O -- "Não" --> P([Produzir])
    F --> P
```

> **Por que a alçada é legítima e não arrogância:** o cliente contrata **porque não sabe estruturar aquilo para vender.** Devolver a decisão de estrutura a ele é devolver o produto sem entregá-lo — e é entregar a pior versão, porque ele escolhe pelo que soa confortável, não pelo que converte.
>
> **O contrapeso que a torna justa:** ele tem **direito de objeção de congruência.** A mudança passa sempre por nós — **ou alteramos, ou explicamos por que não. Sempre, e por escrito.** Nunca silêncio, nunca acatamento automático.
>
> ⚠️ **E propriedade do ativo não é autoria da estrutura.** O site, o perfil e a marca são dele; o que dentro deles faz vender é nosso.

---

## 4 · EXECUÇÃO — quem decide, quem executa, e a antessala

```mermaid
flowchart TD
    T([Tarefa]) --> Q{Decide ou executa?}

    Q -- "decide" --> CL[Claude · papel de CEO<br/>lê CLAUDE.md]
    Q -- "executa<br/>frontend, varredura, volume" --> CX[Executor isolado (opcional)<br/>lê AGENTS-EXEC.md]

    CL --> CAN[(CANÔNICOS<br/>escrita direta)]

    CX --> ANT[(execução Codex/<br/>🔴 ÚNICA escrita dele)]
    ANT --> IDX[Linha no STATUS-CODEX<br/>na mesma tarefa]
    IDX --> RIT{RITO DE INTEGRAÇÃO<br/>gate de 5 passa?}
    RIT -- "Ainda não" --> ANT
    RIT -- "Sim" --> CAN
    CAN --> ST[(ESTADO VIVO)]
```

**As duas regras que o desenho torna visíveis:**

| Regra | Por que existe |
|---|---|
| 🔴 **O executor isolado só escreve em `execução Codex/`** | §0 do `AGENTS-EXEC.md`. Sem isso, proposta vira estado sem ninguém decidir |
| 🔴 **Pacote isolado é PROPOSTA, nunca estado** | e **a promoção é sempre nossa** — divergência entre antessala e canônico é sinal de promoção pendente, não de canônico desatualizado |

> ⚠️ **O buraco que o rito existe para fechar, e ele é real:** a §0 proíbe o Codex de escrever nos canônicos e o §11.3 exige que nada termine sem registro. **Sem rito, as duas regras se anulam** — o trabalho é feito, fica na antessala, e a memória não recebe.
>
> 🔴 **E o `AGENTS-EXEC.md` é a §0 + o corpo do `CLAUDE.md`**, por decisão de desenho. **A fronteira "quem decide × quem executa" existe como desenho e não como estado.** A contenção real vem da §0 e da `REGRA Nº 0`. **Quem altera o `CLAUDE.md` regenera o `AGENTS.md` na mesma tarefa** — replicar à mão foi tentado duas vezes e falhou as duas.

---

## 5 · CIRCUITO — como uma peça de conversão é produzida

**"Criar uma página" não carrega uma skill: abre um circuito de três skills em cinco etapas.**

```mermaid
flowchart TD
    E1[1 · FÍSICA<br/>gerador-web-designer] --> V1{Brief de 9 campos<br/>existe?}
    V1 -- "Não" --> E1
    V1 -- "Sim" --> E2[2 · DIREÇÃO VISUAL<br/>ui-ux, modo direção]
    E2 --> V2{Direção declarada<br/>com limite de caracteres?}
    V2 -- "Genérica" --> E2
    V2 -- "Sim" --> E3[3 · ESCRITA<br/>copywriter-senior]
    E3 --> V3{Pivô apontável<br/>por linha?}
    V3 -- "Não" --> E3
    V3 -- "Sim" --> E4[4 · EXECUÇÃO VISUAL<br/>ui-ux, modo execução]
    E4 --> V4{Clímax na decisão?}
    V4 -- "Não" --> E4
    V4 -- "Sim" --> E5[5 · GATE<br/>gerador, papel do juiz]
    E5 --> S([Veredito de publicação])
```

**Por que a ui-ux entra duas vezes:** antes, para **dar restrição** — quem escreve precisa saber quantos caracteres cabem num título. Depois, porque **desenhar sobre texto real é diferente de desenhar sobre texto simulado.**

**Fronteiras que não se cruzam:** quem faz a física não escreve a frase nem escolhe a fonte · quem escreve não muda a ordem das dobras · quem desenha não reescreve a copy nem move o clímax. **Violação volta para o dono do artefato.**

**Quando encolhe:** auditar página existente → 1 e 5 · trocar oferta → 1 parcial, 3, 5 · refazer só o visual → 2, 4, 5.
🔴 **Nunca encolhem:** a classificação, o brief e o gate.

> ⭐ **Proposta comercial entra aqui.** Proposta não é documento, é peça de conversão — e segue o circuito como qualquer página.

---

## 6 · GATES — o que reprova, e quem checa

**Havia sete métodos com gate declarado, três com gate sob outro nome e dois juízes de skill. Nenhum auditava o CONJUNTO.**

```mermaid
flowchart TD
    O([Output pronto]) --> DC[Declaração de carga<br/>o que foi carregado]
    DC --> P0{P0 · Proporcionalidade<br/>método carregado decidiu algo?}
    P0 -- "Sobrou método" --> CORR[Corrigir]
    P0 -- "OK" --> P1{P1 · Régua de veto<br/>de cada método carregado}
    P1 -- "Veto batido" --> CORR
    P1 -- "OK" --> P3{P3 · Contradição<br/>entre métodos}
    P3 -- "🔴 resolvida em silêncio" --> CORR
    P3 -- "declarada ou inexistente" --> ENT([Entregar])
    CORR --> O
```

> ⭐ **As duas peças que tornam o gate barato: a DECLARAÇÃO DE CARGA no fecho, e a TABELA DE VETOS** — uma linha por método, com o que reprova sozinho. **O auditor checa essas linhas, não relê os métodos.**

**Os vetos que mais reprovam, e todos são binários:**

| Veto | De onde vem |
|---|---|
| cena ou fala de ICP **sem fonte apontável** | procedência (§6.1) |
| peça **sem pivô** E · Mas · Por isso | skill de copy |
| **P1 ou P4 reprovando** nos pilares | bloqueia produção de copy |
| proposta **sem bloco de onboarding** | Gate F da ancoragem |
| elo de cadeia **que não desaba** ao remover o anterior | pontos lógicos |
| peça no swipe file **sem dado de performance** | §11.5 |
| 🔴 **contradição entre métodos resolvida em silêncio** | gate de congruência |

---

## 7 · ENTREGA E REGISTRO — onde o ciclo fecha

> **Premissa:** este repositório é o **único sistema de memória da empresa.** Sem segundo lugar onde a informação viva. **Se algo só existe na conversa com a IA, não existe** — some no fim da sessão.

```mermaid
flowchart TD
    E([Entrega feita]) --> T{Que natureza<br/>tem o que aconteceu?}

    T -- "conversa externa" --> R1[Registro de 4 camadas]
    T -- "call gravada" --> R2[Destilação<br/>nunca resumo]
    T -- "decisão tomada" --> R3[DECISOES do cliente<br/>+ STATUS]
    T -- "peça que performou" --> R4[swipe-file<br/>só com dado]

    R1 --> S[(STATUS.md<br/>atualizado)]
    R2 --> S
    R3 --> S
    R4 --> S
    S --> PROX([Próxima sessão<br/>carrega daqui])
```

**As quatro camadas de todo registro de interação externa — e faltar uma quebra a continuidade:**

| # | Camada | Sem ela |
|---:|---|---|
| 1 | fatos e números | não se sabe onde estamos |
| 2 | decisões **e o descartado** | alguém refaz o caminho já andado |
| 3 | ⭐ **tom e conduta** | **é a que sempre falta.** A próxima mensagem quebra o clima que a anterior construiu |
| 4 | mensagens literais | não se sabe o que a outra parte já ouviu |

> **O teste de suficiência, e é um só:** *outra IA, abrindo só este arquivo, escreveria a próxima mensagem no tom certo e sem repetir erro nosso?*
> Se não, **falta a camada 3 ou a 4.**

---

## 8. O QUE FALTA — nosso × seu

> **Instrução:** liste aqui o que está em aberto na SUA operação e de quem é (seu, de um parceiro ou de um fornecedor). Comece pelos itens que o template deixa para você: a fila do `RITO-INTEGRACAO-CODEX.md` §9 (vazia, se você não usa executor isolado), o inventário Done For You (`30-comercial/oferta.md` §7-bis, tabela vazia a preencher), a verificação em caso real dos métodos 🟡 provisórios e a conferência deste mapa depois de cada método novo (§9).

| O quê | De quem | Estado |
|---|---|---|
| *(preencha)* | *(seu · parceiro · fornecedor)* | *(🔴 aberto · 🟡 em andamento · ✅ fechado)* |

---

## 9. O QUE ESTE MAPA NÃO FAZ

- **Não substitui o `CLAUDE.md`.** O mapa dá o modelo; o kernel dá a autoridade e os detalhes. **Diagrama sozinho vira organograma bonito que ninguém sabe defender.**
- **Não é fonte de regra.** Se este arquivo divergir do `CLAUDE.md`, **vale o `CLAUDE.md`** e a divergência é sinal de que o mapa envelheceu.
- **Não lista todos os métodos.** Lista as seis famílias. O acervo completo está no `§7` do kernel.
- 🔴 **Não se mantém sozinho.** Método novo muda o roteador, e o roteador é a §2 daqui. **Este arquivo entra na mesma tarefa da `REGRA Nº 1`** — ou vira o desenho de um repositório que não existe mais.

---
*Aplicação do `METODO-CAMADA-DE-VER.md`: arquitetura do §7-bis, gramática do §2, Mermaid do §4. **Teste de correspondência: sete caixas no mapa, sete seções — fecha.** A §1 é deliberadamente sem diagrama (acervo, §6 do método).*
