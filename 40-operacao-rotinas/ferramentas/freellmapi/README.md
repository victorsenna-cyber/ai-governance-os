# FreeLLMAPI — cliente N1 (modelo gratuito, só dado público/interno)

> ⚠️ **Ferramenta opcional.** Só vale se você quiser rodar o nível N1 (modelo gratuito) da operação por tasks (`tarefas/README.md`). Instale fora da Governança.

Gateway local (instalar numa pasta própria fora da Governança; documentado na v0.4.1; terceiro, não confiável) que agrega camadas gratuitas de ~34 provedores atrás de um endpoint só e cai para o próximo modelo quando um estoura limite. Apurado lendo o código da v0.4.1.

🔴 **Régua: só dado de classe P (público) ou I (interno sem cliente) passa por aqui; dado C (cliente) ou S (sensível) nunca.** O `n1_cliente.py` recusa C e S (saída 2). Provedores gratuitos podem treinar com o que recebem; além disso o servidor consulta `api.freellmapi.co` (catálogo, 12 h).

## Subir
`cd <pasta do freellmapi> && npm run dev -w server` (`tsx watch`; produção: `npm run build:server` e `npm start -w server`). Sobe **sem chave de provedor**: `/livez` 200, `/readyz` 503 `no_upstreams_configured`. Porta 3001 (`.env`), escuta `[::]`. Banco: `server/data/freeapi.db`. Painel (`npm run dev -w client`, porta 5173) é opcional.

## Endpoints (todos em `http://localhost:3001`)
| Uso | Método e caminho |
|---|---|
| OpenAI | `POST /v1/chat/completions` (também `/v1/responses`, `/v1/embeddings`), `GET /v1/models` |
| Anthropic | `POST /v1/messages`, `/v1/messages/count_tokens`, `GET /v1/models` |
| Saúde | `GET /livez`, `GET /readyz` (sem auth); `GET /v1/providers` (com chave) |
| MCP | `POST /mcp` (JSON-RPC; GET dá 403/405) |

**Modelo:** campo `model`. `auto` = cadeia ativa; `auto:<perfil>` = cadeia nomeada (forte→fraco, em ordem de prioridade, com failover em 429/5xx); `auto:smart|fast|cheap|reliable|balanced` = ordenação global; ou id de modelo fixo; `fusion` = painel + juiz.

## Autenticação
Chave unificada `freellmapi-<48 hex>` (guardada na tabela `settings`, `unified_api_key`; o painel mostra em Keys). Vai em `Authorization: Bearer ...` (OpenAI) ou `x-api-key` (Anthropic). Sem ela: 401 `Invalid API key`. `/api/*` (admin) exige **token de sessão do painel**, outra coisa; a chave unificada não serve ali. Limite 120 req/min por IP. Nosso cliente lê `FREELLMAPI_KEY` e `FREELLMAPI_URL`.

## Chaves de provedor
Ficam no SQLite (`server/data/freeapi.db`, AES-256-GCM, `ENCRYPTION_KEY` do `.env`). Sem painel: (a) **arquivo declarativo**, aplicado a cada boot e idempotente: `FREEAPI_CONFIG_PATH=C:\caminho\freellmapi.config.json` com `{"keys":[{"platform":"groq","key":"gsk_...","label":"main"}]}` (também `models`, `fallback`, `routing`); o arquivo tem segredo em texto puro, fora do repo; (b) **CLI**: `FREELLMAPI_DASHBOARD_TOKEN` + `npx freellmapi keys add groq --key '...'` (token só sai do painel/login); (c) `POST /api/keys {platform,key,label}` com o token. As plataformas de cada perfil estão em `perfis.json`.

## Perfis `auto:<nome>`
Não há arquivo de perfis. Criar: `POST /api/profiles {"name":"continuum-rapido","empty":true}` e `PUT /api/profiles/:id/reorder [{modelDbId,priority,enabled}]` (token do painel). Nome até 20 caracteres. Perfil inexistente: HTTP 400. As listas propostas, com substituições onde o catálogo não tem o modelo, estão em `perfis.json`. Um servidor novo nasce só com o perfil padrão; estes se criam com as chamadas acima.

## MCP
Existe em `/mcp`, **desligado por padrão** (`-32000 MCP server is disabled`; ligar: `PUT /api/settings/enable-mcp {"enabled":true}` com token). Ferramentas: `ask_freellmapi` (chat), `healthcheck`, `list_models`, `provider_health`, `usage_summary`, `routing_info`, `set_routing_strategy`, `cache_stats`, `web_search`.

## Uso (contadores)
Gravado no SQLite: tabelas `requests` (por chamada), `request_hourly` (tokens, sucesso/erro), contadores RPM/RPD/TPM/TPD por chave. Leitura: `/mcp` → `usage_summary {range:24h|7d|30d}` (precisa MCP ligado); `GET /api/analytics/summary|by-platform|by-model|by-key|timeline?range=7d` (token do painel); `GET /v1/providers` e `/v1/quota-forecast` (chave unificada; sem chave de provedor, `providers:[]`).

## Respostas de referência da v0.4.1, sem chave de provedor configurada
- `GET /livez` → `200 {"status":"ok","version":"0.4.1","uptime_s":<segundos>}`
- `GET /readyz` → `503 {"status":"unavailable","reason":"no_upstreams_configured"}`
- `GET /v1/models` com chave → `200 {"object":"list","data":[{"id":"auto",...},{"id":"fusion",...` (~130 KB, catálogo)
- `POST /v1/chat/completions` sem chave → `401 {"error":{"message":"Invalid API key","type":"authentication_error"}}`
- chat `model:"auto"` com chave → `503 {"error":{"message":"No candidate model has a configured, usable provider key. Add provider API keys in the dashboard. All models exhausted. ... 403 models skipped: no key configured for their platform.","type":"service_unavailable","code":"no_providers_configured"}}`
- chat `auto:continuum-rapido` → `400 {"error":{"message":"Profile 'continuum-rapido' not found. ..."}}`
- `/v1/messages` (Anthropic) → `503 {"type":"error","error":{"type":"overloaded_error","message":"No candidate model has a configured, usable provider key..."}}`
- `POST /mcp` → `{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"MCP server is disabled. ..."}}`
