<!-- Molde da task tipo: entregavel (plano de produção de entregáveis, §1). Não copiar à mão: `python3 40-operacao-rotinas/ferramentas/entregaveis.py --nova ...` preenche os <CAMPOS>, calcula o prazo pela régua do §2 e cria a pasta em entregaveis/. O despachante local não lê esta pasta nem executa tipo: entregavel. -->
---
id: <ID>
titulo: <TITULO>
criada: <HOJE>
tipo: entregavel
prazo: <PRAZO>
prazo_duro: <PRAZO_DURO>
conta: <CONTA>
arvore: <ARVORE>
carga: julgamento
classe_dado: C
nivel_minimo: N4
escada: N4
swarm: nao
insumos: <INSUMOS>
saida: <SAIDA>
alcada: nao envia; nao publica; nao decide preco nem contrato; nao escreve em 01 - contexto/
estimativa_tokens: 80000
orcamento:
depende_de:
prioridade: <PRIORIDADE>
recorrencia:
estado: <ESTADO>
agendada_para:
prometido_em: <PROMETIDO_EM>
prometido_para: <PROMETIDO_PARA>
destinatario: <DESTINATARIO>
forma: <FORMA>
fonte: <FONTE>
dinheiro: <DINHEIRO>
atrasado: <ATRASADO>
pronto_em: <PRONTO_EM>
enviado_em:
enviado_por:
---
# <TITULO>

## Pedido
Produzir o entregável prometido a <DESTINATARIO> (conta <CONTA>), na forma `<FORMA>`, no caminho exato de `saida`.

1. Ler a conta inteira: `STATUS.md`, `DECISOES.md`, `PAINEL.md` e a fonte da promessa (`fonte`).
2. Abrir a árvore de `arvore` (`00-core/roteador/ARVORE-<X>.md`) e cumprir a pré-condição dela. Peça para o PÚBLICO do cliente só se a CONTA passou (`PILARES.md` sem P1/P4 reprovando e `lexico-icp/` com fonte `D`); documento para o próprio cliente declara o pilar que falta.
3. Produzir:
   - **mensagem** → `mensagem.md`: uma linha acima com canal e destinatário, depois o texto puro para colar (sem `>`, sem cabeçalho dentro do texto), na voz do {{OPERADOR}}.
   - **documento** → fonte `.html`/`.md` e PDF pelo `gerar_pdf.py`, modelo do `90-templates/CATALOGO-PDF.md` (sem número, o 1). Sem Chrome no ambiente: gravar a fonte e marcar `pdf: pendente-local`.
   - 🔴 **Todo pronto que vai a alguém deixa `mensagem.md` na pasta:** documento, pacote e artefato também, com o texto de envio que acompanha o arquivo. Formato que o painel lê: 1ª linha = canal e destinatário · linha vazia · o texto para colar; várias versões com `## Versão <nome>`; bastidor antes de `TEXTO PARA COLAR`; nota que não se copia em linha começando com `> `.
   - 🔴 **A mensagem e o arquivo moram na mesma pasta, e a mensagem é curta:** o PDF ou HTML que vai junto fica ao lado do `mensagem.md` (se nasceu noutra pasta, copia-se para a pasta da task; nunca se aponta para a pasta antiga); a `saida:` da task de documento aponta para o arquivo, não para a mensagem. Mensagem de envio: o que é, o que a pessoa faz, prazo, valor ou link, em até ~60–90 palavras; o que o documento já diz não se repete, bastidor vai antes de `TEXTO PARA COLAR`. O sistema mostra o caminho do arquivo e reprova (⚠️ no cartão, aviso no `--verificar`) a pasta de documento que só tem a mensagem.
   - **artefato** → o artefato onde ele mora; `LEIA-ME.md` de uma tela na pasta do entregável apontando para ele e dizendo o que o {{OPERADOR}} mostra.
4. Linha no `entregaveis/README.md` da conta (data, o quê, pasta). Preencher `pronto_em`, `estado: pronto`, e mover para `revisao/`.
5. Se `atrasado: sim` e o prazo foi dito ao cliente: escrever `## Ajuste de expectativa` (o fato, a data nova, o que vai junto; sem "com calma", sem desculpa longa).
6. Falta FATO sobre o cliente: cartão em `DECISOES-PENDENTES.md` no molde `tarefas/modelos/cartao-decisao.md`, conferido com `decisoes_cartao.py --lint --id <id>` antes de fechar, com o default declarado na linha "Supondo" ("leio X; se for Y, muda Z") e a task para `decisao/`. Falta ESTRUTURA: decidir (Regra Nº 0).

## Pronto quando
O arquivo de `saida` existe dentro de `clientes/<conta>/entregaveis/<AAAA-MM-DD - nome>/`, a linha está no `entregaveis/README.md` da conta, `pronto_em` preenchido, `## Resposta ao {{OPERADOR}}` escrita, e `entregaveis.py --verificar` em ✅.

## Resposta ao {{OPERADOR}}
<até 600 caracteres, texto de WhatsApp: o que ficou pronto, o caminho, o prazo prometido, o que precisa dele>

## Log
- <HOJE> · criada por `entregaveis.py --nova` · fonte: <FONTE>
