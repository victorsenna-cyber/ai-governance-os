---
id: T-AAAA-MM-DD-nnn
titulo: Portar para os derivados o que a casa mudou (porte-derivados)
criada: AAAA-MM-DD
tipo: porte-derivados
prazo: 
prazo_duro: nao
conta: casa
arvore: CASA
carga: julgamento
classe_dado: C
nivel_minimo: N4
escada: N4
swarm: sim
comando: 
verificacao: python3 -X utf8 40-operacao-rotinas/ferramentas/verificar-propagacao.py
insumos: <DELTA>; 40-operacao-rotinas/derivados/DERIVADOS.json; 40-operacao-rotinas/derivados/README.md; CLAUDE.md §11.7
saida: 40-operacao-rotinas/derivados/PORTE-AAAA-MM-DD.md
alcada: porta para os derivados ativos o que o delta lista, respeitando quarentena e EXCECOES-DA-CASA.md de cada um; cliente e parceiro publicam pelo sincronizar.py; o template NAO e desta task (automatico pelo template.py, §11.7); nao porta item em quarentena; nao muda fato, voz nem decisao de conta; nao manda mensagem a ninguem
estimativa_tokens: 80000
depende_de: 
tipo_decisao: 
prioridade: 2
recorrencia: 
estado: pronta
agendada_para: 
---
# Portar para os derivados o que a casa mudou (porte-derivados)

## Pedido
O `derivados.py --abrir-task` achou <N> arquivo(s) da casa que mudaram desde a base de algum derivado e que o tipo dele recebe. O delta está em `<DELTA>`. Regra: `CLAUDE.md` §11.7; procedimento: `40-operacao-rotinas/derivados/README.md` §3.

## Como executar
1. Ler o delta e, de cada derivado, o `EXCECOES-DA-CASA.md` (se existir) e o `CLAUDE.md` dele. **O kernel do derivado prevalece onde diverge:** porta-se adaptado ou não se porta, e a linha vai ao `PORTE-AAAA-MM-DD.md` com o porquê.
2. Por derivado, um subagente `sonnet` (ou o próprio modelo, se for pouco) porta pelo procedimento do tipo (README §3). Template: 3 vias, anonimização, `python3`, `varrer-publico.py`. Cliente e parceiro: só mecanismo e resultado, nunca `100-métodos/`.
2-bis. **Kernel de cliente e de parceiro:** copiar o bloco entre `MECANISMO-DA-CASA:INICIO` e `:FIM` do `90-templates/repo-cliente/CLAUDE-modelo.md` para o `CLAUDE.md` do derivado, substituindo o bloco que houver (ou, no primeiro porte, a seção de sincronia escrita à mão), trocando `<nome do dono>`. Nada fora dos marcadores se toca. Sem `EXCECOES-DA-CASA.md` no derivado, criá-lo do molde ao lado, com o que o kernel dele já diverge. **Roda no PC:** a nuvem não clona esses repos. 🔴 **Molde de entrega com dado de outra conta se limpa FORA do clone** (pasta de ensaio no scratchpad) e só entra no clone já limpo: o hook `Stop` roda o `sincronizar.py` a cada fim de turno e publica o que estiver no clone, inclusive o trabalho pela metade (caso real: um porte pela metade levou nomes de outras contas para a história do repo de um cliente). Subagente de porte roda com `run_in_background: false`, ou a sessão não fecha o turno enquanto ele porta.
3. Gates do derivado (o `verificar.py` dele; no template, `verificar-propagacao.py` dentro dele + `varrer-publico.py`).
4. Publicar: cliente e parceiro pelo `sincronizar.py` da Governança; template por `git push` puro, autor = e-mail da empresa.
5. `derivados.py --registrar "<nome>" --base <HEAD da Governança usado>` para cada derivado fechado. Derivado que não fechou não anda a base.
6. `PORTE-AAAA-MM-DD.md` com: o que foi, o que ficou e por quê (quarentena, exceção, conflito), e linha no `STATUS.md`.

## Pronto quando
Cada derivado ativo do delta portado (ou com o porquê de não, no `PORTE-<data>.md`), gates do derivado verdes, publicado, base andada pelo `--registrar`, linha no `STATUS.md` e `verificar-propagacao.py` em ✅.

## Log
