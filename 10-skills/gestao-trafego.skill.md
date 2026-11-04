# SKILL — Gestão de Tráfego Pago (método)

> **Tipo:** skill de método · **Fonte completa:** `100-métodos/METODO-TRAFEGO-PAGO.md` (prevalece em conflito)
> Carregar quando o pedido envolve: plano de mídia, campanha, criativo de anúncio, otimização, escala, relatório de tráfego, diagnóstico de CPA.
> Estado do cliente: `clientes/<Cliente>/NN - tráfego pago/`. Números de alçada/preço: `00-core/POLITICAS-DE-DECISAO.md`.

## Cadeia endurecida (nunca pular gate)

**Gate de entrada → Briefing/Matemática → Página aprovada → Matriz de criativos → Estrutura → Tracking verde → Gestão por regras → Relatório.**

## Regras que decidem (resumo operacional)

1. **Sem matemática reversa assinada, não sobe campanha** (ticket → margem → CPA máx → CPL máx → verba mínima = 10-15× CPA alvo/dia).
2. **Sem tracking verde (Pixel+CAPI, eventos testados, UTM padrão), não sobe campanha.**
3. **Sem página aprovada no checklist (§3 do método), não sobe campanha.** Página segue o circuito de página (`00-core/roteador/ARVORE-ESCRITA.md` §6).
4. **Criativo é a segmentação:** broad + 8-12 criativos distintos (ângulo × formato × hook), com `tipo de teste` e `hipótese` na matriz. **Exploração** = conceito novo; **iteração/lateralização** = base com resultado + componente + hipótese (mesmo pivô é legítimo aí). Portfólio 70/30 tem fonte única no `100-métodos/METODO-TRAFEGO-PAGO.md` §4.2. Copy: `10-skills/copywriter-senior-continuum/` + `METODO-CONSTRUCAO-DE-CRIATIVOS-DR.md` (anúncio DR) + `METODO-EMPILHAMENTO-DE-HOOKS.md` (abertura composta) + voz do cliente e `lexico-icp/` (nunca `voz-operador` para cliente).
5. **Consolidação:** 1 campanha por objetivo · 1-3 conjuntos · verba < R$ 100/dia = 1 campanha, 1 conjunto, prazos de decisão dobrados. **Campanha para WhatsApp: objetivo Engajamento por prioridade, por resultado e custo — Engajamento > Leads, Engajamento > Vendas** (direto: conversas; via página: conversão no Contact do pixel) — método §5.2.
6. **Kill/scale por regra, não sensação:** kill hard = 3× CPA sem conversão ou CTR < 0,5% (≥ 2k impr.) · kill = CPA > 3× alvo por 3 dias · fadiga = freq > 3,5 + CTR −20% · escala = +20%/48-72h · não mexer nas primeiras 72h · 1 mudança por vez.
7. **Toda decisão vai para `LOG-DECISOES.md`** (data · o quê · por quê · resultado esperado).
8. **Diagnóstico de CPA alto nesta ordem:** tracking → oferta → página/atendimento → criativo → estrutura/leilão.
9. **Verba na conta do cliente**, cap de gasto configurado, mudança > 30% do plano = aprovação escrita.
10. **Relatório:** manchete é resultado de negócio, nunca vanity metric; plataforma + fonte de verdade lado a lado; cruza `stop-slop`.
11. 🔴 **Posicionamento na Meta:** todo conjunto com posicionamento **personalizado**, só **Instagram Feed + Stories + Reels**; todo o resto desmarcado, Advantage+ de posicionamento proibido. Cada anúncio leva a arte **4:5 no feed** e a **9:16 em Stories e Reels**, as duas veiculadas. Conjunto já no ar fora da regra: corrigir é decisão do {{OPERADOR}} (reinicia aprendizado). Método §5.2.

## Nomenclaturas (lei)

Campanha `[cliente]-[canal]-[objetivo]-[funil]-[data]` · Criativo `[cliente]-[ângulo]-[formato]-[hook]-[versão]` · UTM travada (método §6.3). Campos da conta (`[produto]`, `[linha]`), funil `topo·meio·fundo`, data `aaaammdd` e nome imutável depois de rodar: método §5.5.

## Saída mínima

Decisão · direção · ação coordenada · impacto — com número (CPA/CPL/verba/meta), nunca opinião solta.

---
*Base: `100-métodos/METODO-TRAFEGO-PAGO.md` · pesquisa 2025-26 (pós-Andromeda).*
