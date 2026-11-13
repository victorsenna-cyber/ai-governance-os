# Laya x árvore do roteador

O que é: teste de bancada para ver se o Laya 0.4.12 (checkpoint `multilingual`, CPU) decide a ÁRVORE
de um pedido (NEGOCIO, CONTA, LEITURA, ESCRITA, OPERACAO, CASA, JURIDICO), primeira decisão do `CLAUDE.md` §6.
Não está roteado nem em produção: é medição. Nada aqui altera o roteador.

Como rodar (python do venv; offline, usa o cache do modelo numa pasta `laya-teste` fora da Governança):
`<pasta laya-teste>\.venv\Scripts\python.exe -I avaliar.py` (zero-shot, ~2 min)
`... avaliar.py --treinar --epocas 2` (fine-tune em CPU, limite de 25 min de relógio, ~20 min)

O que mede: gera `dados/` (frases-sinal das 7 `ARVORE-*.md` + coluna "O pedido é sobre" do §6; 80/20 estratificado,
semente 42), acurácia zero-shot com as 7 descrições como opções, matriz 7x7, latência, estabilidade (ordem invertida),
e o mesmo depois do treino. Saída completa em `dados/resultado.json`; tabelas em `RESULTADO-<data>.md`.

Resultado de referência (prova da ordem de uma centena de frases): zero-shot no nível da classe majoritária, pouco acima do acaso; parcela grande das respostas muda
ao inverter as opções. Treinado poucas épocas (menos de meia hora): melhora, mas segue longe do necessário e quase tão instável. Não serve para rotear.
O modelo treinado (1,36 GB, >500 MB) fica fora do repositório, na pasta `laya-teste`.

## Frente 2: o leitor do estado do cliente no onboarding (experimento reprovado)

Depois de tirado do roteador, o Laya foi testado noutro uso: ler cada mensagem do cliente e responder quatro perguntas
fechadas (falou de valor, temperatura, cobrou promessa, pediu algo), para alimentar a saúde e os alertas do
`METODO-ONBOARDING-ORQUESTRADO.md`. O desenho: conjunto montado das capturas de WhatsApp, rótulo inicial por modelo barato,
conferência humana de uma amostra de 50 (corte de 85% de acerto por pergunta, contando a ordem invertida) e, como teste que
decide, uma conta deixada fora do treino cuja renovação foi recusada: o modelo precisava ver o esfriamento antes da recusa.

**Resultado: reprovado.** Treinado, só 8 a 9% do que o modelo marca como "esfriando" está certo, e na conta de teste ele não
mostra subida antes da recusa. O sinal está no ritmo e não no tom: a queda de volume de mensagens do cliente (a média das
últimas 3 semanas cai abaixo da metade da média das 3 anteriores, com base mínima semanal) e a mensagem do cliente sem
resposta nossa. Os dois se medem com código, sem modelo (`onboarding_regras.py` e `sem_resposta.py`). Os scripts do
experimento dependem de capturas de contas reais e ficam na casa; o método que sobrou é este: **sinal de risco de cliente
se mede em ritmo e em resposta pendente, não em classificação de tom**.
