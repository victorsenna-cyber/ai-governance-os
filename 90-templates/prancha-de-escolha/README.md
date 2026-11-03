# prancha-de-escolha/ — o gerador da prancha que o cliente usa para escolher

> **Tipo:** blueprint · **Instituído:** 18/10/2026 · **Método:** `100-métodos/METODO-PRANCHA-DE-ESCOLHA.md` (ler antes).
> **Caso de origem:** a identidade visual da própria {{EMPRESA}}.

## Como usar numa conta de cliente

1. Na pasta da conta, crie `identidade-visual/` com um `tokens.css` próprio (copie `945-branding/01 - identidade visual/sistema/tokens.css` e ajuste cor e fontes da conta).
2. Escreva as peças das opções num JSON (formato de `945-branding/01 - identidade visual/sistema/pecas-demo.json`), com `"tokens": "tokens.css"` em cada item. O caminho é relativo ao JSON. Texto real, com `_procedencia`.
3. Renderize: `python3 945-branding/01 - identidade visual/sistema/render.py <pecas.json> <conta>/identidade-visual/teste/saida`.
4. Escreva o manifesto da prancha (formato no topo de `gerar_prancha.py`) e gere: `python3 90-templates/prancha-de-escolha/gerar_prancha.py <manifesto.json> --png`.
5. Envie o PNG ao cliente. A recomendação vai na mensagem, não na prancha.
6. Registre a escolha **literal** no `DECISOES.md` da conta antes de tocar nos tokens.

**Uma variável por linha. De 2 a 4 opções. Nada que não assinaríamos.** (método §4 e §5)
