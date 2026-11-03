# clientes/ — raiz canônica por cliente

> **Uma pasta por cliente, com o nome do cliente.** A lista viva é a própria pasta. Cópia homônima fora desta raiz é legado: nunca fonte, nunca destino.
> 🔴 **Tudo o que é do cliente mora na pasta dele:** contexto, decisões, estado, tráfego pago, páginas, criativos, registros. Nada de cliente em `30-comercial/`.

## Como nasce uma conta

Pelo trilho `100-métodos/METODO-TRILHO-DE-CONTA-NOVA.md`, copiando o kit `90-templates/conta-nova/` (`PAINEL.md`, `PEDIDO-UNICO.md`, `DECISOES.md` e `STATUS.md` vazios, `01 - contexto/`), no **dia 0**. O `_modelo/` desta pasta é o esqueleto completo, com a numeração.

## O esqueleto

```
clientes/<Cliente>/
├── PAINEL.md               ⭐ a única tela que se abre para saber onde a conta está (frontmatter lido pelo painel de projetos)
├── STATUS.md               estado da conta: fonte única de fato atual dela
├── DECISOES.md             uma DEC-<sigla>-<n> por decisão, com data, o descartado e o porquê
├── PILARES.md              as 5 binárias (METODO-TESTE-DE-PILARES); sem P1/P4 aprovando não há copy
├── PEDIDO-UNICO.md         o que se pede ao cliente, de uma vez, no dia 0
├── CLAUDE.md               (quando a conta recebe repo próprio) o kernel dela — 90-templates/repo-cliente/CLAUDE-modelo.md
├── DESTILACAO-CALL-<data>.md   toda call, destilada (nunca resumida)
├── lexico-icp/             BANCO · FONTES · LACUNAS — grau D
├── benchmark-vsl/          quando a peça for VSL
├── 01 - contexto/          fonte bruta: gravação, transcrição, material recebido, OpenWA/ (captura de WhatsApp)
├── 02 - <área>/            as pastas de execução, numeradas na sequência da própria conta:
├── NN - tráfego pago/      plano de mídia, briefing, estrutura de campanhas, matriz de criativos, log, relatórios, painel.json (molde: 90-templates/trafego-cliente/)
├── NN - web design/        páginas do cliente e a configuração de publicação delas
├── NN - criativos/ · NN - branding/ · NN - registros e arquivo/   conforme a conta precisar
└── execução Codex/         a antessala da conta (proposta do executor externo, nunca estado)
```

`NN` = o próximo número livre na sequência da conta; a pasta que falta é criada com ele **na mesma tarefa**.

## Regras

- **Pedido que cita um cliente carrega `STATUS.md` + `DECISOES.md` + a antessala dele, em qualquer árvore** (`CLAUDE.md` §6).
- **Quem muda o `STATUS.md` muda o frontmatter do `PAINEL.md` no mesmo ato** (`ARVORE-CONTA.md`). O painel é leitor.
- **Peça para o público do cliente só com a conta passada:** `PILARES.md` sem P1/P4 reprovando **e** `lexico-icp/` com fonte `D` (`ARVORE-ESCRITA.md`). Vale sob urgência.
- **Fronteira Governança × cliente** (`CLAUDE.md` §6.2): a casa governa políticas e métodos; a conta governa fatos, voz, oferta, decisões e estado.
- Sessão de conta exportada fica em `NN - registros e arquivo/sessoes-claude/`, não em `40-operacao-rotinas/`.
