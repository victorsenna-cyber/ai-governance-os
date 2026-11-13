# MOLDE — cartão de decisão (face e lastro)

> **Tipo:** blueprint (00-core/TAXONOMIA-DE-ARTEFATOS.md) · **Régua:** `40-operacao-rotinas/ferramentas/decisoes_cartao.py` (V-DEC-1..6, chamada pelo `verificar-propagacao.py`) · **Onde o cartão mora:** `40-operacao-rotinas/tarefas/DECISOES-PENDENTES.md`, seção `## Abertas` · **Quem lê:** a aba Decisões do painel e o `propagar-decisoes.py`.
>
> Motivo do desenho: o cartão era escrito como registro e mostrado como pergunta, e quem decide não conseguia decidir só com ele. Agora tem duas camadas no mesmo arquivo: a **face**, que basta para decidir, e o **lastro**, que prova.

## 1. Quem escreve, nesta ordem

1. `python3 -X utf8 40-operacao-rotinas/ferramentas/decisoes_cartao.py --novo "<Conta>" "<Pergunta?>" --tipo <tipo> [--prazo AAAA-MM-DD]` → imprime o molde com o próximo id do dia e a hora de abertura. Cola em `## Abertas`.
2. Escreve a **face** (seção 2).
3. Pergunta-se: **lendo só a face, quem decide decide sem abrir o lastro?** Se não, falta "Em jogo" ou falta "Supondo".
4. Escreve o **lastro**: fato com fonte, citação literal com hora, o descartado, ids, contas por extenso, adendos.
5. `python3 -X utf8 40-operacao-rotinas/ferramentas/decisoes_cartao.py --lint --id <id>` → ✅ antes de fechar a tarefa. Reprovou, corrige e repete.

## 2. O molde

```
### D-AAAA-MM-DD-NNN · <Conta> — <Pergunta?> · tipo `<tipo>` · autonomia A1 · prazo: AAAA-MM-DD · aberta: AAAA-MM-DD HH:MM
**Em jogo:** <o que está em risco e por que agora>
**Números:** <rótulo>: <valor> (<nota>) · <rótulo>: <valor>
- **A)** <rótulo da escolha>
  ↳ <o que acontece se o operador clicar>
- **B)** <rótulo>
  ↳ <efeito>
- **C)** <rótulo>
  ↳ <efeito>
**Recomendação:** A. <o porquê, em uma ou duas frases>
**Supondo:** <a premissa em que as opções se apoiam>. Se não for, <o que muda>.
**Lastro:**
<texto livre: contexto com fonte, citações com hora, contas por extenso, ids, adendos ⟲>
```

| Campo | Teto | Regra |
|---|---:|---|
| **Pergunta** (depois do ` — ` no cabeçalho) | 90 | uma frase, termina em `?`, sem parêntese. O que se decide, não o que aconteceu |
| **Em jogo** | 160 | o que se perde ou se ganha e por que a decisão é agora |
| **Números** | 4 pares | `rótulo: valor (nota)`, separados por ` · `. **Obrigatório em cartão de dinheiro** (preço, oferta com preço, desconto, cobrança, despesa, remuneração). Só o número que diferencia as letras ou diz se fecha no nosso piso. Rótulo até 24, valor com nota até 40 |
| **Opção: rótulo** | 60 | a escolha em poucas palavras; é o que se vê primeiro e o que aparece depois do clique |
| **Opção: efeito** (`↳`) | 150 | o que o clique dispara e o que custa: quem recebe o quê, quando, quanto |
| **Recomendação** | 200 | a letra e o porquê. Se a razão não cabe, a decisão não está madura: vai para o lastro e volta mais curta |
| **Supondo** | 140 | a premissa que, se for falsa, troca a recomendação ou a pergunta, com o "se não for". É o *"leio X; se for Y, muda Z"* do kernel, posto onde o operador vê |
| **Lastro** | sem teto | tudo o mais. Adendo (`⟲ **Adendo <data, hora>…**`) entra aqui **e**, se muda o peso de uma letra, a face é corrigida no mesmo ato |

**As sete regras da face:**

1. **Língua comum.** Não entra crase, asterisco, nome de arquivo, caminho, id (de cartão, task, ordem, decisão de conta, ponto de destilação), sinal de seção, "item N da lista" ou "do anexo", hash, opção de linha de comando, `n=0`, nem sigla de nível (A1, N4). Tudo isso mora no lastro.
2. **Data escrita.** "Ontem" e "amanhã" não entram: o cartão vive dias. A tela é quem fala "vence amanhã".
3. **Duas ou três opções**, A a C. A quarta saída é a "outra resposta" do operador.
4. **Prazo é data ou `sem prazo`.** O motivo do prazo ("a call é sexta") vai no "Em jogo".
5. **`aberta:` no cabeçalho**, em hora local. É a linha de base da medição (`medir-decisoes.py`).
6. **A face tem de bastar.** Lendo só a face, o operador decide sem abrir o lastro.
7. **Teto somado da face: 1.200 caracteres.**

**O que não muda:** a linha de opção (`- **A)**`) e a de recomendação (`**Recomendação:** A`) casam com o regex do `propagar-decisoes.py`; ele acha o cartão, a letra, o tipo e a conta sem mexer no script. Opção e recomendação **só valem antes do `**Lastro:**`**: no lastro, cite opção antiga como `(A) …`, nunca como `- **A)**`.

## 3. A régua (`decisoes_cartao.py --lint`)

| Régua | Reprova quando |
|---|---|
| **V-DEC-1** | cartão aberto no formato antigo (sem `**Em jogo:**`) |
| **V-DEC-2** | campo da face acima do teto, face acima de 1.200, pergunta sem `?` ou com parêntese |
| **V-DEC-3** | código da casa na face |
| **V-DEC-4** | recomendação sem porquê, sem "Supondo", opção sem a linha `↳`, menos de 2 ou mais de 3 opções |
| **V-DEC-5** | prazo que não é data nem `sem prazo`, ou cabeçalho sem `aberta:` |
| **V-DEC-6** | cartão de dinheiro sem "Números" · cartão já resolvido parado em "Abertas" (cabeçalho começando por `### ✅`) |
| ⚠️ só aviso | "Supondo" sem o "se não for" · "hoje" na face · cartão com data vencida há mais de 72 h |

**Os tetos são hipótese:** se três cartões seguidos estourarem o mesmo teto com texto que não é gordura, o teto sobe no `LIM` do `decisoes_cartao.py`, com registro no `STATUS.md`.

## 4. Exemplo, lado a lado

**Antes** (formato de registro, como a tela mostrava: título, cinco selos, contexto longo cortado, três letras sem efeito):

```
área de motoristas e cotação com recomendação: dentro do contrato, à parte ou depois?
[Cliente X] [D-AAAA-MM-DD-901] [tipo escopo] [A1] [prazo 13/11]
Cliente, 11/11 08:32 (áudio): *"vou ter que ter uma área só para os motoristas…"* ⚠️ Leitura: é o
sistema dele, não o app da fase 1. Área de motoristas cabe no setor Logística…
(A) Área de motoristas entra agora, dentro do contrato; cotação vira orçamento à parte…
(B) As duas entram no contrato como cortesia.
(C) As duas ficam para depois do setup, sem orçar agora.
```

**Depois** (a face; o lastro leva o texto antigo inteiro, com o adendo):

```
### D-AAAA-MM-DD-901 · Cliente X — Área de motoristas e cotação automática: entram no contrato ou viram orçamento? · tipo `escopo` · autonomia A1 · prazo: AAAA-MM-DD · aberta: AAAA-MM-DD 08:41
**Em jogo:** O cliente pediu as duas por áudio e já ouviu do nosso número que "vai ter", sem preço nem prazo. A call da semana é onde isso se acerta.
- **A)** Motoristas agora, cotação orçada à parte
  ↳ Respondemos no grupo, por escrito, que a cotação se orça depois da call (o texto passa pelo operador antes) e ela entra na pauta.
- **B)** As duas entram como cortesia
  ↳ Entram no mapa de telas sem preço. Software sob medida está fora do contrato, e a cortesia vira precedente.
- **C)** As duas ficam para depois do setup
  ↳ Respondemos com a data, depois do setup. Ficou fraca: ele já ouviu "vai ter".
**Recomendação:** A. A área de motoristas é configuração do que ele já comprou. A cotação que indica a melhor loja é sistema novo: dada de graça, abre precedente para todo software sob medida.
**Supondo:** que ele fala do sistema, não do app. O que ele cota ainda não sabemos. Se for do app, a pergunta é outra.
**Lastro:**
(o texto integral de antes, com a fala dele, a leitura, os ids e o adendo)
```

**Cartão de dinheiro** (a faixa de números):

```
### D-AAAA-MM-DD-NNN · Cliente Y — Quanto cobrar pela terceira peça do pacote, o repositório da loja? · tipo `preco_oferta` · autonomia A1 · prazo: AAAA-MM-DD · aberta: AAAA-MM-DD 16:54
**Em jogo:** As outras duas peças têm preço de tabela; esta não tem. O número entra na proposta que sai antes de a cliente voltar de viagem.
**Números:** entrada (com a A): {{PRECO_ENTRADA}} · mensal (com a A): {{PRECO_MENSAL}} · custo total dela: {{VALOR}} (percentual do faturamento) · nossa hora: {{VALOR}} (no piso)
- **A)** Versão leve: {{PRECO_ENTRADA}} + {{PRECO_MENSAL}} por mês
  ↳ Entra na proposta como repositório enxuto da loja, sem site nem integração além das do retorno.
…
**Supondo:** que o que o operador prometeu a ela na call é o repositório do catálogo, na versão leve. Se prometeu outra coisa, a pergunta muda.
```

A linha "Supondo" não evita a premissa errada; ela a deixa barata (um cartão de preço partiu de um produto que não era o prometido, e a resposta veio em texto livre).
