---
name: relatorio-da-operacao
description: "Use quando o dono perguntar como está a operação (hoje, ontem, a semana, uma área: 'e o caixa?', 'o que está parado?', 'o que precisa de mim?') e na rotina do relatório. Lê a foto da operação, escreve por partes e só entrega depois do verificador passar."
procedencia: "Continuum, 31/10/2026. Texto nosso; padrão de interação estudado no mercado, nenhum trecho copiado."
---

# Relatório da operação

## Quando usar

- O dono pergunta: *"como está a operação hoje?"*, *"como foi ontem?"*, *"e o caixa?"*, *"o que está parado?"*, *"o que precisa de mim?"*.
- A rotina do relatório (horário no manual de rotinas da empresa).
- Outro agente pede o estado de uma área para decidir a próxima tarefa.

## De onde vem cada número

**Só da foto da operação mais recente** (o JSON que o leitor da empresa grava; o caminho está no manual de rotinas).

- A foto tem, por item, o valor, a fonte e a hora da leitura. **Você não conta, não soma, não compara e não estima.** Se o número que você quer dizer não está na foto, ele não existe para este relatório: peça ao leitor (o script) que o calcule, ou diga que não leu.
- Foto velha para a pergunta (mais antiga que o limite da área no manual): rode o leitor antes de responder.
- O que entra em **"Precisa de você"** é o que a foto marca em `precisa_de_voce`, que sai das alçadas e das decisões abertas. Não é escolha sua.

## Formato

1. **Abertura, uma linha:** o nome do dono, a hora da leitura e a conclusão. Se há alerta forte (caixa negativo, pagamento grande amanhã, rotina caída), ele vem primeiro.
2. **Uma linha por área**, no formato `Área (fonte, hora): o que aconteceu`. Por dentro da linha, a ordem é: quando · quem viu o quê · quem fez o quê · o efeito. Contador no lugar de prosa (*"respondidas 7, qualificadas 2"*).
3. **Detalhe só do que está fora do normal:** vermelho, vencido, parado. No máximo 3 sublinhas por área.
4. **Pendência humana é estado, com nome:** *"esperando seu áudio"*, *"espera a sua letra"*. Nunca no meio de uma frase.
5. **"Precisa de você:"** lista numerada, agrupada por conta ou assunto, no máximo 5 itens, o mais urgente primeiro, com o código (`D-…`, `T-…`) quando houver.
6. **"Não li:"** as fontes que não responderam, com o motivo. O que não foi lido não é estimado.
7. **Tamanho:** o corpo cabe numa tela de celular, até 12 linhas antes do "Precisa de você".

**Pergunta de uma parte só** (*"e o caixa?"*): responda só aquela linha, mais o que dela está em "Precisa de você", no mesmo formato.

## Regras

- **Algarismo sempre.** Nunca "três".
- **Texto da foto citado vai entre aspas e literal.**
- **Recomendação** cabe em uma frase e se lê como recomendação (*"Ou retomam, ou saem das ativas."*). Nunca decisão em nome do dono.
- **Dado pessoal não entra** (nome de funcionário com problema, salário, documento), mesmo que esteja na foto, salvo se o dono pedir.
- **Sem promessa e sem previsão** que a foto não traga calculada.

## Antes de entregar: o gate

```
python3 ferramentas/verificar_relatorio.py --foto <foto.json> --texto <relatorio.md>
```

- **Só sai com ✅.**
- **Com ❌:** corrija pelo que a foto diz, ou troque o trecho por "não consegui ler".
- 🔴 **Contornar o verificador é falha grave:** número por extenso, número dentro de aspas que não é citação, arredondamento inventado.

## Onde grava

Ao lado da foto: `AAAA-MM-DD-HHhMM-relatorio.md`. Quem envia ao dono (WhatsApp, painel) lê esse arquivo, nunca uma versão que não passou pelo gate.
