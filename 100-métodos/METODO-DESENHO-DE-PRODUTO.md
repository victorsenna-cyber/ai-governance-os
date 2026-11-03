# MÉTODO — Desenho de Produto: do porquê à tela testada

> **Tipo:** método
> **Instituído em:** 01/11/2026 · **Alçada:** {{OPERADOR}} · 🟡 **vigência provisória até o primeiro produto chegar ao degrau 7** (`CLAUDE.md` §7.1, item 4). Roteado desde o primeiro dia (REGRA Nº 1). O primeiro uso real nunca é um cliente: comece por um produto próprio.
> **Vale para:** todo produto digital que a casa cria, **nosso ou de cliente**: site de produto, app, PWA, painel, guia, SaaS, marketplace, ferramenta interna com usuário. **Não vale para:** página de vendas (circuito da `ARVORE-ESCRITA.md` §6), peça de conteúdo, repositório de governança (tem trilho próprio).
> **Carrega:** `METODO-TESTE-DE-PILARES.md` (o ICP já lido, quando há conta) · `ARQUETIPOS-DE-MARCA.md` + `METODO-KIT-DE-MARCA.md` + `METODO-PRANCHA-DE-ESCOLHA.md` (degrau 5) · `10-skills/ui-ux-designer-senior-continuum/` (degraus 5 e 6) · `METODO-GERACAO-DE-RESULTADOS.md` §3-quater (a régua-mãe, antes do degrau 6) · `90-templates/desenho-de-produto/` (os moldes dos entregáveis).

---

## 0. Por que existe

Produto que nasce pela tela nasce aéreo: cada conversa reabre tudo, porque a tela não tem de onde derivar. O que faltava nos projetos da casa não era ideia nem técnica; era **o kernel de produto**, a camada entre o kernel de negócio (quem paga, quanto, por quê) e o contrato técnico (API, banco): **o que a pessoa sente, faz e vê, em que ordem, e por quê a tela é assim.**

Este método é uma escada de sete degraus, do mais abstrato ao mais denso, e uma regra só: **degrau só abre com o anterior escrito.** Pular é o que gera o aéreo: tela sem fluxo, fluxo sem público, público sem porquê.

**O que ele não é:** não é direção de arte, tela nem token. Esses nascem nos degraus 5 e 6 pela skill de UI/UX, e só depois dos degraus 1 a 4.

---

## 1. A espinha: Círculo Dourado + Jobs to be Done

O termo que organiza o método é o **Círculo Dourado** de Simon Sinek (*Start with Why*, 2009): **por quê → como → o quê**, de dentro para fora. Entre o porquê e o quê a casa põe o **para quem**, que não é de Sinek: é o *Jobs to be Done* (Christensen) e é o que já fazemos em toda conta como ICP antes de promessa (`METODO-TESTE-DE-PILARES.md`).

**REGRA Nº 2 aplicada a produto:** o que se modela do escalado é **o job e o conceito** (o que a pessoa faz com produtos daquela classe, validado em uso); **o que se diferencia é tudo o que ela vê e toca.** Fluxo novo é hipótese nossa, e por isso o degrau 7 existe: é o custo de ter cara própria, e é barato.

---

## 2. Os sete degraus

| # | Degrau | Pergunta | Método de origem (quem usa em escala) | Entrega (molde em `90-templates/desenho-de-produto/`) | Gate do degrau |
|---|---|---|---|---|---|
| 1 | **Por quê** | por que o produto existe, numa frase que o usuário repete e quem paga aceita | Círculo Dourado (Sinek) · *Working Backwards* (Amazon: press release + FAQ antes de construir) | `PORQUE.md`: a frase, o press release de uma página escrito como se já tivesse lançado, 5 perguntas frequentes | a frase cabe numa linha, sem "plataforma", "solução" ou "conectar"; quem paga a repete sem ler |
| 2 | **Para quem, para fazer o quê** | o job de cada ator: *"quando [situação], quero [motivação], para [resultado]"* | *Jobs to be Done* (Christensen; Intercom, Basecamp) · entrevista de 5 (Nielsen Norman Group) | `JOBS.md` §1–2: jobs por ator, com citação e fonte; primeira versão marcada hipótese | cada job com **≥ 3 falas de pessoas diferentes**; menos, fica "hipótese fraca" e assim se escreve |
| 3 | **O quê** | quais funcionalidades existem, por classe: obrigatória · desempenho · encanto; o resto sai | modelo de Kano · lei de Hick (uma decisão principal por tela) | `JOBS.md` §3: job → funcionalidade → classe → geração. Deriva o contrato técnico | nenhuma funcionalidade **sem job apontável**; "a referência tem" não é job |
| 4 | **Como flui** | o caminho de cada job, tela a tela, e onde a pessoa precisa agir | fluxo por job · Fogg, B = M·A·P (Stanford) · *Hooked* (Eyal) só onde há retorno · divulgação progressiva | `FLUXOS.md`: um fluxo por job, ponto de ação marcado, o que o desenho faz ali, métrica | todo fluxo chega ao fim em **≤ 5 toques no celular** e tem métrica que o painel lê |
| 5 | **Como parece** | a cara própria, e só aqui | arquétipo da **marca do produto** (não do dono) → kit de marca → direção de arte declarada (skill ui-ux, modo direção) → prancha de escolha · heurísticas de Nielsen como lista de conferência · HIG/Material como vocabulário de componente, nunca como cara | `branding/01 - identidade visual/KIT-DE-MARCA.md` + `kit.json` · `DIRECAO-DE-ARTE.md` + `tokens.css` · prancha · escolha literal no `DECISOES.md` | passe 1 da skill: *"um concorrente poderia usar este mesmo design?"* Se sim, reprova |
| 6 | **Protótipo** | como é na mão, antes de existir: testa a fachada, não a máquina | *Design Sprint* (Google Ventures, Knapp): esboçar → decidir → prototipar → testar | `prototipo/` (HTML estático, dado escrito à mão, sem banco) no ar num domínio de teste · `PROTOTIPO.md` com o que é simulado | roda no celular de quem nunca viu, sem explicação, do início ao fim do job principal |
| 7 | **Prova** | a pessoa faz o job sem ajuda? | teste com 5 por ator (Nielsen: 5 acham ~85% dos problemas) · regra do pico e do fim (Kahneman) | `TESTES.md`: pessoa × tarefa, sucesso, toques, onde travou, o que muda | **≥ 4 de 5 completam o job principal sem ajuda.** Abaixo, volta ao degrau 4, não ao 5: quase sempre é fluxo, não cara |

**Por que HTML e não Figma no degrau 6:** o teste é no lugar onde o job acontece, no celular de quem o tem; um link abre, um Figma não. E a fachada vira a primeira dobra do produto real.

### 2.0 Degrau 4-bis · Ensaio sintético

Entre o fluxo e a cara, e de novo entre o protótipo e a prova, o agente **`.claude/agents/leitor-sintetico.md`** lê o press release, os fluxos e depois o protótipo **na pele de cada ator**, construído só de fala `D` (`JOBS.md`, léxico da conta): teste de 5 segundos, leitura passo a passo em duas vozes (pessoa crua × leitura), o momento em que quase saiu, as objeções sem resposta. A forma vem do *persona walkthrough* do repositório agency-agents; a alçada é da casa: **aponta, nunca aprova; é ensaio, nunca validação.** Serve para não gastar as 5 pessoas reais com quebra óbvia. **Não abate nem substitui o degrau 2 nem o 7**, e laudo dele contado como prova reprova no gate.

### 2.1 As restrições que entram antes do gosto (degrau 5)

É o "comportamento humano" aplicado à tela, e as grandes empresas tratam como lei, não como estilo: mobile primeiro e, quando o uso é na rua, **uma mão** · contraste AA no mínimo, tema escuro de verdade quando o uso é à noite · alvo de toque ≥ 44 px · conteúdo nasce no primeiro paint · **um clímax por tela**, e o clímax do produto é o ato que paga a promessa (skill ui-ux, passe 4) · **sem padrão escuro**: o que é pago aparece como pago, o que é opcional não se esconde (é também o que protege a confiança que o produto vende) · acessibilidade como restrição, não camada final.

---

## 3. Nosso × de cliente

| | Produto nosso | Produto de cliente |
|---|---|---|
| Degraus 1 a 3 | estrutura nossa (REGRA Nº 0); o {{OPERADOR}} objeta por escrito | **estrutura nossa, fato do cliente.** Porquê, jobs e Kano são o diagnóstico do produto: **se vendem antes de se desenhar**, ancorados (`METODO-ANCORAGEM-DE-PROPOSTA.md`), como o Mapa da Ordem é para a operação. O cliente dá fato (preço, capacidade, público que já tem, fala de usuário); nunca decide estrutura |
| Degrau 5 | arquétipo e kit da marca do produto | arquétipo e kit **da conta** (`METODO-KIT-DE-MARCA.md`); a escolha é dele, na prancha, registrada literal |
| Degrau 6 | no domínio de teste nosso ou num servidor da casa | no domínio dele, ou num de teste nosso até ele ter o seu; **código e domínio ficam em nome de quem o contrato diz** (JURÍDICO antes) |
| Degrau 7 | nós e o parceiro testamos | **as 5 pessoas são do público dele**, indicadas por ele; nenhuma amiga próxima de quem decide |
| Dinheiro | régua-mãe §9: antes do degrau 6, **qual dinheiro o produto gera, em quantos dias, em quantos passos**, por escrito | a mesma pergunta, e mais uma: **nossa viabilidade** (hora, margem) na âncora 7, nunca no documento que sai |

🔴 **Fachada antes da máquina, nos dois casos.** O degrau 6 nunca liga banco, pagamento ou integração. A máquina só nasce depois do degrau 7 e da régua de caixa do projeto.

---

## 4. Ordem, dependências e o que trava

- **Pré-condição de entrada:** o produto tem kernel de negócio (quem paga, quanto, por quê; `PILARES.md` ou equivalente). Sem isso, NEGÓCIO antes: o método desenha, não decide se o produto deve existir.
- **O degrau 1 espera o mecanismo de receita desenhado.** O que o usuário vê de pago depende de como se cobra; desenhar o fluxo antes disso é refazê-lo depois.
- **Tempo típico, uma pessoa da casa + o dono do produto:** semana 1, degraus 1 a 3 (hipóteses) e 5 (arquétipo, kit, direção, prancha); semana 2, degraus 4 e 6; semana 3, degrau 2 (entrevistas) e 7 (teste). Custo de serviço R$ 0 (domínio de teste, hospedagem estática).
- **Onde cada entregável mora:** na pasta de web design do projeto ou da conta (`<projeto>/NN - web design/`), nunca em `30-comercial/`. A escolha de cara vai literal no `DECISOES.md`.

---

## 5. Gate do método (régua de veto; linha na tabela do `METODO-GATE-DE-CONGRUENCIA.md` §3)

Reprova sozinho: **tela, token ou protótipo antes dos degraus 1 a 4 escritos** · job **sem três falas** não marcado hipótese fraca · funcionalidade **sem job apontável** ("a referência tem") · fluxo com **mais de 5 toques** ou sem métrica · direção que **um concorrente poderia usar** · **protótipo com máquina ligada** (banco, pagamento, integração) · degrau 7 **sem 5 pessoas por ator**, ou com amiga próxima de quem decide · produto de cliente com degraus 1 a 3 **não vendidos antes** · porquê com "plataforma", "solução" ou "conectar" · **ensaio sintético (degrau 4-bis) contado como validação, ou com persona sem fala `D` por trás**.

## 6. O que não entra neste método, de propósito

Hospedagem definitiva (OPERAÇÃO, G1) · copy do produto (circuito de página, `ARVORE-ESCRITA.md` §6, depois do degrau 5) · contrato técnico (API, banco: deriva do degrau 3, mora em `NN - técnico/`) · app nativo e segunda praça antes da prova.

---
*Manutenção: cada produto que passa pelo degrau 7 devolve para cá o que o teste ensinou (um gate afinado, um método de origem que não serviu, um molde que faltava).*
