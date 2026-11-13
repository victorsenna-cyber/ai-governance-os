# roteiro-do-dia/ — MODELO 10 do catálogo de PDF

**O que é:** o dia do operador num PDF do modelo elétrico A4, cinza, sem fita, com o dia desenhado em **BPMN vertical**:

- raia **Você** (esquerda): os passos, de cima para baixo; `tarefa` · `fixo` (hora marcada, borda branca) · `decisao` (losango: "sim" vira tarefa abaixo, "não" contorna e as duas se juntam);
- raia **A casa** (direita): eventos de tempo (rodada de entregáveis, aviso da agenda, limite do Claude), com seta tracejada quando a casa te chama;
- depois: o laço de cada envio (fixo), a tabela do que é seu agora (com o caminho de cada arquivo), a da tarde, o destaque e o checklist de fechamento.

**Como se gera:** escreve-se o `roteiro.json` na pasta do dia (`40-operacao-rotinas/roteiro-do-dia/AAAA-MM-DD/`) e roda-se

    python3 -X utf8 90-templates/roteiro-do-dia/gerar_roteiro.py <pasta do dia>/roteiro.json

O gerador copia `noturno.css`, `eletrico.css` e `fontes/` do `pdf-noturno/`, escreve o HTML e imprime pelo `gerar_pdf.py` (reprova Type3 e página em branco). **O JSON é a fonte;** o HTML é gerado e não se edita. Defeito de desenho se corrige no `gerar_roteiro.py`.

**De onde vem o conteúdo:** a resposta de cada pronto em `40-operacao-rotinas/tarefas/revisao/`, a agenda do dia, o `STATUS.md` das contas e o que o operador disser do próprio dia (horário, deslocamento, lugar). Horário mudou: refaz-se o JSON e gera-se de novo no mesmo dia.

**Lugar e hora:** o passo leva `"icone"` (`banho` · `lavanderia` · `trabalho` · `casa` · `cafe` · `caminho`) e `"hora"`, e ganha o ícone com a hora à esquerda da caixa; o lugar não se escreve por extenso, o ícone é só referência ilustrada. Dia de imersão, sem envio de colar, leva `"laco": false` e a página do laço sai.
