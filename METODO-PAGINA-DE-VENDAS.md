# PONTEIRO — Método de Páginas de Vendas (absorvido)

> **Este arquivo não é mais fonte ativa.** Em 26/07/2026 o método v2.0 (829 linhas) e a skill compacta `10-skills/pagina-de-vendas.skill.md` foram unificados em duas skills portáteis e modulares.
>
> **Fonte ativa:**
> - `gerador-web-designer-senior-continuum` — a física: classificação, dobras, curva de tensão, extrato de crença, atrito, gate e diagnóstico.
> - `ui-ux-designer-senior-continuum` — o design: direção de arte, tokens, composição, componentes e estados, acessibilidade AA, movimento, performance, implementação e spec.
>
> **Fonte instalável:** a oficina de skills do repositório (a mesma de onde `10-skills/` é publicada).
> **Roteamento e circuito:** `CLAUDE.md` §6.3.

## O circuito que substituiu este arquivo

"Criar uma página de vendas para X" abre cinco etapas, não carrega um documento:

1. **Física** — gerador classifica (ticket, modelo de entrega, ato de conversão, temperatura), preenche o brief de 9 campos e entrega esqueleto, curva e extrato.
2. **Direção visual** — ui-ux em modo direção entrega direção de arte, tokens e o limite de caracteres por bloco.
3. **Escrita** — skill de copy preenche os blocos.
4. **Execução visual** — ui-ux em modo execução desenha e, quando pedido, implementa.
5. **Gate** — o juiz do gerador consolida os três gates e decide a publicação.

## Por que a divisão física × design

No método antigo, o design vivia como instrução de física ("o clímax é escuro", "ícone com função"). Isso bastava para auditar, e não bastava para desenhar: não havia direção de arte, tokens, matriz de estados, régua de acessibilidade nem regra de implementação. A skill de ui-ux existe para carregar essa camada com referências reais de execução, e o gerador ficou com o que sempre foi: a engenharia da decisão.

## Mapa de migração

| Parte do método antigo | Onde está agora |
|---|---|
| 12 leis · Parte 0 (circuito, saldo de atenção, extrato, atrito, 12 perguntas) | gerador · módulos 00 e 01 |
| Parte 1 (dobras canônicas, orçamento de scroll) | gerador · módulo 02 |
| Parte 2 (fios, curva, cadência, contraste visual) | gerador · módulo 03 |
| Parte 3 (elementos: headline, CTA, preço, ícones, mobile, velocidade, vídeo) | dividida: argumento e mecânica no gerador (02 e 04), execução visual na ui-ux (01 a 05) |
| Parte 4 (modulações) | gerador · módulo 04, mais o eixo novo de ato de conversão |
| Parte 5 (brief, ordem de escrita, handoffs) | gerador · módulos 00 e 05 |
| Parte 6 (gate) | gerador · módulo 06, mais o gate visual próprio da ui-ux |
| Parte 7 (medição e diagnóstico) | gerador · módulo 06 |
| Apêndice (anti-padrões) | dividido: anti-padrões de venda no gerador, de design na ui-ux |

## Como alimentar daqui para frente
Cada auditoria, teste e página lançada volta para a skill correspondente, não para este arquivo. Regra nova, exceção documentada ou anti-padrão promovido: física vai para o gerador, visual vai para a ui-ux.

---
*Conteúdo íntegro da v2.0 (18/07/2026): a versão v2.0 (não distribuída no template; o procedimento de legado está em `10-skills/_legado/README.md`). Este ponteiro substituiu o conteúdo na raiz em 26/07/2026.*
