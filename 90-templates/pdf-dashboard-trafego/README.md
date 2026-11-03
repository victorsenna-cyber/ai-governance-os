# PDF dashboard de tráfego: resultado fixo de campanha em uma página

> **Tipo:** blueprint · 🟡 provisório desde 27/10/2026 · criado a pedido do {{OPERADOR}}: um PDF no estilo do dashboard, com os resultados fixos das campanhas de uma conta, mais dados e menos headline, salvo como modelo.
> **Exemplar:** um relatório de resultado de teste de campanha (a estrutura dos dados em `exemplo.json`).

## O que é

Um PDF A4 deitado, de uma página só, com o resultado **fechado** de uma ou mais campanhas, no visual do painel de resultado (`40-operacao-rotinas/ferramentas/painel-resultado/`): fundo quase preto, azul petróleo, ciano como único destaque, Plus Jakarta Sans e o logo da casa. **Mostra dados, não tem título nem frase de venda.** Para enviar ao cliente o fechamento de um teste ou de um ciclo. A leitura viva continua sendo o painel.

| Bloco | Conteúdo |
|---|---|
| Topo | logo + três chips (cliente · produto, canal, período e estado) |
| 6 números | investido (sobre a verba) · **conversas** · **custo por conversa** (os dois em destaque) · impressões com CPM · visitas ao perfil com custo por visita · seguidores |
| 2 gráficos | conversas acumuladas (barras, a última em destaque) · custo por conversa acumulado (linha). Eixo único, valor escrito em cada ponto, porque PDF não tem passar o mouse |
| Tabela | por campanha: investido, conversas, custo/conversa, CPM, impressões, alcance, frequência, visitas, seguidores, conversas por mil impressões. Com mais de uma campanha, a linha de total |
| Nota | a fonte, a data da leitura e o que precisa de ressalva |

## Como gerar

1. Copiar `exemplo.json` para `clientes/<Cliente>/NN - tráfego pago/relatorios/<NOME>.json` e preencher:
   - `campanhas[]`: o Gerenciador de Anúncios na data de fechamento (gasto, conversas, impressões, alcance, visitas, seguidores; `null` vira "—"). CPM, custo, frequência e taxa **se calculam**, não se digitam. `nome` curto (*Campanha 1*), e o nome técnico fica no `LOG-DECISOES.md`.
   - `serie[]`: o acumulado por dia, de **gasto e conversas** (as leituras do `painel.json` do cliente servem; o último ponto é o fechamento).
   - `chips`, `periodo`, `verba`, `nota`, `arquivo` (`saida` é opcional: subpasta de destino).
2. `python3 90-templates/pdf-dashboard-trafego/gerar_dashboard.py "<caminho do .json>"` → `.html`, `.pdf` e `.png` (prévia) ao lado do JSON. Imprime pelo Chrome headless.
3. **Abrir a prévia e olhar** antes de enviar: número cortado, texto quebrando, eixo.

O visual mora em `estilo.css`. Mudou o estilo, muda aqui, nunca no HTML de um cliente.

## Regras

- **Só número com fonte.** Cada número sai do Gerenciador ou do `painel.json`, e a nota diz de onde e de quando.
- **Vendas só entram com dado confirmado** pelo cliente ou lançado no painel. O print do Gerenciador não traz venda; se não houver venda confirmada, o PDF sai sem ela e isso se diz a quem pediu.
- Soma de alcance entre campanhas vai com a ressalva de sobreposição na nota.
- Material que sai da casa: só vai para cliente (regra das classes de PDF, `90-templates/pdf-noturno/README.md` §3-bis).

🔴 **Veto:** número sem fonte declarada na nota · venda ou faturamento sem confirmação · título, headline ou frase de venda no lugar de dado · eixo duplo · CSS próprio por cliente.

## Modo genérico, fontes e conferência *(01/11/2026)*

- **Dois modos no mesmo gerador.** Com `campanhas` e `serie` no JSON, é o modo de campanha de sempre, com os números calculados. Com `kpis`, `graficos` e `tabela`, é o **modo genérico**: seis números, dois gráficos (`barras` ou `linha`) e uma tabela, com rótulos e valores prontos no JSON. O visual é o mesmo.
- **Exemplar do modo genérico:** `exemplo/EXEMPLO-DASHBOARD.json` e o PDF ao lado, com dados dos próprios PDFs da casa.
- **Fontes estáticas em `fontes/`, embutidas no HTML.** A Plus Jakarta Sans pelo link do Google é variável e saía Type3: um PDF real saiu cheio de fontes Type3. Regenerado com o gerador novo, saiu com o mesmo texto, o mesmo desenho e nenhuma Type3.
- **Conferência no próprio gerador:** reprova, com código 1, fonte Type3 ou mais de uma página. Foi ela que pegou o exemplar vazando para a segunda página.
