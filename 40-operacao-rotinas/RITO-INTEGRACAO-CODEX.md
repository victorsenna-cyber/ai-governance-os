# RITO DE INTEGRAÇÃO — do isolamento do Codex para o canônico

> **Tipo:** rito operacional (camada 3) · **Alçada:** {{OPERADOR}}
> ⚠️ **Aplica-se só se você usa um segundo agente executor (ex.: Codex) com escrita isolada na antessala `execução Codex/`. Se opera só com o Claude, a fila (§9) fica sempre vazia e o rito não dispara.**
> **Por que existe:** a §0 do `AGENTS.md` proíbe o executor isolado de escrever nos canônicos — corretamente. **Mas o `CLAUDE.md` §11.3 exige que nada termine sem registro.** As duas regras estão certas e, sem um rito, se anulam: o trabalho é feito, fica na antessala, e a memória da empresa não recebe.
> **Decisão: quem promove é o Claude, em sessão própria.** Não o executor isolado, não à mão.
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

> ⭐ **Há um índice: `execução Codex/STATUS-CODEX.md` §2.** O executor acrescenta uma linha lá ao fechar cada pacote, **na mesma tarefa** — e esse arquivo entrou na carga obrigatória do `CLAUDE.md` §3.
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

- **Não autoriza o Codex a escrever nos canônicos.** A §0 do `AGENTS.md` permanece inteira.
- **Não julga a qualidade do trabalho dele.** Pacote mal feito volta como pergunta ao {{OPERADOR}}, não como correção silenciosa.
- **Não substitui o registro de interação externa.** Se a fonte foi uma call, a destilação continua sendo a destilação — o rito promove, não redestila.

---

## 8. ⚠️ A DÍVIDA QUE O DESENHO ATUAL CARREGA

**Desenho: o `AGENTS.md` é um clone do `CLAUDE.md` + a §0 de isolamento.** Os dois ficam sincronizados, e a diferença de tamanho é exatamente a §0.

> 🔴 **Consequência que precisa estar escrita: toda alteração no `CLAUDE.md` passa a exigir replicação no `AGENTS.md`, ou os dois divergem em silêncio.**
>
> **E divergência silenciosa aqui é pior que em outros arquivos**, porque ninguém compara os dois — cada agente lê o seu e nenhum vê o outro.

**Regra que decorre:** ⭐ **quem altera o `CLAUDE.md` replica no `AGENTS.md` na mesma tarefa**, ou declara por escrito que a alteração não vale para o executor. **As duas coisas são aceitáveis; o silêncio não é.**

### 8.1 Dois defeitos herdados da clonagem, ainda não corrigidos

O próprio executor os documenta quando audita a clonagem, sem ser perguntado:

| # | Defeito | Correção proposta |
|---:|---|---|
| 1 | §3 do `AGENTS.md` diz **"Fronteira `AGENTS.md` × `AGENTS.md`"** — frase sem sentido, produto da substituição literal | **uma linha na §0**, que já tem precedência declarada: *"a §3 é artefato de clonagem e não se aplica"* |
| 2 | Referências a `clientes/<cliente>/CLAUDE.md` viraram `clientes/<cliente>/AGENTS.md` no clone. **Os dois arquivos existem nas contas e têm conteúdos diferentes** — o roteamento do executor aponta para o arquivo errado | mesma linha na §0, ou correção pontual das referências |

⚠️ **Se você mantiver o clone como está, nenhum dos dois se corrige sozinho.** Ficam registrados aqui para não se perderem — **defeito conhecido e não corrigido é decisão; defeito esquecido é acidente esperando.**

---

## 9. FILA ATUAL

Sem pacote pendente.

---
*Alçada {{OPERADOR}}. Instituído após auditoria do trabalho de um executor isolado que entregou pacotes e não os viu promovidos. **A execução deste rito é a fila do §9.***
