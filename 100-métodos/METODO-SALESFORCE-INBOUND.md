# Método Salesforce — Lógica de Inbound (Receita Previsível na fonte)

> **Tipo:** framework · secundário: blueprint (§5) *(reclassificado por auditoria independente de leitura integral; antes: sem campo)*
> Ativo de referência. Destila a lógica de prospecção da Salesforce (onde Aaron Ross escreveu o *Receita Previsível*), para quando implementarmos **inbound / SDR estruturado** na {{EMPRESA}}.
> Não é para copiar mensagem, é para internalizar o **princípio**. Base: Aaron Ross, *Receita Previsível* (2ª ed.).

---

## 1. O princípio central

> **A primeira mensagem não vende o produto. Ela vende a conversa.**

O objetivo do primeiro toque não é despertar desejo pelo produto nem listar features. É **ganhar 15 minutos**. O diagnóstico e a venda acontecem na call, não no chat. Quem tenta vender na abertura queima o lead; quem pede só o próximo passo, avança.

Foi assim que a Salesforce (um SDR, no exemplo) abordou: 3 frases, zero produto, uma referência pessoal e um convite de tempo ("consegue falar ainda hoje?").

---

## 2. Os 4 pilares (do Receita Previsível)

**1. Especialização de papéis.** Ninguém faz tudo. A máquina se divide em funções:
- **SDR / BDR** (outbound) — prospecta frio, qualifica, agenda. Não fecha.
- **Inbound rep / MRR** — trata quem levantou a mão (marketing, site, indicação).
- **Closer / Executivo de contas** — recebe o lead qualificado e fecha.
- **Farmer / CS** — retém e expande a conta.
> Regra: o SDR não fecha, o closer não prospecta. A troca de bastão é o que dá previsibilidade.

**2. Não é sobre volume, é sobre o lead certo.** Pesquisa antes de contatar. Uma referência específica ("vi que vocês buscam integração entre X e Y") vale mais que 100 disparos genéricos. Relevância presumida > insistência.

**3. A primeira mensagem pede o próximo passo, não a venda.** CTA de microcompromisso: "consegue falar 15 min?", responder "Quero". Nunca "compre", "veja o preço", "conheça o produto".

**4. Cadência previsível.** Sequência definida de toques (e-mail + WhatsApp + ligação), com intervalos e número de tentativas fixos. Previsibilidade vem do processo, não do esforço heroico.

---

## 3. Anatomia da abordagem Salesforce (o exemplo de um SDR)

> "Olá [nome], tudo bem? Sou o [nome do SDR] da Salesforce. Vi que você demonstrou interesse em integração entre diferentes soluções da Salesforce e gostaria de entender melhor o que vocês estão buscando na [empresa]. Consegue falar ainda hoje?"

Decompondo:

| Elemento | Função | Por que funciona |
|---|---|---|
| "Sou o [SDR] da Salesforce" | identificação + autoridade | marca forte, tira o estranhamento |
| "vi que você demonstrou interesse em X" | **referência personalizada** | cria o "isso é sobre mim" |
| "entender o que vocês estão buscando" | **pergunta sobre o lead** | faz o lead falar, não empurra produto |
| "consegue falar ainda hoje?" | **microcompromisso de tempo** | pede o próximo passo, não a compra |

O que ele **não** faz: não cita produto, não lista feature, não fala preço, não manda parede de texto.

---

## 4. Contraexemplo — a abertura que lista features (o que evitar no inbound)

Um SDR de outro fornecedor fez o oposto no meio da mensagem: nomeou o produto e listou features com ✅. Isso é vender cedo demais. Funciona menos porque:
- Desloca o foco do lead para o produto.
- Vira parede de texto.
- Dá ao lead motivos para dizer "não preciso disso" antes de você diagnosticar.

> Lição: liste features **na call, depois do diagnóstico**, nunca na abertura.

---

## 5. Como aplicaremos na {{EMPRESA}} (inbound futuro)

Quando estruturarmos inbound (lead que levantou a mão via site, conteúdo, indicação):

1. **Papel dedicado** — um SDR/inbound rep trata quem chega, separado de quem entrega.
2. **Abertura estilo Salesforce** — identificação + referência ao que o lead demonstrou ("vi que você baixou X / se interessou por Y") + pergunta sobre o objetivo dele + convite de call curta.
3. **Cadência definida** — nº de toques e intervalos fixos (ver `40-operacao-rotinas/` quando existir).
4. **Bastão para o closer** — SDR qualifica (BANT, ver `30-comercial/prospeccao-sites/roteiro-qualificacao.md`), closer fecha.
5. **Voz {{OPERADOR}}** quando a abordagem for dele; voz da pessoa quando for de outro SDR.

---

## 6. Relação com o resto do sistema

- Método-base já citado em `PROJECT.md`, `SCOPE.md`, `c-level/CRO.skill.md` (Receita Previsível).
- Aplicação outbound fria: `METODO-ABORDAGEM-FRIA.md` (o método portável).
- Qualificação: `30-comercial/prospeccao-sites/roteiro-qualificacao.md` (SPIN + BANT).
- Voz: `10-skills/voz-operador.skill.md`.

---
*Base: `70-metodologias-chave/Receita Previsível (2ª ed.).pdf` (Aaron Ross / Salesforce); exemplos de abordagem de SDR.*
