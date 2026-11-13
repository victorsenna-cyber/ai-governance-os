# Proposta de revisão de frota · Oficina Alvorada

> Amostra visual do modelo 7 (Continuum formal). Conta fictícia, nenhum dado de cliente.
> Gerar: `python3 -X utf8 build-pdf.py --in exemplo/MODELO-7-CONTINUUM-FORMAL.md --out exemplo/MODELO-7-CONTINUUM-FORMAL.pdf --capa exemplo/MODELO-7-CONTINUUM-FORMAL.capa.json`

## 1. Objeto

**Quando usar:** documento que se lê para **assinar**: proposta final, contrato, material formal.

Esta proposta descreve o plano de revisão mensal da frota de doze carros atendida pela Oficina Alvorada, com o escopo, o preço, as condições e o prazo. Ela é a versão para assinatura: o mecanismo e a economia já foram apresentados em documentos anteriores.

> Documento que se lê para assinar vai no claro. Cada cláusula abaixo é o que se compromete, e nada além dela.

## 2. Escopo

| Item | O que está incluído | O que não está |
|---|---|---|
| Revisão mensal | conferência de 30 itens por carro, com foto de cada item | peças trocadas, cobradas à parte |
| Agenda | um dia por carro, marcado com uma semana de antecedência | remarcação no mesmo dia |
| Relatório | o resumo do mês, enviado até o dia 5 | laudo técnico para seguradora |
| Retorno no mesmo dia | o carro volta até as 18 h | carro que depende de peça encomendada |

### Os compromissos, por código

- **C-01** · o carro volta no mesmo dia, ou a revisão daquele carro não é cobrada.
- **C-02** · o relatório do mês chega até o dia 5 do mês seguinte.
- **C-03** · peça só se troca com aprovação por escrito do responsável da frota.

## 3. Preço e condições

| Condição | Valor |
|---|---|
| Revisão por carro | {{PRECO_POR_CARRO}} por mês |
| Frota de 12 carros | {{PRECO_FROTA}} por mês |
| Pagamento | boleto, todo dia 10 |
| Prazo mínimo | 6 meses |
| Reajuste | anual, pelo IPCA |

---

## 4. Validade e assinatura

Esta proposta vale por 15 dias a partir de {{DATA_DA_PROPOSTA}}. A primeira revisão acontece na semana seguinte à assinatura, no carro mais rodado da frota.

```
Contratante: ______________________________   Data: ___/___/______

Oficina Alvorada: __________________________   Data: ___/___/______
```
