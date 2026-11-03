# 945-branding

> **Alçada:** {{OPERADOR}}
> **Por que existe:** branding não é marketing em si. Toda peça é classificada e colocada na pasta correta; se não houver pasta, ela é criada.
> **Número:** 945, antes de `950-marketing/`. A marca vem antes da peça que a divulga.

---

## O que é branding aqui, e o que não é

| Mora aqui (branding) | Mora em outro lugar |
|---|---|
| como a marca **aparece**: cor, tipografia, tipos de arte, sistema de criativo, ambiente de gravação | a **peça** que usa esse sistema → `950-marketing/` |
| como a marca **se posiciona**: narrativa central, pitch, bio, o lugar que ocupamos na cabeça do público | o que se **vende** e por quanto: ICP, oferta, preço, proposta → `30-comercial/` |
| | **quem somos** (arquétipo, cultura, princípio) → `00-core/` (`CULTURA.md` §9 · `MANIFESTO.md`), carregado sempre |
| | a marca pessoal do {{OPERADOR}}, se houver, como **conta** (decisões, pilares, voz) → `clientes/<conta>/` |

**Pergunta que decide:** *isto define como a marca aparece ou se posiciona, ou é uma peça que usa a marca?* A primeira resposta manda para cá; a segunda, para marketing.

## Mapa

| Pasta | O que tem | Fonte que governa |
|---|---|---|
| `01 - identidade visual/` | o arquétipo no ambiente (nível mais baixo de Dilts): `IDENTIDADE-VISUAL.md`, `sistema/` (tokens, componentes, `render.py`), `fontes/`, a leitura das referências coletadas, as pranchas. Começa vazia: preencha a partir do arquétipo escolhido (`100-métodos/ARQUETIPOS-DE-MARCA.md`) | `IDENTIDADE-VISUAL.md` |
| `02 - posicionamento/` | a narrativa central (inimigo, big idea, crenças, promessa e fronteira) · pitch e bio do operador (bio e pitch falado do perfil). Começa vazia | cada arquivo; em conflito, `30-comercial/ICP.md` e `oferta.md` prevalecem no fato comercial (`CLAUDE.md` §3) |

## Regra de lugar

🔴 Toda peça entra na pasta da natureza dela. **Se a pasta não existe, ela é criada na mesma tarefa**, com `README.md`, linha no `CLAUDE.md` §7 e os caminhos antigos corrigidos. Rota: `00-core/roteador/ARVORE-CASA.md`.
