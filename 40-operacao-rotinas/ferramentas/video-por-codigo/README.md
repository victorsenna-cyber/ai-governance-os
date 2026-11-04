# AVISO — vídeo feito por código: motor e biblioteca de prompts

> **Tipo:** ponteiro de recurso (não é método) · **Alçada:** {{OPERADOR}}
> ⚠️ **Recurso opcional, instalado fora da Governança.** Este arquivo é o aviso de que ele existe, para quando for preciso criar vídeo por código (para a casa e para clientes), incluindo edição de VSL, em que as imagens ilustrativas são decisivas.
> **Carrega-se por:** `00-core/roteador/ARVORE-OPERACAO.md` (linha de vídeo por código) e pela linha de VSL da `ARVORE-ESCRITA.md`, na etapa de edição.

---

## 1. O que existe, e onde

| Recurso | Onde | O que faz |
|---|---|---|
| **Motor** — plugin HyperFrames | skills `hyperframes:*` do Claude Code (entrada: `hyperframes:hyperframes`) · fonte do plugin instalada fora da Governança | escreve a animação como HTML (GSAP, Canvas, SVG, Three.js) e renderiza em vídeo. Cobre motion graphic, explainer, legenda, sobreposição em vídeo gravado e a remontagem de talking head (`hyperframes:talking-head-recut`) |
| **Biblioteca** — *awesome-opus5-5-videos* | repositório público instalado em pasta de repositórios de apoio · **fora da Governança, de propósito** | 703 prompts de vídeos feitos pelo Opus 5.5 escrevendo código: motion 369 · 3D 117 · explainer 116 · interativo 101. Um `.md` por vídeo em `prompts/` e o índice em `data/videos.json` (autor, post original, categoria, tecnologia). **207 prompts estão incompletos** (`prompt_partial: true`) |
| **Corte de fala** — ferramenta da casa | `40-operacao-rotinas/ferramentas/edicao-video/` | corte do bruto, jump cut, legenda, áudio a −14 LUFS. **Não faz** b-roll, imagem nem motion: é daqui que esses pedidos saem |

## 2. Quando acender

Todo pedido de vídeo **que não seja só cortar fala gravada**:

- 🔴 **imagens ilustrativas de VSL**: a camada visual que acompanha a fala do expert, bloco a bloco; é importantíssima na VSL. A composição de cada VSL fica no `COMPOSICAO-VSL.md` da conta
- b-roll, motion graphic, texto animado, diagrama animado, explainer de produto ou serviço, vídeo de lançamento, anúncio em vídeo animado, vinheta de marca
- vídeo para nós (`950-marketing/`) **e** para conta de cliente

## 3. Como usar a biblioteca

Ela é **repertório de forma**: ritmo, transição, linguagem visual e a maneira de pedir. Achar o prompt-modelo pelo tipo de peça:

```powershell
python3 -I -c "import json,sys; d=json.load(open(sys.argv[1],encoding='utf-8')); [print(x['slug'],'|',x['category'],'|',x['prompt'][:140].replace(chr(10),' ')) for x in d if x['category']==sys.argv[2] and not x['prompt_partial']]" "<pasta do repositório>\awesome-opus5-5-videos-main\data\videos.json" explainer
```

Pontos de partida já lidos: `alex-prompter-997524` (explainer de 30 s em 5 cenas: dor → o que faço → 3 passos → prova → nome) · `redpersongpt-284430` (anúncio de app: "base tudo no produto real, não invente feature") · `verbove-268381` e `twoclipping-000267` (pedem os insumos antes de começar: telas reais, cores, música) · `felipemoller-936736` (9:16 com Playwright e FFmpeg, em português).

**O padrão que se aproveita dos melhores prompts:** pedir os insumos antes de animar (produto real, telas reais, dados reais, cores, fonte, música) e proibir o inventado. É a nossa régua de procedência escrita por outra pessoa.

## 4. 🔴 Veto — reprova sozinho

| Veto | Por quê |
|---|---|
| **prompt da biblioteca usado como estrutura de venda** (promessa, lead, ordem de elementos) | "viral no X entre devs" não é escalado no sentido da REGRA Nº 2. A estrutura vem da referência escalada e do roteiro aprovado; daqui vem só a forma |
| **imagem ilustrativa que cria fato** (número, depoimento, resultado, cliente, cena que a fala não diz) | procedência: a imagem ilustra o que a frase diz no mesmo segundo, nunca acrescenta prova |
| **edição de VSL sem roteiro aprovado e sem laudo do A7** | a camada visual se monta sobre a versão que vai ao ar (`METODO-PRODUCAO-VSL-POR-AGENTES.md` §5) |
| **render final sem roteiro visual aprovado pelo {{OPERADOR}}** (bloco → segundo → o que aparece) | mesma regra do corte em `METODO-EDICAO-DE-VIDEO-CURTO.md`: quem decide o que vai ao ar aprova antes do render |
| **texto, logo ou arte de terceiro copiados do vídeo de referência** | modela-se a forma; texto e marca de outro nunca entram |

## 5. O que este recurso ainda não resolve

- **Gerar imagem** (foto, ilustração) pede um gerador com chave. O HyperFrames compõe e anima o que recebe. Para gerar imagem, a ferramenta escolhida se instala isolada e **só entra na iteração com permissão do {{OPERADOR}}**.
- Não há método de edição de VSL. Este arquivo é aviso e veto. **O método nasce do primeiro caso real de VSL de uma conta**, pela REGRA Nº 1 e pelo `CLAUDE.md` §7.1, item 4.

*Licença da biblioteca: MIT (`LICENSE` na pasta). Os prompts são dos autores citados em cada arquivo, que linka o post original.*
