---
id: T-AAAA-MM-DD-nnn
titulo: Coleta diária de campanha — <Cliente> (Haiku cita, não lê)
criada: AAAA-MM-DD
prazo: 
prazo_duro: nao
conta: <Cliente>
arvore: OPERACAO
carga: mecanica
classe_dado: C
nivel_minimo: N2
escada: N2
swarm: nao
comando: 
verificacao: python3 -c "import sys,datetime as d; from pathlib import Path; sys.exit(0 if Path('clientes/<Cliente>/NN - tráfego pago/diario/'+d.date.today().isoformat()+'.md').exists() else 1)"
insumos: clientes/<Cliente>/NN - tráfego pago/diario/README.md; 90-templates/trafego-cliente/diario/AAAA-MM-DD.md; clientes/<Cliente>/NN - tráfego pago/LOG-DECISOES.md; <fonte dos números: export do Gerenciador em clientes/<Cliente>/NN - tráfego pago/diario/entrada/AAAA-MM-DD.csv, ou saída do coletar-campanha.py>
saida: clientes/<Cliente>/NN - tráfego pago/diario/AAAA-MM-DD.md
alcada: nao envia; nao toca na plataforma; nao interpreta, nao compara, nao sugere; nao escreve em LOG-DECISOES.md nem em DECISOES.md
estimativa_tokens: 15000
depende_de: 
tipo_decisao: 
prioridade: 2
recorrencia: diaria
estado: planejada
agendada_para: AAAA-MM-DDT08:00
---
# Coleta diária de campanha — <Cliente>

## Pedido
`100-métodos/METODO-ANALISE-DIARIA-DE-CAMPANHA.md` §2 e contrato §6.1. Com os números do insumo, escrever o diário de hoje pelo molde, todas as colunas, fonte e hora em todo número, `—` onde não há dado. Copiar no rodapé as entradas dos últimos 3 dias do `LOG-DECISOES.md`, literais. Sem adjetivo, seta, comparação ou sugestão.

⚠️ Esta task só roda agendada quando o insumo chegar sem sessão: `coletar-campanha.py` (N0, a construir) ou um export do Gerenciador salvo em `diario/entrada/`. Até lá, a coleta roda na sessão, pelo contrato §6.1, com um subagente `haiku`.

## Pronto quando
`diario/<hoje>.md` existe, tem as seis seções do molde e nenhuma célula das tabelas 2–4 está vazia (valor ou `—`).

## Log
