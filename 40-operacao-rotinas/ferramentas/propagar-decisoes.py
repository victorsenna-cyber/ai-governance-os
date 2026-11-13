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


APELIDOS = {}   # rótulo de cartão (minúsculo) → nome da pasta em clientes/, quando o rótulo não é o nome da pasta
# Conta de parceiro mora em parceiros/<Parceiro>/ e resolve por contas_da_casa.py


def pasta_da_conta(rotulo):
    """Rótulo do cartão → pasta em clientes/. None = casa (ou rótulo sem pasta: vai para DECISOES-CASA com aviso)."""
    r = (rotulo or "").strip()
    base = os.path.join(RAIZ, "clientes")
    if not r or r.lower() in ("casa", "comercial") or not os.path.isdir(base):
        return None
    if os.path.isdir(os.path.join(base, r)):
        return r
    if r.lower() in APELIDOS and os.path.isdir(os.path.join(base, APELIDOS[r.lower()])):
        return APELIDOS[r.lower()]
    pastas = [n for n in os.listdir(base) if os.path.isdir(os.path.join(base, n)) and not n.startswith("_")]
    for n in pastas:   # o conta: do frontmatter do PAINEL.md
        p = os.path.join(base, n, "PAINEL.md")
        if os.path.exists(p):
            m = re.search(r"^conta:\s*(.+)$", io.open(p, encoding="utf-8").read(2000), re.M)
            if m and m.group(1).strip().lower() == r.lower():
                return n
    # subprojeto de cliente (clientes/<Conta>/<subpasta>/PAINEL.md, conta: próprio) decide no DECISOES da mãe
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        import contas_da_casa
        pp = contas_da_casa.pasta_da_conta(RAIZ, r)
        if pp and contas_da_casa.eh_subprojeto(RAIZ, pp):
            return os.path.basename(os.path.dirname(os.path.normpath(pp)))
    except ImportError:
        pass
    mesmas = [n for n in pastas if n.lower().split()[0] == r.lower().split()[0]]
    return mesmas[0] if len(mesmas) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=JSON_PADRAO)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if not os.path.exists(a.json):
        print(f"sem {os.path.relpath(a.json, RAIZ)}: exporte a coleção `decisoes` da página primeiro."); return 1
    dados = json.load(io.open(a.json, encoding="utf-8"))
    docs = dados if isinstance(dados, list) else (dados.get("documents") or dados.get("docs") or [])
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
        if esc.upper() == "LIVRE":      # o botão "enviar" do sistema, sem letra (resposta livre)
            esc, nota = "resposta livre", nota
            linha = f"- **{quando}** · resposta livre do {{{{OPERADOR}}}} (sem letra): {nota}" + (f" · recomendado: {rec}" if rec else "")
        else:
            linha = f"- **{quando}** · escolha literal: **{esc}**" + (f" · ajuste: {nota}" if nota else "") + (f" · recomendado: {rec}" if rec else "")
        abertas = abertas.replace(cartao, "", 1)
        decididas = decididas.rstrip("\r\n") + nl + nl + cartao + nl + linha + nl
        # DECISOES.md da conta (o rótulo do cartão não é, necessariamente, o nome da pasta; nunca se cria pasta)
        pasta = pasta_da_conta(conta)
        if not pasta:   # conta de parceiro: o DECISOES.md da pasta do parceiro, versionado na Governança
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            try:
                import contas_da_casa
                pp = contas_da_casa.pasta_da_conta(RAIZ, conta)
                pasta = os.path.relpath(pp, os.path.join(RAIZ, "clientes")) if pp and os.sep + "parceiros" + os.sep in pp else None
            except ImportError:
                pasta = None
        destino = os.path.join(RAIZ, "clientes", pasta, "DECISOES.md") if pasta else os.path.join(TAR, "log", "DECISOES-CASA.md")
        if not pasta and conta.lower() not in ("casa", "comercial"):
            nota = (nota + " · " if nota else "") + f"conta '{conta}' sem pasta em clientes/"
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
