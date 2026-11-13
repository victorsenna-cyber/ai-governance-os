# Produto digital (e-book/guia), escuro violeta, capa 3D

**Tipo:** Página de produto digital.

**Para que serve:** E-book, guia ou material de iniciação vendido em página própria: capa em 3D, abas de amostra, estrutura por capítulos, entrega, quem escreve, oferta e FAQ.

![prévia](previa.png)

## Ordem das seções (cada uma marcada por um comentário numerado no HTML)

1. Topo fixo com preço e CTA (aparece depois do hero).
2. Hero: promessa, capa 3D, preço, CTA.
3. Reconhecimento.
4. Virada.
5. O produto.
6. Diferencial.
7. Jornada em 4 movimentos (acende ao rolar).
8. Demonstração em abas.
9. Perguntas que responde.
10. Estrutura por capítulos.
11. Para quem é.
12. Como receber.
13. O que entrega e o que não promete.
14. Autor(a).
15. Oferta.
16. Clareza antes da decisão.
17. Chamada final.
18. Rodapé legal e links.

## O que trocar

- **Cores e fontes:** só o bloco `:root` no topo do `<style>` (`--cor-fundo`, `--cor-texto`, `--cor-acento`, `--cor-acento-2`, `--fonte-titulo`, `--fonte-texto` e os extras listados ali). O resto do CSS lê dessas variáveis. Fonte nova entra pelo `<link>` do Google Fonts no `<head>` (ou `@font-face` local do cliente).
- **Texto:** todo `[ROTULO: dica]` é um espaço de copy. O rótulo diz o papel do bloco, a dica diz o que escrever. Escreva a copy pela skill de copy do repositório e pelas réguas da árvore ESCRITA; o molde dá estrutura, não texto.
- **Imagens:** `assets/ph-*.svg` são placeholders com a proporção no rótulo. Troque o `src` pela imagem do cliente (mesma proporção) e o `alt` por descrição real.
- **Links:** `{{LINK_CTA}}`, `{{LINK_WHATSAPP}}`, `{{LINK_PRIVACIDADE}}`, `{{LINK_TERMOS}}` e `{{FORM_ACTION}}` viram a URL real (busque `{{` no arquivo). `href="#"` é link a decidir.
- **Título da página:** `<title>` e a meta description (não existe no molde, acrescente) são do cliente.
- **Rastreio, checkout e formulário:** o molde não traz nada disso. Pixel, GTM, checkout e o destino do formulário entram por decisão da conta, nunca copiados de outra página.
- A capa 3D é CSS (`.ebook-cover`): o texto da capa é placeholder; para imagem real, coloque um `<img>` dentro.
- Variáveis extras: `--cor-fundo-2`, `--cor-fundo-3`, `--cor-acento-claro`, `--cor-texto-suave`.

## O que NÃO quebrar

- `#topbar`, `#hero`, `.reveal`, `.step`, `.demo-tab`, `.demo-panel`, `.faq-btn`: o script do fim lê todos.
- Os nomes de classe e `id` que o JavaScript lê (estão no `<script>` no fim do arquivo). Mudar o nome sem mudar o script derruba a interação.
- As proporções das imagens e o `viewport` (a página é responsiva: confira no celular antes de entregar).
- Cada bloco tem comentário numerado: apagar a seção inteira é permitido; deixar o bloco pela metade, não.

## Como abrir

Abra `index.html` direto no navegador (funciona em `file://`, sem build). Prévias: `previa.png` (1440×900) e `previa-celular.png` (500×844; o Chrome headless não renderiza abaixo de 500 px, o layout de 390 px é o mesmo).
