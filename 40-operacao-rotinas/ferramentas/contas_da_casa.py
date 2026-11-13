"""contas_da_casa.py — onde mora cada conta que o sistema lê.

Toda conta é uma pasta de `clientes/`. Projeto em sociedade pode ser repo próprio dentro de `parceiros/<Parceiro>/`
(ignorado pela Governança: o Action do GitHub não o enxerga); o cartão do projeto no sistema mora então na pasta do
parceiro, versionada aqui: `parceiros/<Parceiro>/PAINEL.md`, e o nome da conta é o `conta:` dele.

Projeto novo de uma conta que já existe, com contrato próprio, vira **subprojeto**: uma subpasta da conta com `PAINEL.md` e
`conta: <Conta> · <Projeto>` no frontmatter. Ele tem cartão, marcos, tasks, contrato, recebido e régua de onboarding
próprios; **fato, decisões, captura e silêncio continuam na conta-mãe** (a pasta acima: `STATUS.md`, `DECISOES.md`,
`01 - contexto/`, `entregaveis/`), nunca duplicados. Exemplo: `clientes/<Conta>/04 - app/PAINEL.md`.

Uma regra só, usada por painel-projetos.py, acoes_do_painel.py, propagar-decisoes.py, entregaveis.py e comercial_regras.py:
  clientes/<Conta>/                          → conta "<Conta>" (o nome da pasta)
  clientes/<Conta>/<subpasta>/PAINEL.md      → subprojeto: conta = o `conta:` do frontmatter (tem de existir e ser
                                               diferente de "<Conta>"); vem logo depois da conta-mãe
  parceiros/<Parceiro>/PAINEL.md             → conta = o `conta:` do frontmatter (sem ele, o nome da pasta do parceiro)
Pasta de parceiro sem PAINEL.md não é conta (é só a relação). Subpasta que começa com "_" ou "." nunca é subprojeto.
Nunca cria pasta.

Dinheiro: o `contrato:`/`recebido:` de cada PAINEL é só do seu contrato. Um lançamento do financeiro (mesma contraparte)
vai para o subprojeto quando o `financeiro_ref:` dele aparece na descrição do lançamento; o resto fica na mãe
(painel-projetos.py). Sem `financeiro_ref:`, o subprojeto não pega lançamento nenhum: nada se conta duas vezes.
"""
import io, os, re

PARCEIROS = "parceiros"


def _conta_do_painel(arq):
    try:
        cab = io.open(arq, encoding="utf-8").read(3000)
    except OSError:
        return None
    m = re.search(r"^conta:\s*(.+?)\s*$", cab, re.M)
    return m.group(1).strip() if m else None


def _subprojetos_da_pasta(pasta_mae, nome_mae):
    """[(nome, pasta)] das subpastas com PAINEL.md e `conta:` próprio (diferente do da mãe)."""
    out = []
    try:
        filhas = sorted(os.listdir(pasta_mae))
    except OSError:
        return out
    for s in filhas:
        p = os.path.join(pasta_mae, s)
        painel = os.path.join(p, "PAINEL.md")
        if s.startswith(("_", ".")) or not os.path.isdir(p) or not os.path.exists(painel):
            continue
        nome = _conta_do_painel(painel)
        if nome and nome.lower() != nome_mae.lower():
            out.append((nome, p))
    return out


def contas(raiz):
    """[(nome, pasta_absoluta, pasta_relativa_com_barra_normal)] — clientes primeiro (cada um seguido dos seus
    subprojetos), depois parceiros com PAINEL.md."""
    out = []
    cli = os.path.join(raiz, "clientes")
    if os.path.isdir(cli):
        for n in sorted(os.listdir(cli)):
            if os.path.isdir(os.path.join(cli, n)) and not n.startswith(("_", ".")):
                out.append((n, os.path.join(cli, n), f"clientes/{n}"))
                for nome, p in _subprojetos_da_pasta(os.path.join(cli, n), n):
                    out.append((nome, p, f"clientes/{n}/{os.path.basename(p)}"))
    par = os.path.join(raiz, PARCEIROS)
    if os.path.isdir(par):
        for n in sorted(os.listdir(par)):
            pasta = os.path.join(par, n)
            painel = os.path.join(pasta, "PAINEL.md")
            if os.path.isdir(pasta) and not n.startswith(("_", ".")) and os.path.exists(painel):
                out.append((_conta_do_painel(painel) or n, pasta, f"{PARCEIROS}/{n}"))
    return out


def pasta_da_conta(raiz, nome):
    """Pasta absoluta da conta pelo nome exato (sem diferenciar caixa), ou None. Subprojeto → a subpasta dele."""
    alvo = (nome or "").strip().lower()
    for n, p, _ in contas(raiz):
        if n.lower() == alvo:
            return p
    return None


def eh_subprojeto(raiz, pasta):
    """True se a pasta é clientes/<Conta>/<subpasta>/ com PAINEL.md e `conta:` próprio."""
    pasta = os.path.normpath(pasta)
    mae = os.path.dirname(pasta)
    if os.path.normcase(os.path.dirname(mae)) != os.path.normcase(os.path.normpath(os.path.join(raiz, "clientes"))):
        return False
    nome = _conta_do_painel(os.path.join(pasta, "PAINEL.md"))
    return bool(nome) and nome.lower() != os.path.basename(mae).lower()


def pasta_dos_fatos(raiz, pasta):
    """Onde moram STATUS.md, DECISOES.md, 01 - contexto/ e entregaveis/ da conta: a mãe, se for subprojeto; senão ela mesma."""
    if pasta and eh_subprojeto(raiz, pasta):
        return os.path.dirname(os.path.normpath(pasta))
    return pasta


def conta_mae(raiz, nome):
    """Nome da conta que guarda os fatos: o da mãe para um subprojeto, o próprio nome para o resto."""
    p = pasta_da_conta(raiz, nome)
    if p and eh_subprojeto(raiz, p):
        return os.path.basename(os.path.dirname(os.path.normpath(p)))
    return nome


def subprojetos(raiz, pasta_mae):
    """[(nome, pasta)] dos subprojetos de uma conta de clientes/ (vazio para o resto)."""
    pasta_mae = os.path.normpath(pasta_mae or "")
    if os.path.normcase(os.path.dirname(pasta_mae)) != os.path.normcase(os.path.normpath(os.path.join(raiz, "clientes"))):
        return []
    return _subprojetos_da_pasta(pasta_mae, os.path.basename(pasta_mae))
