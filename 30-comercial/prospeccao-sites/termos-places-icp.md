# Termos de busca — Places API (modelo: ICP de profissionais autônomos de saúde e bem-estar)

> ⚠️ **MODELO — a lista abaixo é o exemplo de um nicho. Substitua pelos termos do SEU ICP (`30-comercial/ICP.md`), mantendo a estrutura: tiers, exclusões e notas de operação.**
> **Tipo:** ativo operacional de prospecção · Consumidor: sistema de scraping do {{EMPRESA}} OS → CRM
> Padrão de query (Text Search): `"<termo> em <cidade>"` ou `"<termo> <bairro> <cidade>"` para adensar. Rodar por cidade-alvo, deduplicar por place_id/telefone antes de sincronizar.
> **Filtro de qualificação primário: ausência de `websiteUri`** (lead com ficha no mapa e sem site = dor exata do produto). `businessStatus = OPERATIONAL` obrigatório.

## Campos a capturar → slots do script (`scripts-whatsapp.md`)

| Campo Places | Slot / uso |
|---|---|
| displayName | nome (regra do "você": se for nome de pessoa, falamos com ela; nome fantasia só se real) |
| termo que encontrou | `[modalidade]` |
| cidade/bairro (formattedAddress) | `[cidade]` |
| websiteUri ausente / só ficha | `[estado digital]` (é o fato que a copy afirma) |
| rating + userRatingCount | contexto de qualificação (muitas avaliações + sem site = lead quente) |
| telefone | canal WhatsApp (validar formato) |

## Tier 1 — núcleo do ICP (rodar primeiro)

fisioterapeuta · fisioterapia · clínica de fisioterapia
nutricionista · consultório de nutrição
personal trainer · treinamento funcional
studio de pilates · pilates
psicóloga · psicoterapia

## Tier 2 — adjacente (rodar após saturar Tier 1)

massoterapia · drenagem linfática
yoga · estúdio de yoga · meditação
acupuntura · auriculoterapia *(mais clínico: qualificar com mais cuidado)*

## Tier 3 — espaços e lojas do meio (produto site também serve)

loja de produtos naturais · espaço de bem-estar

## Exclusões (anti-ICP — não sincronizar)

Hospitais, redes e franquias (outro ICP) · instituições públicas · registro duplicado do mesmo profissional em dois endereços.

## Notas de operação

1. **Quem não aparece no Places:** profissionais 100% online (sem endereço). Esse recorte vem por Instagram, não por Places — canal separado, `a calibrar`.
2. Cidades-alvo iniciais: `<cidade-alvo>` e a região metropolitana dela; expandir por capitais com densidade do nicho. Registrar no OS quais cidades/termos já rodaram.
3. Termo novo descoberto em campo (lead usa palavra que não está aqui) → adicionar aqui via atualização registrada, não só no scraper. Este arquivo é a fonte; o scraper é o consumidor.

---
*Fonte do ICP: `30-comercial/ICP.md` + `PROJECT.md` (pertencimento). Handoff: `50-integracoes-dados/OS-STATUS.md` (execuções reportadas lá).*
