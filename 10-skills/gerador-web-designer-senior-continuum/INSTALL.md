# Instalação

Mesma base, dois modos de execução. O conteúdo de `referencias/` e `agentes/` é idêntico nos dois. O que muda é quem executa os papéis.

## A. Interface de chat e ambientes sem subagentes (modo sequencial)

1. Zipar a pasta inteira, com o `SKILL.md` na raiz da pasta, não dentro de uma subpasta.
2. No app: Customize, Skills, criar skill, upload do ZIP.
3. Ligar o toggle da skill.

Aqui os arquivos de `agentes/` funcionam como roteiro de papéis. O modelo assume um papel por vez, na mesma janela, declarando qual é antes de produzir o artefato. Reforce isso pedindo por etapa:

```
Rode o classificador para este pedido.
[recebe a classificação e o brief]
Agora o arquiteto de dobras, com base nesse brief.
[recebe o esqueleto]
Agora o engenheiro de tensão.
...
```

Limites: `description` tem teto de 200 caracteres e `name` de 64. Campos de frontmatter fora do padrão são ignorados aqui, sem erro.

## B. Ambiente com subagentes (modo delegado)

1. Copiar a pasta para o diretório de skills, pessoal ou do projeto.
2. Copiar os 6 arquivos de `agentes/` para o diretório de agentes. Eles já têm o frontmatter de subagente.
3. Confirmar que carregaram.

Ganho real deste modo: cada revisor roda em janela própria e recebe só o artefato mais a rubrica, sem ver como quem produziu chegou lá. É o que faz a revisão pegar o que a autorrevisão perde.

## C. API e SDK

Upload da mesma pasta como skill do workspace; os arquivos de `agentes/` viram as definições dos subagentes do orquestrador. A ordem do esquadrão e as regras de veto estão no `SKILL.md`.

## Teste de aceitação (rode antes de confiar)

1. Peça uma página de vendas sem dar contexto. O classificador deve marcar LACUNA e formular as perguntas ao dono da oferta, nunca inventar ICP, preço ou prova.
2. Descreva uma oferta de ticket alto com compra direta. O classificador deve sinalizar a combinação de risco e propor troca do ato de conversão.
3. Peça o esqueleto de uma página. Nenhum bloco pode existir sem a pergunta do leitor que ele responde.
4. Dê um esqueleto com prova só no fim. O contador de crença deve reprovar por saldo negativo na fronteira da oferta.
5. Peça uma auditoria de página. O caçador de atrito deve devolver achados P0/P1/P2 com o bloco citado, e não deve reescrever nada.

Se algum falhar, o problema costuma estar na `description` do SKILL.md (a skill não disparou) ou em pedir produção e auditoria na mesma resposta.

## Nota de escopo

Esta skill é genérica e portátil por decisão: sem nome de cliente, sem exemplo real, sem caminho de arquivo de nenhum repositório. Todo roteamento (quando ela entra, com quem ela se combina) vive no orquestrador do projeto que a instala, nunca aqui dentro.
