# Instalação

Mesma base, dois modos de execução. O conteúdo de `referencias/` e `agentes/` é idêntico nos dois. O que muda é quem executa os papéis.

## A. Interface de chat e ambientes sem subagentes (modo sequencial)

1. Zipar a pasta inteira, com o `SKILL.md` na raiz da pasta, não dentro de uma subpasta.
2. No app: Customize, Skills, criar skill, upload do ZIP.
3. Ligar o toggle da skill.

Aqui os arquivos de `agentes/` funcionam como roteiro de papéis. O modelo assume um papel por vez, na mesma janela, declarando qual é antes de produzir o artefato. Reforce isso pedindo por etapa:

```
Rode o diretor de arte para este projeto.
[recebe a direção declarada]
Agora o designer de sistema, com base nessa direção.
[recebe tokens e limite de caracteres por bloco]
...depois, com a copy aprovada, o designer de tela.
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

1. Peça uma direção de arte sem dizer nada sobre a marca. O diretor deve fazer as cinco perguntas antes de escolher, e não deve entregar adjetivo solto do tipo "moderno e limpo".
2. Proponha uma direção com tipografia neutra de sistema e gradiente sobre fundo branco. O diretor deve reprovar pela lista de veto.
3. Peça os tokens. Deve vir a tabela de limite de caracteres por bloco junto, medida a partir da escala e da grade.
4. Peça um botão. Deve vir com a matriz de estados completa, incluindo foco, carregando, erro e desabilitado com motivo.
5. Entregue uma tela com texto cinza-claro pequeno. O auditor deve pegar o contraste do microcopy e classificar como crítico ou maior, e não deve sugerir a cor pronta.
6. Peça a implementação. O conteúdo da primeira tela não pode depender de script para existir.

Se algum falhar, o problema costuma estar na `description` do SKILL.md (a skill não disparou) ou em pedir produção e auditoria na mesma resposta.

## Nota de escopo

Esta skill é genérica e portátil por decisão: sem nome de cliente, sem exemplo real, sem caminho de arquivo de nenhum repositório. Todo roteamento (quando ela entra, com quem ela se combina) vive no orquestrador do projeto que a instala, nunca aqui dentro.
