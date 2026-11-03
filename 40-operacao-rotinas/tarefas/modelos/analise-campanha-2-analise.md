---
id: T-AAAA-MM-DD-nnn
titulo: Análise e briefing de otimização — <Cliente> (Fable decide, por regra)
criada: AAAA-MM-DD
prazo: 
prazo_duro: nao
conta: <Cliente>
arvore: OPERACAO
carga: julgamento
classe_dado: C
nivel_minimo: N5
escada: N5
swarm: nao
comando: 
verificacao: 
insumos: clientes/<Cliente>/NN - tráfego pago/diario/ (hoje + 7 anteriores); clientes/<Cliente>/NN - tráfego pago/PLANO-DE-MIDIA.md; clientes/<Cliente>/NN - tráfego pago/LOG-DECISOES.md; clientes/<Cliente>/NN - tráfego pago/painel.json; clientes/<Cliente>/NN - tráfego pago/estrutura-campanhas.md; clientes/<Cliente>/NN - tráfego pago/matriz-criativos.md; 100-métodos/METODO-TRAFEGO-PAGO.md; 100-métodos/METODO-ITERACAO-DE-CPA.md; 100-métodos/METODO-ANALISE-DIARIA-DE-CAMPANHA.md
saida: clientes/<Cliente>/NN - tráfego pago/diario/AAAA-MM-DD-BRIEFING.md
alcada: nao executa na plataforma; nao coleta; nao inventa numero fora dos diarios; ordem A1 nasce com aprovada: aguardando {{OPERADOR}}; ordem A2 nasce aprovada: sim; criativo ou publico novo vira task em fila/, nunca ordem
estimativa_tokens: 60000
depende_de: <id da coleta de hoje>
tipo_decisao: kill_hard_campanha
prioridade: 2
recorrencia: diaria
estado: planejada
agendada_para: AAAA-MM-DDT09:00
---
# Análise e briefing de otimização — <Cliente>

⚠️ N5 agendado (`claude -p --model claude-fable-5-1`) só vale depois de provado fora de sessão nesta instalação; até lá esta task roda em sessão aberta.

## Pedido
`100-métodos/METODO-ANALISE-DIARIA-DE-CAMPANHA.md` §3 e contrato §6.2. Escrever dois arquivos pelos moldes: `diario/<hoje>-ANALISE.md` (estado por item com o número que disparou a regra, §7.3 do método-mãe, plano da conta prevalece; anomalia e degrau do diagnóstico §7.4; CPA como juiz; amostra mínima; decisões em resumo; o que NÃO se faz, com motivo; aprendizado do dia) e `diario/<hoje>-BRIEFING.md`, o briefing de otimização: ordens na ordem, com `id`, nível, ação exata, de → para, regra + número, resultado esperado em número e data, `tipo_decisao`, alçada (§5 do método) e `aprovada`; via e prova; o que não tocar. O Sonnet executa só pelo briefing. Máximo uma mudança estrutural. Série com menos de 3 diários: só kill hard. Ordem A1 → também cartão em `40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md`.

## Pronto quando
`diario/<hoje>-ANALISE.md` e `diario/<hoje>-BRIEFING.md` existem; toda linha do §1 do briefing tem as dez colunas; o §4 da análise não está vazio; nenhum número dos dois arquivos falta nos diários carregados.

## Log
