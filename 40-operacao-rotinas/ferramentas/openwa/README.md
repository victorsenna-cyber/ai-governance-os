# Captura de WhatsApp (OpenWA)

**Tipo:** ferramenta · alçada {{OPERADOR}} · 🟡 provisória até a 1ª captura real

> ⚠️ **Ferramenta opcional.** Depende de instalar o motor OpenWA (externo, em Docker) e de usar WhatsApp Business com etiquetas. Sem isso, o repo funciona igual: a conversa entra por registro manual (`CLAUDE.md` §11).

Intenção: o motor roda e o Claude capta os dados das conversas do {{OPERADOR}} para alimentar o repo, em vez de printar, salvar áudios e transcrever à mão a cada vez. A etiqueta é o interruptor (fácil de aplicar a qualquer momento), e há uma pasta com 1 script para cada grupo e cada pessoa individual.

## Como se usa

| Quero… | Faço |
|---|---|
| **pôr uma conversa na captura** | no WhatsApp Business, aplica-se a etiqueta **Cliente**, **Parceiro** ou **Prospect** na conversa (privada ou grupo). A próxima rodada abre a pasta e começa a capturar |
| tirar uma conversa | tira-se a etiqueta. A captura para, e o que já foi capturado fica |
| capturar tudo | `python3 rodada.py` (pelo agendador ou por um atalho seu) |
| capturar uma conversa só | `python3 capturar.py --chat <chatId>` |
| escanear o QR, ver sessões e conversas | o painel do motor OpenWA (`http://127.0.0.1:2785`), instalado fora do repositório |

🔴 As três etiquetas precisam existir no WhatsApp Business, com esses nomes. O motor `whatsapp-web.js` não cria etiqueta, então quem cria é o {{OPERADOR}}, no celular. As outras etiquetas que você usar (lead, follow-up…) **não** entram na captura.

## Onde cai

| Etiqueta | Raiz |
|---|---|
| Cliente | `clientes/<Nome>/` |
| Parceiro | `parceiros/<Nome>/` |
| Prospect | `30-comercial/assessoria-prospects/<nome>/` (minúsculas-com-hífen; a pasta nasce na primeira captura) |

```
<raiz>/<Nome>/
  README.md               só quando a captura abriu a pasta: "conta NÃO aberta"
  01 - contexto/OpenWA/
    texto/    AAAA-MM-DD - <conversa>.md   literal, horário de Brasília, áudio transcrito embutido
    áudios/   WhatsApp Ptt AAAA-MM-DD at HH.MM.SS.ogg  +  .md ao lado  +  README.md (regra de transcrição)
    imagens/  PDF/  html/
    vídeos/  outros/      só quando aparece arquivo desse tipo
    .estado.json          cursor por conversa
```

- **Pasta do contato:** acha a pasta existente pelo primeiro nome (o grupo "<Conta> | {{EMPRESA}}" cai em `clientes/<Conta>/`). Procura primeiro na raiz da etiqueta, depois nas outras. Se houver mais de uma candidata, não chuta: avisa, e o campo `pasta` se preenche à mão no `conversas.json`. Se não houver nenhuma, cria a pasta com o nome do contato. Num grupo, o nome é o que vem antes de `|` ou ` - `, sem "Assessoria".
- **A máquina não abre conta.** A pasta nova tem só o contexto e um README que diz isso. Nada de `STATUS.md` ou `DECISOES.md`: cliente se abre pelo trilho de conta nova, por decisão. A cada rodada, o script lista os clientes que têm conversa e ainda não têm `STATUS.md`.
- **Tipo divergente**, por exemplo etiqueta Cliente numa pasta que mora em prospects: a captura grava na pasta existente e avisa. Promover o contato é decisão, e a pasta se move à mão.
- **A estrutura `OpenWA/` nasce em todo cliente**, a cada rodada. Em parceiro e prospect, só quando há conversa no mapa.
- A pasta de contexto que já existe (`01-contexto`, `01- contexto`, `01-Contexto`) é usada como está. Sem ela, nasce `01 - contexto`. Nada se renomeia.

## Mídia

- **Depois da conexão:** o OpenWA guarda a mídia que chega, e ela baixa direto.
- **Antes da conexão:** a mídia baixa do WhatsApp na hora, mas **só entre as 100 mensagens mais recentes de cada conversa**. É o teto do OpenWA. Mídia mais antiga que isso, grande demais ou expirada no servidor do WhatsApp fica marcada na linha como `[mídia não baixável…]`. O texto da mensagem entra sempre, até 2.000 mensagens por conversa na 1ª rodada.
- **Na prática:** numa conversa curta, quase toda a mídia baixa, com os nomes originais preservados; o que pode faltar é documento grande.
- **Nome dos arquivos:**
  - áudio, imagem e vídeo saem no padrão do export do WhatsApp (`WhatsApp Ptt AAAA-MM-DD at HH.MM.SS.ogg`);
  - documento sai com o nome original (`AAAA-MM-DD at HH.MM.SS - <nome original>.m4a`);
  - documento de áudio vai para `áudios/`, mas **não** é transcrito: só nota de voz e áudio de conversa são.
- 🔴 Um áudio já transcrito à mão em outra pasta da conta é reconhecido pelo nome, e a transcrição antiga é **copiada**, nunca movida (função `ja_transcritos`). O `transcrever-audio.py` sozinho faria `git mv` dela e quebraria as destilações que citam aquele caminho.

## Mapa (`conversas.json`)

O mapa é gerado e mantido pelo script. Mexer à mão só em três casos:
- `pasta` de uma conversa ambígua;
- uma conversa sem etiqueta que precisa entrar (`origem: manual`), por exemplo o 2º número de um mesmo cliente;
- os nomes das etiquetas, em `etiquetas`.

Campos de cada conversa: `chatId` · `relacao` (cliente, parceiro ou prospect) · `pasta` · `nome` (aparece no arquivo de texto e como autor das mensagens da outra ponta) · `tipo` (grupo ou privada) · `origem` (etiqueta, manual ou manual+etiqueta) · `ativa`. Uma conversa manual com só o campo `busca` (o nome no WhatsApp) recebe o `chatId` sozinha na próxima rodada.

## Comandos

| Comando | O que faz |
|---|---|
| `python3 rodada.py --espaco 30` | **a rotina**: uma conversa por vez, cada uma num processo `capturar.py --chat` próprio, 30 s entre elas; para em 2 falhas seguidas; relatório em `tarefas/log/CAPTURA-*.md`; `--max N`, `--so "<Pasta>"`, `--lista <json>`, `--dry-run`. É o que a task diária de captura roda (`tarefas/README.md`). |
| `python3 capturar.py` | captura **só o que é novo** nas conversas do mapa e transcreve (é o que o botão roda). Conversa sem atividade depois do cursor não é lida; as outras, no máximo as últimas 50 mensagens |
| `python3 capturar.py --chat <chatId>` | só uma conversa (é o que os scripts de `por-conversa/` rodam) |
| `python3 capturar.py --chat <chatId> --historico` | histórico fundo (até 2.000 mensagens) **de uma conversa só**. Nunca sem `--chat` |
| `python3 capturar.py --help` | mostra o uso e não lê nada. Argumento desconhecido também não lê nada |
| `python3 capturar.py --so "<Pasta>"` | só as conversas de uma pasta |
| `python3 capturar.py --mapa` | só lê as etiquetas e atualiza o mapa, as pastas, os scripts e a chave do MCP |
| `python3 capturar.py --listar` | conversas da sessão, com id, tipo e última atividade |
| `python3 capturar.py --estrutura` | só cria a estrutura `OpenWA/` em todos os clientes |
| `python3 capturar.py --desde AAAA-MM-DD` | na 1ª captura de uma conversa, não volta antes dessa data. ⚠️ O que ficar antes não é capturado depois |
| `python3 capturar.py --sem-transcrever` | baixa os áudios e deixa a transcrição para a próxima rodada |

## Motor e chaves

- **OpenWA** instalado fora da Governança, em pasta isolada à sua escolha (nunca dentro do repo): Docker, `whatsapp-web.js`, porta só em `127.0.0.1:2785`. No `.env` local:
  - `CHAT_HISTORY_MEDIA_BUDGET_BYTES` em 100 MiB;
  - limites de requisição altos, porque só a máquina local chega lá. Com os limites padrão, a 1ª carga esbarrava no 429.
- 🔴 **O motor não vem com o repositório.** Sem ele instalado e ligado, `capturar.py` só devolve erro de conexão. **App OpenWA (opcional):** um atalho que liga o Docker e o container e abre o painel já logado, na pasta de instalação do motor. Ao fechar, o OpenWA continua rodando, para a sessão do WhatsApp ficar conectada.
- **Chave do script:** `OPENWA_KEY` no ambiente, ou `data/.api-key` (admin). O script só lê as conversas do mapa. A chave limitada por conversa não abre a rota de mídia, por isso não serve aqui.
- **Chave do Claude (MCP):** viewer, limitada às conversas ativas do mapa (`allowedChats`), em `data/.mcp-key.json`. O script cria e atualiza essa chave a cada rodada.
- Todas as chaves ficam fora do repositório.

## 🔴 Leitura leve (alçada {{OPERADOR}})

Regra: não se captura tudo de todas as mensagens a cada rodada. O script lê só o que é novo.

**O motivo da regra:**
- Numa versão anterior, o script não conhecia `--help`: ignorava o argumento e fazia uma **rodada completa**, com todas as conversas do mapa.
- As conversas nunca capturadas eram lidas com `deep=true` até 2.000 mensagens, e a mídia baixada em janelas crescentes (20, 40… 100), que rebaixavam os mesmos arquivos.
- **Esse volume de leitura pode interromper a conexão do WhatsApp, e aí é preciso abrir o WhatsApp no celular para restabelecê-la.**
- **A conduta:** não se roda script de rede com argumento que não se sabe se existe. Um `--help` em script sem `argparse` é um comando executado, não uma consulta. Antes de rodar, lê-se o cabeçalho do script.

**O que mudou no `capturar.py`:**

| Antes | Agora |
|---|---|
| argumento desconhecido era ignorado e a rodada seguia | argumento desconhecido **para tudo antes de ler**; `--help` mostra o uso |
| toda conversa do mapa era lida a cada rodada | só é lida a conversa com atividade depois do cursor (última atividade da lista de conversas) |
| 1ª captura: até 2.000 mensagens com `deep=true` | 1ª captura: as últimas 50. O resto, só com `--chat <id> --historico`, uma conversa por vez |
| mais de 100 mensagens desde o cursor: busca funda automática | lê as últimas 50 e **avisa a lacuna** com o comando para completar |
| mídia em janelas de 20 a 100 | uma janela só, do tamanho das mensagens novas |
| conversas lidas em sequência, sem pausa | 3 s entre conversas; **2 falhas de conexão seguidas param a rodada** |

**Efeito:** as conversas já capturadas têm cursor. A próxima rodada lê só o que chegar depois dele.

## Limites

- O WhatsApp derruba o aparelho conectado depois de cerca de 14 dias sem conexão. Aí é preciso escanear o QR de novo, no app.
- Se o celular pedir passkey ao conectar, nenhum dos dois motores completa a conexão.

## 🔴 Veto

- envio de mensagem, ou escrita de etiqueta ou de conversa, por esta ferramenta ou pelo MCP;
- chave do OpenWA dentro da Governança;
- conversa pessoal, ou de terceiro fora da operação, no mapa;
- editar o texto capturado (a leitura vai em outro arquivo, que aponta para este);
- tratar a captura como destilação (destilar continua sendo `METODO-DESTILACAO-DE-CALLS.md`);
- a máquina abrindo conta, ou promovendo prospect a cliente.
