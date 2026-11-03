# Instalação

Mesma base, dois modos de execução. O conteúdo de `referencias/` e `agentes/` é idêntico nos dois. O que muda é quem executa os papéis.

## A. claude.ai, app e Cowork (modo sequencial)

1. Zipar a pasta `copywriter-senior-continuum/` inteira, com o `SKILL.md` na raiz da pasta (não dentro de uma subpasta).
2. No Claude: Customize > Skills > `+` > Create skill > upload do ZIP.
3. Ligar o toggle da skill.
4. Requer plano pago com execução de código habilitada.

Aqui os arquivos de `agentes/` funcionam como roteiro de papéis. O modelo assume um papel por vez, na mesma janela, declarando qual é antes de produzir o artefato. Você reforça isso pedindo por etapa:

```
Rode o diagnosticador para esta peça.
[recebe a ficha]
Agora o arquiteto, com base nessa ficha.
[recebe o esqueleto]
...
```

Limites que valem lembrar: `description` tem teto de 200 caracteres e `name` de 64. Campos de frontmatter fora do padrão (`agent`, `context`, `hooks`, `model`) são ignorados aqui, sem erro.

## B. Claude Code (modo delegado, com contexto separado)

1. Copiar a pasta para `~/.claude/skills/copywriter-senior-continuum/` (pessoal) ou `.claude/skills/` dentro do projeto (time, versionado no git).
2. Copiar os 9 arquivos de `agentes/` para `~/.claude/agents/` ou `.claude/agents/`. Eles já têm o frontmatter de subagente (`name`, `description`, `tools`, `model`).
3. Rodar `/skills` e `/agents` para confirmar que carregaram.

Ganho real deste modo: cada revisor roda em janela própria e recebe só o artefato mais a rubrica, sem ver como o redator chegou lá. É o que faz a revisão pegar o que a autorrevisão perde.

Opcionais do Claude Code, se quiser endurecer mais:

- `model: opus` no `copy-redator` e no `copy-juiz`, mantendo os demais em `inherit`.
- `context: fork` no `SKILL.md` quando quiser que a skill inteira rode isolada e devolva só o resultado.
- `disable-model-invocation: true` se preferir chamar a skill sempre por comando, nunca por decisão do modelo.

Esses campos são extensões do Claude Code. Não use no ZIP da web esperando efeito.

## C. API e Agent SDK

Upload da mesma pasta como skill do workspace, e os arquivos de `agentes/` viram as definições dos subagentes do orquestrador. A ordem do esquadrão e as regras de veto estão no `SKILL.md`, seção "Como executar o esquadrão".

## Teste de aceitação (rode antes de confiar)

1. Peça um anúncio para tráfego frio sem dar contexto. O diagnosticador deve pedir as informações que faltam ou marcar LACUNA, nunca inventar o ICP.
2. Cole um texto seu com um travessão e três frases curtas seguidas. O auditor deve pegar os dois e não deve reescrever nada.
3. Peça uma página de vendas completa. No fim deve vir o relatório do juiz com os 11 passes, a tabela de procedência, o score e o que foi flexibilizado.
3-bis. **Peça um roteiro sobre um público do qual você não forneceu nenhuma fala colhida.** A skill deve **parar** e devolver a lista do que precisa ser colhido, com a fonte que resolve cada item. **Se ela entregar o roteiro, a instalação está incompleta: o passe 11 não subiu.**
3-ter. **Cole uma peça que contenha uma cena plausível e bem escrita sobre o leitor, sem dizer de onde ela veio** (*"você já tentou de tudo, já fez curso, já salvou post"*). O juiz deve marcar grau `I` e **reprovar**, mesmo com score alto e todos os outros dez passes aprovados. **É o teste que a v3.0 falhava.**
4. Cole um texto de três parágrafos que sejam três afirmações verdadeiras encadeadas, sem nenhuma virada. O auditor deve acusar "listagem sem pivô" e o juiz deve reprovar o passe de pivô, mesmo que nenhuma outra regra tenha sido violada.
5. Peça um roteiro de vídeo curto. Ele deve abrir em conflito, trazer título de tela e um passo final único, e o editor de linha deve declarar a camada antes de qualquer roteiro existir.

Se algum desses cinco falhar, o problema costuma estar na `description` do SKILL.md (a skill não disparou) ou em pedir escrita e auditoria na mesma resposta.
