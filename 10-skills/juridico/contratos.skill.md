# SKILL — Contratos (geração e revisão)

> **Tipo:** skill de método · **Criado em:** 2026-07-13 · Política-mãe: `80-juridico/POLITICAS-JURIDICAS.md`
> Carrega quando: fechar venda (site, Assessoria, tráfego) · gerar/revisar contrato · aditivo de escopo · futuro: ToS SaaS, termos de infoproduto.
> Regra: contrato não é burocracia pós-venda; é a Fase 8 do fechamento. Venda sem instrumento não é venda concluída.

## 1. Motor de geração (passo a passo)

1. **Selecionar template** em `80-juridico/contratos/` conforme o produto (tabela §2).
2. **Preencher slots** `[colchetes]` — todos. Slot vazio = contrato não sai. **Os dados do contratado (nós) vêm de `80-juridico/DADOS-DO-CONTRATADO.md`, nunca de pergunta ao {{OPERADOR}}.**
3. **Anexo de escopo:** escrever ANTES do contrato, em linguagem que o cliente entende. O anexo é o anti-scope-creep; o que não está nele, não está no preço.
4. **Gate de red lines** (`POLITICAS-JURIDICAS.md` §4): rodar o checklist §3 abaixo. Red line alterada = alçada do {{OPERADOR}} + registro do porquê.
5. **Formalizar no nível certo** (`POLITICAS` §2): site = proposta + aceite escrito (mínimo) · Assessoria/tráfego = contrato assinado (padrão) · societário = só assinado.
6. **Arquivar:** PDF final + aceite/assinatura + comprovante da entrada, nomeado `AAAA-MM-DD-<cliente>-<produto>`, cópia em drive.

## 2. Matriz produto → instrumento

| Produto | Template | Nível mínimo | Particularidade |
|---|---|---|---|
| Site ({{TICKET_SITE}}) | `TEMPLATE-CONTRATO-SITE.md` | proposta + aceite escrito | 50/50 · prazo conta do material completo · direito de portfólio |
| Assessoria ({{TICKET_ASSESSORIA}}/mês) | `TEMPLATE-CONTRATO-ASSESSORIA.md` | contrato assinado | escopo em anexo · mês antecipado · aviso 30 dias |
| Gestão de tráfego | adaptar template Assessoria | contrato assinado | verba de mídia é do cliente, na conta do cliente — nunca transita por nós |
| SaaS (futuro, gate MRR ≥ {{MRR_GATE_SAAS}}) | construir ToS + privacidade + DPA | aceite eletrônico | **antes** da 1ª venda (`POLITICAS` §6) |
| Infoproduto (futuro, gate MRR ≥ {{MRR_GATE_INFOPRODUTO}}) | termos de compra + reembolso | aceite no checkout | CDC 7 dias obrigatório |

## 3. Checklist de gate (antes de enviar qualquer contrato)

- [ ] Obrigação de meio (zero promessa de resultado garantido)?
- [ ] Escopo fechado em anexo + mudança só por aditivo escrito?
- [ ] Pagamento nunca 100% pós-entrega?
- [ ] IP: entregável do cliente ao cliente após quitação · método/base/know-how permanecem nossos · direito de portfólio expresso?
- [ ] Zero exclusividade e zero não-competição contra nós?
- [ ] LGPD: papel de operador definido; dados só para a entrega?
- [ ] Foro [cidade/UF]?
- [ ] Contratante correto (hoje: {{OPERADOR}}, pessoa física; cláusula de cessão ao futuro CNPJ presente)?
- [ ] Valores, datas e slots conferidos por leitura em voz alta?
- [ ] O cliente consegue entender o anexo de escopo sem tradutor? (contrato claro fecha mais rápido)

## 4. Revisão de contrato de terceiro (quando NOS mandam um)

1. Ler procurando o que nos proíbe, não o que nos dá: exclusividade · não-competição · multa desproporcional · IP sobre nosso método · renovação automática · foro distante.
2. Qualquer restrição pós-contrato (não-competir, não-atender) → só com limite de tempo/escopo e contrapartida; caso contrário, recusar o ponto por escrito.
3. Nunca assinar na pressa do fechamento. 24h de leitura é cláusula nossa de sanidade.
4. Dúvida em contrato de valor alto → advogado antes da assinatura (`POLITICAS` §0).

## 5. Aditivos e scope creep

Pedido fora do anexo → resposta padrão: "entra como aditivo" (escopo + valor + prazo, 5 linhas, aceite escrito). Aditivo arquivado junto ao contrato-mãe.

## 6. Handoffs

← CRO/fechamento (venda ganha → instrumento) · ← blue-team (defesa que vira cláusula) · → CLO.skill (exceção às red lines) · → `40-operacao-rotinas` (arquivo e renovações).

---
*Base: red lines em `POLITICAS-JURIDICAS.md` §4 · templates em `80-juridico/contratos/`. Disclaimer: `POLITICAS` §0 — advogado revisa antes de contrato ≥ {{LIMITE_REVISAO_ADVOGADO}} ou recorrência ≥ 6 meses.*
