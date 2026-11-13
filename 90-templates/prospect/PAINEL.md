---
prospect: Nome como aparece na conversa
etapa: contato
dor: 
dor_fonte: 
produto: 
oferta_recomendada: 
oferta_gatilho: 
dor_sem_produto: 
valor: 
recorrencia: 
meses: 
probabilidade: 
validade: 
proximo_passo: 
proximo_prazo: 
decisor: 
origem: 
ultimo_toque: 
embarque_jornada: 
embarque_primeiro_valor: 
embarque_plano: 
aceite: 
motivo_perda: 
atualizado: AAAA-MM-DD
---
# PAINEL — <prospect>

> **A ficha do prospect.** Camada de máquina no frontmatter acima, lida por `40-operacao-rotinas/ferramentas/painel-projetos.py` → área **Comercial** do sistema. Os fatos moram no `REGISTRO.md` e nas destilações desta pasta; aqui só o que o funil precisa.
> Método do Embarque: `100-métodos/METODO-ONBOARDING-ORQUESTRADO.md` §3.

## Os campos

| Campo | O que é | Valores |
|---|---|---|
| `etapa` | onde está no funil, na ordem da casa (`CLAUDE.md` §9.1) | `contato` · `g0` (diagnóstico pago ou em curso) · `ancoras` (âncoras e veredito) · `proposta` (enviada) · `aceite` · `perdido` |
| `dor` · `dor_fonte` | a dor que decide a oferta, em uma linha · de onde ela vem (`100-métodos/METODO-DECISAO-DE-OFERTA.md` §2): fala dela, fato observado por nós, indicador, ou leitura nossa | texto · `D` · `O` · `I` · `V` (I e V são hipótese: o sistema alerta "oferta com dor só de indicador") |
| `produto` | nome do catálogo (`POLITICAS-DE-DECISAO.md` §5): o que vai na proposta, depois da escolha do operador | ex.: Mapa da Ordem, Assessoria Estratégica |
| `oferta_recomendada` · `oferta_gatilho` | o que o método recomendou (pode diferir do `produto`, se o operador trocou) · o fato que troca a recomendação | texto · "se X, Y passa a valer" |
| `dor_sem_produto` | a dor não cabe em produto do catálogo (método §5; 3 fichas com a mesma dor viram alerta) | `sim` · vazio |
| `valor` | o valor da proposta: mensalidade, se `recorrencia: mensal`; total, se `projeto` | número, sem R$ |
| `recorrencia` · `meses` | mensal ou projeto · meses do contrato | `mensal` · `projeto` |
| `probabilidade` | só se diferente do padrão da etapa (contato 10 · g0 25 · ancoras 40 · proposta 60) | 0–100 |
| `validade` | até quando a proposta vale | data |
| `proximo_passo` · `proximo_prazo` | o próximo ato e a data | texto · data |
| `decisor` | quem decide do lado dele | texto |
| `origem` | indicação, inbound, prospecção, rede | texto |
| `ultimo_toque` | só se não houver captura de WhatsApp na pasta (o leitor pega a data dela) | data |
| `embarque_*` | a checklist de Embarque: jornada de onboarding mostrada · primeiro valor datado no esboço · esboço do plano de sucesso | `sim` · `nao` |
| `aceite` | data do aceite: vira o `onb_d0` da conta | data |
| `motivo_perda` | por que não fechou, literal quando houver | texto |
