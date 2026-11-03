# FOTO DA OPERAÇÃO — o esquema

> A foto é o único lugar de onde o relatório tira número. Quem a monta é um script (o **leitor** da empresa), sem IA. O agente lê, escreve, e o `verificar_relatorio.py` confere o texto contra ela.
> Procedência: Continuum, 31/10/2026.

## Campos

```json
{
  "empresa": "Nome da empresa",
  "pergunta": "como está a operação hoje?",
  "gerado_em": "AAAA-MM-DD HH:MM",
  "hoje": "AAAA-MM-DD",
  "areas": [
    {
      "area": "Caixa",
      "agente": "financeiro",
      "itens": [
        {"id": "caixa.entra_hoje", "rotulo": "entra hoje", "valor": 18240.0,
         "fonte": "extrato + títulos", "lido_em": "05:00"}
      ]
    }
  ],
  "precisa_de_voce": [
    {"id": "D-…", "texto": "…", "conta": "…", "prazo": "AAAA-MM-DD", "atraso_dias": 3, "fonte": "…"}
  ],
  "nao_lido": [{"fonte": "ERP", "motivo": "sem acesso ainda"}],
  "contagens": {"precisa_de_voce": 1, "precisa_por_conta": {"…": 1}}
}
```

## As réguas do leitor

1. **Todo número que o relatório pode dizer está na foto como número,** nunca só dentro de uma frase. Inclui as contagens que o texto vai usar (quantas vermelhas, quantos itens por conta, maior atraso) e os atrasos em dias, positivos.
2. **Todo item tem `fonte` e `lido_em`.** O texto cita os dois.
3. **`precisa_de_voce` sai da regra, não do gosto:** decisões abertas, marcos vencidos cujo dono é o dono, títulos vencidos, tasks em `decisao/` e o que passa da alçada (os limites ficam no repo da empresa).
4. **Fonte que não respondeu vai para `nao_lido`,** nunca fica fora calada.
5. **Texto que o relatório pode citar entre aspas** (título de marco, decisão) vai literal num campo de texto.
6. **Dado pessoal** pode estar na foto para o cálculo; quem decide se aparece é a skill (regra: só se o dono pedir).

## Leitores existentes

| Empresa | Leitor | Fontes |
|---|---|---|
| {{EMPRESA}} | `40-operacao-rotinas/ferramentas/foto-da-operacao.py` (Governança) | o payload do `painel-projetos.py`: PAINEL.md das contas, tasks, decisões, A receber |
| Cliente | na pasta de leitores do repo dele | as fontes dele: planilha de entregas, financeiro, tarefas da equipe, ponto, CRM, WhatsApp |
