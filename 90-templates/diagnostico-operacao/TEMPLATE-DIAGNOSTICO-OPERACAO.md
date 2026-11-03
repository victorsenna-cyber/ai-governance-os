# Mapa da Ordem — {{CLIENTE}}

> **Template instanciável.** Copiar para `clientes/{{CLIENTE}}/DIAGNOSTICO-{{AAAA-MM-DD}}.md` e preencher.
> **Destino no repo:** `90-templates/diagnostico-operacao/TEMPLATE-DIAGNOSTICO-OPERACAO.md`
> **Método que governa:** `100-métodos/METODO-DIAGNOSTICO-DE-OPERACAO.md`
>
> **⚠️ Régua de redação, antes de escrever a primeira linha:**
> banidas — *vazamento · erro · falha · problema grave · você deveria · auditoria · está errado*.
> máximo **3 vermelhos** no documento. Todo achado sai com **o porquê a decisão fazia sentido** e **o que fazer**.
> Cada seção na ordem: **o que está de pé → o potencial travado → o que trava → o que destrava.**

---

**Preparado para:** {{NOME}} · {{OPERAÇÃO}}
**Data:** {{DATA}} · **Base:** call de {{DATA_CALL}} + varredura de ativos
**Devolutiva:** {{DATA_DEVOLUTIVA}}

---

## 1. O QUE EU VI

*{{2 a 4 parágrafos. Abre pelo que está de pé, com especificidade — número, ativo, fato nomeado. Fecha nomeando o potencial travado, sem ainda dizer o que trava.}}*

**O que esta operação já tem, e não é pouco:**

| | |
|---|---|
| {{ativo 1}} | {{o que ele vale, em número quando houver}} |
| {{ativo 2}} | |
| {{ativo 3}} | |

**O número que muda a conversa:**

> {{a frase única do documento. O potencial travado, em unidade do cliente. Forma: a quantidade por mês que se perde, o que o cliente já paga para ela chegar e onde ela trava.}}

---

## 2. O MAPA

> **Versão vendida:** {{Núcleo (dimensões 1–5) · Operação (dimensões 1–10)}}. Apagar as linhas fora do escopo.

| # | Dimensão | Estado | Em uma linha |
|---:|---|:---:|---|
| 1 | **ICP** | {{🟢🟡🔴}} | {{}} |
| 2 | **Promessa** | {{}} | {{}} |
| 3 | **Oferta** | {{}} | {{}} |
| 4 | **Narrativa** | {{}} | {{}} |
| 5 | **Pivô de Conversão** | {{}} | {{}} |
| 6 | **Página** | {{}} | {{}} |
| 7 | **Funil** | {{}} | {{}} |
| 8 | **Conteúdo** | {{}} | {{}} |
| 9 | **Tráfego** | {{}} | {{}} |
| 10 | **Dados e tracking** | {{}} | {{}} |

**Leitura do mapa:** {{1 parágrafo. Onde está a causa e onde estão os sintomas. Se há vermelho no bloco de fundação, dizer que os achados de cima são consequência.}}

---

## 3. BLOCO A · NÚCLEO

### 3.1 ICP — {{🟢🟡🔴}}

**O que está de pé:** {{}}
**O que eu observei:** {{evidência nomeada: o que os últimos clientes pagaram × o preço do produto-alvo, como a equipe qualifica hoje}}
**Por que está assim:** {{a decisão que fazia sentido no contexto em que foi tomada}}
**O que isso custa hoje:** {{em número do cliente}}
**O próximo passo:** {{ação concreta}}

### 3.2 Promessa — {{}}

**O que está de pé:** {{}}
**O teste que eu rodei:** {{as respostas de "o que você faz?" que ouvi, literais}}
**Por que está assim:** {{}}
**O que isso custa hoje:** {{}}
**O próximo passo:** {{}}

### 3.3 Oferta — {{}}

**O que está de pé:** {{}}

| Produto | Preço hoje | Preços nos últimos 90 dias | Observação |
|---|---:|---|---|
| {{}} | {{}} | {{}} | {{}} |

**Por que está assim:** {{}}
**O que isso custa hoje:** {{}}
**O próximo passo:** {{}}

### 3.4 Narrativa — {{}}

**O que está de pé:** {{}}
**O mecanismo:** {{tem nome fixo? qual? quantos nomes diferentes apareceram?}}
**O diferencial declarado:** *"{{frase literal}}"* — {{cabe na boca do concorrente?}}
**A prova que existe e não está sendo usada:** {{}}
**O próximo passo:** {{}}

### 3.5 ⭐ Pivô de Conversão — {{}}

> O ponto onde o ativo deixa de informar e passa a vender. Método: `100-métodos/METODO-PIVO-DE-CONVERSAO.md`.

| Ativo | O pivô existe? | Aponta para a causa que a oferta resolve? | Onde está |
|---|---|---|---|
| {{conteúdo}} | {{}} | {{}} | {{segundo / slide}} |
| {{página}} | {{}} | {{}} | {{dobra}} |
| {{call / VSL}} | {{}} | {{}} | {{momento}} |

**A frase-teste:** depois de consumir, a pessoa completa *"então o meu problema real é ______"* com {{a palavra da oferta / outra palavra}}.
**Modo de falha observado:** {{ausente · múltiplo · causa errada · tardio}}
**Por que está assim:** {{}}
**O próximo passo:** {{}}

---

## 4. BLOCO B · CONVERSÃO

### 4.1 Página — {{}}

| Item | Estado |
|---|---|
| H1 é promessa, dor ou método? | {{}} |
| Ordem das dobras | {{}} |
| CTA único e repetido? | {{}} |
| Preço / prazo / o que acontece depois | {{}} |
| Pixel e eventos | {{}} |
| Link da bio aponta para | {{}} |

**O próximo passo:** {{}}

### 4.2 Funil — {{}}

**O caminho hoje, passo a passo:** {{}} → {{}} → {{}} → {{pagamento}}

| Item | Estado |
|---|---|
| Tempo de primeira resposta | {{}} |
| Cadência de recontato escrita? | {{}} |
| Onde o histórico fica | {{}} |
| Sobrevive à troca de pessoa? | {{}} |

**O próximo passo:** {{}}

---

## 5. BLOCO C · AQUISIÇÃO

### 5.1 Conteúdo — {{}}

**Amostra analisada:** {{n}} peças, de {{data}} a {{data}}.

#### ⭐ As três que mais funcionaram, e por quê

| Peça | Número | Por que funcionou |
|---|---|---|
| {{}} | {{retenção / conversas}} | {{o elemento específico: hook, cena, especificidade}} |
| {{}} | {{}} | {{}} |
| {{}} | {{}} | {{}} |

#### A matriz

| Retenção 3s | Engajamento | Conversas | Diagnóstico |
|---|---|---|---|
| {{}} | {{}} | {{}} | **{{HOOK / PIVÔ / CTA / fundação}}** |

#### Hook — {{🟢🟡🔴}}

{{o padrão observado nos hooks. Cita 2 exemplos literais da operação, um que funcionou e um que não.}}

#### Pivô — {{}}

{{existe ponto de virada? a causa apontada é a que a oferta resolve? onde está a queda de retenção?}}

#### CTA — {{}}

{{um destino ou vários? rastreável? compatível com o estágio da peça?}}

#### ⭐ Três hooks reescritos, prontos para gravar

> 1. *"{{}}"*
> 2. *"{{}}"*
> 3. *"{{}}"*

**O ângulo que ainda não foi explorado:** {{}}

### 5.2 Tráfego — {{}}

| Item | Estado |
|---|---|
| De quem é a conta | {{}} |
| Verba mensal | {{}} |
| Objetivo de otimização | {{}} |
| Custo por lead | {{medido ou `a calibrar`}} |
| Custo por venda | {{medido ou `a calibrar`}} |
| Teto de custo por venda definido? | {{}} |

**O próximo passo:** {{}}

### 5.3 Dados e tracking — {{}}

| Item | Estado |
|---|---|
| Pixel / tags instalados | {{}} |
| Eventos que disparam de verdade | {{}} |
| Padrão de UTM | {{}} |
| **De qual peça veio a última venda?** | {{}} |
| Gerenciador × checkout batem? | {{}} |
| Existe um lugar único de leitura? | {{}} |

**O próximo passo:** {{}}

> {{Se houver 🔴 no bloco A, escrever aqui: "Não recomendo subir verba antes de fechar {{dimensão}}. Verba sobre fundação em aberto compra mais gente para a mesma recusa."}}

---

## 6. A PRIMEIRA ALAVANCA — o que já está pago

> **Antes de construir qualquer coisa, o que dá retorno mais rápido nesta operação é: {{alavanca}}.**

**Por que ela vem primeiro:** {{não depende de construção nova, usa ativo que já existe e já foi pago}}
**O que precisa acontecer:** {{ação}}
**Prazo estimado até o retorno:** {{}}
**A conta:** {{aritmética com os números dele}}

*{{Premissa declarada. Se o insumo X for diferente, a conta muda — e a refazemos com o número certo antes de qualquer decisão.}}*

---

## 7. A ORDEM

**Não é lista de prioridade. É ordem de dependência:** cada item só se sustenta se o anterior estiver de pé.

| # | O quê | Por que nesta posição | Prazo |
|---:|---|---|---|
| 1 | {{}} | {{}} | {{}} |
| 2 | {{}} | {{}} | {{}} |
| 3 | {{}} | {{}} | {{}} |

**Próximo ciclo** *(real, e não agora)*: {{itens amarelos que ficam para depois, nomeados e datados — para que ninguém sinta que foram esquecidos}}

---

## 8. O QUE EU NÃO CONSEGUI APURAR

| O que falta | Por que importa | Quem tem |
|---|---|---|
| {{}} | {{o que muda na leitura quando chegar}} | {{}} |

> Marcado como `a calibrar`. **Não foi estimado em silêncio.**

---

## 9. O QUE FICA FORA DESTE DOCUMENTO

| Frente | Degrau |
|---|---|
| Execução do que está acima | Assessoria Estratégica — setup {{R$}} + {{R$}}/mês |
| {{se Núcleo:}} as 5 dimensões de operação (página, funil, conteúdo, tráfego, tracking) | **Mapa da Ordem · Operação**, a partir de {{TICKET_MAPA_OPERACAO}} — abate o que já foi pago, em até {{n}} dias |
| {{página adicional}} | {{TICKET_SITE}} |
| {{outro}} | {{a orçar}} |

---

## 10. O PRÓXIMO PASSO

Este documento é o mapa. **Executar é outra conversa, e ela é opcional.**

Se você quiser fazer sozinha, o que está aqui é suficiente para isso.
Se quiser que eu faça com você, o valor deste diagnóstico abate integralmente no setup, se fecharmos em até 15 dias desta devolutiva.

**As sugestões deste documento são o que fazer e em que ordem. A Assessoria é quem faz junto, toda semana.**

---

# ⛔ FOLHA INTERNA — não vai ao cliente

*Separar em arquivo próprio, ou cortar antes de exportar.*

## Rubrica preenchida

| Dimensão | Estado | Evidência | Teste que falhou |
|---|:---:|---|---|
| ICP | | | |
| Promessa | | | |
| Oferta | | | |
| Narrativa | | | |
| **Pivô de Conversão** | | | |
| Página | | | |
| Funil | | | |
| Conteúdo | | | |
| Tráfego | | | |
| **Dados e tracking** | | | |

## Leitura comercial

| | |
|---|---|
| **Score de ICP** (`30-comercial/ICP.md` §5) | {{0–100}} |
| **Roteamento** | {{≥80 entrar · 60–79 amadurecer · 40–59 porta de entrada · <40 não aderente}} |
| **Degrau indicado** | {{}} |
| **Âncoras que este diagnóstico preencheu** | {{quais das 7 de `METODO-ANCORAGEM-DE-PROPOSTA`}} |
| **Âncoras ainda faltantes** | {{}} |
| **Capacidade** | {{cabe na carteira? qual fase? colide com qual conta?}} |
| **Risco desta conta** | {{}} |

## Checagem antes de entregar

- [ ] 8 dimensões classificadas com evidência nomeada
- [ ] no máximo 3 vermelhos
- [ ] primeira alavanca identificada, com premissa declarada
- [ ] ordem escrita, com razão para a ordem
- [ ] 3 hooks reescritos
- [ ] zero palavras banidas
- [ ] `a calibrar` em tudo que não foi apurado
- [ ] o que fica fora com preço do degrau
- [ ] folha interna separada do que vai ao cliente

---
*Template criado em 12/09/2026.*
