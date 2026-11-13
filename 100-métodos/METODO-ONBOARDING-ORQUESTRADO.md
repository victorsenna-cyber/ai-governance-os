# MÉTODO — ONBOARDING ORQUESTRADO (do aceite ao valor percebido)

> **Tipo:** método · secundário: gate (§11)
> **Alçada:** {{OPERADOR}} · **Estado:** 🟡 **provisório, `n=0`**. Gradua quando 2 contas tiverem percorrido a régua do D0 à revisão de valor com as datas registradas e sem alerta falso.
> **Fonte:** Donna Weber, *Onboarding Orquestrado* (orig. *Onboarding Matters*), lido inteiro. As páginas citadas abaixo são do livro. O livro é de SaaS B2B; **toda adaptação à nossa operação está marcada [casa]**.
> **Em código:** `40-operacao-rotinas/ferramentas/onboarding_regras.py` (a régua, a saúde e os alertas) → aba **Onboarding** do painel de projetos. **Prazo ou peso que muda aqui muda lá no mesmo ato.**
> **Convive com:** `30-comercial/onboarding.md` (o plano de sucesso antes da venda: o livro confirma, é a etapa de Embarque) · `METODO-TRILHO-DE-CONTA-NOVA.md` (a entrega técnica dos mesmos dias: este método é a jornada do cliente por cima dela) · `10-skills/heads/head-onboarding-orquestrado.skill.md` (a persona).

---

## 1. A tese, em causa e efeito

**A renovação se decide no onboarding, não no vencimento** (livro p.45). A assinatura abre no cliente uma janela de ruminação, o remorso de quem arriscou dinheiro e reputação, e **ela não se fecha sozinha** (p.44). Fecham-na três coisas:

- **marcos explícitos**, que dão "fechamento cognitivo": a compra acabou, a entrega começou, e é assim que ela anda (p.44, p.110);
- **a parte do cliente escrita e aprovada**, porque ele só se responsabiliza pelo que assinou (p.89, p.113);
- **o primeiro valor percebido por ele**, o "aha" que para a prospecção negativa e vira o viés de confirmação a nosso favor (p.43, p.180).

Silêncio conta como interação negativa (p.43). Sem resultado em 90 dias, a chance de renovar cai para menos de 10% (p.187).

**[casa] Contrato mensal: os 90 dias do livro são três faturas.** O primeiro valor precisa ficar perceptível **antes da segunda fatura (D+30)**. E se **a mesma pessoa vende e entrega**, a tendência é "já começar a trabalhar" sem o marco que encerra a compra. O trabalho começa e a ruminação do cliente continua.

## 2. A cadeia causal, e onde ela quebra

1. Embarque mostra o pós-venda e abre o plano de sucesso → expectativa realista, confiança de que "já fizemos isso" (p.79, p.83).
2. Assinatura → **janela do remorso aberta** (p.44).
3. Passagem para o registro → quem entrega sabe tudo o que foi dito na venda; o cliente não repete nada (p.95–97).
4. Passagem com o cliente em até 10 dias → fecha a compra; "estou em boas mãos" (p.104, p.114).
5. Plano aprovado pelo decisor → a parte dele vira compromisso (p.89, p.113).
6. Kickoff → mapa de quem faz o quê; o cliente para de imaginar o pior (p.119, p.125).
7. Adoção: implementação + capacitação + mudança de hábito (p.129–137).
8. Vitória rápida e primeiro valor → o remorso para (p.188).
9. Revisão de ~90 dias, com dados e sem venda → valor confirmado, renovação medida cedo (p.143–145).
10. Expansão → onboarding de quem chega, de cada mudança e do próximo degrau → renovação, compra de mais, indicação (p.53, p.160).

**Os três elos que mais quebram:**
- **2 → 4, o vão entre a assinatura e a passagem.** É onde se joga fora a confiança da venda (p.78); no caso do livro, a maioria saía nos primeiros 30 dias (p.62).
- **7 → 8, primeiro valor fora da janela, ou medido errado.** Valor é o que reverbera no cliente, não o nosso KPI: campanha no ar, login e CPL não são primeiro valor (p.184, p.189).
- **5 → 7, o cliente não faz a parte dele.** [casa] Em tráfego para PME é a quebra mais cara: o lead chega e morre no atendimento, e o churn vem atribuído à mídia.

## 3. As seis etapas na nossa operação

| Etapa | O que produz no cliente | O que fazemos [casa] | Passa quando | Prazo |
|---|---|---|---|---|
| **1 · Embarque** | expectativa realista; confiança no método | a jornada de onboarding aparece na proposta; o **esboço do plano de sucesso** sai do diagnóstico inicial (`30-comercial/onboarding.md`) com primeiro valor datado, a parte do cliente e o que não se promete | proposta aceita (D0) | dentro do ciclo de venda |
| **2a · Passagem para o registro** | — (prontidão nossa) | call de venda destilada; as seis perguntas do livro (quem é, o que comprou, por quê, contatos, termos, objetivos) respondidas na conta; **cada promessa feita na venda confrontada com o escopo**: promessa sem lastro vira item do plano ou correção por escrito | as seis respondidas | D+2 |
| **2b · Passagem com o cliente** | fechamento da compra; confiança transferida | 30–45 min **com o decisor**; plano mandado antes; fechamento dito em voz: *"até aqui eu te vendi; daqui em diante respondo pelo resultado, e esta é a régua"*; resultado esperado reperguntado; riscos com "depende de"; **kickoff e revisão de valor marcados na própria reunião** | plano aprovado por escrito (WhatsApp vale) | **até D+10** (p.104); aprovação em 3 dias |
| **3 · Kickoff** | clareza do próximo passo; "estão no comando" | 60 min com quem executa do lado dele (o atendente, quem cuida do site); cada entrega dele com dono e data; canal oficial e cadência; vitória rápida e primeiro valor relembrados; **resumo no mesmo dia** | resumo enviado | até 10 dias úteis da passagem (p.121); **nunca junto com a passagem** (p.119) |
| **4 · Adoção** | a coisa existe; ele sabe usar; o hábito mudou | **primeiro no ar** (campanha veiculando com rastreio, site publicado, sistema rodando) na data do plano; o atendente treinado no roteiro **antes** do no ar; a mensagem pronta que o dono manda ao time explicando o que muda; um hábito por vez, começando pelo que ele já faz | primeiro valor na fala dele | primeiro no ar: data do plano · primeiro valor: **D+30** |
| **5 · Revisão** | valor confirmado; ser ouvido | ~90 dias do kickoff, com o decisor; plano v1 lado a lado com o resultado (relatório da operação ou painel de resultado); uma pergunta direta sobre renovar; uma sobre o próprio onboarding; **zero venda na pauta** (p.143); próxima revisão marcada antes de sair | ações com dono e data; plano v2 salvo | kickoff + 90 |
| **6 · Expansão** | valor contínuo; adesão | atendente novo no cliente = onboarding de usuário em 7 dias; mudança de canal ou de estratégia comunicada com o porquê em 48 h (a régua "captura propaga"); upgrade de produto ou unidade nova **volta à passagem** (p.159); escada de maturidade na língua do dono | — | contínua |

## 4. Primeiro valor e vitórias rápidas

- **Primeiro valor é fala do cliente, com data e fonte.** "Chegou cliente novo pelo anúncio e virou venda" é candidato; "a campanha está no ar" não é. Descobre-se perguntando (p.184–185): como você sabe que teve resultado com a gente? qual foi o momento? quanto tempo levou? o que impediu? do que precisa para chegar mais rápido?
- **Quem registra:** a captura ou o transcrito trazem a fala; o agente classifica; **o {{OPERADOR}} confirma.** Agente não decide sozinho que houve primeiro valor (§9).
- **Vitórias rápidas em D+10, D+30, D+60 e D+90** (p.191), cada uma em dinheiro ou tempo do cliente, nunca em atividade nossa (p.189), e **reconhecida por ele**. Candidatas: primeiro lead atendido no roteiro e convertido; primeira venda rastreada até o anúncio; um roteiro que fecha mais que o anterior.
- **Escopo em ondas de 30 dias, cada onda com resultado próprio** (p.192). "Mês 1 = setup" sem resultado no mês 1 leva direto ao vale da desilusão.

## 5. A régua (o que o painel confere)

| Marco | Prazo | Vencido vira | Livro |
|---|---|---|---|
| Passagem com o cliente | D0 + 10 | 🔴 | p.104 |
| Plano aprovado pelo decisor | passagem + 3 | 🟡 | p.113 |
| Kickoff | passagem + 14 (10 úteis) | 🔴 | p.121 |
| Primeiro no ar | data do plano (sem data, 🟡 depois da passagem) | 🔴 | p.275 |
| Vitória rápida D+10 · D+30 · D+60 · D+90 | D0 + 10 / 30 / 60 / 90 | 🟡 | p.191 |
| Primeiro valor (fala dele) | D0 + 30 🟡 · **D0 + 90 🔴** | — | p.187 · D+30 [casa] |
| Revisão de valor | kickoff + 90 (aviso 14 dias antes) | 🔴 | p.143 |

Marco que venceu **antes de a régua valer para a conta** (`onb_desde`, padrão: a data em que a régua entrou em uso) aparece cinza, *"não registrado (antes do método)"*, e não acusa: a conta antiga não fica vermelha pelo que ninguém mediu.

## 6. A saúde da conta (0 a 100)

Poucos critérios, com peso, em verde, amarelo e vermelho (p.205–207). Critério sem dado sai da conta, não entra como zero.

| Critério | Peso | Cheio | Meio | Zero |
|---|---:|---|---|---|
| Marcos do método no prazo | 25 | feitos no prazo | feitos atrasados | vencidos |
| Primeiro valor | 25 | registrado, ou ainda dentro do prazo | D+30 a D+90 sem fala | depois de D+90 sem fala |
| Cliente em dia (marcos dele no `PAINEL.md`) | 15 | nenhum vencido | um vencido | dois ou mais |
| Contato (último toque: STATUS ou WhatsApp) | 15 | até 7 dias no 1º mês, 14 depois | até o dobro | mais que o dobro |
| Pagamento (*A receber*) | 15 | nada vencido | — | vencido |
| Temperatura de renovação | 5 | sim | talvez | não |

**Verde ≥ 70 · amarelo 45–69 · vermelho < 45.** 🔴 **Recusa de renovação ("não") põe a conta no vermelho, seja qual for a nota.** É fato consumado, não critério: uma conta que recusou renovar e saía verde, com 93, mostrou que a nota sozinha mente.

## 7. Os alertas

Cada alerta sai com **o que aconteceu, o porquê (o efeito no cliente, com a página), e o ato mínimo**. Os do §5, mais: silêncio acima do limite (p.43, p.206) · *A receber* vencido, lido como sintoma e não como causa (p.28) · pendência do cliente vencida (p.120, p.243) · temperatura "talvez" ou "não" (p.145) · conta em entrega sem D0.

🔴 **Alerta é para o {{OPERADOR}}, nunca para o cliente.** O que chega ao cliente sai de um canal, uma voz, na cadência combinada no kickoff. Dez avisos automáticos ao cliente são o "andar em bando" do livro, em versão digital (p.138).

## 8. Os campos no `PAINEL.md`

No frontmatter, ao lado dos que já existem. Todos opcionais, datas `AAAA-MM-DD`:

```
onb_d0:                  # aceite da proposta ou assinatura
onb_passagem:            # passagem com o cliente realizada
onb_plano_aprovado:      # plano aprovado por escrito pelo decisor
onb_kickoff:
onb_golive_previsto:     # a data prometida no plano
onb_golive:              # o primeiro no ar
onb_vitoria_10:          # e _30, _60, _90: vitória reconhecida pelo cliente
onb_primeiro_valor:      # a data em que ELE disse
onb_primeiro_valor_fala: # a fala literal + fonte
onb_revisao:
onb_proxima_revisao:
onb_renovacao:           # sim | talvez | nao
onb_desde:               # desde quando a régua acusa
onb_fora:                # sim = projeto próprio ou parceria, fora da régua
```

**Quem escreve:** quem registra o fato, no mesmo ato (a régua "captura propaga" do `CLAUDE.md` §6). A etapa **não se declara**: sai das datas preenchidas, para não haver dois lugares dizendo coisas diferentes. A pendência do cliente continua nos `marcos:` com `dono:` dele.

## 9. Os agentes na VPS (fase seguinte, com a chave de API)

**O que o agente mede sozinho, com o que a casa já captura:** dias entre marcos; silêncio do cliente (captura do WhatsApp); pendências dele vencidas; fatura atrasada; mudança de canal sem comunicação (captura × plano); troca de interlocutor (nome novo na conversa); candidata a primeiro valor ou vitória numa fala dele (classifica e propõe, com a frase literal).

**O que o agente não decide:** se o primeiro valor aconteceu (§4); o que se diz ao cliente (passa pela fila de envio, com o ✅ do {{OPERADOR}}).

**A ordem, pelo próprio livro:** primeiro a mão, depois a automação (p.278). A régua roda com o {{OPERADOR}} em 2 ou 3 contas; só o alerta que se mostrou útil vira automático. Tecnologia sobre processo que não funciona "só cria mais selvas" (p.231).

## 10. O que não se faz

- Juntar passagem e kickoff "para ganhar tempo" (p.119).
- Mandar ao cliente um plano em branco para ele preencher (p.89).
- "Me chama se precisar" no lugar do kickoff (p.119).
- Contar campanha no ar, login ou CPL como primeiro valor (p.184, p.189).
- Vender na revisão (p.143).
- Começar pelo caso mais difícil do cliente (p.160).
- Fazer pelo cliente o que ele precisa saber fazer: cria dependência e não escala (p.213).

## 11. Gate — o que reprova sozinho

- conta em entrega sem `onb_d0` no `PAINEL.md`;
- passagem e kickoff na mesma reunião;
- primeiro valor registrado sem fala do cliente com data e fonte;
- revisão com oferta de venda na pauta;
- alerta automático enviado ao cliente;
- mudança de prazo ou peso no método sem a mesma mudança em `onboarding_regras.py`, ou o inverso.

---

*Base: o livro de Donna Weber (não distribuído com o template: adquira a obra) · `30-comercial/onboarding.md`.*
