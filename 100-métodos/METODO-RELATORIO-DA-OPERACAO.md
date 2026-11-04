# MÉTODO — RELATÓRIO DA OPERAÇÃO (foto → redação → verificador)

> **Tipo:** método · secundário: gate (§4)
> **Origem:** casa de origem do template · **Alçada:** {{OPERADOR}} · **Estado:** 🟡 **provisório, `n=1`.** Gradua com 5 dias úteis de relatório da operação sem reprovação do verificador na versão entregue e sem correção do {{OPERADOR}}.
> **Roda dentro de:** operação por tasks (`40-operacao-rotinas/tarefas/README.md`).
> **Fonte operacional única do texto que o agente segue:** `90-templates/repo-agentes/skills/relatorio-da-operacao/SKILL.md`. Este arquivo é o porquê e o gate; a skill é o como, e é ela que vai para o cliente.

---

## 1. O princípio: três mãos, três verbos

| Mão | Verbo | Peça |
|---|---|---|
| **script (leitor)** | **calcula** | a foto da operação: cada número com fonte e hora (`90-templates/repo-agentes/ferramentas/FOTO-DA-OPERACAO.md`) |
| **agente** | **escreve** | o relatório no formato da skill, só com o que a foto tem |
| **script (verificador)** | **confere** | `verificar_relatorio.py`: todo número, hora, data, código e citação do texto existe na foto, ou o relatório não sai |

**Por que assim:** sem esta terceira mão, o agente lê o JSON do conector e escreve o número, e **nenhum código confere se a frase bate com a fonte**. Um relatório que o dono precisa conferir não poupa o tempo dele, só muda o trabalho de lugar. **O relatório só tem valor se o dono puder agir sem abrir a fonte.**

## 2. A anatomia da resposta

1. Abertura de uma linha, com a conclusão.
2. Uma linha por área: `Área (fonte, hora): …`, na ordem quando · quem viu · quem fez · efeito.
3. Detalhe só do que está fora do normal.
4. Pendência humana como estado com nome.
5. "Precisa de você", fechado: até 5 itens, agrupado, com código.
6. "Não li", com o motivo.

O texto completo está na skill. **Pergunta de uma parte só** recebe só aquela linha.

## 3. Onde mora, por empresa

| Empresa | Leitor | Foto e relatório |
|---|---|---|
| **{{EMPRESA}}** | `40-operacao-rotinas/ferramentas/foto-da-operacao.py` | `40-operacao-rotinas/operacao-hoje/AAAA-MM-DD-HHhMM-{foto.json,relatorio.md}` |
| **Cliente** | a pasta de leitores do repo dele (o leitor é sempre do cliente) | a pasta de resumos do manual de rotinas dele |

**Fonte nova** entra primeiro no leitor e só depois no texto. Na {{EMPRESA}}, o leitor lê o payload do `painel-projetos.py`, para o painel e o relatório nunca divergirem.

## 4. 🔴 Gate e régua de veto

**Roda antes de todo envio:**

```
python3 90-templates/repo-agentes/ferramentas/verificar_relatorio.py --foto <foto> --texto <relatorio>
```

**Reprova sozinho:**

- número, valor, hora, data, código ou citação **fora da foto**;
- **contornar o verificador** (número por extenso, aspas que não são citação);
- **fonte não lida sem a linha "Não li"**;
- item em "Precisa de você" que **não está em `precisa_de_voce` da foto**;
- **relatório enviado sem ✅.**

## 5. Como o método foi provado (n=1)

Sobre uma foto real de operação, o relatório **passou com todos os itens conferidos.** Uma cópia com números trocados de propósito foi **reprovada em cada um deles, com a linha de cada um.**

**Achado do próprio relatório:** contas marcadas como ativas apareceram com marcos vencidos há muito tempo. A decisão de retomar ou arquivar voltou para o dono.

## 6. O que fica fora deste método

- Envio pelo WhatsApp e rotina com horário: entram quando houver motor de agentes rodando.
- O nome da conta precisa ser o mesmo nos cartões de decisão e nas pastas; se não for, a mesma conta aparece duas vezes na contagem.
