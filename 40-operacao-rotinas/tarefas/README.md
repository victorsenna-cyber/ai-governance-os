# TAREFAS — operação por carga e por modelo

> **Tipo:** trilho (camada 3) · **Alçada:** {{OPERADOR}}
> **Princípio:** toda tarefa nasce como arquivo, planejada pelo Opus (ou por esta sessão); o despachante (`ferramentas/despachar.py`, script sem LLM) a executa no nível mais barato que a sustenta, dentro do orçamento medido; a saída cai em revisão e só sai da casa pelo {{OPERADOR}}.

## 1. O estado é a pasta (kanban em disco)

| Pasta | Significa | Quem move |
|---|---|---|
| `fila/` | planejada ou pronta para rodar | o Opus escreve aqui |
| `executando/` | um worker está nela (há `.lock` na raiz de `tarefas/`) | despachante |
| `revisao/` | executada; espera amostra do Opus (N1, N3, N4 e N5 sempre; N2 quando `carga` ≠ `mecanica`) | despachante → Opus (task recorrente `revisar-amostra`) |
| `decisao/` | precisa de escolha do {{OPERADOR}} (também vira cartão em `DECISOES-PENDENTES.md`, no molde `modelos/cartao-decisao.md`, régua `ferramentas/decisoes_cartao.py --lint`) | despachante ou Opus |
| `entregue/` | pronta e conferida | despachante (N0/N2 mecânica com verificação) ou Opus |
| `falhou/` | gate reprovou ou o worker quebrou; o motivo está no `## Log` | despachante |
| `log/` | uma linha por execução em `GASTO.jsonl` (tokens, nível, modelo, resultado) e um `RODADA-*.md` por rodada | despachante |
| `modelos/` | tasks-modelo com `<Cliente>`/`NN`/`AAAA-MM-DD` por preencher; **o despachante não lê esta pasta** — copiar para `fila/` e preencher (`analise-campanha-1-coleta`, `-2-analise`, `-3-implementacao`, `cartao-decisao`, `contexto-propagar`, `destilar-decisoes`, `entregavel`, `ordem-whatsapp`, `portar-derivados`, `porte-template`, `porte-template-modelo`) | o Opus |

Arquivo `PAUSA` em `tarefas/` para tudo. Três falhas seguidas numa rodada param a rodada.

## 2. Esquema da task (frontmatter)

```
---
id: T-AAAA-MM-DD-001          # único; prefixo T-<data>-<nnn>
titulo: ...
criada: AAAA-MM-DD
prazo: AAAA-MM-DD             # vazio = sem prazo
prazo_duro: nao               # sim = não pode adiar
conta: casa                   # ou o nome da pasta em clientes/
arvore: OPERACAO              # NEGOCIO CONTA LEITURA ESCRITA OPERACAO CASA JURIDICO
carga: mecanica               # mecanica leitura rascunho julgamento decisao
classe_dado: I                # P público · I interno sem cliente · C cliente · S sensível
nivel_minimo: N2              # N0 script · N1 gratuito · N2 Haiku · N3 Sonnet · N4 Opus · N5 Fable
escada: N2,N3                 # níveis permitidos, do piso para cima
swarm: nao                    # sim = pode ir ao Ruflo como worker externo (N4)
comando: python3 x.py              # só N0: o que rodar (cwd = raiz do repo)
verificacao: python3 y.py          # opcional, N0: comando que prova o "pronto quando" (saída 0 = passou)
insumos: a.md; b.md           # caminhos exatos, separados por ;
saida: caminho.md             # UM caminho
alcada: nao envia; nao decide preco; nao escreve em DECISOES.md
estimativa_tokens: 20000      # input + cache novo + output (sem cache lido)
orcamento:                    # `isento` = não espera a fatia (só ordem do {{OPERADOR}} por mensagem)
depende_de:                   # ids separados por ,
tipo_decisao:                 # se produz decisão: o tipo (para a escada A0–A3)
prioridade: 2                 # 1 fogo · 2 esta semana · 3 quando couber
recorrencia:                  # vazio · diaria · semanal
estado: pronta                # planejada pronta executando em_revisao aguardando_operador entregue bloqueada falhou
agendada_para:                # ISO; vazio = já
# — só tipo: entregavel (nasce por `entregaveis.py --nova`) —
tipo:                         # entregavel = promessa nossa ao cliente; o despachante local pula, uma rotina agendada executa
prometido_em:                 # data da call ou da mensagem em que prometemos
prometido_para:               # prazo DITO ao cliente; vazio = sem prazo dito
destinatario:                 # a pessoa, não a conta
forma:                        # documento · mensagem · artefato · pacote
fonte:                        # arquivo + ID do ponto + timestamp; sem fonte não nasce
pronto_em:                    # a rotina preenche
enviado_em:                   # só o clique Enviado do {{OPERADOR}} (ou a ordem literal dele) preenche
enviado_por:                  # painel | sessao-operador
---
# <título>
## Pedido
<o que fazer, para um executor que não viu a conversa>
## Pronto quando
<critério verificável; sem ele a task não roda>
## Log
<o despachante acrescenta aqui>
```

🔴 Réguas: dado `C`/`S` nunca em N1 · nada sai para cliente sem o {{OPERADOR}} · sem `## Pronto quando` não roda · nunca abaixo do `nivel_minimo`; orçamento batido = adia (se tem prazo e cabe) ou vira cartão de decisão (molde `modelos/cartao-decisao.md`) · um escritor no repo por vez.

## 3. Níveis

| Nível | Executor | Pode tocar | Faz | Nunca faz |
|---|---|---|---|---|
| N0 | script (`comando`) | tudo, local | medir, verificar, sincronizar, transcrever, `curl`, contar | ler sentido |
| N1 | gratuito (`ferramentas/freellmapi/n1_cliente.py`) | só `P` e `I` | rascunho interno, benchmarking público, formatação | dado `C`/`S`; peça final; canônico |
| N2 | `claude -p --model haiku` | `P I C` | edição mecânica, conferência, extração por checklist | escolha com duas opções válidas |
| N3 | `claude -p --model sonnet` | `P I C S*` | auditoria por checklist, rascunho para aprovação, inventário, opções para decisão | estrutura, preço, copy final |
| N4 | `claude -p --model opus` (ou Ruflo se `swarm: sim`) | tudo | planejar, decidir (REGRA Nº 0), copy, diagnóstico, revisar amostra | mecânico |
| N5 | `claude -p --model <modelo mais capaz disponível>` | tudo | o raro e caro: plano de iteração do repositório, auditoria de peça-mestra, passada global do juiz de VSL, decisão que cruza várias áreas, revisar amostra do N4 | tudo o que N4 sustenta; nunca por padrão |

## 4. Orçamento

`tokens/ORCAMENTO.json` guarda o teto semanal (calibrado por `medir-tokens.py --calibrar`) e a divisão sugerida 40/35/25 ({{OPERADOR}} · agendado · folga). O despachante soma o que o agendado já gastou na semana (`log/GASTO.jsonl`) e só lança task cuja `estimativa_tokens` cabe na fatia da rodada. N0 e N1 não contam.

## 5. Como rodar

```
python3 40-operacao-rotinas/ferramentas/despachar.py --dry-run     # lista, ordena, mostra orçamento, não executa
python3 40-operacao-rotinas/ferramentas/despachar.py               # uma rodada
python3 40-operacao-rotinas/ferramentas/despachar.py --so N0,N2    # só esses níveis
```

O agendador do sistema roda uma rodada por hora — Windows: Agendador de Tarefas (`continuum-despachante`); macOS: LaunchAgent instalado por `ferramentas/macos/instalar-mac.sh`; Linux: cron —, na janela que você definir. A primeira do dia escreve o brief (task `brief-diario`, recorrente).
