# PDF claro

## O que é

O gerador de PDF claro da casa. Recebe um `.md` e um JSON de capa e devolve um PDF A4 em papel quente, com títulos em Lora e corpo em Poppins. **Não muda uma vírgula do conteúdo: só diagrama.**

Nasceu, extraído do PDF da destilação de uma call, e foi generalizado para a casa.

## Quando usar

| Pergunta do leitor | Classe | Este modelo? |
|---|---|---|
| "Eu assino?" | Formal | **sim** |
| "Como isso funciona?" | Estrutura | não, vai no elétrico |
| "Por que eu faria isso?" | Decisão | não, vai no elétrico |

> Documento que se lê para assinar vai no claro. Documento que se lê para entender vai no escuro.

Serve a proposta, contrato e material formal que sai da casa. **Não serve a documento interno:** o Markdown é o formato de trabalho, e PDF desnecessário cria duas versões do mesmo fato.

## Como se gera

```
python3 build-pdf.py --in documento.md --out documento.pdf --capa capa.json --paleta ouro-rubi
```

No Windows, o `build-pdf.py` não roda sozinho. Ele depende do WeasyPrint e de fontes instaladas no caminho do Linux. Este exemplar saiu pelo contorno do Chrome sem interface, com as fontes estáticas.

## O que ele faz com o Markdown

| Elemento | Tratamento |
|---|---|
| título de seção | Lora em realce, com filete dourado, nunca sozinho no fim da página |
| citação | Lora itálico com filete à esquerda |
| tabela | sem grade vertical, cabeçalho em versalete e repetido na quebra de página |
| código | chip dourado em fonte monoespaçada |
| identificador | os códigos curtos, como C-01 e F-12, viram etiquetas douradas sozinhos no meio da frase |

### As paletas

| Paleta | Quando |
|---|---|
| ouro-rubi | o padrão: cliente, proposta, destilação |
| grafite | relatório técnico, material sóbrio |
| vinho-sobrio | jurídico, contraparte, contrato |

---

## O estado deste modelo

**Em revisão.** Ele nasceu de um PDF de conta e nunca foi reescrito como modelo da casa. Também não tem conferência automática: nada reprova uma fonte quebrada antes da entrega.

> A regra deste modelo: não se escreve CSS por documento.
