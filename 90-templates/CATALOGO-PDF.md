# CATÁLOGO DE MODELOS DE PDF · o número que o operador manda

> **Os modelos são numerados para que o pedido seja um número.** **O pedido vem como "PDF modelo 3"; este arquivo diz o que é, e nada mais se pergunta.** Sem número no pedido, vale o **modelo 1**. Cada modelo aponta para a pasta que o gera; a regra de cada um mora lá, não aqui.

## Os modelos

| Nº | Nome | Como é | Quando | Gerador e carga |
|---|---|---|---|---|
| **1** | **Elétrico A4** ⭐ padrão | fundo preto-azulado, azul elétrico, Anton caixa alta; capa com as duas fitas diagonais; A4 | documento de conta, plano, estrutura, proposta que se lê para **entender** | `pdf-noturno/`: `noturno.css` → `eletrico.css` · `gerar_pdf.py` |
| **2** | **Elétrico celular** | o mesmo, em página 90 × 160 mm, para ler no telefone | quem recebe só tem o celular (roteiros, stories, listas) | `noturno.css` → `noturno-celular.css` → `eletrico.css` |
| **3** | **Elétrico claro A4** | mesmas fontes e classes, fundo claro, **cor da conta** no lugar do azul, **capa sem fita** | conta com paleta própria, leitura no PC | `noturno.css` → `eletrico.css` → `eletrico-claro.css`, com `html[data-paleta="<conta>"]` (paleta nova entra na folha, nomeada) |
| **4** | **Elétrico claro celular** | o 3 em página de celular | idem, no telefone | `noturno.css` → `noturno-celular.css` → `eletrico.css` → `eletrico-claro.css` |
| **5** | **Pacote de colagem** | capa limpa → o quê × quando → campos na ordem da tela, um bloco `.copiar` por campo → mensagens prontas → um post por página | quando o leitor vai **colar** texto em algum lugar (perfil, bio, mensagens, posts); nenhuma decisão para ele | `pdf-noturno/modelo-colagem-claro.html` (claro, A4); o mesmo pacote no escuro usa o 1 com `.copiar` |
| **6** | **Noturno puro** | fundo `#1e1e20`, destaque laranja `#e9a183`, sem fita | **só com pedido do operador** | `noturno.css` só |
| **7** | **Continuum formal** | fundo claro, Markdown → PDF sem mudar uma vírgula, capa por JSON | documento que se lê para **assinar**: proposta final, contrato, material formal. ⚠️ marcado para revisão | `pdf-continuum/build-pdf.py --in doc.md --capa capa.json` |
| **8** | **Dashboard de tráfego** | uma página, visual do painel de resultado, números de campanha | resultado fechado de campanha para o cliente | `pdf-dashboard-trafego/gerar_dashboard.py` com o JSON do cliente |
| **10** | **Roteiro do dia** | modelo cinza (elétrico A4, cinza, sem fita): capa → **o dia em BPMN vertical**, raia "Você" × raia "A casa" (tarefa, hora marcada de borda branca, decisão em losango, evento de tempo da casa com aviso tracejado) → o laço de cada envio → tabelas do que é seu, com o caminho de cada arquivo → checklist de fechamento | o dia do operador, a pedido (*"PDF roteiro para o meu dia"*); refaz-se no mesmo dia quando o horário muda | `roteiro-do-dia/gerar_roteiro.py roteiro.json` (o JSON é a fonte; o HTML é gerado, não se edita) |
| **9** | **Prancha de escolha** | opções visuais lado a lado, para o cliente escolher uma | degrau 5 do desenho de produto, kit de marca, direção de arte | `prancha-de-escolha/gerar_prancha.py` (`METODO-PRANCHA-DE-ESCOLHA.md`) |

## A classe vem junto, quando fizer diferença

O número escolhe a **cara**. A **classe** escolhe o que o documento faz (`pdf-noturno/README.md` §3-bis), e se decide pelo momento do leitor, não pelo pedido:

| Letra | Classe | Pergunta do leitor | Eixo |
|---|---|---|---|
| **E** | ESTRUTURA | "como isso funciona?" | o mecanismo, diagrama, peça por peça |
| **D** | DECISÃO | "por que eu faria isso?" | a economia: custo da inação, cenários, payback |
| **F** | FORMAL | "eu assino?" | escopo, preço, condições, prazo (modelo 7) |
| **C** | COLAGEM | "o que eu colo, onde, quando?" | campos e mensagens prontas (modelo 5) |

Pedido "PDF 1-D" = elétrico A4, classe decisão. Sem letra, a classe segue a régua do §3-bis (quem não visualiza recebe ESTRUTURA).

## O que vale para todos

- **Todo PDF do noturno (1 a 6) sai pelo `pdf-noturno/gerar_pdf.py`**, que reprova Type3, fita cortada e página em branco. Reprovado não se entrega.
- **Documento de cliente mora em `clientes/<Conta>/entregaveis/<AAAA-MM-DD - nome>/`**, HTML e PDF juntos, linha no `entregaveis/README.md`.
- **Parte-se do modelo da pasta, nunca do HTML do último cliente.** CSS novo por documento não existe; defeito se corrige no modelo.
- **Folha para o operador** (roteiro de call, interno): modelo 1, uma página, sem capa, rótulo "INTERNO · SÓ {{OPERADOR}}".
- 🔴 **Tudo o que é para o operador ler sai também em PDF, no modelo cinza:** modelo 1 (elétrico A4) em preto e cinza, sem fitas, com o bloco `<style>` de cinza (`--azul:#8F8F8F`, `--azul-claro:#C4C4C4`, fundo `#0A0A0A`, `.capa .botao` claro) que mora no exemplo de uma análise anterior da própria conta. Vale para pauta de call, preparação e documento interno; o pedido não precisa vir.

## A amostra visual de cada modelo

Um PDF por modelo, conta fictícia "Oficina Alvorada", rótulo "MODELO N · amostra" na capa, fonte ao lado:

| Nº | PDF |
|---|---|
| 1 | `pdf-noturno/exemplos/MODELO-1-ELETRICO-A4.pdf` |
| 2 | `pdf-noturno/exemplos/MODELO-2-ELETRICO-CELULAR.pdf` |
| 3 | `pdf-noturno/exemplos/MODELO-3-ELETRICO-CLARO-A4.pdf` (paleta `papel-musgo`) |
| 4 | `pdf-noturno/exemplos/MODELO-4-ELETRICO-CLARO-CELULAR.pdf` (paleta padrão) |
| 5 | `pdf-noturno/exemplos/MODELO-5-PACOTE-COLAGEM.pdf` |
| 6 | `pdf-noturno/exemplos/MODELO-6-NOTURNO-PURO.pdf` |
| 7 | `pdf-continuum/exemplo/MODELO-7-CONTINUUM-FORMAL.pdf` (⚠️ o `build-pdf.py` exige WeasyPrint; sem ele, sai pelo Chrome sem interface, com a capa dentro da área útil) |
| 8 | `pdf-dashboard-trafego/exemplo/MODELO-8-DASHBOARD-TRAFEGO.pdf` |
| 10 | `90-templates/roteiro-do-dia/` (o JSON é a fonte; o HTML é gerado) |
| 9 | `prancha-de-escolha/exemplo/MODELO-9-PRANCHA-DE-ESCOLHA.pdf` (🔴 defeito conhecido do modelo: o `gerar_prancha.py` carrega fontes variáveis do Google, que saem como Type3 no PDF; imprimir com fontes estáticas, como no noturno) |

Exemplos antigos continuam em `pdf-noturno/exemplos/EXEMPLO-*.pdf`.

**Modelo novo entra aqui com o próximo número livre, na mesma tarefa em que nasce** (REGRA Nº 1). Número nunca se reaproveita.
