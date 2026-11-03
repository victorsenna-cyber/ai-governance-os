# POLÍTICAS JURÍDICAS — Regras Permanentes

> **Tipo:** política (camada 2) · Dono: {{OPERADOR}} (CLO em exercício)
> Em conflito de regra jurídica, este arquivo prevalece sobre skills e templates. Precedência geral: `CLAUDE.md` > este arquivo > `10-skills/juridico/*` > templates.

## §0 — Disclaimer permanente (ler antes de tudo)

Nada neste departamento substitui advogado. Somos leigos operando defesa preventiva. Regra de uso: **template escrito e aceito > acordo verbal > nada** — um contrato imperfeito assinado protege mais que nenhum. Todo template passa por advogado antes do primeiro uso em contrato de valor ≥ {{LIMITE_REVISAO_ADVOGADO}} ou recorrência ≥ 6 meses; abaixo disso, usamos o template com risco assumido e registrado (realidade de quem ainda constrói caixa). Quando houver caixa, a revisão integral por advogado vira prioridade (ver `STATUS.md` pendências).

## §1 — Regra de ouro: nada sem instrumento escrito

Por quê: sem instrumento assinado, nenhuma das partes consegue provar o que foi combinado.

- **Nenhuma prestação de serviço inicia** sem, no mínimo: proposta escrita + aceite expresso registrado (mensagem escrita do cliente serve como mínimo absoluto; contrato assinado é o padrão).
- **Nenhuma pessoa trabalha conosco** (freelancer, parceiro, futuro vendedor) sem contrato escrito definindo: escopo, remuneração, prazo, propriedade intelectual, confidencialidade e condições de saída.
- **Nós não trabalhamos para ninguém** sem o mesmo. Inclusive — e principalmente — quando há amizade ou afinidade pessoal envolvida. Documento não é desconfiança; é cuidado com a relação.
- Cláusula citada só existe se estiver escrita e aceita ANTES do fato. Obrigação verbal alegada depois do fato não é cláusula, é pressão.

## §2 — Hierarquia de formalização (do mais forte ao mínimo)

1. Contrato assinado (e-sign com trilha de auditoria ou físico).
2. Proposta em PDF + aceite expresso por escrito ("aceito a proposta X de DD/MM") + comprovante de pagamento vinculado.
3. Termos enviados na conversa + aceite expresso por escrito.
4. ~~Verbal~~ — não existe juridicamente para nós. Proibido operar aqui.

Venda de site (ticket baixo): mínimo nível 3, padrão nível 2. Assessoria/MRR e tráfego: mínimo nível 2, padrão nível 1. Societário e parcerias: somente nível 1.

## §3 — Alçadas

| Decisão | Quem |
|---|---|
| Assinar contrato de venda (site, Assessoria, tráfego) | {{OPERADOR}} (contratos em nome de quem responde legalmente pela {{EMPRESA}}) |
| Alterar cláusula inegociável de template | {{OPERADOR}} + registro do porquê no rodapé do contrato gerado |
| Responder a conflito/ameaça jurídica | **Ninguém responde a quente.** Blue team primeiro (`blue-team.skill.md` §3), resposta em até 48h |
| Acordo, renúncia de direito ou assunção de dívida | {{OPERADOR}}, com advogado quando o valor justificar |
| Contratar advogado | {{OPERADOR}} (validação financeira `CLAUDE.md` §9) |

## §4 — Red lines em contrato (inegociáveis)

1. **Obrigação de meio, nunca de resultado garantido.** Não assinamos "garantia de X clientes/faturamento/posição no Google".
2. **Escopo fechado em anexo** + processo de mudança (aditivo escrito). Anti-scope-creep é cláusula, não conversa.
3. **Pagamento antes ou junto da entrega** (site: 50/50; Assessoria: mês antecipado). Nunca 100% pós-entrega.
4. **Propriedade intelectual:** entregável do cliente é do cliente após quitação; **método, código-base, templates e know-how são nossos e permanecem nossos**. Direito de portfólio expresso.
5. **Sem exclusividade e sem não-competição contra nós.** Não aceitamos cláusula que nos proíba de atender o nicho. (Reciprocidade: não fazemos com outros o que não aceitamos para nós — nossos contratos também não impõem no-compete abusivo a quem trabalhar conosco.)
6. **Foro:** `<cidade>/<UF>`.
7. **LGPD mínima:** dados do cliente usados só para a entrega; dados de terceiros (leads do cliente) tratados sob instrução do cliente, que é o controlador.

## §5 — Registro e memória (blue team)

- Todo conflito, ameaça, cobrança indevida ou "conversa estranha" vira **registro de caso** em `registros/` no dia em que acontece (template em `blue-team.skill.md` §2).
- Evidência se preserva no ato: export da conversa, prints com data/hora visíveis, comprovantes de pagamento, e-mails. Cópia fora do dispositivo (drive).
- Prazos que vencem (prescrições, notificações) entram no registro com data-limite e vão para `STATUS.md` pendências se exigirem decisão.

## §6 — Gates de evolução do departamento

| Gate | Dispara |
|---|---|
| Caixa permite (≥ `{{CAIXA_GATE_JURIDICO}}` livres) | Revisão dos templates por advogado + constituição de CNPJ (avaliar MEI/SLU/LTDA com contador) |
| 1º contrato de Assessoria novo | Contrato nível 1 (assinado) obrigatório — estreia do template revisado |
| Produto SaaS à venda | Construir: ToS, política de privacidade, DPA — **antes** da primeira venda |
| Infoproduto à venda | Termos de compra + política de reembolso (CDC: 7 dias) — antes da primeira venda |

---
*Registro: blindagem documental é política permanente do departamento jurídico: nada sem instrumento escrito (§1).*
