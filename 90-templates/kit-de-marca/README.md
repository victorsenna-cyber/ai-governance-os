# Kit de marca · blueprint

> **Tipo:** blueprint · **Método:** `100-métodos/METODO-KIT-DE-MARCA.md` · **Framework:** `100-métodos/ARQUETIPOS-DE-MARCA.md` · **Instituído:** 18/10/2026

| Arquivo | O que é |
|---|---|
| `KIT-DE-MARCA-modelo.md` | o documento do kit: arquétipos com as falas, teste da peça, Dilts, direção, paleta, tipografia, veto, gate, continuidade com o ativo |
| `kit-modelo.json` | os **valores** do kit: cores nos nove tokens do motor, combinações tipográficas, paletas alternativas, tipos, veto e as peças com procedência |
| `gerar_kit.py` | lê o `kit.json` e gera `tokens.css`, as peças (`saida/`), a `prancha-teste` e a página `kit.html`, com PNG de cada |

## Como usar

1. Na conta, crie `branding/01 - identidade visual/` e `branding/02 - posicionamento/` (este com um `README.md` que aponta para `PILARES.md` e a narrativa da conta, sem copiar).
2. Copie `KIT-DE-MARCA-modelo.md` como `KIT-DE-MARCA.md` e `kit-modelo.json` como `kit.json` para a pasta `01`.
3. Preencha a leitura no `.md` e os valores no `.json`.
4. Gere: `python3 90-templates/kit-de-marca/gerar_kit.py "clientes/<cliente>/<pasta de design>/branding/01 - identidade visual/kit.json"`.
5. Olhe os PNG. **O gate se passa no PNG, nunca no código.**

## Contrato com o motor

O motor é o da casa (`945-branding/01 - identidade visual/sistema/render.py` + `componentes.css`). Ele lê **nove tokens de cor com nome fixo**. Na conta, o nome é só o lugar, não a cor:

| Token | Lugar | | Token | Lugar |
|---|---|---|---|---|
| `--noite` | fundo escuro | | `--papel` | fundo claro |
| `--carvao` | cartão no escuro | | `--tinta` | texto no claro |
| `--borda` | fio, divisória | | `--luz` | **o acento** |
| `--pedra` | rótulo, texto secundário | | `--halo` | brilho do acento, nunca texto |
| `--osso` | texto no escuro | | | |

Opcionais: `--papel-2` (cartão no claro), `--borda-claro`. Com `"fundo": "claro"` no kit, **todo tipo de peça** sai no fundo claro (o motor troca os tokens escuros pelos claros). Combinações tipográficas: `--f-display`, `--f-mono`, `--f-corpo`, `--f-grito` (só na combinação de grito, com `"grito": true`), `--t` (tamanho do título), `--vira-estilo` (`italic` ou `normal`, para display sem itálico).

**Os PNG não entram no git** (`.gitignore`: `**/saida/` das contas e `**/prancha-*.png`): se regeneram do `kit.json`.
