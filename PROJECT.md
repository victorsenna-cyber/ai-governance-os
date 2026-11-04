# PROJECT.md — {{EMPRESA}}

> Identidade e contexto da empresa. **Fonte** para `20-projeto-escopo/` e para o papel do `CLAUDE.md`. Em conflito de fato atual, `STATUS.md` prevalece.
> ⚠️ **MODELO — preencher.** Campo sem resposta vira `A CONFIRMAR`, nunca palpite.

## 1. Identidade

| Campo | Valor |
|---|---|
| Nome | {{EMPRESA}} |
| O que somos, em uma frase | `{{…}}` |
| Operador / alçada | {{OPERADOR}} (100%) |
| Constituição | `{{CNPJ ou "sem CNPJ, em fase de construção de caixa"}}` |
| Cidade / fuso | `{{…}}` |
| **Vocabulário de trabalho do operador** (`CLAUDE.md` §5.1 lê daqui) | `{{termos, modelos e referências que o operador usa sem tradução — ex.: o jargão técnico ou simbólico da sua área; a IA os usa como língua de trabalho e só distingue simbólico de empírico quando muda uma decisão}}` |

## 2. Princípio fundador

**Quem integra o sistema vence com ele. Quem o ignora, é vencido por ele.** (`00-core/PRINCIPIO-CONTINUUM.md`). `{{A leitura própria do operador sobre o princípio, se houver.}}`

## 3. Missão · Visão · Valores

- **Missão:** `{{…}}`
- **Visão:** `{{…}}`
- **Valores:** os de `00-core/CULTURA.md` (comportamento, não cartaz), mais `{{os seus}}`.

## 4. Problema que resolvemos

`{{a dor estrutural do ICP, em uma frase com verbo — ver 30-comercial/ICP.md §1}}`

## 5. O que fazemos (dimensões)

| Dimensão | O que entregamos | Onde está o método |
|---|---|---|
| Estratégia | `{{…}}` | `100-métodos/METODO-DIAGNOSTICO-DE-OPERACAO.md`, `METODO-ALICERCE.md` |
| Comercial | `{{…}}` | `30-comercial/`, `100-métodos/METODO-ABORDAGEM-FRIA.md`, `METODO-ANCORAGEM-DE-PROPOSTA.md` |
| Marketing | `{{…}}` | `METODO-DIRECT-RESPONSE.md` e galhos, `100-métodos/METODO-TRAFEGO-PAGO.md` |
| Onboarding / CS | `{{…}}` | `30-comercial/onboarding.md` |
| Financeiro | `{{…}}` | `00-core/POLITICAS-DE-DECISAO.md`, `45-financeiro/` |
| Operação | `{{…}}` | `40-operacao-rotinas/` |
| Dados | `{{…}}` | `50-integracoes-dados/` |
| Cultura | `{{…}}` | `00-core/CULTURA.md` |
| Tecnologia | `{{…}}` | `30-comercial/produtos.md` |

## 6. Produto / Plataforma

`{{o que existe, em que fase, com que gate de venda — ver 30-comercial/produtos.md}}`

## 7. Modelo de negócio

Setup + recorrência; serviço avulso só como porta de entrada (`00-core/POLITICAS-DE-DECISAO.md` §5). Escada em `30-comercial/oferta.md` §3.

## 8. Sociedade / Governança societária

`{{quem detém o quê; instrumento escrito e data; se não houver instrumento, escrever "acordo verbal — não oponível" e abrir pendência em 80-juridico/societario/}}`

## 9. Stack / Infraestrutura

| Função | Ferramenta | Dono / conta |
|---|---|---|
| Agente que carrega este kernel | `{{Claude Code / outro}}` | {{OPERADOR}} |
| Repositório | git, remoto privado | {{OPERADOR}} |
| CRM | `{{…}}` | |
| Automação | `{{…}}` | |
| Site / páginas | `{{…}}` | |
| Painéis (opcional) | Supabase + GitHub Actions (`980-web-design/painel-*/`) | |

## 10. Referências internas

`{{pastas irmãs fora deste repositório, se existirem — são proveniência, não leitura obrigatória}}`
