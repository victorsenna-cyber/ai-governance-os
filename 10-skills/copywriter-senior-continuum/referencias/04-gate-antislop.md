> Módulo de referência. Carregar no passe 7 (humanização) e em qualquer revisão de texto pronto.

# PARTE 6 · Gate de humanização (anti-slop)

Não é blocklist cega. É julgamento: cortar o que é tell, preservar o que é humano.

## O que cortar

**Frases-tell**
- Aberturas de pigarro: "vamos lá", "antes de mais nada", "é importante notar que", "olha, a verdade é que".
- Bajulação e servilismo: "Ótima pergunta!", "Com certeza!", "Você está certíssimo".
- Fechamentos genéricos otimistas: "o futuro é promissor", "rumo à excelência", "tempos empolgantes".
- Meta-comentário: "espero que ajude", "quer que eu detalhe?", "sem mais delongas".

**Padrões estruturais**
- **Listagem sem pivô (o tell estrutural mais caro).** Parágrafos encadeados por acúmulo: uma coisa verdadeira, mais outra, mais outra, sem nenhuma virada. Tudo correto, nada move. É a assinatura estrutural da IA e não aparece em varredura de palavra, só em leitura de arco. *Detecção:* troque a ordem de dois parágrafos do meio. Se nada quebra, não há pivô. *Devolução:* apontar onde falta o "Mas" e qual fato ele precisaria carregar (módulo 01, §2.4-bis). Não sugerir a frase.
- **Pivô excessivo.** O contrário do anterior: cada parágrafo contraria o anterior. O texto parece brigar consigo e o leitor desconfia. Um pivô-mestre por peça.
- **"Mas" como tique.** A estrutura do pivô é obrigatória; a palavra não. Três ou mais parágrafos abrindo em "Mas", "Porém", "Só que" é cadência de máquina, não ênfase.
- **Regra de três forçada:** "inovação, inspiração e resultados", quando não há motivo real para serem três.
- **Contraste binário batido:** "não é só X, é Y", "não se trata de X, e sim de Y". Ver Parte 9 para a fronteira com o traço 8.
- **Falsos ranges:** "de X a Y" onde X e Y não estão numa escala real.
- **Variação elegante:** trocar sinônimo a cada frase só para não repetir (a empresa, o negócio, a operação, a marca).
- **Aforismo vazio:** "X é a linguagem de Y", "X é a moeda de Z".
- **Hedging excessivo:** "poderia possivelmente talvez". Diga a coisa.

**Tells de estilo**
- **Travessão (—): cortar.** É o tell número 1. Trocar por ponto, vírgula, dois-pontos ou parênteses. Vale também para ` -- `.
- Negrito mecânico em cada termo.
- Title Case em títulos. Usar caixa normal.
- Aspas curvas. Usar retas.

**Ritmo, o tell mais sutil**
- IA escreve tudo no mesmo comprimento. Humano varia: frase curta. Depois uma mais longa, que demora um pouco a chegar onde quer chegar. Misturar.

## O que preservar (sinais humanos, não cortar)
- Detalhe específico e difícil de inventar: um nome, um valor exato, uma referência local.
- Sentimento ambíguo, dúvida honesta ("acho que funciona, mas me incomoda algo aqui").
- Opinião que a gente consegue defender.
- Aside, parêntese genuíno, autocorreção.
- Uma frase curta isolada para dar ênfase. Só vira tell quando vêm várias seguidas, forçando drama.
- 🔴 **Informação. O gate corta enchimento, nunca informação.** Frase curta com substantivo sem dono ("uma situação", "com número") ou verbo sem como ("trabalho isso", "te devolvo o que apareceu") é deleção, e deleção tira a especificidade da peça. **Na tese, no mecanismo e na oferta, cada substantivo e cada verbo responde o quê, quem, quando e como.** Se a resposta existe na fonte, entra. Se não existe, vira pergunta de fato a quem tem o dado, e o trecho fica marcado até a resposta chegar; cortar a frase não resolve. A omissão segue valendo onde o módulo 07 a autoriza: na cena que o leitor completa com a própria vida e na conclusão que a cadeia deixa sem escrever.

> **Regra de ouro do falso-positivo:** um tell isolado não é nada. É o cluster que denuncia (travessão + regra de três + "vibrante" + conclusão genérica = confissão).

## Calibração por canal
A régua se adapta ao canal.

| Canal | Emoji | Tom | Frase |
|---|---|---|---|
| **WhatsApp (prospecção e venda)** | 1 a 2 por mensagem, ok, humaniza | coloquial, direto, áudio quando der | muito curta, 1 ideia |
| **Proposta e e-mail comercial** | evitar | profissional e humano | média, varia |
| **Post e conteúdo** | conforme linha editorial | autoral, com opinião | varia muito |
| **Roteiro de vídeo curto** | falado, não escrito | conflito na primeira frase | frase de fala, curta |
| **Documento interno** | não | neutro e claro | direto |

> No WhatsApp, emoji e "oi, tudo bem?" não são slop: são código humano do canal. Não aplicar régua de artigo de enciclopédia a mensagem de WhatsApp.

## Voz Continuum (default quando não há amostra)
Direta, sem rodeio, sem bajulação. Confiante sem arrogância. Linguagem em "nós". Reconhece o que não sabe. Frase que respira. Sem jargão de consultoria vazio. Havendo amostra aprovada nossa ou do cliente, espelhar a amostra em vez do default.

## Score de saída (1 a 10 por dimensão)

| Dimensão | Pergunta |
|---|---|
| Diretividade | É afirmação ou anúncio do que vai dizer? |
| Ritmo | Varia ou é metrônomo? |
| Confiança | Respeita a inteligência de quem lê? |
| Autenticidade | Soa humano? |
| Densidade | Tem algo cortável? |
| Tensão | Tem pivô apontável, ou é acúmulo de acordos? |

**Abaixo de 42/60, revisar.** Em mensagem direta, priorizar Autenticidade e Diretividade. Em conteúdo e anúncio, Tensão é a dimensão que mais explica peça correta que não performa. Nota 4 ou menos em Tensão reprova sozinha, independentemente da soma: peça sem virada não se conserta com ajuste de frase.

## Loop de humanização
1. Rascunho.
2. Auditar com a pergunta: "o que ainda soa como IA aqui?" Listar os tells restantes.
3. Reescrever. Antes de entregar, varrer por travessão, por regra de três e pela ausência de pivô. Qualquer hit significa que não terminou.
4. **Conferir o que o corte levou junto.** Reler tese, mecanismo e oferta perguntando o quê, quem, quando e como. Texto que ficou mais limpo e menos informativo perdeu na revisão: devolver a informação.

---
