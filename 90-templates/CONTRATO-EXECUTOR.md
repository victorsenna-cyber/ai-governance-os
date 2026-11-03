# CONTRATO DE EXECUTOR — template

> **Tipo:** template (camada 3) · **Criado:** 2026-09-12 · **Dono:** {{OPERADOR}}
> **Para que serve:** é o único arquivo que um executor (Codex, Code Assist, ou qualquer modelo em papel de execução) precisa receber para começar. Sem ele, o executor devolve a tarefa.
> **Base:** `00-core/PROTOCOLO-MULTI-MODELO.md` §2 · `AGENTS.md` §2
> **Como usar:** copiar para a pasta da tarefa como `CONTRATO-<tarefa>-<data>.md` e preencher. **Campo vazio vira pergunta ao dono, nunca invenção.**

---

## 1. Objeto

**O que existe no fim, em uma frase:**
`{{ex.: a página de vendas implementada em HTML/CSS/JS estático, responsiva em 390/768/1440, pronta para revisão — sem publicar}}`

**O que NÃO é o objeto** (delimitar evita 80% do retrabalho):
- `{{ex.: não é decidir a ordem das seções — ela vem travada}}`
- `{{ex.: não é publicar nem configurar domínio}}`

---

## 2. Fontes — máximo 5

| # | Arquivo | Para quê | Ler inteiro? |
|---|---|---|---|
| 1 | `{{caminho}}` | `{{o quê}}` | `{{sim / só §X}}` |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

> 🔴 **Se a tarefa exige mais de 5, o contrato está mal feito.** Voltar ao agente que decide e fatiar a tarefa — não expandir a lista.

---

## 3. Insumos travados (usar literalmente, não interpretar)

| Insumo | Onde está | Estado |
|---|---|---|
| **Copy final, bloco a bloco** | `{{caminho}}` | ✅ travada — **literal, zero edição** |
| **Tokens** (cor, tipo, espaçamento, raio) | `{{caminho}}` | |
| **Grade e escala** | `{{caminho}}` | |
| **Limite de caracteres por bloco** | `{{caminho}}` | |
| **Assets** (imagens, vídeo, ícones) | `{{caminho}}` | |
| **Stack e restrições técnicas** | `{{ex.: HTML/CSS/JS puro, sem framework, sem CDN externo}}` | |

**Se a copy não couber no espaço:** devolver o bloco com a contagem de caracteres e o excedente. **Não reescrever, não encurtar, não trocar palavra.**

---

## 4. Saída e gate

**Onde entregar:** `{{caminho exato}}`
**Formato:** `{{ex.: um arquivo .html autocontido + README de 5 linhas}}`

**Gate — o executor roda e declara item a item, antes de dizer que terminou:**

- [ ] Renderiza sem erro de console em 390 / 768 / 1440
- [ ] Copy idêntica à fonte travada (diff limpo)
- [ ] Todos os `{{placeholder}}` resolvidos **ou listados como pendência**
- [ ] Lighthouse ≥ `{{meta}}` em performance / acessibilidade / boas práticas / SEO
- [ ] Nenhum link, pixel, checkout ou domínio ativado
- [ ] `{{gate específico da tarefa}}`

---

## 5. 🔴 Proibido decidir — devolver em vez de resolver

Além da lista permanente do `AGENTS.md` §3, nesta tarefa especificamente:

- `{{ex.: se faltar asset, usar placeholder cinza com a dimensão escrita — nunca buscar imagem de banco}}`
- `{{ex.: se um bloco não fizer sentido visualmente, entregar como está e apontar no fecho}}`
- `{{ex.: ordem das dobras é decisão da etapa 1 — não reordenar mesmo que pareça melhor}}`

---

## 6. Fecho obrigatório do executor

```
ARQUIVOS ALTERADOS
- caminho — o que mudou (1 linha)

GATE
- item a item, com resultado real (não "deve funcionar")

TRAVEI EM
- toda parada por falta de contrato, com a pergunta exata
- "nenhuma" é resposta válida e rara

PENDÊNCIAS
- o que ficou como placeholder e por quê
```

> **"TRAVEI EM" é o campo mais valioso do fecho.** Cada parada registrada é um buraco de contrato encontrado antes de virar retrabalho.

---

## 7. Metadados

| | |
|---|---|
| **Tarefa** | `{{nome}}` |
| **Executor** | `{{Codex / outro}}` |
| **Dono da decisão** | {{OPERADOR}} |
| **Contrato escrito por** | `{{agente}}` em `{{data}}` |
| **Etapa do circuito** (se página) | `{{4 · execução visual}}` |
| **Revisão cruzada por** | `{{quem audita — nunca quem escreveu}}` |

---
*Regra-mãe: prompt curto que aponta vence prompt longo que explica. Se o executor precisou ler o repositório para entender a tarefa, o contrato falhou — não o executor.*
