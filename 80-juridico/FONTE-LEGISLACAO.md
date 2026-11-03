# FONTE DE LEGISLAÇÃO — o acervo `leis-main`

> **Tipo:** fonte externa (referência; não é método nem gate) · **Acervo opcional, instalado fora do repositório.** Sem ele, as árvores JURÍDICO e ESCRITA seguem funcionando: a conferência de lei passa a ser feita no link oficial.
> **Para que serve:** um repositório com as leis do Brasil em Markdown, no mapa para uso em criações, ads, contratos e mais.

## 1. Onde está

Numa pasta de repositórios de apoio à sua escolha, **fora da Governança** (ex.: `<pasta-de-repositórios>\leis-main\`). Registre aqui o caminho depois de instalar.

🔴 **Fica fora da Governança e não é copiado para dentro dela.** São mais de 323 mil normas; uma cópia aqui dentro quebraria o git e o `sincronizar.py`. A Governança só aponta para ele.

## 2. O que tem

| Pasta | Conteúdo |
|---|---|
| `constituicao.md` | Constituição Federal, texto vigente |
| `federal/leis-ordinarias/AAAA/` · `leis-complementares/` · `decretos-lei/` · `leis-delegadas/` | normas federais, de 1822 até hoje |
| `estaduais/UF/` · `municipais/UF/<municipio>/` | direito estadual, distrital e municipal (a cobertura está em `COBERTURA.md`) |
| `reguladores/<orgao>/` | atos infralegais: ANVISA, ANS, BCB, CVM, CONTRAN, conselhos profissionais e outros |
| `jurisprudencia/<tribunal>/` | súmulas e temas vinculantes: STF, STJ, TST, TNU e outros |
| `tratados/` | tratados internalizados |

🔴 **O que NÃO está aqui:** o CONAR (é autorregulamentação, não lei) e as políticas de anúncio da Meta e do Google. Peça de anúncio confere essas três fontes por fora.

## 3. Como buscar

- **Pelo número:** o arquivo se chama `lei-<numero>-<data>.md`. Exemplo: `federal/leis-ordinarias/2006/lei-11343-2006-08-23.md`.
- **Pelo artigo:** grep no arquivo (`"Art. 23-A"`, `"§ 9º"`). **Nunca rodar grep na raiz inteira**: a varredura completa passa de 2 minutos. Restrinja à esfera e à pasta.
- **Cabeçalho YAML de cada norma:** `titulo`, `tipo`, `data`, `ementa`, `revogada`, `versao_texto` (compilada = texto vigente), `urn`, `fonte` (link oficial) e `baixado_em`.

## 4. Regra de uso

1. **Citação de lei numa peça ou num documento leva a URN e o link `fonte` do cabeçalho.** Ninguém cita de memória.
2. **Conferir `revogada: false` e `versao_texto: compilada`** antes de usar.
3. **O aviso do próprio acervo:** o texto não substitui o Diário Oficial, é conversão automática ou OCR, e é uma foto da data de `baixado_em`. Para pesquisar, criar e conferir uma peça, o acervo basta. **Para contrato, notificação ou peça jurídica, confere-se o artigo no link oficial.**
4. O acervo não é atualizado sozinho. Para atualizar: `git pull` dentro da pasta, quando houver remoto, ou baixar de novo a versão nova.

## 5. Quem usa e quando (rota nas árvores)

- **JURÍDICO** (`00-core/roteador/ARVORE-JURIDICO.md`): é a fonte do texto de lei em contratos, LGPD e disputas.
- **ESCRITA** (`00-core/roteador/ARVORE-ESCRITA.md`): anúncio, página, VSL ou roteiro que toque assunto regulado confere a lei antes de publicar. Exemplos de assunto regulado: saúde, dependência química, medicamento, alimento, crédito e investimento, promessa de resultado, dado pessoal.

## 6. Exemplo de uso

Antes de publicar peça ou plano que toque assunto regulado, confira a norma no acervo: abra o arquivo da lei pelo número, localize o artigo (`grep` restrito à pasta), confirme `revogada: false` e `versao_texto: compilada`, e cite com a URN e o link `fonte` do cabeçalho. Registre no plano ou na peça o artigo conferido, a data de `baixado_em` e a consequência para a oferta. Primeiro uso real do acervo na sua operação: registre aqui a data, a norma e a peça.
