# TEMPLATE — REPO DE CLIENTE ("o cérebro da operação")

> **Tipo:** blueprint *(antes: "template de entrega"; 26/09/2026)* · camada 3 · **Instituído:** 23/09/2026 · **Alçada:** {{OPERADOR}}
> **Origem:** insight do {{OPERADOR}} — entregamos também um repo exclusivo, criado para aquela empresa, para quem quer que opere dentro de um repo preparado, com toda a ficha técnica que direcionamos; a ideia é entregar um cérebro para tomada de decisões e criação, assim como este repo já faz.
> **O que ele é no nosso sistema:** `METODO-DIRECT-RESPONSE.md` §4.2 — **degrau 3 do Done For You, o ativo funcional.** É o primeiro item real do inventário do `30-comercial/oferta.md` §7-bis, que estava vazio desde 18/09.

---

## 1. A TESE, E ELA NÃO É "ENTREGAR ORGANIZADO"

**Hoje entregamos ICP, promessa, mecanismo, oferta e plano como DOCUMENTOS.** Documento é lido uma vez e arquivado. **Três semanas depois, quem escreve o anúncio não abre o PDF do ICP — escreve de memória.**

> ## ⭐ O repo não é a entrega organizada. É o CONTINENTE que faz a entrega ser carregada toda vez que alguém for produzir.
>
> **A diferença é mecânica, não estética:** documento depende de alguém lembrar de consultar. **Repo com kernel é carregado por um agente a cada sessão** — e é exatamente por isso que o repo da {{EMPRESA}} funciona e uma pasta de PDFs não funcionaria.

**É a `REGRA Nº 1` do nosso `CLAUDE.md` §8 aplicada ao cliente: *nunca se ativa método na mão.*** Se aplicar o ICP depende de alguém lembrar dele, ele não está em produção — está guardado.

### 1.1 🔴 O que isso resolve na objeção que ninguém verbaliza

`METODO-DIRECT-RESPONSE.md` §4.1: dentro de toda venda opera uma **baixa autoestima** — *"seu método funciona, mas eu não vou conseguir executar."*

**O repo responde essa objeção melhor que qualquer promessa**, porque o cliente não precisa executar o julgamento: **o julgamento está instalado no kernel, e a equipe dele opera dentro dele.**

---

## 2. 🔴 A FRONTEIRA QUE DECIDE O QUE ENTRA — e ela protege o nosso produto

**Dois conteúdos parecem a mesma coisa e não são:**

| | Entra no repo do cliente | Fica na {{EMPRESA}} |
|---|---|---|
| **O quê** | **o RESULTADO das nossas decisões** para aquela operação | **os MÉTODOS que produziram as decisões** |
| Exemplos | o ICP *dele*, com léxico e fonte · a promessa *dele* · o mecanismo *dele*, com apelido · a oferta *dele* · a voz da marca *dele* · as provas que ele pode afirmar · os gates daquela operação | `METODO-DIRECT-RESPONSE` · `METODO-ALCADA-DE-ESTRUTURA` · `METODO-PONTOS-LOGICOS` · `METODO-BENCHMARKING` · `METODO-TESTE-DE-PILARES` · o gate de congruência · **todo o `100-métodos/`** |
| A metáfora | **o peixe** | **a vara** |

> 🔴 **Por que a linha existe, e não é mesquinharia:** o `CLAUDE.md` §8 registra que **o que vendemos é a forma de pensar estratégia — hora é insumo comprável, ela não.** Entregar o `100-métodos/` dentro do repo do cliente é entregar o produto inteiro no preço de uma implementação.
>
> ⚠️ **E há um segundo produto escondido aqui, que NÃO temos e não se vende por acidente: transferência de método.** Se algum dia vendermos isso, é contrato próprio, preço próprio e cláusula própria. **Misturar os dois na mesma proposta é vender o caro no preço do barato.**

**O teste de uma linha, quando surgir dúvida sobre um arquivo:**

> **Este arquivo serviria a outro cliente com um copiar-colar?**
> **Sim → é método nosso, não entra.** · **Não, é específico desta operação → entra.**

---

## 3. O ESQUELETO — e ele é fechado de propósito

```
<empresa>/
├── CLAUDE.md              ← o kernel. Papel, roteador, réguas, precedência
├── STATUS.md              ← estado vivo daquela operação
├── DECISOES.md            ← log com data e razão, incluindo o descartado
├── 01-QUEM-COMPRA.md      ← ICP + léxico do público, com grau de procedência
├── 02-O-QUE-VENDEMOS.md   ← promessa · mecanismo e apelido · oferta · preço
├── 03-COMO-FALAMOS.md     ← voz da marca, e o que nunca se diz
├── 04-PROVAS.md           ← o que pode ser afirmado, e a fonte de cada afirmação
├── 05-GATES.md            ← o que reprova uma peça antes de publicar
├── pecas/                 ← o que foi produzido, com o dado de performance
├── NN - tráfego pago/     ← plano de mídia, estrutura de campanhas, scripts de criação de campanha, matriz de criativos, log, relatórios (molde: 90-templates/trafego-cliente/)
└── NN - web design/       ← páginas e site do cliente e a configuração de publicação delas (deploy)
```

> ⭐ **Regra de lugar:** tudo o que é do cliente mora no repo dele, e as duas pastas de execução entram no esqueleto com a numeração do próprio cliente (`NN` = o número que a pasta tem na sequência dele; se não existe, cria-se com o próximo livre). Páginas de cliente ficam em `NN - web design/`; scripts de campanha e plano de mídia ficam em `NN - tráfego pago/`. Nada de cliente em `30-comercial/`.

🔴 **Nove itens de kernel mais as duas pastas de execução (25/10/2026), e o esqueleto não cresce por pedido.** Repo é fácil de prometer e cresce sozinho — **e repo que cresce vira o PDF de 40 páginas que ninguém abre, com passos a mais.** Item novo entra por decisão registrada, não por conveniência de uma tarefa.

**O `CLAUDE.md` do cliente é a peça central**, e o modelo está em `CLAUDE-modelo.md`, nesta pasta. Os oito arquivos restantes **são a entrega que já vendemos** — ICP, promessa, mecanismo, oferta, voz — apenas escritos dentro do continente em vez de soltos como documento. **Isso é o que torna o repo barato para nós: ele não adiciona entrega, adiciona forma.**

---

## 3-bis. 🔴 O REPO VIVO — onde mora e como sincroniza *(instituído 30/10/2026, alçada {{OPERADOR}}; `CLAUDE.md` §11.6)*

Repo entregue não é pasta entregue. **Ele mora na pasta do cliente, em `clientes/<Cliente>/entregaveis/<pasta>/`, como clone git com GitHub próprio, e só ali se edita** — como a Governança.

| Ato, na tarefa em que o repo nasce | Como |
|---|---|
| 1 · clone vivo na pasta do cliente | `git clone <remoto> clientes/<Cliente>/entregaveis/<pasta>` (ou o repo criado ali e publicado) |
| 2 · linha no `.gitignore` da Governança | `clientes/<Cliente>/entregaveis/<pasta>/` — sem ela a sincronia pula o repo, para ele não virar gitlink |
| 3 · linha no registro da conta | `clientes/<Cliente>/entregaveis/repositorios.json`: `nome`, `pasta`, `remoto`, `ferramentas` (onde as ferramentas moram dentro do repo) |
| 4 · ferramentas e hooks | **nada a fazer à mão**: a próxima sincronia copia `ferramentas/` desta pasta e cria `.claude/settings.json` a partir de `settings.modelo.json` |
| 5 · gate do repo | `verificar.py` dentro dele: vetos de dado sensível (bloqueiam a publicação), rota no `CLAUDE.md` do cliente, índice no `README.md`, caminhos que existem. Pastas estritas e isentas em `verificar.json`, ao lado |
| 6 · máquina do cliente | Git e Python instalados; o primeiro `git clone` loga no GitHub pelo navegador; daí em diante os hooks sincronizam ao abrir e ao fechar cada conversa |

🔴 **A fonte das ferramentas é `ferramentas/`, nesta pasta.** Muda-se aqui, e a sincronia propaga. Ferramenta editada dentro do repo de um cliente é sobrescrita na rodada seguinte.
**Transferência de dono no GitHub:** troca-se o `remoto` no `repositorios.json`; a próxima sincronia acerta o clone.

---

## 4. 🔴 AS TRÊS CONDIÇÕES DE ENTREGA — sem elas o repo vira pasta morta

**Nenhuma é opcional, e as três entram no bloco de onboarding da proposta** (`METODO-ANCORAGEM-DE-PROPOSTA.md` §0-ter, régua 2-bis).

| # | Condição | Sem ela |
|---:|---|---|
| **1** | ⭐ **Um agente carrega o kernel.** O repo só é "cérebro" se houver uma IA lendo o `CLAUDE.md` a cada sessão — Claude Code, Cowork, Codex ou equivalente | **vira uma pasta de markdown**, que é pior que PDF: tem a mesma inércia e parece mais trabalho |
| **2** | 🔴 **Alguém nomeado escreve nele.** O nosso repo funciona porque o `§11.3` é executado. **No repo do cliente, quem executa?** Nome, não cargo | **congela em 30 dias**, e a equipe passa a decidir sobre estado velho — pior que não ter, porque o erro vem com aparência de fonte |
| **3** | **A equipe usa, e a primeira peça é escrita conosco dentro dele** | fica sendo o nosso jeito, imposto a quem trabalha de outro jeito. **Adoção não se pede, se demonstra uma vez** |

> ⚠️ **A condição 1 é LACUNA DE FATO** (`REGRA Nº 0`): com que ferramenta a equipe do cliente trabalha hoje? **Pergunta obrigatória, e ela precede a promessa do repo na proposta.** Prometer repo a quem não tem como carregá-lo é prometer o degrau 3 e entregar o degrau 1 — o erro que o `METODO-DIRECT-RESPONSE.md` §4.3 nomeia, e que o cliente detecta na primeira semana.

---

## 5. A ECONOMIA — por que isto é barato para nós e caro de copiar

| | |
|---|---|
| **Custo de construção** | **uma vez** — este template. Já pago ao ler esta linha |
| **Custo por cliente** | ⭐ **quase zero de conteúdo novo**: os oito arquivos recebem o que já produzimos. O custo é de **forma**, não de matéria |
| **Classificação** (`METODO-DIRECT-RESPONSE.md` §4.3) | **DFY escalável** — construído uma vez, entregue muitas. **Passa nas três perguntas** |
| **O que muda no preço** | 🔴 **nada, sozinho.** Ele aumenta percepção de valor e **reduz a hora do cliente** — e é isso que se escreve no bloco de onboarding. **Não é justificativa para preço maior na mesma entrega** |

> 🔴 **A armadilha:** somar entregável a uma proposta que o cliente achou cara é responder *"caro demais"* com *"então te dou mais coisa"*. **É deixar o escopo crescer enquanto o preço cai**, quando a política manda o inverso (`00-core/POLITICAS-DE-DECISAO.md`).
>
> **O repo entra como FORMA da entrega que já foi vendida. Nunca como argumento para destravar uma negociação parada.**

---

## 6. QUANDO **NÃO** ENTREGAR

| Não entregar | Por quê |
|---|---|
| **operação que ainda não existe** — produto em desenvolvimento, sem canal, sem venda | **cérebro de decisão sem decisão a tomar.** Régua-mãe do `§9`: resultado antes de construção |
| **cliente sem ninguém que opere** — sem equipe e sem intenção de ter | o repo pressupõe operador. Sem ele, é o nosso processo entregue a ninguém |
| **conta em negociação travada por preço** | ver `§5` — vira concessão disfarçada |
| **conta com risco estrutural aberto** (regulatório, societário, de produto) | o repo assume que a direção está decidida. **Se o negócio pode mudar de forma no mês seguinte, o cérebro nasce desatualizado** |

---

## 7. O QUE ESTE TEMPLATE NÃO FAZ

- **Não substitui a entrega.** O repo é continente; ICP, promessa e mecanismo continuam sendo o trabalho.
- **Não é software.** São arquivos de texto. **Nada de app, nada de banco, nada de manutenção técnica nossa.**
- **Não nos obriga a operar dentro dele.** Quem opera é a equipe do cliente; nós direcionamos.
- 🔴 **Não transfere método.** Ver `§2`. Se um dia transferirmos, é outro contrato.

---
*Instituído em 23/09/2026, alçada {{OPERADOR}}. Primeiro item real do inventário DFY (`30-comercial/oferta.md` §7-bis). Aplicação de `METODO-DIRECT-RESPONSE.md` §4.2 (escada), §4.3 (fronteira de margem) e §4.6 (o bloco de onboarding). **Verificação em caso real pendente — 🟡 vigência provisória.***
