# SKILL — Blue Team Jurídico (defesa, registro, evidência)

> **Tipo:** skill de método · **Criado em:** 2026-07-13 · Política-mãe: `80-juridico/POLITICAS-JURIDICAS.md`
> Carrega quando: conflito ativo · ameaça (jurídica ou velada) · cobrança indevida · "conversa estranha" com cliente/parceiro/ex-contratante · necessidade de registrar caso ou preservar evidência.
> Postura: **defensiva sempre.** Não atacamos, não ameaçamos, não blefamos. Blindamos e registramos.

## 1. Função no sistema

Transformar conflito em registro estruturado e exposição em risco mapeado — antes que vire disputa. O blue team não vence brigas; evita que elas existam ou que nos peguem sem arquivo.

## 2. Protocolo de registro de caso (obrigatório, no dia)

Todo evento gera arquivo em `80-juridico/registros/AAAA-MM-caso-<nome>.md` com esta estrutura:

```
# Registro de Caso — <título>
> Status: ativo / monitoramento passivo / encerrado · Risco: severidade (baixa/média/alta/crítica) × probabilidade (baixa/média/alta)
1. Partes e contexto
2. Fatos (linha do tempo com datas — só fato verificável, sem adjetivo)
3. Posição registrada (a nossa, em tese defensável)
4. Exposições mapeadas (tabela: exposição · de quem · leitura honesta · mitigação)
5. Evidências (checklist de preservação)
6. Aprendizados incorporados ao sistema (que política/skill mudou por causa disto)
```

Regras do registro: fato separado de interpretação · exposição NOSSA registrada com a mesma honestidade que a do outro (autoengano em registro é autossabotagem) · toda decisão tomada no caso ganha data.

## 3. Protocolo de resposta a conflito (a regra das 48h)

Aprendizado direto de um conflito real:

1. **Não responder a quente. Nunca.** Prazo interno: até 48h. Silêncio de 2 dias não perde direito nenhum; resposta raivosa cria arquivo contra nós.
2. Antes de responder: registrar o caso (§2) e preservar evidência (§4) — a conversa pode ser apagada pelo outro lado.
3. A resposta tem no máximo **3 elementos**: posição objetiva (1-2 frases) · fato que a sustenta · porta aberta ou encerramento cordial. **Proibido:** lição de moral, ataque à competência do outro, ironia, ameaça, admissão de culpa, promessa nova.
4. Teste antes de enviar: *esta mensagem lida em voz alta por um juiz nos ajuda ou nos atrapalha?*
5. Ameaça explícita de processo/notificação → parar tudo, não responder mais nada no canal, escalar para advogado real (alçada: `POLITICAS-JURIDICAS.md` §3).

## 4. Preservação de evidência (no ato, não depois)

- Export completo da conversa (WhatsApp: exportar com mídia) + prints com data/hora visíveis.
- Cópia fora do dispositivo no mesmo dia (drive) — nomear `AAAA-MM-DD-<fonte>-<assunto>`.
- Comprovantes financeiros (Pix, NF, extrato) vinculados ao caso.
- E-mail relevante: encaminhar para arquivo próprio, não deixar só na caixa.
- Prova de iniciativa do cliente (quem procurou quem) é ouro — preservar a 1ª mensagem sempre.

## 5. Mapa de prazos (referência leiga — confirmar com advogado antes de agir)

| Matéria | Prazo usual | Nota |
|---|---|---|
| Trabalhista (ajuizar após fim do vínculo) | ~2 anos | retroage até 5 anos de direitos |
| Consumidor (vício de serviço) | 90 dias a 5 anos conforme o caso | relevante como réus potenciais: entregar bem e documentar aceite |
| Cível geral (reparação) | ~3 anos · contratos ~10 | referência ampla |
| Direito de arrependimento (venda online — futuro infoproduto/SaaS) | 7 dias | CDC art. 49 — política de reembolso obrigatória antes de vender |

Prazos que nos afetam entram no registro do caso com data-limite + `STATUS.md` se exigirem decisão.

## 6. Checklists preventivos (rodar ANTES, não depois)

**Antes de qualquer venda:** instrumento no nível mínimo da `POLITICAS-JURIDICAS.md` §2? · escopo em anexo? · red lines §4 intactas? · aceite registrado e arquivado?
**Antes de qualquer pessoa trabalhar conosco:** contrato escrito (escopo, valor, prazo, IP, confidencialidade, saída)? · sem cláusula que não aceitaríamos para nós?
**Antes de nós trabalharmos para alguém:** tudo por escrito ANTES do primeiro dia · qualquer restrição futura (exclusividade, não-competição) só vale escrita, delimitada e compensada · FGTS/INSS/NF conforme o formato real da relação — não aceitar arranjo informal que, na prática, tem natureza de vínculo.

## 7. Handoffs

← CEO (decisão de abrir/encerrar caso) · → CLO.skill (decisão jurídica estratégica) · → contratos.skill (quando a defesa é cláusula) · → advogado real (gatilhos do §3.5 e `POLITICAS` §0).

---
*Disclaimer permanente: `POLITICAS-JURIDICAS.md` §0.*
