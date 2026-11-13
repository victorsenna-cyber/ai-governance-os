# Doação / apoio institucional, claro

**Tipo:** Doação ou institucional curta.

**Para que serve:** Instituição, projeto social ou causa que pede apoio financeiro: promessa emocional, o lugar que o apoio sustenta, valores sugeridos, prova de apoiadores e CTA repetido.

![prévia](previa.png)

## Ordem das seções (cada uma marcada por um comentário numerado no HTML)

1. Barra do topo: selo de credibilidade e botão fixo.
2. Hero: promessa, CTA primário e cartão de confiança (documento, tempo de casa, segurança).
3. Galeria rolando (cartões 4:5 com legenda).
4. Cartão de valores: abas "única" e "recorrente", valores sugeridos e campo livre.
5. Mural de apoiadores (fichas com iniciais).
6. CTA final.
7. Rodapé legal.

## O que trocar

- **Cores e fontes:** só o bloco `:root` no topo do `<style>` (`--cor-fundo`, `--cor-texto`, `--cor-acento`, `--cor-acento-2`, `--fonte-titulo`, `--fonte-texto` e os extras listados ali). O resto do CSS lê dessas variáveis. Fonte nova entra pelo `<link>` do Google Fonts no `<head>` (ou `@font-face` local do cliente).
- **Texto:** todo `[ROTULO: dica]` é um espaço de copy. O rótulo diz o papel do bloco, a dica diz o que escrever. Escreva a copy pela skill de copy do repositório e pelas réguas da árvore ESCRITA; o molde dá estrutura, não texto.
- **Imagens:** `assets/ph-*.svg` são placeholders com a proporção no rótulo. Troque o `src` pela imagem do cliente (mesma proporção) e o `alt` por descrição real.
- **Links:** `{{LINK_CTA}}`, `{{LINK_WHATSAPP}}`, `{{LINK_PRIVACIDADE}}`, `{{LINK_TERMOS}}` e `{{FORM_ACTION}}` viram a URL real (busque `{{` no arquivo). `href="#"` é link a decidir.
- **Título da página:** `<title>` e a meta description (não existe no molde, acrescente) são do cliente.
- **Rastreio, checkout e formulário:** o molde não traz nada disso. Pixel, GTM, checkout e o destino do formulário entram por decisão da conta, nunca copiados de outra página.
- O botão de gerar a doação **não faz nada**: a cobrança (Pix, link de pagamento) é decisão da conta, entra no `onclick`/`href` do botão depois. As quantias dos botões estão no `onclick="selecionarValor(this,50,'unica')"`.
- Os dados do mural e da galeria estão no `<script>` final (`WALL`, `FOTOS`).

## O que NÃO quebrar

- Funções `trocarTab`, `selecionarValor`, `formatarValor` e os ids `panel-unica`, `panel-recorrente`, `valorUnico`, `valorRecorrente`.
- Os nomes de classe e `id` que o JavaScript lê (estão no `<script>` no fim do arquivo). Mudar o nome sem mudar o script derruba a interação.
- As proporções das imagens e o `viewport` (a página é responsiva: confira no celular antes de entregar).
- Cada bloco tem comentário numerado: apagar a seção inteira é permitido; deixar o bloco pela metade, não.

## Como abrir

Abra `index.html` direto no navegador (funciona em `file://`, sem build). Prévias: `previa.png` (1440×900) e `previa-celular.png` (500×844; o Chrome headless não renderiza abaixo de 500 px, o layout de 390 px é o mesmo).
