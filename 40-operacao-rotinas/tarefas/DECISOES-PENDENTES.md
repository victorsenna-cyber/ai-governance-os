# DECISÕES PENDENTES — a fila do operador

> **Tipo:** registro vivo (camada 3) · **Fonte do fato:** o banco da página de decisão (se houver); **este arquivo é a memória**, regravado por `ferramentas/propagar-decisoes.py`.
> **Formato de cada cartão:** contexto em 2 linhas · opções A/B/C já escritas · recomendação · nível de autonomia do tipo (`ferramentas/autonomia.py`) · prazo. O operador responde com uma letra. A escolha vai para o `DECISOES.md` da conta (ou para `log/DECISOES-CASA.md`) com data, hora e a letra literal.

## Abertas

*(nenhuma)*

### Modelo de cartão
```
### D-AAAA-MM-DD-nnn · <Conta ou Casa> — <título> · tipo `<tipo_decisao>` · autonomia A0 · prazo <data ou "sem prazo">
**Contexto:** <2 linhas>
- **A)** <opção>
- **B)** <opção>
- **C)** <opção>
**Recomendação:** <letra>. **O que acontece:** <consequência da recomendada>.
```

## Decididas

*(o `propagar-decisoes.py` move para cá, com data, hora e a letra literal; o par recomendação × escolha alimenta `ferramentas/autonomia.py`)*
