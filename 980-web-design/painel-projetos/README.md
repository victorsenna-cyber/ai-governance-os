# painel-projetos — Projetos · {{EMPRESA}}

> Alçada: {{OPERADOR}}. Painel para ver os projetos e o andamento deles no dia a dia: prazos, o que resta entregar, o que precisa de decisão. Mesma base do dashboard e do sistema financeiro.
> 🟡 **Provisório** até a 1ª semana de uso com os frontmatters de cada conta mantidos pela regra da `ARVORE-CONTA.md`.

## Como o dado anda

```
clientes/<Conta>/PAINEL.md (frontmatter) · STATUS.md (datas) · 01 - contexto/OpenWA/ (datas nos nomes)
40-operacao-rotinas/tarefas/*/T-*.md · tarefas/DECISOES-PENDENTES.md · 45-financeiro/LANCAMENTOS-EMPRESA.md
   └→ push na main (sincronizar.py, ao abrir e fechar toda sessão)
       └→ GitHub Action projetos-painel → ferramentas/painel-projetos.py --publicar
            └→ Supabase <projeto-supabase>, tabela projetos_estado (um documento JSON; mesmo token e leitores do financeiro)
                 └→ https://financeiro.{{DOMINIO}}/projetos/  (estático, mesmo login do Caixa)
```

- **Fonte única é o `.md`.** O Supabase é cópia reescrita a cada push. **Nunca se edita dado no Supabase nem no site.**
- **Leitor:** `40-operacao-rotinas/ferramentas/painel-projetos.py` (regras de leitura e de saúde no cabeçalho dele). `--json` dá o estado a qualquer sessão em uma chamada N0; `--verificar` é o gate (sai 1 se algum painel está inválido ou defasado > 3 dias do STATUS).
- **Ponte:** `.github/workflows/projetos-painel.yml` — a cada push na `main` que mexa em `PAINEL.md`, `STATUS.md`, OpenWA, tasks, cartões ou *A receber*; e uma vez por noite, logo após a meia-noite no seu fuso (os contadores de dias andam sem push).
- **Banco:** `supabase/006-projetos.sql` — tabela `projetos_estado`, função `sincronizar_projetos(token, payload)` (mesmo hash do `FINANCAS_SYNC_TOKEN`), RLS pela mesma `financas_privado.leitores`.
- **Site:** `index.html` (página própria, sem artefato: CSS e JS inline, só o supabase-js de fora) + `config.js` (chave publicável, igual ao financeiro) + `.htaccess`. Mora em `/projetos/` do domínio do Caixa de propósito: **mesma origem, mesma sessão** — quem já entrou no financeiro entra aqui sem senha. `publicar.py` sobe os três arquivos pela API da Hostinger (token em `~/.continuum/hostinger-token.txt`); `publicar.py --conferir` compara byte a byte.

## O que o painel mostra

| Aba | Conteúdo |
|---|---|
| **Hoje** | vencidos · próximos 7 dias (marcos, tasks com prazo, decisões com prazo, *A receber*) · decisões abertas · contas sem toque há mais de 7 dias · *A receber* em aberto · marcos sem data · painéis a corrigir |
| **Projetos** | um cartão por conta: saúde · fase · projeto · próximo marco com prazo e dono · motivos da cor · risco · marcos abertos · tasks da operação · decisões · contrato, recebido, a receber · último registro, último WhatsApp, data do painel · caminhos dos arquivos (clique copia) |
| **Decisões** | os cartões abertos de `DECISOES-PENDENTES.md`: contexto, A/B/C, recomendação, autonomia, prazo. A resposta continua sendo uma letra na sessão (fase 3 do plano: botão aqui) |
| **Prazos** | linha do tempo por dia: vencidos dos últimos 60 dias e os próximos 45, com os quatro tipos de prazo etiquetados |

Filtro **Ativas · Todas · uma conta** no topo; teclas **1 a 4** trocam de aba. Conta `pausada`, `encerrada` ou `arquivada` só aparece em *Todas*.

## A camada de máquina da conta (frontmatter do `PAINEL.md`)

```yaml
---
conta: Conta A
fase: construir            # prospecto · proposta · fundar · construir · operar · pausada · encerrada · arquivada
projeto: <projeto principal> (principal) · <projeto secundário> (secundário)
proximo_marco: <o próximo marco, em uma frase>
marco_prazo: AAAA-MM-DD
marco_dono: {{OPERADOR}}
contrato: 0                # valor contratado, em reais
recebido: 0                # valor já recebido, em reais
risco: <o risco aberto da conta, em uma frase>
atualizado: AAAA-MM-DD
marcos:
  - { o_que: <marco 1>, prazo: AAAA-MM-DD, dono: {{OPERADOR}}, duro: nao }
  - { o_que: <marco 2>, prazo: AAAA-MM-DD, dono: {{OPERADOR}}, duro: sim }
---
```

- Só `chave: valor` e a lista `marcos:` com itens inline `{ }` (sem vírgula dentro de `o_que`). Sem PyYAML de propósito.
- 🔴 **Regra de manutenção (`ARVORE-CONTA.md`):** toda tarefa que mexe no `STATUS.md` de uma conta atualiza `atualizado:`, `proximo_marco`, `marco_prazo` e `marcos:` no mesmo ato. O painel cobra quando falta (*"STATUS mais novo que o painel há N dias"*).
- **Saúde é calculada** (cabeçalho do script): 🔴 prazo vencido, a receber vencido, decisão vencida, sem toque > 14 dias em `construir`/`operar`, frontmatter inválido · 🟡 prazo em até 7 dias, sem toque > 7, defasagem > 3 dias, contrato vazio além de `proposta` · 🟢 o resto. Ninguém escreve a cor.
- Para criar os frontmatters das contas existentes, um subagente lê o `STATUS.md` §5 e o `DECISOES.md` de cada conta e propõe o bloco; as dúvidas de cada um vão para o `STATUS.md` da casa e são do {{OPERADOR}}.

## Uma vez só

- **Supabase:** rodar `supabase/006-projetos.sql` no SQL Editor do projeto `<projeto-supabase>` (depois do `001` do financeiro). Sem ele o Action fica vermelho (`sincronizar_projetos` não existe).
- **Supabase, Redirect URLs:** `https://financeiro.{{DOMINIO}}/projetos/` para o link por e-mail voltar aqui. Sem isso o link cai na raiz do Caixa, já logado, e `/projetos/` abre sem senha na mesma sessão.
- **GitHub:** nada. O secret `FINANCAS_SYNC_TOKEN` já existe e é o mesmo.

## Rotina

- Task N0 diária `painel-projetos-verificar` (antes do `brief-diario`): `painel-projetos.py --verificar --json 40-operacao-rotinas/rotinas/PAINEL-PROJETOS.json`. O brief lê esse JSON em vez de todas as entradas do `STATUS.md`.
- Mudou `index.html`, `config.js` ou `.htaccess`: `python3 publicar.py` e depois `python3 publicar.py --conferir`.
