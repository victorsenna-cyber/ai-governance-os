# PDF CONTINUUM — template padrão

> **Tipo:** template de artefato · **Instituído em:** 12/08/2026 · **Status:** VIGENTE
> **Origem:** extraído do PDF de uma destilação de call, generalizado.
> **Regra de ouro:** **não se escreve CSS novo por documento.** Todo PDF nosso sai daqui, com a mesma assinatura visual.

---

## 1. Para que serve

Transformar qualquer `.md` do repositório em um PDF apresentável, **sem alterar uma vírgula do conteúdo**. Diagramação apenas.

**Use quando** o material vai para alguém de fora que não lê Markdown com conforto: cliente, prospect, parceiro, contraparte jurídica, investidor.

**Não use** para documento interno. Markdown é o formato de trabalho; PDF é embalagem, e embalagem desnecessária cria duas versões do mesmo fato.

---

## 2. Arquivos

| Arquivo | Papel |
|---|---|
| `build-pdf.py` | gerador. CLI. **é o único ponto de entrada** |
| `estilo.css` | folha de estilo. **Não editar por documento** |
| `capa.exemplo.json` | modelo de capa, para copiar e preencher |

---

## 3. Uso

**Sem capa** — documento corrido, começa direto no conteúdo:

```bash
python3 build-pdf.py --in doc.md --out doc.pdf --cabecalho "TÍTULO CORRIDO · DATA"
```

**Com capa** — o modo normal para material que sai da casa:

```bash
python3 build-pdf.py --in doc.md --out doc.pdf --capa capa.json
```

**Trocando a paleta:**

```bash
python3 build-pdf.py --in doc.md --out doc.pdf --capa capa.json --paleta vinho-sobrio
```

### Opções

| Flag | Efeito |
|---|---|
| `--in` | `.md` de origem (obrigatório) |
| `--out` | `.pdf` de destino (obrigatório) |
| `--capa` | JSON da capa. Sem ele, não há capa |
| `--paleta` | `ouro-rubi` (padrão) · `grafite` · `vinho-sobrio` |
| `--cabecalho` | texto do cabeçalho corrido. Também pode vir no JSON |
| `--manter-titulo` | preserva o H1 e o bloco de metadados do `.md`. Por padrão, quando há capa, esse bloco é cortado porque a capa já o substitui |

### Dependências

```bash
pip install weasyprint markdown --break-system-packages
```

Fontes esperadas em `/usr/share/fonts/truetype/google-fonts/`: **Lora** (variable + italic) e **Poppins** (Light, Regular, Medium, Bold, Italic, LightItalic).

---

## 4. Paletas

| Nome | Quando usar | Realce |
|---|---|---|
| **`ouro-rubi`** | padrão institucional. Cliente, proposta, destilação | rubi/vinho `#6B1E36` sobre dourado `#C9A24B`, papel quente `#FBF8F3` |
| **`grafite`** | documento técnico, relatório, material sóbrio | azul-ardósia `#2E3A45` sobre neutro |
| **`vinho-sobrio`** | jurídico, contraparte, contrato | vinho fechado `#5A1A22`, menos ouro |

Paleta nova entra como bloco em `PALETAS` no `build-pdf.py` — **nunca como CSS solto no documento.**

---

## 5. O que o template faz com o Markdown

| Elemento | Tratamento |
|---|---|
| `##` | seção: Lora 17pt em realce, filete dourado, nunca órfã no fim da página |
| `###` | subseção com losango dourado |
| tabelas | sem grade vertical, cabeçalho em versalete, zebra discreta, **cabeçalho repete quando quebra página**, linha nunca parte no meio |
| `>` citação | Lora itálico com filete de realce à esquerda |
| `` `código` `` | monoespaçada em chip dourado |
| blocos ```` ``` ```` | fundo quente com barra dourada, quebra preservada |
| `---` | ornamento centrado |
| **IDs** `C-01`, `F-12` | viram etiquetas douradas automaticamente. Qualquer padrão `LETRA(S)-NÚMERO` |
| emojis | convertidos em marcas tipográficas — `⚠` vira selo, `⭐` e `🟡` viram losango e ponto dourados. **Evita quadradinho preto no leitor do destinatário** |

---

## 6. A capa

Campos do JSON, todos opcionais exceto `titulo`:

```json
{
  "sobretitulo": "linha pequena, versalete espaçado, acima do título",
  "titulo": "primeira linha, romana",
  "titulo_italico": "segunda linha, itálica — o contraste que dá o tom",
  "subtitulo": ["cada item vira uma linha", "em Lora itálico"],
  "meta": { "Rótulo": "valor" },
  "rodape": { "rotulo": "…", "frase": "…", "nota": "…" },
  "cabecalho": "TEXTO DO CABEÇALHO CORRIDO"
}
```

A marca geométrica do canto superior direito — círculos concêntricos com vesica — **é neutra de propósito**. Herda as cores da paleta e não tenta imitar a identidade de nenhum cliente. Quando o cliente tiver logo própria e autorizada, ela substitui a marca, e a troca é feita no `build-pdf.py`, não no documento.

O rodapé da capa existe para uma coisa: **declarar a regra de leitura do arquivo** antes de a pessoa abrir a primeira seção.

---

## 7. Antes de enviar

1. **Conferir o texto extraído**, não o visual: `pdftotext` e comparar contagens com o `.md`.
2. **Renderizar as páginas críticas** em PNG e olhar — capa, primeira seção, uma página só de tabela, uma com citação.
3. **Decidir sobre o conteúdo interno.** Nossos documentos costumam conter leitura comercial — margem, escopo não precificado, âncoras, risco da conta. Decidir conscientemente se o destinatário deve ver.

---

## 8. Exemplar de referência

Uma destilação de call em PDF, na paleta `ouro-rubi`, capa completa. O `capa.exemplo.json` desta pasta serve de modelo preenchido.

## 9. Exemplar para ver o modelo e o estado no Windows *(01/11/2026)*

`exemplo/EXEMPLO-PDF-CLARO.pdf`, com o `.md` e o JSON de capa ao lado, fala só do próprio modelo.

🔴 **No Windows, o `build-pdf.py` não roda sozinho.** Ele importa o WeasyPrint, que não carrega no Windows, e aponta as fontes para `/usr/share/fonts`. O exemplar saiu por um contorno que roda o `build-pdf.py` sem alterá-lo, troca o WeasyPrint pelo Chrome sem interface e carrega Lora e Poppins **estáticas** (a variável do Google sai Type3). Esse contorno não está neste modelo. **Integrar o contorno e as fontes aqui é pendência aberta**, junto com a revisão marcada desde 18/09.

A conferência de fonte e página em branco funciona sobre qualquer PDF: `python3 90-templates/pdf-noturno/gerar_pdf.py --conferir arquivo.pdf`.

Defeito achado pelo exemplar: **código curto no começo de célula ou de parágrafo não vira etiqueta** (a regra exclui o que vem logo depois de uma marca HTML). No meio da frase funciona.

---

**Base:** `../../100-métodos/METODO-DESTILACAO-DE-CALLS.md` §8 · `../../CLAUDE.md` §7
