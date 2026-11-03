# COMO MODELAR UMA REFERÊNCIA DESTA PASTA

> Regra do {{OPERADOR}}: as proporções dos criativos feitos com base em referências são iguais às referências, com as mesmas composições e elementos nos mesmos pixels. As cores podem e, na maior parte das vezes, precisam mudar, mas isso fica no planejamento. Alterações de proporção e composição são aprovadas ou sinalizadas.
> Vale para todo criativo, de qualquer conta, feito a partir de um arquivo desta pasta. A leitura de cada referência e os IDs (V001 em diante) ficam em `../945-branding/01 - identidade visual/` (arquivo `LEITURA-REFERENCIAS-960-<data>.md`, gerado quando você coletar as primeiras referências).

## 1. A regra

| O que é | Regra |
|---|---|
| **Proporção** (tamanho de cada elemento em relação à tela) | **igual à referência** |
| **Composição** (posição, ordem, alinhamento e espaço entre os elementos) | **igual à referência: cada elemento no mesmo pixel**, medido na escala da peça final |
| **Elementos** (figurinha, cartão, selo, avatar, tarja, ícone, emoji, botão) | **os mesmos.** Nada se acrescenta e nada se tira |
| **Cor** | **pode mudar, e quase sempre muda** para a identidade da conta. A troca é decidida no **planejamento**, antes da produção, e registrada no `PLANO-COPY.md` ou no `CRIATIVO.md` do lote |
| **Texto** | é da conta, com procedência (regras de copy e de procedência da casa) |
| **Qualquer mudança de proporção, composição ou elemento** | 🔴 **só com aprovação do {{OPERADOR}}, ou sinalizada por escrito na entrega** (o que mudou, quanto e por quê). Mudança silenciosa reprova a peça |

## 2. Como medir, sempre

1. **Escala:** a referência é um print (ex.: 828 × 1792). A peça final tem 1080 × 1920 (story) ou 1080 × 1350 (feed). Fator = largura da peça ÷ largura da referência.
2. **Medir no pixel**, não no olho: caixa de cada elemento (x, y, largura, altura), tamanho do texto pela altura da letra, distâncias entre elementos. Um script de leitura de pixels (Python + Pillow) resolve.
3. **Multiplicar pelo fator** e montar a peça com esses números.
4. **Conferir lado a lado** (referência × peça, na mesma escala) antes de entregar, e salvar a comparação na pasta `referencias/` do lote.

Exemplo medido (selo de verificado de um print de tuíte): no print, selo de 24 px, nome com 25 px de altura e 23 px de distância entre eles. Na peça, com nome de 35 px: selo de 34 px e 32 px de distância.

## 3. O que já deu errado (para não repetir)

- **Copiar o estilo e perder o mecanismo.** Numa referência, a gravura virou foto em círculo e a mensagem virou promessa, sem entregar nada. Em outra, a conta com números grandes virou uma lista. As duas peças foram reprovadas.
- **Pôr algo onde a referência não tem nada.** No tuíte, as faixas pretas são o preenchimento do Instagram em volta do print. Um "Siga @…" ali quebra a ilusão de print.
- **Simular foto real em desenho.** Um flip chart feito em HTML ficou ruim. Formato fotográfico pede foto de verdade.
- **Compor "de cabeça".** O espaço entre os elementos, o tamanho de cada bloco e o alinhamento se medem. Não se estimam.

## 4. Quando a peça precisa ser diferente

Formato diferente da referência (ex.: referência de feed usada em story), texto que não cabe na mesma composição, elemento que não existe na conta: **para e pergunta, ou entrega sinalizado**, com a referência e a peça lado a lado e a lista do que mudou.
