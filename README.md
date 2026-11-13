# AI Governance OS

**O repositório de governança da Continuum AI Systems, aberto.** Uma empresa inteira escrita em arquivos que uma IA lê antes de responder: quem ela é, quais números decidem, o que já foi combinado com cada cliente e o que falta fazer hoje. A IA para de improvisar e passa a operar pelas regras da sua casa.

Este é o mesmo sistema que roda a operação de origem todos os dias, sem os dados dela. Você recebe a arquitetura, os métodos, os gates e as ferramentas. Os números, os clientes e a voz são seus.

---

## O que muda quando a empresa mora num repositório

| Sem ele | Com ele |
|---|---|
| Cada conversa com a IA começa do zero e você reexplica o negócio | Ela abre o `CLAUDE.md`, carrega política e estado, e responde como quem já estava na sala |
| A decisão de ontem some no histórico do chat | Toda decisão fica registrada com o porquê e com o que foi descartado |
| Preço e desconto saem da intuição do dia | Piso, teto e alçada estão escritos; proposta que fura a régua é reprovada antes de sair |
| O método bom depende de alguém lembrar de usá-lo | O roteador leva cada pedido ao método certo; o que não está roteado não existe |
| O modelo mais caro lê pasta e conta linha | Trabalho mecânico vai para o modelo barato, por regra e por trava |
| Você descobre o erro quando o cliente reclama | Um verificador reprova a tarefa que deixou ponta solta |

**Para quem:** dono de agência, consultor, operador solo e time pequeno que vende serviço e já usa IA todo dia. Funciona com Claude Code e com qualquer agente que leia `AGENTS.md`.

---

## Começo em 15 minutos

```bash
git clone https://github.com/victorsenna-cyber/ai-governance-os.git minha-governanca
cd minha-governanca
python3 40-operacao-rotinas/ferramentas/instanciar-template.py --listar      # todos os {{campos}} a preencher
python3 40-operacao-rotinas/ferramentas/instanciar-template.py --definir EMPRESA="Sua Empresa"
python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py              # tem de fechar em ✅
```

Depois abra a pasta no seu agente e peça: **"leia o `LEIA-ME-TEMPLATE.md` e me entreviste"**. O roteiro de entrevista (§8 de lá) preenche o repositório com a sua operação em uma tarde. O que você não souber responder fica `a calibrar`. Campo inventado contamina toda peça que vier depois.

Use um remoto **privado**. Repositório público só depois de ler `00-core/POLITICAS-DE-DECISAO.md` §8 e ligar o `varrer-publico.py`.

---

## Como ele pensa

Três camadas, carregadas nesta ordem a cada pedido:

1. **Identidade** (`00-core/`): princípio, cultura, modos de resposta. Muda raramente.
2. **Política** (`00-core/POLITICAS-DE-DECISAO.md`, `30-comercial/`): os números e as alçadas. Muda por decisão registrada.
3. **Estado** (`STATUS.md`, `60-planos/`, `clientes/<conta>/`): o que é verdade hoje. Muda toda semana.

**O roteador** (`CLAUDE.md` §6 e `00-core/roteador/`) classifica o pedido em uma de sete árvores: negócio, conta, leitura, escrita, operação, casa, jurídico. Cada árvore diz o que carregar, em que ordem, e o que veta a entrega. Quando o pedido cai em duas, abre primeiro a que produz o insumo da outra: proposta passa pelas âncoras antes da copy.

**Três regras seguram o resto** (`CLAUDE.md` §8):

- **Regra nº 0.** A estrutura de conversão é de quem opera, nunca do cliente. Lacuna de fato se pergunta; lacuna de estrutura se decide.
- **Regra nº 1.** Método criado sai roteado na mesma tarefa. O que depende de alguém lembrar de carregar está guardado, fora de produção.
- **Regra nº 2.** Em resposta direta, só se constrói sobre o que já está escalado no mercado.

---

## As ferramentas

O repositório funciona porque regra importante tem um script que a confere. Todas ficam em `40-operacao-rotinas/ferramentas/`, rodam com `python3` e não pedem servidor.

### Propagação: nada fica pela metade

| Ferramenta | O que faz | Quando roda | O que reprova |
|---|---|---|---|
| `verificar-propagacao.py` | Confere que todo método está no caminho certo, na árvore, no mapa, no registro e com régua de veto | Ao fechar toda tarefa que cria ou altera artefato | Método sem rota, arquivo que aponta para o que não existe, entregável fora do lugar |
| `sincronizar.py` | Commita, mescla com a `main`, regenera o `AGENTS.md` e publica. Faz o mesmo nos repositórios vivos de cliente | Ao abrir e ao fechar a sessão (hooks em `.claude/settings.json`) | Conflito real para a mescla e avisa; dado sensível em repositório de cliente não sobe |
| `derivados.py` | Calcula o que mudou no seu repositório desde a última vez que cada repositório derivado (o de um cliente, o de um parceiro) foi atualizado, e abre a tarefa de porte | Semanal | Porte que leva item em quarentena ou contraria exceção declarada do derivado |
| `backup-governanca.py` | Cópia fora da pasta, só acrescenta | Em toda sincronia e antes de mexer no kernel | — |

```bash
python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py
python3 40-operacao-rotinas/ferramentas/sincronizar.py            # sem remoto: --sem-push
python3 40-operacao-rotinas/ferramentas/derivados.py --estado
```

### Roteamento de modelo: o caro só decide

A regra está em `00-core/PROTOCOLO-MULTI-MODELO.md`: varrer pasta, contar, conferir e transcrever é trabalho do modelo barato; decisão, estrutura e copy ficam com o modelo forte. Quatro peças fazem a regra valer sem depender de disciplina:

| Peça | O que faz |
|---|---|
| `despachar.py` | O despachante. Lê a fila de tasks, confere orçamento, janela e dependência, e lança cada uma no nível mais barato que a resolve: **N0** script puro · **N1** modelo gratuito · **N2** rápido · **N3** intermediário · **N4** forte · **N5** o mais forte |
| `gate-delegacao.py` | Hook que nega ao modelo caro a leitura mecânica (captura, transcrito, varredura longa) e o manda delegar |
| `.claude/agents/varredor.md` | O agente barato que faz esse trabalho e devolve achado com caminho e linha |
| `tokens/ORCAMENTO.json` + arquivo `PAUSA` | Teto de gasto por semana e por rodada; criar o arquivo `PAUSA` em `tarefas/` para tudo na hora |

```bash
python3 40-operacao-rotinas/ferramentas/despachar.py --dry-run    # mostra a fila, a ordem e o orçamento, sem executar
python3 40-operacao-rotinas/ferramentas/despachar.py              # uma rodada
python3 40-operacao-rotinas/ferramentas/medir-tokens.py           # consumo por dia, modelo e sessão
python3 40-operacao-rotinas/ferramentas/medir-contexto.py         # quanto cada peça custa de contexto fixo
```

### Operação por tasks: o trabalho que anda sozinho

`40-operacao-rotinas/tarefas/` é uma fila em pastas: `fila/ → executando/ → revisao/ → entregue/` (ou `falhou/`, ou `decisao/`). Cada task é um arquivo com pedido, insumos, saída, alçada e nível mínimo de modelo. O despachante roda em agenda; rotina diária é task com recorrência. O esquema completo está em `tarefas/README.md`.

### Gates: o que impede o erro de sair

| Ferramenta | O que segura |
|---|---|
| `varrer-publico.py` | Nome de cliente, segredo, documento e caminho de máquina em tudo o que é público, histórico do git incluído. O dicionário sai das suas próprias pastas de conta |
| `autonomia.py` | A lista fechada do que a IA nunca faz sem a sua palavra (dinheiro, contrato, mensagem a terceiro, apagar, infraestrutura). Fora da lista, ela faz e avisa. `--ato "<ato>"` classifica |
| `gate-fecho.py` | Devolve a resposta que termina oferecendo o que podia ter feito. Vem desligado: ligue no `.claude/settings.json` quando a lista fechada estiver calibrada |
| `decisoes_cartao.py` | O formato único do cartão de decisão: opções, recomendação, lastro. Decisão que chega sem isso é pergunta mal feita |

### O resto da caixa

`renomear-conta.py` (renomeia uma conta e reescreve todo caminho no mesmo ato) · `foto-da-operacao.py` (o retrato do dia, com cada número conferido) · `transcrever-audio.py` (áudio vira `.md` ao lado, local) · `propagar-decisoes.py` (a escolha vai ao registro da conta) · `painel-projetos.py` e `980-web-design/` (painéis que leem o repositório) · `90-templates/` (PDF, kit de marca, repositório de cliente, páginas de referência). Cada pasta tem o seu README.

---

## Mapa

| Pasta | O que contém |
|---|---|
| `CLAUDE.md` | O kernel: papel, carga, roteador, regras permanentes, rastro. `AGENTS.md` é a réplica para outros agentes |
| `00-core/` | Identidade, políticas de decisão, taxonomia de artefatos, protocolo multi-modelo e as sete árvores |
| `100-métodos/` | Os métodos, tipados: framework, trilho, método, política, gate |
| `10-skills/` · `.claude/` | Skills portáteis de copy, página e interface; personas; agentes; hooks |
| `30-comercial/` | ICP, oferta, onboarding, prospecção, swipe file. Esqueletos com a forma certa |
| `40-operacao-rotinas/` | Ferramentas, tasks, orçamento de tokens, rituais |
| `80-juridico/` | Políticas, modelos de contrato, registros |
| `90-templates/` | Moldes de entrega |
| `clientes/` | Uma pasta por conta, a partir de `_modelo/` |
| `STATUS.md` | O estado vivo. Fonte única do que é verdade hoje |

O grafo de funcionamento, com o que acontece depois de cada passo, está em `MAPA-DO-REPO.md`.

---

## De onde vem e como evolui

Criado e mantido pela **Continuum AI Systems**. Cada método e cada ferramenta daqui existe porque uma operação real precisou, e só entra depois de rodar num caso real dela. O que a casa de origem aprende chega a este repositório por um porte automático e anônimo: código vem copiado, texto vem reescrito sem cliente, sem preço e sem pessoa, e cinco gates conferem antes de qualquer publicação.

Método marcado com 🟡 é provisório: funciona, ainda não acumulou casos. Use e ajuste.

Achou um defeito ou adaptou para outro tipo de negócio? Abra uma issue. O repositório melhora pelo uso.
