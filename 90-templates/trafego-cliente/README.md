# Template — pasta de tráfego pago do cliente

> **Tipo:** blueprint · regra: cada cliente tem um repo próprio e tudo relacionado a ele mora nele; a pasta `30-comercial/` é só dos processos comerciais da {{EMPRESA}}.
> O método que governa tudo: `100-métodos/METODO-TRAFEGO-PAGO.md` (fonte em `100-métodos/`).

## Onde isto mora

**Dentro do cliente, nunca em `30-comercial/`:** `clientes/<Cliente>/NN - tráfego pago/`. `NN` é o número que a pasta tem na numeração do cliente; se a pasta não existe, cria-se com o próximo número livre. (Se uma conta herdou outro nome para a pasta, ex.: `NN - mídia paga/`, não renomear sem decisão.)

- **Tráfego pago** — briefing, plano de mídia, estrutura de campanhas, matriz de criativos, log de decisões, relatórios, scripts de criação de campanha, `painel.json` do painel de resultado → `NN - tráfego pago/`.
- **Páginas e site do cliente** (e a configuração de publicação delas) → `NN - web design/` do cliente.
- Criativos pesados (vídeo, imagem, exports de plataforma) ficam na pasta de criativos do cliente; referenciar no rodapé `Base:` de cada artefato.

`30-comercial/` guarda só os processos comerciais da {{EMPRESA}} (ICP, oferta, prospecção, onboarding). Nada de cliente.

## O que o template traz

`BRIEFING.md` · `PLANO-DE-MIDIA.md` · `estrutura-campanhas.md` · `matriz-criativos.md` · `LOG-DECISOES.md` · `relatorios/README.md` · **`diario/`** (o diário de campanha do `METODO-ANALISE-DIARIA-DE-CAMPANHA.md` — `AAAA-MM-DD.md` da coleta e `AAAA-MM-DD-ANALISE.md` da análise e implementação). Só markdown leve: é o que se carrega para operar o cliente.

## Como abrir um cliente novo

1. Passou no **gate de entrada** (`100-métodos/METODO-TRAFEGO-PAGO.md` §1)? Senão, não abre pasta.
2. Copiar o conteúdo deste template para `clientes/<Cliente>/NN - tráfego pago/` e preencher `BRIEFING.md`.
3. Preencher `PLANO-DE-MIDIA.md` (matemática reversa §2.2 assinada pelo cliente).
4. Seguir a cadeia do método: página (`NN - web design/`) → criativos → estrutura → tracking → gestão.

## Mudança de canal ou de estrutura *(regra da casa)*

Quando o canal muda (Google → Meta, por exemplo) ou a estrutura muda (objetivo, destino, verba), **a mudança não está feita até os arquivos de parâmetro dizerem a mesma coisa:** `PLANO-DE-MIDIA.md` (o plano antigo vai para `PLANO-DE-MIDIA-<CANAL>-<AAAA-MM>.md` com cabeçalho de arquivamento e o porquê), `estrutura-campanhas.md` (mapa vivo), `BRIEFING.md`, `LOG-DECISOES.md`, e o `PAINEL.md` + `STATUS.md` §1 do cliente. A análise diária (`METODO-ANALISE-DIARIA-DE-CAMPANHA.md` §3.1) carrega o plano e **para** se ele não for do canal que roda.

## Painel de resultado

Ferramenta nossa, em `40-operacao-rotinas/ferramentas/painel-resultado/` (atalho "Painel de Resultado" na área de trabalho). Onde se lançam os números de cada cliente e se lê a projeção; o `servir.py` grava o `painel.json` na pasta de tráfego do cliente (`clientes/<Cliente>/NN - tráfego pago/painel.json`) e sincroniza com a main. Detalhe: o `README.md` da ferramenta.

## Clientes com pasta de tráfego (a lista viva é `clientes/`)

A lista de quais clientes têm pasta de tráfego é a própria `clientes/` (cada um com `NN - tráfego pago/`). O estágio, a verba e o status de cada conta moram no `STATUS.md` do cliente, não aqui: uma tabela de clientes ativos neste README envelheceria.
