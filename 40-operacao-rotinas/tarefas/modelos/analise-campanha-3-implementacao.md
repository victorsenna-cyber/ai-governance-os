---
id: T-AAAA-MM-DD-nnn
titulo: Implementação do briefing de otimização — <Cliente> (Sonnet executa, só o briefing)
criada: AAAA-MM-DD
prazo: 
prazo_duro: nao
conta: <Cliente>
arvore: OPERACAO
carga: mecanica
classe_dado: C
nivel_minimo: N3
escada: N3,N4
swarm: nao
comando: 
verificacao: 
insumos: clientes/<Cliente>/NN - tráfego pago/diario/AAAA-MM-DD-BRIEFING.md; clientes/<Cliente>/NN - tráfego pago/scripts/; clientes/<Cliente>/NN - tráfego pago/LOG-DECISOES.md
saida: clientes/<Cliente>/NN - tráfego pago/diario/AAAA-MM-DD-BRIEFING.md
alcada: executa so ordens com aprovada: sim, uma por vez, na ordem; nada fora da ordem; le o status de volta nos tres niveis antes de dizer feito; falhou = para e registra; nao decide; nao envia nada ao cliente
estimativa_tokens: 30000
depende_de: <id da análise de hoje>
tipo_decisao: 
prioridade: 2
recorrencia: diaria
estado: planejada
agendada_para: AAAA-MM-DDT10:00
---
# Implementação do briefing de otimização — <Cliente>

## Pedido
`100-métodos/METODO-ANALISE-DIARIA-DE-CAMPANHA.md` §4 e contrato §6.3. Lê só o briefing (nem a análise, nem o diário). Se o §1 do briefing não tem nenhuma ordem `aprovada: sim`, a task termina em `entregue/` com "nada a executar" no log (ordens `aguardando {{OPERADOR}}` ficam no cartão). Para cada ordem aprovada: executar pelo script da conta em `scripts/` (agendado) ou pelo MCP da Meta (sessão), ler o status de volta em campanha, conjunto e anúncio, escrever a linha no `LOG-DECISOES.md` (data · o quê · por quê · resultado esperado · medido: —) e a linha do §4 do briefing. Mudou `verbaDia`: atualizar `painel.json`. Achado fora das ordens: §4 do briefing, sem mexer.

## Pronto quando
Toda ordem `aprovada: sim` tem linha no §4 do briefing com status lido de volta **e** linha no `LOG-DECISOES.md`; ou o log da task diz "nada a executar".

## Log
