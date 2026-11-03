# conta-nova — o kit que se copia inteiro

> **Uso:** copiar esta pasta para `clientes/<cliente>/` **na etapa 0 do trilho**, antes de qualquer outra coisa.
> Método: `100-métodos/METODO-TRILHO-DE-CONTA-NOVA.md`.

---

## O que copiar, e quando

| Arquivo / pasta | De onde | Quando | Etapa |
|---|---|---|---|
| **`PAINEL.md`** | daqui | **sempre, no dia 0** | 0 |
| **`PEDIDO-UNICO.md`** | daqui | **sempre, no dia 0** — e enviado no mesmo dia | 0 |
| `DECISOES.md` · `STATUS.md` da conta | criar vazios, no padrão de 4 camadas (`CLAUDE.md` §11.1) | sempre | 0 |
| `contexto/` | criar vazia | sempre — recebe gravação e transcrição brutas | 0 |
| **`lexico-icp/`** | `90-templates/lexico-icp/` | 🔴 **no onboarding, nunca na primeira peça** — na primeira peça já é tarde | 4 |
| `PILARES.md` | gerado pelo `METODO-TESTE-DE-PILARES.md` | ato II | 3 |
| **`benchmark-vsl/`** | `90-templates/benchmark-vsl/` (4 arquivos) | quando a peça for VSL | 6 |
| `diagnostico/` | `90-templates/diagnostico-operacao/` | se o G0 for Mapa da Ordem | 1 |

---

## A estrutura que nasce

```
clientes/<cliente>/
├── PAINEL.md              ⭐ a única tela que se abre para saber onde a conta está
├── PEDIDO-UNICO.md        o que se pede ao cliente — de uma vez, no dia 0
├── DECISOES.md            uma DEC por decisão, com o que foi descartado e por quê
├── STATUS.md              estado da conta
├── contexto/              fonte bruta: gravação, transcrição, material recebido
├── lexico-icp/            BANCO · FONTES · LACUNAS — grau D
├── PILARES.md             as 5 binárias
└── benchmark-<peça>/      matriz · estrutura invisível · espaço vazio · destilações
```

---

## As três regras que fazem o kit funcionar

1. 🔴 **O pedido único sai no dia 0.** Latência é a camada que não comprime, e é o gargalo real de conta nova. **Pedido fracionado multiplica latência, não esforço.**
2. 🔴 **O painel se atualiza no fecho de cada etapa** — é o item 2 do gate de passagem, não tarefa à parte.
3. 🔴 **Pendência nasce declarada**, com dono e com o que a destrava. **Pendência descoberta depois é retrabalho; declarada no nascimento é trabalho.**

---

## O que este kit NÃO resolve

- **Não substitui gate nenhum.** Ele ordena os métodos; os gates continuam onde estão.
- **Não decide o trilho A ou B** — isso sai do `30-comercial/ICP.md` §4-bis, e **os dois não se misturam**.
- **Não autoriza começar pela peça.** É o pedido mais comum e o mais caro de aceitar.

---
*Instituído em 20/09/2026, junto com `METODO-TRILHO-DE-CONTA-NOVA.md`. 🟡 Verificação em caso real pendente.*
