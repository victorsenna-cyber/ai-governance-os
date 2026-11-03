# SCOPE.md — Escopo de Atuação da {{EMPRESA}}

> Delimita onde a governança atua, quem servimos, o que entregamos e os limites permanentes. Em conflito de fato comercial, `30-comercial/ICP.md` prevalece.
> ⚠️ **MODELO — preencher.**

## 1. Níveis de governança

| Nível | O que governa | Onde vive |
|---|---|---|
| Identidade | quem somos, como nos comportamos | `00-core/` |
| Política | números, alçadas, pisos e tetos | `00-core/POLITICAS-DE-DECISAO.md`, `30-comercial/` |
| Estado | metas, pipeline, capacidade, pendências | `STATUS.md`, `60-planos/`, `40-operacao-rotinas/` |
| Conta | fatos, voz, oferta, decisões e estado de cada cliente | `clientes/<cliente>/` (kernel próprio) |

## 2. Escopo de mercado (quem servimos)

### Dentro
- `{{ICP primário — 30-comercial/ICP.md §2}}`
- `{{ICP B — constrói do zero, só pelo Alicerce (§4-bis)}}`

### Fora (não-ICP)
- `{{30-comercial/ICP.md §4}}`

## 3. Escopo de oferta (o que entregamos)

### Dentro
- `{{escada de 30-comercial/oferta.md §3: diagnóstico pago, construção, assessoria recorrente, produto de maior valor}}`

### Fora
- Execução isolada sem estrutura ("só tráfego", "só automação").
- Garantia de resultado (garantia de execução é permitida: `POLITICAS` §5).
- Construção de sistema dentro de oferta de processo (desenhamos; o cliente ou o dev dele constrói).
- Transferência de método a cliente fora de contrato próprio (`90-templates/repo-cliente/README.md` §2).

## 4. Escopo por área (resumo — detalhe nas skills)

| Área | Persona | O que decide |
|---|---|---|
| Estratégia e empresa | `10-skills/c-level/CEO.skill.md` | prioridade, gargalo, o que não fazer |
| Receita | `CRO.skill.md` | pipeline, conversão, canal |
| Finanças | `CFO.skill.md` | caixa, piso, margem, tripwires |
| Operação | `COO.skill.md` | capacidade, entrega, onboarding |
| Tecnologia | `CTO.skill.md` | stack, integrações, dados |
| Jurídico | `CLO.skill.md` + `juridico/` | instrumento, risco, disputa |
| Heads | `10-skills/heads/` | tráfego, conteúdo, CS, onboarding, financeiro, TI |

## 5. Limites permanentes

- Nada sem instrumento escrito (`80-juridico/POLITICAS-JURIDICAS.md` §1).
- Não escalar sem previsibilidade (`POLITICAS` §3).
- Não vender sem saber quem entrega; falta de hora aciona contratação, nunca recusa (`POLITICAS` §4-bis).
- A estrutura de conversão é nossa (`CLAUDE.md` §8, REGRA Nº 0).
- Em resposta direta, só sobre o que já está escalado (REGRA Nº 2).
- Nenhum cliente acima de 40% da receita (`POLITICAS` §6).
