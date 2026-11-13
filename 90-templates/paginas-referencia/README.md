# Páginas de referência (moldes para copiar)

**Tipo:** blueprint · 🟡 provisório (princípio: páginas de cliente se fazem **copiando** um molde e trocando copy, tokens, imagens e links, não codando do zero).

Cada pasta é uma página completa, **já sanitizada**: sem texto, marca, foto, link, rastreio, checkout ou formulário de terceiro. Todo texto é um placeholder `[PAPEL: dica]` do tamanho aproximado do original, para o layout não quebrar. Abre direto no navegador (`file://`), um `index.html` + `assets/` pequeno, sem build.

## Os moldes

| Molde | Tipo | Quando usar | Seções (em ordem) | Prévia |
|---|---|---|---|---|
| [`link-bio-claro`](link-bio-claro/) | Link na bio | Negócio local ou institucional que precisa de 1 tela com prova rápida e botões de contato | Cabeçalho + selos · carrossel · botões (WhatsApp, ação, rota) · rodapé | [desktop](link-bio-claro/previa.png) · [celular](link-bio-claro/previa-celular.png) |
| [`doacao-institucional`](doacao-institucional/) | Doação / institucional curta | Causa, projeto social, instituição que pede apoio | Barra · hero · galeria · valores (única/recorrente) · mural de apoiadores · CTA · rodapé | [desktop](doacao-institucional/previa.png) · [celular](doacao-institucional/previa-celular.png) |
| [`captura-evento-escura`](captura-evento-escura/) | Captura de evento/live | Aula ao vivo, meditação, encontro com data marcada e contagem | Barra · hero + contagem · o que é · virada · como funciona · programa · preparação · inscrição · rodapé | [desktop](captura-evento-escura/previa.png) · [celular](captura-evento-escura/previa-celular.png) |
| [`captura-workshop-azul`](captura-workshop-azul/) | Captura de workshop gratuito | Lead com formulário já na 1ª dobra, evento gratuito | Faixa rolante · hero com dados + foto + formulário · promessa · 2 provas · CTA · rodapé | [desktop](captura-workshop-azul/previa.png) · [celular](captura-workshop-azul/previa-celular.png) |
| [`obrigado-passos-escuro`](obrigado-passos-escuro/) | Obrigado / confirmação | Depois da inscrição: "falta só um passo" | Logo + progresso · headline · pergunta (opcional) · ação que conclui · rodapé | [desktop](obrigado-passos-escuro/previa.png) · [celular](obrigado-passos-escuro/previa-celular.png) |
| [`quiz-passos-claro`](quiz-passos-claro/) | Quiz | Diagnóstico por perfil que termina na oferta | Introdução · perguntas com progresso · captura opcional · resultado + CTA | [desktop](quiz-passos-claro/previa.png) · [celular](quiz-passos-claro/previa-celular.png) |
| [`vsl-curta-clara`](vsl-curta-clara/) | VSL curta | Tráfego frio que decide numa dobra: vídeo + bullets + autoridade | Topo + vídeo · bullets + CTA · para quem é · autoridade · CTA · rodapé | [desktop](vsl-curta-clara/previa.png) · [celular](vsl-curta-clara/previa-celular.png) |
| [`vsl-vendas-longa-clara`](vsl-vendas-longa-clara/) | VSL + vendas longa | Aula em vídeo no topo e página de vendas completa embaixo, CTA abre modal de captura | Hero + vídeo · prints · identificação · virada · método · efeitos · depoimentos · oferta · autora · FAQ | [desktop](vsl-vendas-longa-clara/previa.png) · [celular](vsl-vendas-longa-clara/previa-celular.png) |
| [`vendas-curta-escura`](vendas-curta-escura/) | Vendas curta (produto de entrada) | Produto de ticket baixo em 16 blocos enxutos, CTA fixo | Hero · identificação · consequência · reenquadre · causa · método · etapas · antes×depois · conteúdo · para quem · por que agora · oferta · pós-compra · garantia · FAQ · CTA | [desktop](vendas-curta-escura/previa.png) · [celular](vendas-curta-escura/previa-celular.png) |
| [`vendas-longa-escura`](vendas-longa-escura/) | Vendas longa | Treinamento/método de ticket médio com pilha de valor | Hero · identificação · diagnóstico · custo da inação · revelação · mecanismo · módulos · resultados · depoimentos · reenquadre · oferta · garantia · FAQ · CTA | [desktop](vendas-longa-escura/previa.png) · [celular](vendas-longa-escura/previa-celular.png) |
| [`produto-ebook-violeta`](produto-ebook-violeta/) | Página de produto digital | E-book/guia/iniciação com capa 3D, amostra em abas e capítulos | Topo fixo · hero + capa 3D · reconhecimento · virada · produto · diferencial · jornada · demonstração · capítulos · para quem · entrega · autor(a) · oferta · FAQ · chamada | [desktop](produto-ebook-violeta/previa.png) · [celular](produto-ebook-violeta/previa-celular.png) |

**Fora do acervo, por ora:** vagas/lista de espera (use `captura-workshop-azul` ou `captura-evento-escura` trocando o CTA por "entrar na lista") e página institucional longa de empresa (nenhuma referência de UX resolvida o bastante para entrar).

## Como fazer a página de um cliente (5 passos)

1. **Escolha o molde pelo tipo de página** (tabela acima) e **copie a pasta inteira** para `clientes/<Conta>/NN - web design/<página>/` (ou para o diretório de trabalho do fabricante da página). Nunca edite o molde aqui: ele é fonte.
2. **Troque os tokens.** No `:root` do `index.html`, aponte `--cor-fundo`, `--cor-texto`, `--cor-acento`, `--cor-acento-2`, `--fonte-titulo`, `--fonte-texto` (e os extras do molde) para a identidade do cliente. Se o cliente tem `tokens.css` (em `clientes/<Conta>/NN - identidade visual/tokens.css`), copie-o para junto da página, ligue com `<link rel="stylesheet" href="tokens.css">` antes do `<style>` e referencie: `--cor-acento: var(--cliente-cor-marca); --fonte-titulo: var(--cliente-fonte-titulo);`. Fonte do cliente entra por `@font-face` local (estática, nunca variável).
3. **Troque os placeholders pela copy.** Cada `[PAPEL: dica]` pede o texto daquele papel, no tamanho aproximado. O molde dá a **estrutura e a ordem**; **a copy é nossa**, escrita pela skill de copy da casa (`copywriter-senior-continuum`) e pelas réguas da árvore ESCRITA (`00-core/roteador/ARVORE-ESCRITA.md`): a conta já passou (`PILARES.md`, léxico com fonte `D`), nenhuma cena, dor ou fala sem fonte apontável, promessa/oferta/mecanismo são decisão nossa (REGRA Nº 0). Seção que a oferta não pede se apaga inteira.
4. **Troque imagens e links.** `assets/ph-*.svg` → imagem do cliente na mesma proporção, com `alt` real. `{{LINK_CTA}}`, `{{LINK_WHATSAPP}}`, `{{LINK_PRIVACIDADE}}`, `{{LINK_TERMOS}}`, `{{FORM_ACTION}}` → URL real (busque `{{`). Rastreio, pixel e checkout entram por decisão da conta, nunca copiados de outra página.
5. **Confira no celular** (e no desktop) antes de entregar: abra em largura de 390 px, role a página inteira, teste cada botão, o FAQ/abas/carrossel/quiz do molde e o formulário. Rode `verificar-propagacao.py`. Depois de publicado, a peça é do cliente; o molde continua intacto.

## Regras de manutenção do acervo

- **Molde novo** nasce de uma página que já se mostrou boa (UX resolvido, estática ou fácil de limpar), entra sanitizado: texto vira placeholder, imagem vira SVG cinza local, link vira `#`/`{{...}}`, rastreio/checkout/formulário de terceiro saem, cores e fontes viram variáveis no `:root`. **Nunca com o nome do site de origem**, nem no HTML, nem no README, nem na pasta.
- Antes de qualquer publicação: `python3 -X utf8 40-operacao-rotinas/ferramentas/varrer-publico.py --pasta 90-templates/paginas-referencia` em ✅.
- Defeito de molde se corrige **no molde** (aqui), no mesmo ato, para o próximo cliente não herdar.
- Os moldes `captura-workshop-azul`, `vsl-curta-clara`, `obrigado-passos-escuro` e `quiz-passos-claro` foram **reconstruídos** a partir da estrutura de referências pesadas (CSS de construtor de página); os demais são cópias sanitizadas do layout original.
