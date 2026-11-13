# MÉTODO — DECISÃO DE OFERTA (o que propor a esta pessoa, com o que já sabemos fazer)

> **Tipo:** método
> **Alçada:** {{OPERADOR}} · **Estado:** 🟡 **provisório, `n=0`**. Gradua quando 10 recomendações feitas por ele tiverem a escolha do {{OPERADOR}} registrada e o tipo `oferta_catalogo` subir a A2 pela escada (`40-operacao-rotinas/ferramentas/autonomia.py`).
> **Pedido que instituiu:** expandir a autonomia do sistema para decidir sobre ofertas, de acordo com o que o {{OPERADOR}} pode oferecer (conhecimento e possibilidades de criação) e com o que as pessoas expressam como necessidade. A decisão "qual produto do catálogo" **nasce em A1**: o sistema recomenda, o {{OPERADOR}} escolhe.
> **Lê:** `30-comercial/INVENTARIO-DE-CAPACIDADES.md` (o que podemos oferecer) · a ficha da pessoa (`PAINEL.md` + `REGISTRO.md`) · `00-core/POLITICAS-DE-DECISAO.md` §5 (preço e pisos) · `30-comercial/ICP.md` §4-bis · `CLAUDE.md` §9.1.
> **Escreve:** `REGISTRO.md` §2 da ficha · frontmatter do `PAINEL.md` (`dor`, `dor_fonte`, `produto`, `oferta_recomendada`, `oferta_gatilho`, `dor_sem_produto`) · linha `oferta_catalogo` em `40-operacao-rotinas/tarefas/log/DECISOES.jsonl` (`autonomia.py --registrar … --ficha`).

---

## 1. A tese, em causa e efeito

A decisão de oferta já tinha régua na casa, espalhada em vários lugares (Regra Nº 0, Regra Nº 2, ordem de conta nova, pisos de preço, gate de contratação, a regra de que indicação se aceita e diagnóstico de indicador não). Sem um método que as junte na ordem, a oferta nasce **do que se lembra e do entusiasmo de quem indicou**, não do que a pessoa disse e do que temos. E o erro mais caro é sempre o mesmo: **vender a ferramenta que a pessoa percebe (IA, site, repositório) em vez do produto que entrega o efeito que ela quer.** A ferramenta é efeito; o produto é o que causa o efeito, e ele já tem preço.

## 2. A procedência da necessidade (o passo 1 depende disto)

Toda dor entra no `REGISTRO.md` com fonte, e a fonte decide o peso:

| Fonte | O que é | Peso |
|---|---|---|
| **D** | fala literal da própria pessoa, com data e hora (call destilada, captura de WhatsApp) | **decide** |
| **O** | fato observado **por nós** ou documento dela: o sistema dela na tela, o site, a calçada, o extrato, um número dela | **decide** |
| **I** | indicador, filho, sócio, parceiro falando por ela, **mesmo que ele tenha visto o fato** | **hipótese**: vira pergunta da primeira conversa, nunca produto |
| **V** | leitura do {{OPERADOR}} ou nossa, sem fala dela | **hipótese**, marcada como tal |

**Uma pergunta converte I em D:** *"o indicador me contou que você manda o aniversário à mão; é assim mesmo?"* Dita por ela, a dor passa a decidir.

**O {{OPERADOR}} como fonte (desempate com o `CLAUDE.md`, seção de autonomia):** ele é a primeira pessoa a quem se pergunta um fato de cliente, e a resposta dele **herda a classe do que ele relata**: *"ela me disse X"* com data, ou a fala dela capturada → **D** (fonte `{{OPERADOR}}, data`); *"eu vi X"* no sistema, na loja, no extrato → **O**; *"eu imagino"*, *"creio que"*, *"pelo que captei"* → **V**. Fala dela ampliada por ele (*"você disse X, Y e Z"* sobre um áudio dela que só tem X) se separa: **só o X decide**, o resto é V.

**Dor D de objeto indefinido não decide** (*"quero estar com tudo bonitinho"*, *"quero crescer"*): passa a ser a primeira pergunta aberta da conversa (*"o que precisa estar pronto para você sentir que está bonitinho?"*), para o passo 2 não escolher o produto pela nossa leitura. **Várias D que se contradizem:** vale a mais recente, e a contradição vai para as perguntas. **Desejo de ferramenta** (*"quero IA"*) não é dor: é efeito pedido, e vira a pergunta *"o que você queria que ela fizesse por você?"*. As perguntas confirmam fato e desejo; **nunca pedem a ela o desenho da oferta** (Regra Nº 0).

## 3. O passo 0 e os sete passos, na ordem

| # | Passo | Pergunta | Fonte | 🔴 Reprova sozinho |
|---|---|---|---|---|
| 0 | **Já é escopo?** *(só cliente ativo)* | o que ela pede já está no contratado? | `DECISOES.md` e escopo da conta | oferta nova para o que o contrato já cobre (é rodada de entrega) · trabalho fora do contrato feito de graça |
| 1 | **Procedência** | que dor tem fonte D ou O? | ficha (§2 acima) | oferta recomendada sobre dor só I ou V |
| 2 | **Dor → produto** | qual produto do catálogo já resolve essa dor, com preço? | inventário, camada 1 | produto escolhido pela ferramenta pedida, não pela dor |
| 3 | **Quem opera** | o produto exige operador do lado dela? está nomeado? | ficha (`decisor`, equipe), coluna "exige do cliente" do inventário | produto que exige operador sem operador nomeado |
| 4 | **Trilho e ordem** | ICP A ou B? família de venda local (fecha na reunião) ou não (G0 → âncoras → folha → veredito → proposta)? mentoria? | `ICP.md` §4-bis, `CLAUDE.md` §9.1 | combo fora do catálogo fechado na mesma reunião · diagnóstico de quem já fatura vendido a quem constrói do zero |
| 5 | **Viabilidade** | horas somadas × {{VALOR_HORA_PISO}} ≤ preço? margem ≥ {{MARGEM_MINIMA}}? setup > mensal? escopo somado recalculou o preço? | `POLITICAS` §5 (a conta fica na folha interna) | escopo maior no mesmo preço · hora nossa mostrada ao cliente |
| 6 | **Capacidade e caixa** | prende hora semanal do {{OPERADOR}}? faturamento dela conhecido? referência escalada, se a oferta é nova? | `STATUS.md`, `METODO-GATE-DE-CONTRATACAO.md`, Regra Nº 2 | ticket alto com `n=0` · oferta nova sem referência escalada · recorrência semanal **sem a hora declarada** (falta de hora não reprova: aciona o `METODO-GATE-DE-CONTRATACAO`, e a recomendação sai com a hora a comprar escrita; `CLAUDE.md` §8) |
| 7 | **Registro** | recomendada, descartadas e o porquê, **gatilho de troca**, perguntas da conversa | `REGISTRO.md` §2, `PAINEL.md`, `DECISOES.jsonl` | recomendação sem descartado · sem gatilho de troca |

**Como cada passo se aplica:**

1. **Procedência.** Liste as dores com fonte. Se nenhuma é D ou O, o método **não emite recomendação**: emite **hipótese de entrada** (§4), e a primeira pergunta da conversa é a que converte a dor em D.
2. **Dor → produto.** Leia a coluna "dor que resolve" da camada 1 do inventário. Escreva a frase: *"a dor X é resolvida pelo efeito Y, que o produto Z entrega"*. Se a pessoa pediu uma ferramenta, ela entra no Y, nunca no Z. Composição entre produtos do catálogo (um produto mais o seu módulo; o diagnóstico núcleo depois o de operação; a assessoria estratégica depois a completa) **é catálogo**. Peça fora do catálogo, ou preço que não está na tabela, **não é**: siga o §5.
3. **Quem opera.** Repositório, mentoria, atendimento por IA e tudo o que o cliente roda sozinho pedem um nome do lado dele. Sem nome, o produto sai da recomendação e entra no gatilho de troca (*"se X disser que opera, Z volta"*).
4. **Trilho e ordem.** ICP A lê evidência (diagnóstico); ICP B cria hipótese (alicerce). Só a família de venda local fecha na mesma reunião (`METODO-PROSPECCAO-PRESENCIAL-LOCAL.md` §6). Exceção a essa ordem é palavra do {{OPERADOR}}, conta a conta, e se registra como tal.
5. **Viabilidade.** Some as horas de cada peça (coluna do inventário). Se a composição soma escopo, o preço soma junto; o piso de hora e a margem mínima vetam. A conta é interna e nunca sai da casa.
6. **Capacidade e caixa.** Operação de uma pessoa: cada hora semanal fixa é hora do {{OPERADOR}}. Faturamento desconhecido é `n=0`, e com `n=0` não se recomenda ticket alto no escuro: recomenda-se a porta de menor risco e o degrau seguinte com gatilho.
7. **Registro.** O bloco do §6 vai inteiro para o `REGISTRO.md` §2 e os campos para o `PAINEL.md`. A recomendação entra em `DECISOES.jsonl` pelo `autonomia.py --registrar <id> oferta_catalogo "<recomendado>" "<escolhido>" --ficha <pasta>`, **com os nomes da camada 1 do inventário** (composição com " + "; o script grava a chave de catálogo e avisa peça fora dele), **gravada antes da conversa** (recomendação escrita depois de saber a escolha infla o acerto); hipótese de entrada entra com `--saida hipotese` e fica fora da contagem da escada, e o resultado (aceite, recusa, perdido) pelo `--resultado`, chamado pelo `acoes_do_painel.py` quando a ficha fecha no sistema.

## 4. As duas saídas possíveis

| Saída | Quando | O que é | Vai ao {{OPERADOR}} como |
|---|---|---|---|
| **Recomendação** | há dor D ou O, e os passos 2 a 6 passam | produto (ou composição) do catálogo, descartadas com motivo, gatilho de troca, perguntas | cartão A1 tipo `oferta_catalogo` enquanto o tipo estiver em A1; depois, aviso (A2) |
| **Hipótese de entrada** | só há dor I ou V | a família provável, marcada `hipótese`, e a **pergunta que converte a dor em D** como primeira pergunta da conversa | linha na ficha e aviso; nunca proposta, nunca preço fechado |

Hipótese de entrada não é recomendação: ela orienta a conversa, e a recomendação nasce depois da fala dela. **Ela roda os passos 2 a 6 sobre a dor hipotética e usa o mesmo bloco do §6**, com `Recomendado:` trocado por `Família provável (hipótese):`, e **também exige descartados e gatilho de troca**. Se a dor vira D **dentro** da conversa, a hipótese gravada antes passa a valer como recomendação e o {{OPERADOR}} escolhe na hora; o que entra na escada é **a hipótese gravada antes** como `recomendado` e o que ele levou como `escolhido` (nada se escreve depois de saber a escolha). Recomendação que nasce na call e não estava na hipótese é do {{OPERADOR}}, não do método, e entra com `--saida pre_metodo`. Por isso o preço de tudo o que pode ser escolhido na call (o catálogo, ou o combo já ancorado) precisa existir **antes** dela.

## 5. Quando a dor não cabe no catálogo

1. A ficha registra `dor_sem_produto: sim`. O `comercial_regras.py` conta: a mesma dor em 3 fichas aparece na área Comercial como *"necessidade recorrente sem produto"*.
2. Abre-se `30-comercial/propostas-de-produto/<nome>.md`: degraus 1 a 3 do `METODO-DESENHO-DE-PRODUTO.md` (por quê, para quem, o quê), **referência escalada** (Regra Nº 2, com fonte e estado), horas, piso, setup e mensal pelos pisos do §5, trilho.
3. Cartão para o {{OPERADOR}}, tipo `produto_novo` (A1 sempre, lista TETO do `autonomia.py`).
4. Enquanto não entra no §5, a pessoa recebe **o produto do catálogo mais próximo, ou nada**. Gate de recusa do §5: oferta sem probabilidade de receita ou estrutura viável *"não deveria existir"*.

Combo com peça fora do catálogo, ou com preço que ainda não existe, é produto novo ou preço novo: tipo `produto_novo` ou `oferta_preco`, os dois no TETO.

## 6. O bloco de saída (vai para o `REGISTRO.md` §2)

```
### Oferta — AAAA-MM-DD (METODO-DECISAO-DE-OFERTA, saída: recomendação | hipótese de entrada)
- Dor que decide: "<frase>" · fonte D|O (<onde, data e hora>)   [ou: só I/V → hipótese]
- Recomendado: <produto do catálogo ou composição> · efeito que a pessoa percebe: <ferramenta/efeito>
- Descartados: <produto> — <motivo, com o passo que reprovou> · …
- Operador: <nome> | não nomeado → <o que sai da recomendação>
- Trilho e ordem: ICP A|B|local|fundador · fecha na reunião? sim|não (por quê)
- Viabilidade (interna): <horas> × {{VALOR_HORA_PISO}} vs preço do §5 · setup > mensal? · margem
- Capacidade e caixa: hora semanal do {{OPERADOR}}? faturamento conhecido? referência escalada?
- Gatilho de troca: "se <fato>, <outra oferta> passa a valer"
- Perguntas da conversa (na ordem): 1. … 2. …
```

## 7. A fronteira de autonomia

| O sistema decide e registra (ato interno, reversível) | Segue com o {{OPERADOR}}, um a um |
|---|---|
| qual produto do catálogo recomendar · a composição entre produtos do catálogo · o que descartar e por quê · o gatilho de troca · as perguntas da conversa · a folha interna · a ficha e o painel · recomendar **contra** uma ideia do {{OPERADOR}}, por escrito, com a régua | preço fora da tabela · desconto · combo com peça fora do catálogo · produto novo · prazo e escopo contratual · contrato · **toda mensagem ou proposta que chega à pessoa** · aceitar cliente (gate de capacidade) |

**Na escada (`autonomia.py`):** `oferta_catalogo` está em **A1**: a recomendação vira cartão no molde `40-operacao-rotinas/tarefas/modelos/cartao-decisao.md` (oferta com preço leva a linha "Números"; a premissa do que foi prometido vai no "Supondo") e ele escolhe. Sobe a **A2** (decide e avisa, 24 h de veto) com 10 acertos e taxa ≥ 90%; a **A3** com 20 recomendações seguidas sem troca, todas com resultado registrado e aceite não pior que o das anteriores. **Duas trocas do {{OPERADOR}} sobre o mesmo produto em 4 semanas devolvem o tipo a A1.** Troca do {{OPERADOR}} não é erro dele: é dado, e entra no histórico igual.

## 8. 🔴 Régua de veto (na tabela do `METODO-GATE-DE-CONGRUENCIA.md` §3)

**Oferta recomendada sem dor de fonte D ou O apontável · produto que exige operador sem operador nomeado · produto escolhido pela ferramenta pedida e não pela dor · combo com peça fora do catálogo tratado como catálogo · recomendação sem descartado ou sem gatilho de troca · preço escrito fora da fonte canônica do produto (o §5, ou a oferta aprovada por cartão) · hipótese de entrada registrada como recomendação.**

## 9. Desempates (🟡 leitura default declarada; o {{OPERADOR}} reverte com uma palavra)

Onde o método obrigava a adivinhar, vale isto até a palavra dele:

| Ponto | Leitura default |
|---|---|
| **Família de venda local × ICP A/B** | negócio de bairro com endereço (loja, serviço local) entra pela **família local**; ICP A/B (`ICP.md` §4-bis) é para expert, serviço consultivo e infoproduto. A família foi desenhada para a reunião presencial: **por indicação e online, a reunião única só vale com a palavra do {{OPERADOR}}, conta a conta** |
| **ICP de quem vende várias coisas** | classifica-se **pela linha que se vai vender**: quem vende a mentoria e quer lançar um curso nunca testado é ICP A na mentoria e hipótese no curso |
| **Dor que casa com um degrau que exige outro produto antes** (módulo que só vale a partir de certo mês do produto-base) | **degrau sem a entrada não se oferece** (a trava é estrutural, não de preço: `POLITICAS` §5). A dor do degrau vira **gatilho**, e as perguntas da conversa testam a dor da entrada (de onde vem cliente novo, quem atende); se a entrada não tiver dor nenhuma, `dor_sem_produto: sim` (com dor D ou O) |
| **"Porta de menor risco"** | o **menor compromisso com trava de saída já desenhada** na família (a reunião única da família local, o escopo fechado do diagnóstico), não o menor ticket |
| **"Ticket alto"** | tudo acima da porta paga da família |
| **"Composição do catálogo"** | produtos do catálogo somados a **preço de tabela**, cada um com a regra de entrada dele respeitada, em sequência ou ao mesmo tempo; qualquer preço que precise ser inventado faz dela `oferta_preco` |
| **Decisor duplo** (passo 4) | só fecha na mesma reunião se **os dois** decisores estiverem nela; o convite ao segundo é a primeira pergunta, antes da reunião, e vale mesmo quando o decisor duplo é fonte I |
| **Comissão de indicação** (passo 5) | sai da **nossa** margem, nunca do preço dela. **Se ela entra na conta do piso de hora é decisão do {{OPERADOR}}**; até a palavra dele, a folha interna mostra a conta com e sem a comissão |
| **Margem mínima** (passo 5) | como está no `POLITICAS` §5: sobre o nosso custo, **hora + ferramenta**. O método não redefine a régua; onde a conta não fecha por falta de custo-hora definido, isso se declara na folha, não se inventa |
| **Setup maior que o mensal** | só se aplica a produto que tem setup |
| **Operador** (passo 3) | precisa de **nome** quando o produto roda entre os nossos encontros sem nós (repositório, mentoria, atendimento por IA, roteiro de WhatsApp); **vazão conta**: quem tem dois silêncios de mais de 14 dias registrados na conta não conta como operador até mostrar ritmo |
| **Capacidade sem dado vivo** (passo 6) | sem número de horas comprometidas, é `n=0`: recorrência semanal nova sai com a hora a comprar declarada e o gate de contratação acionado, nunca recusada por hora; a **janela da pessoa** (data que ela deu) entra aqui, contra a capacidade |
| **"Oferta nova"** (passo 6) | nova **para nós** (nenhum caso entregue): pede referência escalada no nicho dela, pela Regra Nº 2 |
| **Caminho do §5 (produto novo)** | só abre com dor **D ou O**; dor só V ou I não marca `dor_sem_produto`. **Combo ou preço que o {{OPERADOR}} escolhe por conta dele** não passa por aqui: é `oferta_preco`, preço dele, e pode ser fechado antes da conversa por cartão, qualquer que seja a fonte da dor |
| **Cliente ativo sem ficha de prospect** | o bloco vai para o `STATUS.md` da conta, e o `--ficha` aceita `clientes/<Conta>` |

## 10. O que este método não faz

Não decide preço, desconto, contrato nem envio. Não cria produto (o §5 abre o caminho, o {{OPERADOR}} decide). Não pula a ordem de conta nova (`CLAUDE.md` §9.1). Não trata hipótese de entrada como proposta.
