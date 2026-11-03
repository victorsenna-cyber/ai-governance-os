# sistema/ — o sistema de criativos da marca

O motor já vem pronto. O que o operador muda é o valor, quando a identidade (`../IDENTIDADE-VISUAL.md`) estiver decidida:

| Arquivo | O que é | Quem consome |
|---|---|---|
| `tokens.css` | cor, tipografia, espaçamento e raio como variáveis CSS. Vem em valores neutros; os da marca saem das tabelas §2 e §3 | `render.py`, `90-templates/prancha-de-escolha/`, `90-templates/kit-de-marca/` |
| `componentes.css` | a forma de cada tipo de criativo (§4): N1 N2 N3 P1 P2 B1 C1 D1 F1 | `render.py` |
| `render.py` | gera PNG de cada peça a partir de um JSON, pelo Chrome headless: `python3 render.py pecas-demo.json <pasta de saída>` | a produção de peças, a prancha e o kit de marca |
| `pecas-demo.json` | uma peça de exemplo por tipo, toda fictícia, para testar o sistema. F1 pede foto (`"foto"`, relativa ao JSON), por isso fica de fora | `render.py` |

Regra: a peça nunca é desenhada "no gosto". Entra pelo tipo de criativo, com a referência medida (`960-referências criativos/LEIA-ME-MODELAGEM.md`), e passa pelo gate visual (§7 da identidade).
