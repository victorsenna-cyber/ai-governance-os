> Módulo de referência. Carregar antes de publicar e depois de medir.

# PARTE 6 · Gate de publicação

**Entrada**
- [ ] Classificação nos 4 eixos, escrita.
- [ ] Brief com os 9 campos; nenhum fato inventado; **lacuna de fato virou pergunta ao dono da oferta, lacuna de estrutura virou decisão nossa com a razão junto** (Lei 11-bis).
- [ ] Inventário de provas auditável; zero prova fabricada ou "melhorada".
- [ ] Escassez declarada é verificável no mundo real.

**Mensagem**
- [ ] Teste dos 5 segundos com alguém de fora: o que é, para quem, o que ganha, próximo passo.
- [ ] Título é promessa de estado, específica, sem superlativo.
- [ ] Sobretítulo qualifica o público na primeira dobra.
- [ ] As 12 perguntas têm resposta, na ordem, e nada na página está fora delas.
- [ ] Correspondência de mensagem com a origem do tráfego, em palavras.

**Tensão**
- [ ] A dobra de custo existe e tem peso.
- [ ] Nenhum trecho com 2 telas ou mais sem CTA.
- [ ] Clímax visual coincide com a oferta ou com o fecho, e é único.
- [ ] Fecho ecoa o título uma oitava acima.
- [ ] Curva numerada sem três dobras iguais seguidas.

**Crença**
- [ ] Mapa de quitação preenchido: toda promessa forte tem prova nomeada a no máximo 1 dobra.
- [ ] Saldo do extrato maior ou igual a zero na entrada da oferta, lido dobra a dobra.
- [ ] Qualificação inclui "para quem NÃO é".
- [ ] Foto real de quem conduz com credencial concreta, ou seção movida para depois da oferta.

**Valor e oferta**
- [ ] Pilha tangível antes do preço.
- [ ] Ancoragem honesta; escassez real com motivo; zero contagem falsa.
- [ ] Reversão de risco colada no CTA; se condicional, condições mensuráveis e cobertas em contrato.
- [ ] Uma decisão por bloco.
- [ ] Mecânica conferida contra o tipo de oferta e o ato de conversão.
- [ ] Objeções cobrem tempo, "já tentei", risco e a objeção identitária.

**Atrito, as 4 famílias**
- [ ] Cognitivo: nenhuma frase que precise ser relida; informação na dobra da pergunta certa.
- [ ] Decisório: um primário por tela; nenhuma escolha dupla no mesmo bloco.
- [ ] Sensorial e técnico: primeira dobra inteira no primeiro paint; vídeo sem som automático; legendas.
- [ ] Confiança: números batem entre dobras; promessa do título igual à promessa da oferta.

**Integridade**
- [ ] Mobile testado em aparelho real.
- [ ] Contraste AA, foco visível, teclado funciona, movimento reduzido respeitado.
- [ ] Medição instalada e conferida.
- [ ] Zero placeholder visível.
- [ ] Gate da skill de copy aprovado. Gate da skill de ui-ux aprovado.
- [ ] Aprovação humana registrada.

**Classificação de achado:** P0 impede a publicação (mentira, prova inventada, escassez falsa, promessa acima da capacidade, quebra de acessibilidade que bloqueia uso, placeholder no ar). P1 corrige antes do tráfego pago. P2 entra na fila de otimização.

---

# PARTE 7 · Medição e diagnóstico

## 7.1 Instrumentação padrão

Mesmos nomes em toda página, para poder comparar entre páginas:

- `view_dN` — fronteira de cada dobra atingida, por dobra e não por porcentagem.
- `cta_click_{origem}` — clique por porta. Qual porta converte importa mais que quantas.
- `faq_open_{n}` — abertura por pergunta.
- `video_play` e `video_50`, se houver vídeo.
- `checkout_start` e `purchase`, ou `form_start`, `form_submit`, `call_booked`.

Tempo na dobra de oferta e gravação de sessão completam o quadro.

## 7.2 Árvore de diagnóstico

| Sintoma | Onde olhar | Primeira correção |
|---|---|---|
| Abandono alto abaixo de 10 segundos | primeira dobra, correspondência de mensagem | reescrever a promessa com as palavras da peça de origem; teste dos 5 segundos |
| Scroll morre na fronteira espelho e custo | espelho genérico | trocar conceito por cena; léxico do brief, não da persona imaginada |
| Scroll morre no mecanismo | D4 | menos passos, mais resultado parcial; o currículo virou atrito |
| Scroll alto e clique baixo | crença, saldo negativo | prova vizinha das promessas maiores; garantia mais visível |
| Tempo alto na oferta sem clique | D8 | recapitular valor antes do preço; uma decisão por bloco; âncora honesta |
| Clique alto e venda baixa | checkout ou handoff | continuidade visual, campos a menos, meios de pagamento. A página não é a ré |
| Uma pergunta do FAQ aberta por mais da metade | objeção central mal alocada | promover a resposta a bloco no corpo da página |
| Converte no quente e não no frio | modulação ignorada | versão fria completa: espelho e custo vívidos, prova cedo |

## 7.3 Ordem de otimização
Primeira dobra, depois oferta, depois prova, depois cadência de CTA, depois o resto. Nunca otimizar a qualificação antes da primeira dobra.

## 7.4 Protocolo de teste
Um teste por vez, com hipótese escrita ("mudar X move Y porque Z") e critério de parada definido ANTES, para a ansiedade não decidir no meio. Sem tráfego para testar: aplicar o padrão e coletar dado qualitativo, porque cinco entrevistas valem mais que opinião interna. Resultado de teste, ganho ou perda ou empate, volta para esta skill como regra nova, exceção documentada ou anti-padrão promovido.

---

# APÊNDICE · Anti-padrões

Sinais de página que saca em vez de depositar. Nenhum passa no gate.

1. Primeira dobra centralizada clichê, título mais subtítulo mais dois botões, com carrossel.
2. Promessa absoluta.
3. Contagem regressiva falsa, escassez sem motivo, "mais vendido" em lote temporal.
4. Preço antes do valor; número sem pilha.
5. Deserto de CTA, com 3 telas ou mais sem porta, ou floresta de CTA, com 3 portas por tela.
6. Depoimento sem nome, elogio vago, logo sem relação com o ICP.
7. Imagem de banco genérica, imagem sintética apresentada como foto, emoji como ícone, um ícone decorativo por item.
8. Efeito visual da moda aplicado em tudo; animação que atrasa o valor.
9. Parede de texto sem hierarquia, ou fragmentação total com negrito em tudo.
10. FAQ de marketing.
11. Placeholder no ar, link quebrado, checkout com outra cara.
12. Página que o próprio dono não mandaria para um amigo sem pedir desculpas.
13. Notificação falsa de compra e contador de visitantes inventado.
14. Interrupção que sequestra a leitura antes do espelho: a página interrompendo a própria venda.
15. Seção institucional autobiográfica no meio da subida. Biografia serve à prova, nunca ao ego.
16. Duas ofertas diferentes na mesma página. Página de vendas tem UM destino; o resto é funil.
17. Texto com cheiro de máquina: tríades genéricas, simetria perfeita de itens, adjetivos em fila.
18. Curva plana: dez dobras com a mesma altura emocional e o mesmo peso visual. Página sem pico projetado é catálogo com botão.

---
