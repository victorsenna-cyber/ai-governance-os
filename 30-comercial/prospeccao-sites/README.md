# Prospecção Ativa de Sites — WhatsApp (Serviços Locais)

> Playbook operacional para levantar caixa rápido vendendo sites via prospecção ativa Google Maps → WhatsApp.
> **Abordagem:** diagnóstico SPIN (conduzir o prospect a concluir que precisa do site) — o preview entra como prova **depois** do interesse, não antes.
> **Nicho 1:** serviços locais gerais sem site. Outros nichos têm preço e abertura próprios: cada um ganha o seu plano de oferta e processo, e este README vale para o nicho 1.
> **Meta mês 1:** `{{META_SITES_MES}}` sites. Preço: `{{TICKET_SITE}}` nos primeiros (fundador), `{{TICKET_SITE}}` do seguinte em diante.
> Método aplicado: `SPIN Selling` (Rackham) como espinha da conversa · `$100M Leads` (Hormozi) para volume e escassez · `Onboarding Orquestrado` (Weber) para entregar e expandir.

---

## 1. A tese (por que SPIN)

Empresa de serviço local sem site sente uma dor que não verbaliza: **parece amadora ao lado do concorrente que tem site, e perde cliente que pesquisa no Google.** Ela não acorda querendo "comprar um site".

A abordagem SPIN não empurra a solução — ela **faz o prospect enxergar a própria dor e concluir sozinho** que precisa resolver. Perguntamos sobre como captam cliente hoje, expomos a perda silenciosa de quem pesquisa e não acha, e deixamos o próprio dono dizer "faz sentido ter um site". Quando ele conclui, o preço deixa de ser obstáculo.

> Princípio Rackham: **o cliente conclui, não é convencido.** A pergunta de Implicação (o que essa falta está custando) é a que vende. O preview é a prova que confirma a decisão — não a abertura.

---

## 2. O fluxo (7 passos)

```
1. LISTA      Google Maps → empresas de serviço local SEM site
2. ABORDAGEM  WhatsApp: abertura leve + 1ª pergunta de diagnóstico (SPIN)
3. DIAGNÓSTICO Conduzir Situação → Problema → Implicação → Necessidade
4. PROVA      Mostrar preview/modelo do site DELE (confirma a decisão que ele já tomou)
5. OFERTA     {{TICKET_SITE}} (primeiros 5) / {{TICKET_SITE}} — entrega em 7 dias úteis
6. ENTREGA    Onboarding curto: dados → publicação → handoff
7. EXPANSÃO   "Agora que tem site, vamos trazer cliente pra ele?" → Assessoria
```

Arquivos do playbook:

- `scripts-whatsapp.md` — mensagens do **{{OPERADOR}}** (ângulo resultado/Google), da abertura SPIN ao fechamento. Se um vendedor entrar, ele ganha um arquivo próprio com a mesma estrutura, voz e gancho dele.
- `roteiro-qualificacao.md` — o coração SPIN: as 4 perguntas e como conduzir.
- `narrativas-objecoes.md` — narrativa de venda + respostas a objeções.
- `followup.md` — cadência de follow-up (a maioria fecha no follow-up, não no 1º contato).
- `conversao-assessoria.md` — o pulo do gato: site → recorrência.

---

## 3. Como montar a lista (Google Maps)

Alvo: **serviços locais sem site** no Google Maps (o campo "site" vazio é o sinal de compra).

Segmentos quentes (decisão rápida, valorizam imagem): oficinas mecânicas, pet shops, restaurantes/lanchonetes, barbearias/salões, academias/studios, borracharias, lava-rápidos, assistências técnicas, materiais de construção, marmorarias.

Critérios de inclusão:
- **Sem site** (ou só link de Instagram/iFood).
- Telefone com **WhatsApp**.
- Avaliações (já tem operação real, tem o que mostrar).

Ferramenta: Apify Google Maps Scraper (já no nosso stack) ou coleta manual. Campos: nome, telefone, endereço, categoria, nota, nº de avaliações, fotos disponíveis.

> Capacidade-meta: **conversas iniciadas por dia útil = fechamentos desejados no mês ÷ taxa de conversão medida ÷ dias úteis.** Não precisa de mil leads — precisa de constância.

---

## 4. O preview como prova (não como abertura)

No SPIN, **não montamos preview no escuro para todos.** Abrimos com diagnóstico; o preview entra quando o prospect já demonstrou interesse — para **confirmar** a decisão que ele acabou de tomar mentalmente.

- Template único reaproveitável (1 layout que serve a qualquer serviço local).
- Trocar: nome, logo (ou texto), cor, 3–5 fotos (puxar do Google/Instagram dele), serviços, telefone/WhatsApp, mapa.
- Tempo-alvo de montagem: **15–25 min**, feito **só para o lead já qualificado** (que respondeu bem ao diagnóstico).
- Hospedar em link temporário (Netlify/Vercel/preview) ou enviar vídeo curto de tela.

> Vantagem operacional do SPIN aqui: economiza esforço — montamos preview só para quem já está quente, não para a lista inteira.

---

## 5. Regras de operação (anti-fricção e anti-ban)

- Aprovação humana antes de qualquer disparo em volume (regra da casa).
- WhatsApp: espaçar envios (45–75s), ~10–15 primeiras mensagens/dia por número, horário comercial.
- Tom humano, nunca robótico. Toda mensagem passa pela régua `10-skills/stop-slop.skill.md` (sem cara de IA, sem travessão, calibrada ao WhatsApp — emoji 1–2 OK). Áudio curto converte mais que texto longo (ótimo para as perguntas SPIN).
- Registrar cada lead e status (planilha ou CRM Twenty): novo → em diagnóstico → qualificado → preview enviado → fechado → entregue → expansão.
- **Nunca** prometer prazo que não cumprimos. Entrega em 7 dias úteis é compromisso.

---

## 6. Funil e metas

| Etapa | Meta diária | Meta mês 1 |
|---|---|---|
| Conversas iniciadas | conversas do mês ÷ dias úteis | fechamentos ÷ taxa de conversão medida |
| Entraram em diagnóstico | diagnósticos do mês ÷ dias úteis | conversas × taxa de entrada em diagnóstico medida |
| Qualificados (preview enviado) | qualificados do mês ÷ dias úteis | diagnósticos × taxa de qualificação medida |
| Fechamentos | — | **`{{META_SITES_MES}}` sites** |
| Conversão p/ Assessoria | — | **fechamentos × taxa de expansão medida** |

> Lembrete estratégico: o site paga o mês; a **Assessoria paga o futuro**. Toda entrega de site abre a conversa de recorrência (`conversao-assessoria.md`).

---
*Base metodológica: `70-metodologias-chave/` (SPIN Selling, 100M Leads, Onboarding Orquestrado). Base interna: `30-comercial/{oferta,servicos,onboarding,ICP}.md` e o material de prospecção ativa. Provenância, não leitura obrigatória.*
