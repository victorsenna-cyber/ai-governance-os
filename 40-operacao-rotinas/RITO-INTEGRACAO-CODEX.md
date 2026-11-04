# RITO DE INTEGRAÇÃO — do isolamento do Codex para o canônico

> **Tipo:** rito operacional (camada 3) · **Alçada:** {{OPERADOR}}
> ⚠️ **Aplica-se só se você usa um segundo agente executor (ex.: Codex) com escrita isolada na antessala `execução Codex/`. Se opera só com o agente principal, a fila (§9) fica sempre vazia e o rito não dispara.**
> **Por que existe:** a §0 do `AGENTS-EXEC.md` proíbe o executor isolado de escrever nos canônicos — corretamente. **Mas o `CLAUDE.md` §11.3 exige que nada termine sem registro.** As duas regras estão certas e, sem um rito, se anulam: o trabalho é feito, fica na antessala, e a memória da empresa não recebe.
> **Decisão: quem promove é o agente principal, em sessão própria.** Não o executor isolado, não à mão.
>
> 🔴 **Pacote isolado é PROPOSTA, nunca estado — e a promoção é sempre nossa, nunca dele.** ⚠️ **Se o estado de uma conta parece velho, o primeiro lugar a olhar é a fila do `execução Codex/STATUS-CODEX.md` §2.** *(afirmação que antes existia só no `CLAUDE.md` §6 e se perderia na compactação; por isso mora aqui também)*

---

## 1. O PROBLEMA QUE ELE RESOLVE, COM O CASO QUE O CRIOU

**O caso típico: o executor isolado entrega a destilação da call de uma conta** — com IDs por ponto, evidência por timestamp e várias decisões candidatas. O arquivo abre declarando: `PACOTE ISOLADO CODEX · NÃO APLICADO AOS CANÔNICOS`.

**Um dia depois, os canônicos da conta seguem com a data anterior à do pacote, e o `STATUS.md` raiz com data ainda mais velha.**

> **O trabalho estava feito e a empresa não sabia.** Isolamento sem rito de integração não protege a memória — **adia a perda em vez de evitá-la.**

---

## 2. QUANDO RODA

| Gatilho | Urgência |
|---|---|
| **{{OPERADOR}} pede** — "integra o que o Codex fez" | na hora |
| Sessão de Claude aberta e há pacote isolado **não promovido há > 48h** | 🔴 **abre a sessão por aí**, antes do que foi pedido |
| Antes de qualquer decisão que dependa do estado da conta | bloqueante |
| Ritual semanal (segunda) | varredura completa |

> ⚠️ **A regra de 48h existe porque a fila é invisível.** Ninguém sente falta de um registro que nunca existiu — **a dívida só aparece quando alguém decide sobre estado velho.**

---

## 3. COMO ACHAR O QUE ESTÁ PENDENTE

> ⭐ **Há um índice: `execução Codex/STATUS-CODEX.md` §2.** O executor acrescenta uma linha lá ao fechar cada pacote, **na mesma tarefa** — e esse arquivo se lê no início de toda sessão em que a antessala tem pendência.
>
> **Ler o índice primeiro. A varredura abaixo continua valendo como conferência** — porque índice depende de disciplina, e **pacote que existe e não foi indexado é exatamente o caso que o índice não pega.**


**As pastas de isolamento:**

```
execução Codex/                              (governança geral)
clientes/<cliente>/execução Codex/           (por conta)
```

**Varredura:**

```bash
find . -path "*execução Codex*" -name "*.md" -newermt "-7 days" \
  -not -path "./910*" -printf "%TY-%Tm-%Td %TH:%TM  %p\n" | sort -r
```

**Um pacote está pendente quando:** existe em `execução Codex/`, declara `NÃO APLICADO AOS CANÔNICOS` ou equivalente, **e o canônico de destino tem data anterior à dele.**

---

## 4. 🔴 O GATE DE PROMOÇÃO — cinco itens, e nenhum é dispensável

**Antes de mover qualquer linha para um canônico:**

- [ ] **1 · Procedência conferida.** Todo fato promovido tem fonte apontada — timestamp, ID, ou arquivo. **Fato sem fonte não sobe**, mesmo que pareça verdadeiro.
- [ ] **2 · Contradição verificada.** O que o pacote afirma bate com o canônico atual? **Divergência não se resolve promovendo: se resolve perguntando ao {{OPERADOR}}.**
- [ ] **3 · Fronteira de decisão respeitada.** O Codex marcou como "decisão candidata" — **candidata não é decisão.** O que exige alçada (preço, escopo, posicionamento, estrutura) só sobe com aval explícito. Ver `CLAUDE.md` §8, **REGRA Nº 0**.
- [ ] **4 · Camadas do §11.1 completas.** Registro de interação externa precisa das quatro: fatos · decisões e descartes · **tom e conduta** · mensagens literais. **A camada 3 é a que o pacote isolado quase nunca traz** — e é a que se perde para sempre se não for reconstituída agora.
- [ ] **5 · Destino correto.** Estado → `STATUS.md` · decisão → `DECISOES.md` da conta · execução → diário · peça que performou → `swipe-file/` (§11.5).

---

## 5. O QUE SOBE, E O QUE NUNCA SOBE

| Sobe | Não sobe |
|---|---|
| fato com fonte | inferência do Codex sobre intenção de terceiro |
| decisão **já tomada** por quem tem alçada | decisão candidata sem aval |
| citação literal com data e hora | paráfrase |
| número com origem declarada | número derivado sem a conta à vista |
| peça com dado de performance | peça sem dado (§11.5) |

⚠️ **Análise do Codex sobre o que deveria ser feito não é estado — é insumo.** Vai para o corpo do registro como leitura marcada, nunca como fato.

---

## 6. COMO SE REGISTRA A PROMOÇÃO

**No canônico de destino:** a informação, no formato do arquivo, **com a origem citada** — *"via pacote Codex de `<caminho>`, `<data>`"*.

**No pacote isolado:** marcar o topo com `🟢 PROMOVIDO em <data> · destinos: <lista>`.
🔴 **O pacote não se apaga e não se move.** É a evidência de onde o fato veio, e a regra de não-deleção vale aqui igual.

**No `STATUS.md`:** uma linha por sessão de integração — o que foi promovido, o que ficou de fora **e por quê**.

> **O "por quê" do que ficou de fora é a parte que mais vale.** É o que impede a mesma proposta de ser reavaliada do zero na próxima sessão.

---

## 7. O QUE ESTE RITO NÃO FAZ

- **Não autoriza o executor a escrever nos canônicos.** A §0 do `AGENTS-EXEC.md` permanece inteira.
- **Não julga a qualidade do trabalho dele.** Pacote mal feito volta como pergunta ao {{OPERADOR}}, não como correção silenciosa.
- **Não substitui o registro de interação externa.** Se a fonte foi uma call, a destilação continua sendo a destilação — o rito promove, não redestila.

---

## 8. O DESENHO DOS DOIS KERNELS

**`CLAUDE.md` e `AGENTS.md` são o mesmo kernel, para o agente principal** (o `40-operacao-rotinas/ferramentas/sincronizar.py` regenera o segundo a partir do primeiro a cada sincronia; ninguém replica à mão). **`AGENTS-EXEC.md` é o contrato do executor:** a §0 de isolamento e, abaixo dela, o corpo do kernel sem alçada. Quem altera o `CLAUDE.md` não toca no `AGENTS.md`; quem altera a §0 altera só o `AGENTS-EXEC.md`.

---

## 9. FILA ATUAL

Sem pacote pendente.

---
*Alçada {{OPERADOR}}. Instituído após auditoria do trabalho de um executor isolado que entregou pacotes e não os viu promovidos. **A execução deste rito é a fila do §9.***
