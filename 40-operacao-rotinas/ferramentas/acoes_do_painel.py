# -*- coding: utf-8 -*-
"""
acoes_do_painel.py — o que o operador marca no sistema sobre um prazo (feito, descartar, nova data, nota, fase da conta)
vira mudança no repo. Chamado pelo decisoes-do-painel.py (a ponte do sistema, na VPS, a cada 2 min).

Motivo: projeto vencido que já não faz sentido precisa de uma saída (descartar) e de um campo para o operador
acrescentar informação.

O que cada ação faz (a fonte continua sendo o .md; o sistema só lê o que isto escreve):
  marco · feito/descartar   tira a linha de `marcos:` no frontmatter do PAINEL.md; se era o próximo marco, o próximo passa
                            a ser o marco aberto mais perto (ou fica vazio, e o sistema cobra)
  marco · nova_data         troca o `prazo:` da linha (e o `marco_prazo`, se era o próximo)
  proximo · …               o mesmo sobre `proximo_marco`/`marco_prazo` (e sobre a linha de `marcos:` igual, se houver)
  task · feito/descartar    `estado: entregue|descartada` e o arquivo vai para tarefas/entregue/ (o sistema deixa de mostrar)
  task · nova_data          troca `prazo:`
  conta · fase              troca `fase:` (pausada, encerrada e arquivada saem de "Ativas")
  qualquer uma · nota       a nota vai, literal, para o STATUS.md da conta (seção "Registro do sistema", fonte: o operador e a data);
                            na task, também para o corpo dela
Toda ação deixa linha em tarefas/log/ACOES-DO-SISTEMA.md e põe `atualizado:` de hoje no PAINEL.md.
Nunca cria pasta de conta. Alvo que não se acha volta como erro e aparece no sistema.
"""
import datetime, io, os, re, shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CLIENTES = RAIZ / "clientes"
TAR = RAIZ / "40-operacao-rotinas" / "tarefas"
LOG = TAR / "log" / "ACOES-DO-SISTEMA.md"
PASTAS_TASK = ("fila", "executando", "revisao", "decisao", "falhou", "entregue")
BRT = datetime.timezone(datetime.timedelta(hours=-3))
ROTULO = {"feito": "feito", "descartar": "descartado", "nova_data": "nova data", "nota": "nota", "fase": "fase"}
CHAVES = r"(o_que|prazo|dono|duro)"


def _ler(p):
    b = Path(p).read_bytes().decode("utf-8")
    return b, ("\r\n" if "\r\n" in b else "\n")


def _gravar(p, texto):
    Path(p).write_bytes(texto.encode("utf-8"))


def _br(iso):
    try:
        a, m, d = iso.split("-")
        return f"{d}/{m}/{a}"
    except Exception:  # noqa: BLE001
        return iso or "sem data"


def _marco_da_linha(linha):
    item = linha.strip()
    if not (item.startswith("- {") and item.endswith("}")):
        return None
    d = {k: v.strip().strip('"').strip("'") for k, v in re.findall(CHAVES + r"\s*:\s*(.*?)(?=,\s*(?:o_que|prazo|dono|duro)\s*:|$)", item[3:-1])}
    return d if d.get("o_que") else None


def _iso(v):
    v = (v or "").strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", v)
    if m:
        return v
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", v)
    return f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}" if m else ""


def _mesmo(a, b):
    norm = lambda s: re.sub(r"\s+", " ", (s or "").strip().lower())
    return norm(a) == norm(b)


def _pasta(conta):
    if not conta or conta.lower() == "casa":
        return None
    p = CLIENTES / conta
    if p.is_dir():
        return p
    import sys   # conta de parceiro (parceiros/<P>/PAINEL.md, conta: no frontmatter)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import contas_da_casa
    q = contas_da_casa.pasta_da_conta(str(RAIZ), conta)
    return Path(q) if q else None


def _contas_da_casa():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import contas_da_casa
    return contas_da_casa


def _tem_alvo(arq, acao):
    """O PAINEL.md tem o marco (ou o próximo marco) que a ação nomeia?"""
    try:
        texto, _ = _ler(arq)
    except OSError:
        return False
    m = re.match(r"^﻿?---\r?\n(.*?)\r?\n---\r?\n", texto, re.S)
    if not m:
        return False
    ref, prazo = acao.get("ref") or "", acao.get("prazo") or ""
    for l in m.group(1).splitlines():
        d = _marco_da_linha(l)
        if d and _mesmo(d["o_que"], ref) and (_iso(d.get("prazo")) == prazo or not prazo):
            return True
        mm = re.match(r"^proximo_marco\s*:\s*(.*)$", l)
        if mm and _mesmo(mm.group(1), ref):
            return True
    return False


def _painel(conta, acao, hoje):
    """Aplica marco/proximo/conta no frontmatter. Devolve a descrição do alvo para o registro.
    Conta com subprojeto (contas_da_casa.py). O sistema manda a pasta da conta-mãe também para o cartão do
    subprojeto; marco ou próximo marco que não está no PAINEL da mãe é procurado no PAINEL dos subprojetos dela."""
    pasta = _pasta(conta)
    if not pasta or not (pasta / "PAINEL.md").exists():
        raise ValueError(f"conta sem PAINEL.md: {conta}")
    if acao.get("alvo") in ("marco", "proximo") and not _tem_alvo(pasta / "PAINEL.md", acao):
        for _, p in _contas_da_casa().subprojetos(str(RAIZ), str(pasta)):
            if _tem_alvo(Path(p) / "PAINEL.md", acao):
                pasta = Path(p)
                break
    return _painel_em(pasta / "PAINEL.md", acao, hoje)


def _painel_em(arq, acao, hoje):
    texto, nl = _ler(arq)
    m = re.match(r"^(﻿?---\r?\n)(.*?)(\r?\n---\r?\n)", texto, re.S)
    if not m:
        raise ValueError("PAINEL.md sem frontmatter")
    linhas = m.group(2).split(nl) if nl in m.group(2) else m.group(2).split("\n")
    campos = {}
    for i, l in enumerate(linhas):
        mm = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", l)
        if mm:
            campos[mm.group(1)] = i
    def val(k):
        return linhas[campos[k]].split(":", 1)[1].strip() if k in campos else ""
    def pôr(k, v):
        if k in campos:
            linhas[campos[k]] = f"{k}: {v}"
    alvo, a, ref, prazo = acao["alvo"], acao["acao"], acao.get("ref") or "", acao.get("prazo") or ""
    desc = ""
    # as linhas de marco
    idx_marcos = [i for i, l in enumerate(linhas) if _marco_da_linha(l)]
    def achar(o_que, pz):
        for i in idx_marcos:
            d = _marco_da_linha(linhas[i])
            if _mesmo(d["o_que"], o_que) and (_iso(d.get("prazo")) == (pz or "") or not pz):
                return i
        return None
    eh_proximo = False
    if alvo == "conta":
        desc = f"conta (fase {val('fase') or '?'})"
        if a == "fase":
            desc = f"conta (fase {val('fase') or '?'} → {acao['valor']})"
            pôr("fase", acao["valor"])
    elif alvo in ("marco", "proximo"):
        i = achar(ref, prazo)
        eh_proximo = alvo == "proximo" or (_mesmo(val("proximo_marco"), ref) and (_iso(val("marco_prazo")) == prazo or not prazo))
        if i is None and not eh_proximo:
            raise ValueError(f"marco não encontrado no PAINEL.md: {ref[:60]} ({prazo})")
        desc = f"{'próximo marco' if alvo == 'proximo' else 'marco'} *{ref}* (prazo {_br(prazo)})"
        if a in ("feito", "descartar"):
            if i is not None:
                del linhas[i]
            if eh_proximo:
                restantes = [_marco_da_linha(l) for l in linhas if _marco_da_linha(l)]
                abertos = sorted([d for d in restantes if _iso(d.get("prazo")) >= hoje], key=lambda d: _iso(d.get("prazo")))
                if abertos:
                    pôr("proximo_marco", abertos[0]["o_que"]); pôr("marco_prazo", _iso(abertos[0]["prazo"])); pôr("marco_dono", abertos[0].get("dono", ""))
                else:
                    pôr("proximo_marco", ""); pôr("marco_prazo", ""); pôr("marco_dono", "")
        elif a == "nova_data":
            nova = acao["valor"]
            if i is not None:
                linhas[i] = re.sub(r"(prazo\s*:\s*)([^,}]*)", lambda mo: mo.group(1) + nova, linhas[i], count=1)
            if eh_proximo:
                pôr("marco_prazo", nova)
    pôr("atualizado", hoje)
    novo = m.group(1) + nl.join(linhas) + m.group(3) + texto[m.end():]
    if novo != texto:
        _gravar(arq, novo)
    return desc


def _task(acao, agora):
    tid = acao.get("ref") or ""
    achado = None
    for p in PASTAS_TASK:
        f = TAR / p / f"{tid}.md"
        if f.exists():
            achado = f
            break
    if not achado:
        cand = [f for p in PASTAS_TASK for f in (TAR / p).glob(f"{tid}*.md")] if tid else []
        achado = cand[0] if len(cand) == 1 else None
    if not achado:
        raise ValueError(f"task não encontrada: {tid}")
    texto, nl = _ler(achado)
    conta = (re.search(r"^conta:\s*(.*)$", texto, re.M) or [None, ""])[1].strip()
    titulo = (re.search(r"^titulo:\s*(.*)$", texto, re.M) or [None, tid])[1].strip()
    a = acao["acao"]
    if a in ("feito", "descartar"):
        estado = "entregue" if a == "feito" else "descartada"
        texto = re.sub(r"^estado:.*$", f"estado: {estado}", texto, count=1, flags=re.M)
        # "Enviado" na aba Entregáveis = feito numa task tipo: entregavel;
        # só este clique (ou a ordem literal do operador na sessão) preenche enviado_em (V-ENT-6)
        if a == "feito" and re.search(r"^tipo:\s*entregavel\s*$", texto, re.M):
            texto = re.sub(r"^enviado_em:.*$", f"enviado_em: {agora[:10]}", texto, count=1, flags=re.M)
            texto = re.sub(r"^enviado_por:.*$", "enviado_por: painel", texto, count=1, flags=re.M)
    elif a == "nova_data":
        texto = re.sub(r"^prazo:.*$", f"prazo: {acao['valor']}", texto, count=1, flags=re.M)
    if acao.get("nota") or a in ("feito", "descartar"):
        texto = texto.rstrip("\r\n") + nl + nl + f"## Do sistema · {agora}" + nl + nl + \
            f"O operador marcou **{ROTULO[a]}**{(' (' + _br(acao['valor']) + ')') if a == 'nova_data' else ''} no dashboard." + \
            (f" Nota, literal: *\"{acao['nota']}\"*" if acao.get("nota") else "") + nl
    _gravar(achado, texto)
    if a in ("feito", "descartar") and achado.parent.name != "entregue":
        destino = TAR / "entregue" / achado.name
        shutil.move(str(achado), str(destino))
    return conta, f"task {tid} — {titulo[:90]}"


def _status(conta, linha):
    pasta = _pasta(conta)
    if pasta:   # subprojeto não tem STATUS próprio; a nota vai para o da conta-mãe
        pasta = Path(_contas_da_casa().pasta_dos_fatos(str(RAIZ), str(pasta)))
    if not pasta or not (pasta / "STATUS.md").exists():
        return
    arq = pasta / "STATUS.md"
    texto, nl = _ler(arq)
    if "## Registro do sistema" not in texto:
        texto = texto.rstrip("\r\n") + nl + nl + "## Registro do sistema" + nl + nl + \
            "> O que o operador marcou no dashboard (feito, descartado, nova data, fase, nota), levado ao repo pela ponte do sistema " \
            "(`40-operacao-rotinas/ferramentas/acoes_do_painel.py`). **Fonte: o operador, na data da linha.** A nota é literal." + nl + nl
    else:
        texto = texto.rstrip("\r\n") + nl
    _gravar(arq, texto + linha + nl)


def _log(linhas):
    novo = not LOG.exists()
    with io.open(LOG, "a", encoding="utf-8", newline="\n") as f:
        if novo:
            f.write("# AÇÕES DO SISTEMA — o que o operador marcou no dashboard sobre prazos e contas\n\n"
                    "> Escrito por `40-operacao-rotinas/ferramentas/acoes_do_painel.py`. Uma linha por ação aplicada no repo.\n\n"
                    "| Aplicada em | # | Conta | Alvo | Ação | Nota |\n|---|---:|---|---|---|---|\n")
        for l in linhas:
            f.write(l + "\n")


# ── área Comercial — aceite e etapa do prospect ──────────────
ETAPAS_COM = ("contato", "g0", "ancoras", "proposta", "aceite", "perdido")


def _proximo_id(hoje):
    # 13/11/2026 (T-2026-11-12-022): o gerador único, com faixa por origem; contar só esta máquina colidia com a VPS
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import tarefa_id
    return tarefa_id.proximo(dia=hoje, tarefas=str(TAR))


def _fm_por(texto, nl, campos):
    """Troca ou acrescenta `chave: valor` no frontmatter (acrescenta antes do fecho)."""
    m = re.match(r"(﻿?---\r?\n)(.*?)(\r?\n---)", texto, re.S)
    if not m:
        raise ValueError("ficha sem frontmatter")
    linhas = m.group(2).split(nl) if nl in m.group(2) else m.group(2).split("\n")
    for k, v in campos.items():
        for i, l in enumerate(linhas):
            if re.match(rf"^{k}\s*:", l):
                linhas[i] = f"{k}: {v}"
                break
        else:
            linhas.append(f"{k}: {v}")
    return m.group(1) + nl.join(linhas) + m.group(3) + texto[m.end():]


def _fechar_oferta(ref, res):
    """Aceite ou perda da ficha fecha a recomendação oferta_catalogo dela
    no DECISOES.jsonl (autonomia.py --resultado). Falha aqui nunca impede a ação do operador."""
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import autonomia
        h = autonomia.resultado_por_ficha(ref, res)
        return f" · oferta {h['id']} → {res}" if h else ""
    except Exception:  # noqa: BLE001
        return ""


def _prospect(acao, hoje, carimbo):
    ref = (acao.get("ref") or "").strip().strip("/")
    if not (ref.startswith("30-comercial/assessoria-prospects/") or ref.startswith("clientes/")) or ".." in ref:
        raise ValueError(f"ficha fora do lugar: {ref}")
    arq = RAIZ / ref / "PAINEL.md"
    if not arq.exists():
        raise ValueError(f"ficha não encontrada: {ref}/PAINEL.md")
    texto, nl = _ler(arq)
    nome = acao.get("conta") or ref.rsplit("/", 1)[-1]
    a = acao["acao"]
    if a == "etapa":
        if acao.get("valor") not in ETAPAS_COM:
            raise ValueError(f"etapa inválida: {acao.get('valor')}")
        _gravar(arq, _fm_por(texto, nl, {"etapa": acao["valor"], "atualizado": hoje}))
        extra = _fechar_oferta(ref, "perdido") if acao["valor"] == "perdido" else (_fechar_oferta(ref, "aceite") if acao["valor"] == "aceite" else "")
        return nome, f"funil · {nome}{extra}"
    if a == "aceite":
        data = acao.get("valor") or hoje
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data):
            raise ValueError(f"data de aceite inválida: {data}")
        campos = {"etapa": "aceite", "aceite": data, "atualizado": hoje}
        extra = _fechar_oferta(ref, "aceite")
        if ref.startswith("clientes/"):              # conta que era proposta: o D0 entra direto e a conta vai a fundar (trilho, ato II)
            campos.update({"onb_d0": data, "fase": "fundar"})
            _gravar(arq, _fm_por(texto, nl, campos))
            return nome, f"aceite · {nome} · D0 {_br(data)}{extra}"
        _gravar(arq, _fm_por(texto, nl, campos))
        tid = _proximo_id(hoje)
        task = (f"---\nid: {tid}\ntitulo: Abrir a conta {nome} (aceite em {_br(data)}, marcado no sistema)\ncriada: {hoje}\n"
                f"prazo: {hoje}\nprazo_duro: sim\nconta: casa\narvore: CONTA\ncarga: julgamento\nclasse_dado: C\nnivel_minimo: N4\nescada: N4\n"
                f"swarm: nao\ncomando: \nverificacao: python3 40-operacao-rotinas/ferramentas/verificar-propagacao.py\n"
                f"insumos: CLAUDE.md; 100-métodos/METODO-TRILHO-DE-CONTA-NOVA.md; 100-métodos/METODO-ONBOARDING-ORQUESTRADO.md; {ref}/PAINEL.md\n"
                f"saida: clientes/<Conta>/\nalcada: abre a conta e move a pasta do prospect; nao envia mensagem ao cliente; nao muda preco nem contrato\n"
                f"estimativa_tokens: 60000\ndepende_de: \ntipo_decisao: \nprioridade: 1\nrecorrencia: \nestado: pronta\nagendada_para: \n---\n"
                f"# Abrir a conta {nome}\n\nO operador marcou **aceite** no sistema em {carimbo} (data do aceite: {_br(data)}). Ficha: `{ref}/PAINEL.md`.\n\n"
                f"1. Etapa 0 do `METODO-TRILHO-DE-CONTA-NOVA.md`: a pasta do prospect vira `clientes/<Nome>/` (mover, nunca copiar; "
                f"`40-operacao-rotinas/ferramentas/renomear-conta.py` reescreve os caminhos), com `PAINEL.md` da conta, `STATUS.md` e `DECISOES.md`.\n"
                f"2. No frontmatter da conta: `fase: fundar`, `onb_d0: {data}`, produto, contrato e `recorrencia`/`mensalidade` da ficha.\n"
                f"3. Régua do `METODO-ONBOARDING-ORQUESTRADO.md`: passagem interna até D+2 (as 6 perguntas na conta); passagem com o cliente até D+10, "
                f"como marco com dono operador; compromisso de data e hora na agenda.\n"
                f"4. `verificar-propagacao.py` ✅ e `sincronizar.py`.\n")
        (TAR / "fila").mkdir(parents=True, exist_ok=True)
        (TAR / "fila" / f"{tid}.md").write_bytes(task.encode("utf-8"))
        return nome, f"aceite · {nome} · D0 {_br(data)} · task {tid} (abrir a conta){extra}"
    if a == "nota":
        reg = RAIZ / ref / "REGISTRO.md"
        linha = f"- **{carimbo}** · nota do operador no sistema, literal: *\"{acao.get('nota') or ''}\"*"
        if reg.exists():
            t2, nl2 = _ler(reg)
            _gravar(reg, t2.rstrip("\r\n") + nl2 + nl2 + linha + nl2)
        else:
            _gravar(arq, texto.rstrip("\r\n") + nl + nl + linha + nl)
        return nome, f"nota · {nome}"
    raise ValueError(f"ação {a} não vale para prospect")


def aplicar(acoes):
    """Aplica as ações em ordem. Devolve (ids aplicados, {id: erro})."""
    agora = datetime.datetime.now(BRT)
    hoje, carimbo = agora.date().isoformat(), agora.strftime("%Y-%m-%d %H:%M")
    feitos, erros, log = [], {}, []
    for ac in acoes:
        try:
            a = ac["acao"]
            if ac["alvo"] == "prospect":
                conta, desc = _prospect(ac, hoje, carimbo)
                o_que = {"aceite": "aceite", "etapa": f"etapa → {ac.get('valor')}", "nota": "nota"}.get(a, a)
                if (ac.get("ref") or "").startswith("clientes/"):
                    _status(conta, f"- **{carimbo}** · {desc} · **{o_que}** (marcado no dashboard)" + (f" · nota do operador: *\"{ac.get('nota')}\"*" if ac.get("nota") else ""))
                log.append(f"| {carimbo} | {ac['id']} | {conta} | {desc.replace('|', '/')} | {o_que} | {(ac.get('nota') or '—').replace('|', '/')} |")
                feitos.append(ac["id"])
                continue
            if ac["alvo"] == "task":
                conta, desc = _task(ac, carimbo)
            else:
                conta = ac.get("conta") or ""
                desc = _painel(conta, ac, hoje)
            o_que = ROTULO[a] + (f" → {_br(ac['valor'])}" if a == "nova_data" else "") + (f" → {ac['valor']}" if a == "fase" else "")
            try:
                quando = datetime.datetime.fromisoformat(ac["criado_em"].replace("Z", "+00:00")).astimezone(BRT).strftime("%d/%m %H:%M")
            except Exception:  # noqa: BLE001
                quando = "?"
            nota = ac.get("nota") or ""
            _status(conta, f"- **{carimbo}** · {desc} · **{o_que}** (marcado no dashboard em {quando})" + (f" · nota do operador: *\"{nota}\"*" if nota else ""))
            log.append(f"| {carimbo} | {ac['id']} | {conta or 'casa'} | {desc.replace('|', '/')} | {o_que} | {nota.replace('|', '/') or '—'} |")
            feitos.append(ac["id"])
        except Exception as e:  # noqa: BLE001
            erros[str(ac["id"])] = f"{type(e).__name__}: {e}"[:300]
    if log:
        _log(log)
    return feitos, erros
