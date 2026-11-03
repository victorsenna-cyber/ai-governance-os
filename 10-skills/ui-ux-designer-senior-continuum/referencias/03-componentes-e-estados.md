> Módulo de referência. Carregar ao desenhar ou documentar componente.

# PARTE 3 · Componentes e estados

## 3.1 A matriz de estados (obrigatória)

**Componente sem estado é metade de um componente.** Todo elemento interativo é entregue com esta matriz preenchida ou não é entregue.

| Estado | Quando | O que muda | Erro comum |
|---|---|---|---|
| **Repouso** | padrão | a forma base | nenhum |
| **Sobre** | ponteiro em cima | uma mudança clara e barata: elevação, superfície, borda | mudar tamanho e empurrar o layout |
| **Foco** | teclado ou leitor de tela | anel de foco visível, com contraste próprio | remover o contorno padrão sem colocar outro. É a falha de acessibilidade mais comum que existe |
| **Ativo** | no instante do clique ou toque | resposta imediata, sub-100ms | não ter, e o usuário clicar duas vezes |
| **Desabilitado** | ação indisponível | aparência atenuada mais o motivo dito por perto | desabilitar sem dizer por quê |
| **Carregando** | ação em curso | indicação no próprio elemento, largura preservada | o botão encolher e o layout pular |
| **Erro** | falhou ou inválido | sinal, mensagem específica e o caminho de saída | mensagem genérica do tipo "algo deu errado" |
| **Vazio** | não há dados ainda | explicação do que é e a primeira ação | tela em branco |

**Regra do foco:** anel de foco visível é inegociável. Se a direção de arte não gosta do padrão do navegador, desenhe um melhor. Remover sem substituir reprova a entrega inteira.

## 3.2 Ação principal

- **Um primário por tela.** Secundários são discretos: contorno ou apenas texto, e nunca competem em cor ou peso.
- **Rótulo em primeira pessoa e específico.** "Quero meu diagnóstico" vence "Enviar". Nunca "Saiba mais" ou "Clique aqui".
- **O mesmo verbo do topo ao fim da página.** Trocar o verbo no meio quebra o trilho mental do compromisso.
- **Microcopy embaixo do botão** é o texto mais lido depois do título: desarma a última objeção (garantia, tempo, "sem cartão").
- **Alvo de toque de no mínimo 44 por 44**, com espaçamento suficiente entre alvos vizinhos.
- **Largura:** no celular, ação principal em largura total ou quase. Botão pequeno centralizado é o gargalo mais bobo que existe.

## 3.3 Campo e formulário

- **Rótulo sempre visível.** Rótulo que só existe como texto interno some quando a pessoa começa a digitar, e ela esquece o que estava preenchendo. Usar rótulo acima do campo.
- **Cada campo a mais é atrito.** Pedir só o que o próximo passo exige de fato.
- **Validação no momento certo:** verificar quando o campo perde o foco, não a cada tecla. Mensagem específica, do lado, dizendo como corrigir.
- **Erro não é só cor.** Sinal, texto e ícone juntos, porque cor sozinha não é acessível.
- **Ordem de tabulação segue a ordem visual.** Sempre.
- **Ação de envio nunca fica desabilitada em silêncio.** Se falta algo, dizer o que falta.

## 3.4 Bloco de prova

- Foto real, nome, contexto e, quando existir, o número. Depoimento sem identificação é ruído.
- **Hierarquia dentro do bloco:** o resultado em maior peso, a fala em corpo de leitura, a identificação em micro.
- Aspas decorativas gigantes competem com a fala. Se a direção pede aspas, elas são estruturais, não ornamento.
- **Nunca:** parede de logos sem relação com o público, avaliação genérica como única prova, rosto de banco de imagem.

## 3.5 Bloco de oferta

- **Uma decisão por bloco.** Se há plano, período e complemento para escolher, sequenciar em passos, nunca empilhar no mesmo cartão.
- **Um item aceso.** O recomendado ou vigente recebe o único tratamento de destaque; os outros são contexto.
- **O número precisa ser legível de relance:** variante tabular, peso alto, nenhum efeito por cima.
- **Reversão de risco colada na ação**, não no rodapé do bloco.
- **Proibido:** contagem regressiva sem prazo real, preço riscado inventado, selo de "mais escolhido" em opção que muda por data.

## 3.6 Acordeão e conteúdo colapsado

- Fechado por padrão, com a pergunta legível e completa.
- Área clicável é a linha inteira, não só a seta.
- Estado aberto e fechado distinguível sem depender de cor.
- Nunca esconder atrás de acordeão informação de que a decisão depende. Acordeão é para resíduo, não para o essencial.

## 3.7 Documentação de componente

Todo componente novo entra no sistema com esta ficha. Se não está documentado, não existe.

```
COMPONENTE:      [nome]
FUNÇÃO:          [o que resolve, e quando NÃO usar]
VARIANTES:       [nome -> quando usar]
TAMANHOS:        [se aplicável]
ESTADOS:         [matriz da §3.1 preenchida]
TOKENS USADOS:   [cor, espaço, tipo, raio, elevação]
ACESSIBILIDADE:  [papel semântico · teclado · como o leitor de tela anuncia]
FAZER / NÃO FAZER: [uma linha cada]
```

## 3.8 Princípios do sistema

1. **Consistência acima de criatividade dentro do sistema.** O sistema existe para ninguém redecidir o óbvio. A criatividade mora na direção de arte, não no décimo botão.
2. **Flexibilidade dentro de restrição.** Componente deve ser componível, não rígido nem infinitamente configurável.
3. **Documentar enquanto desenha.** Documentação adiada é documentação que não acontece.
4. **Mudança que quebra precisa de caminho de migração.** Trocar um token sem avisar onde ele era usado é criar bug visual invisível.

---
