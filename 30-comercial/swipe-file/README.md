# SWIPE FILE CONTINUUM — memória de padrão

> **Tipo:** ativo acumulativo (camada 3) · **Alçada:** {{OPERADOR}}
> **Vale para TODO o método Continuum**, não só para VSL: anúncio, página, VSL, mensagem fria, proposta, roteiro, e-mail.
> **Gatilho e obrigatoriedade:** `CLAUDE.md` §11.5.

---

## 1. O que isto é, e por que não é uma pasta de inspiração

> **Reconhecer que uma peça está fora do padrão do que vende não é intuição — é estatística acumulada em forma de repertório.**

Quem leu centenas de peças **que comprovadamente venderam** carrega o padrão sem precisar consultá-lo. É isso que este diretório constrói: não um arquivo para copiar, **um treino de olho.**

> ⭐ **É o único ativo do método que se valoriza com o tempo, e o único que não se terceiriza.** Skill se instala, método se lê, repertório se acumula — e só acumula em quem passou os olhos.

---

## 2. 🔴 GATILHO DE ENTRADA — o que qualifica, e é medível

**Peça sem dado não entra. Peça bonita e morta contamina o repertório e é pior que pasta vazia.**

### 2.1 Peça NOSSA → `nosso/`

| Gatilho | Critério |
|---|---|
| **Criativo escalou** | ≥ 7 dias em veiculação **com CPA ≤ meta do plano** |
| **Peça de conversão bateu breakeven** | VSL, página ou funil que se pagou |
| **Peça 1-a-1 fechou venda** | mensagem, proposta ou script que produziu pagamento registrado |
| **Peça superou a anterior** | conversão medida acima da referência anterior **da mesma conta** |

### 2.2 Peça de MERCADO → `mercado/`

| Gatilho | Critério |
|---|---|
| **Validada no benchmark** | passou o gate de evidência do `METODO-BENCHMARKING.md` §3.2 — nº de anúncios ativos, tráfego medido, ou tempo em veiculação. **Para VSL, a leitura de padrão vem da destilação** (`METODO-DESTILACAO-DE-VSL.md` §11) |

### 2.3 O que NUNCA entra

- Peça nossa que **ainda não rodou** — por melhor que esteja
- Peça de terceiro **sem evidência de que vende** — inclusive de player conhecido
- Peça que "ficou boa" — **impressão não é gatilho**

---

## 3. 🔴 O que se registra — padrão, nunca texto

**Trava permanente, e vale para os dois diretórios:**

> **Registra-se estrutura, dose, ordem e categoria de argumento. Não se cola copy alheia.**
> Em `nosso/`, a peça própria pode ir na íntegra — é nossa.
> Em `mercado/`, vai a **leitura**: a ordem dos elementos, o volume por bloco, o mecanismo nomeado, o tipo de prova. **Trecho literal só como âncora curta de análise.**

### Formato de cada entrada

```
## [data] · [tipo de peça] · [nicho] · [nosso | mercado]

**O DADO QUE QUALIFICOU** — o número, com fonte e janela

**O PADRÃO** — ordem dos elementos · volume por bloco · mecanismo · tipo de prova dominante

**O QUE ESTA PEÇA ENSINA** — 1 a 3 linhas. Se não dá para escrever isto, a entrada não vale

**ONDE REUSAR** — em que tipo de peça e em que condição

**FONTE** — caminho no repo, ou link + data da coleta
```

⚠️ **O campo "o que esta peça ensina" é o gate da entrada.** Sem ele, o arquivo vira depósito — e depósito não produz repertório.

---

## 4. Organização

```
swipe-file/
├── nosso/      peças nossas com dado — podem ir na íntegra
└── mercado/    leitura de peças de terceiro — padrão, nunca texto integral
```

**Dentro de cada um, um arquivo por tipo:** `vsl.md` · `anuncios.md` · `paginas.md` · `mensagens.md` · `propostas.md` · `roteiros.md`. **Nicho vai como tag na entrada**, não como subpasta — nicho novo não deve criar estrutura nova.

---

## 5. Revisão

**Trimestral, e é uma pergunta só:** alguma entrada envelheceu a ponto de ensinar o errado?
**Entrada obsoleta não se apaga** (regra de não-deleção) — **marca-se `[SUPERADA em <data>: <o que mudou>]`.** Saber que um padrão parou de funcionar é tão valioso quanto saber que funcionava.

---
*Alimentado automaticamente pela regra `CLAUDE.md` §11.5. **Fonte canônica de benchmark: `100-métodos/METODO-BENCHMARKING.md`** (ponteiros para `METODO-FUNIL-DE-VSL.md` §4). Extração de VSL: `METODO-DESTILACAO-DE-VSL.md`.*
