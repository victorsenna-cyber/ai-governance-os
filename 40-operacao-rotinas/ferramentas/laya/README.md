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
