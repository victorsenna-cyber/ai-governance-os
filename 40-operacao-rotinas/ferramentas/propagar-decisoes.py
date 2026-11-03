# -*- coding: utf-8 -*-
"""
propagar-decisoes.py — leva as escolhas feitas na página de decisão para o repo.

Fonte do fato: o banco da página (coleção `decisoes`, um documento por cartão, com o
campo `escolha` = "A"|"B"|"C"|"veto"|"adiar" e `escolhido_em`). Quem lê o banco é a
sessão do Claude (ferramenta ArtifactData, `list` da coleção) e salva o JSON em
40-operacao-rotinas/tarefas/log/decisoes-pagina.json. Este script faz o resto:

  1. Para cada cartão com `escolha` e ainda "Aberto" no DECISOES-PENDENTES.md: move o
     cartão para "Decididas" com data, hora e a letra literal.
  2. Acrescenta a decisão ao DECISOES.md da conta (campo `conta`), ou ao
     40-operacao-rotinas/tarefas/log/DECISOES-CASA.md quando conta = casa.
  3. Registra o par recomendação × escolha em DECISOES.jsonl (autonomia.py).

  python3 propagar-decisoes.py [--json caminho] [--dry-run]
"""
import argparse, datetime, io, json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TAR = os.path.join(RAIZ, "40-operacao-rotinas", "tarefas")
PEND = os.path.join(TAR, "DECISOES-PENDENTES.md")
JSON_PADRAO = os.path.join(TAR, "log", "decisoes-pagina.json")
AUTONOMIA = os.path.join(RAIZ, "40-operacao-rotinas", "ferramentas", "autonomia.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=JSON_PADRAO)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.exists(a.json):
        print(f"sem {os.path.relpath(a.json, RAIZ)}: exporte a coleção `decisoes` da página primeiro."); return 1
    dados = json.load(io.open(a.json, encoding="utf-8"))
    docs = dados.get("documents") or dados.get("docs") or dados if isinstance(dados, list) else dados.get("documents", [])
    if isinstance(docs, dict):
        docs = [dict(v, id=k) for k, v in docs.items()]
    texto = io.open(PEND, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in texto else "\n"
    abertas, decididas = texto.split("## Decididas", 1)
    n = 0
    for d in docs:
        did = d.get("id") or d.get("doc_id") or ""
        esc = (d.get("escolha") or "").strip()
        if not did or not esc:
            continue
        m = re.search(rf"(### {re.escape(did)}[^\n]*\n(?:(?!### ).*\n?)*)", abertas)
        if not m:
            continue
        cartao = m.group(1).rstrip("\r\n")
        quando = d.get("escolhido_em") or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        rec = re.search(r"\*\*Recomendação:\*\*\s*([A-C])", cartao)
        rec = rec.group(1) if rec else ""
        tipo = re.search(r"tipo `([^`]+)`", cartao); tipo = tipo.group(1) if tipo else "sem_tipo"
        conta = d.get("conta") or re.search(r"### [^·]+· ([^—·]+?) —", cartao)
        conta = conta if isinstance(conta, str) else (conta.group(1).strip() if conta else "casa")
        nota = d.get("ajuste") or ""
        linha = f"- **{quando}** · escolha literal: **{esc}**" + (f" · ajuste: {nota}" if nota else "") + (f" · recomendado: {rec}" if rec else "")
        abertas = abertas.replace(cartao, "", 1)
        decididas = decididas.rstrip("\r\n") + nl + nl + cartao + nl + linha + nl
        # DECISOES.md da conta
        destino = os.path.join(RAIZ, "clientes", conta, "DECISOES.md") if conta.lower() != "casa" else os.path.join(TAR, "log", "DECISOES-CASA.md")
        registro = (f"{nl}## {did} — decidido em {quando} (página de decisão){nl}{nl}"
                    f"**Escolha literal do {{OPERADOR}}:** {esc}{(' · ajuste: ' + nota) if nota else ''}. **Recomendado:** {rec or '—'}. **Tipo:** `{tipo}`.{nl}{nl}{cartao}{nl}")
        print(f"{did}: escolha {esc} (recomendado {rec or '—'}) → {os.path.relpath(destino, RAIZ)}")
        if not a.dry_run:
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            io.open(destino, "a", encoding="utf-8", newline="").write(registro)
            veto = ["--veto"] if esc.lower() == "veto" else []
            subprocess.run([sys.executable, AUTONOMIA, "--registrar", did, tipo, rec or "-", esc] + veto, cwd=RAIZ)
        n += 1
    if n and not a.dry_run:
        abertas = re.sub(r"\n{3,}", "\n\n", abertas)
        io.open(PEND, "w", encoding="utf-8", newline="").write(abertas + "## Decididas" + decididas)
    print(f"propagadas: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
