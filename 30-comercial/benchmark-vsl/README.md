# 30-comercial/benchmark-vsl — VSLs de terceiro destiladas sem conta

> **Lugar de VSL de mercado lida pela casa quando o pedido não é de nenhuma conta.** VSL lida para uma conta vai para `clientes/<cliente>/benchmark-vsl/`, nunca para cá.
> **Rota:** `00-core/roteador/ARVORE-LEITURA.md` (linha *VSL, podcast ou peça de terceiro*) → `100-métodos/METODO-DESTILACAO-DE-VSL.md` → `90-templates/benchmark-vsl/DESTILACAO-VSL.md`.
> 🔴 **Grau `R` / `[B]`, sempre.** Nada daqui entra em `lexico-icp/`. Estudo sem evidência de escala **não é base de construção** (REGRA Nº 2) e não entra no swipe file (`CLAUDE.md` §11.5).

## Uma pasta por peça

```
<peça>/
├── fontes/
│   ├── R1-BRUTO.<ext>        vídeo original, nunca editado
│   ├── R1-BRUTO.md           transcrição da máquina, íntegra (transcrever-audio.py)
│   ├── R1-LIMPO.md           limpa por script, com total de palavras
│   └── limpar_e_contar.py    o script da limpeza e da contagem
└── DESTILACAO-R1.md          a saída do método
```

## Índice

| Peça | Data | Estado de escala | Formato | Destilação |
|---|---|---|---|---|
| *(uma linha por peça destilada: nome da peça, nicho e preço do produto)* | `AAAA-MM-DD` | escalado / em escala / testando (REGRA Nº 2) | formato da VSL | `<pasta-da-peça>/DESTILACAO-R1.md` |
