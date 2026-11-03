"""Exporta a transcrição de uma sessão do Claude Code (.jsonl) para Markdown legível.

Uso:
    python3 40-operacao-rotinas/ferramentas/exportar-sessao.py <sessao.jsonl> <saida.md>

Mantém: falas do usuário, texto do assistente, resumos de compactação e o nome/descrição de cada ferramenta usada.
Descarta: resultados de ferramenta, raciocínio interno, lembretes do sistema e imagens.
Roda sem IA: o custo é só o comando.
"""
import json, re, sys
from datetime import datetime, timezone, timedelta

BRT = timezone(timedelta(hours=-3))
LEMBRETE = re.compile(r'<system-reminder>.*?</system-reminder>', re.S)


def hora(ts):
    try:
        return datetime.fromisoformat(ts.replace('Z', '+00:00')).astimezone(BRT).strftime('%d/%m %H:%M')
    except Exception:
        return ''


def limpar(t):
    return LEMBRETE.sub('', t or '').strip()


def main(src, dst):
    linhas, n_user, n_asst = [], 0, 0
    with open(src, encoding='utf-8') as f:
        for raw in f:
            try:
                e = json.loads(raw)
            except ValueError:
                continue
            tipo, msg = e.get('type'), e.get('message') or {}
            quando = hora(e.get('timestamp', ''))
            if e.get('isCompactSummary') or tipo == 'summary':
                txt = limpar(e.get('summary') or (msg.get('content') if isinstance(msg.get('content'), str) else ''))
                if txt:
                    linhas.append(f'\n---\n\n### ⟲ Resumo de compactação {quando}\n\n{txt}\n')
                continue
            if tipo not in ('user', 'assistant') or e.get('isMeta'):
                continue
            conteudo = msg.get('content')
            blocos = [{'type': 'text', 'text': conteudo}] if isinstance(conteudo, str) else (conteudo or [])
            textos, ferramentas = [], []
            for b in blocos:
                if not isinstance(b, dict):
                    continue
                if b.get('type') == 'text':
                    t = limpar(b.get('text'))
                    if t:
                        textos.append(t)
                elif b.get('type') == 'tool_use' and tipo == 'assistant':
                    inp = b.get('input') or {}
                    desc = inp.get('description') or inp.get('file_path') or inp.get('pattern') or ''
                    ferramentas.append(f"`{b.get('name')}`" + (f' — {str(desc)[:140]}' if desc else ''))
            if tipo == 'user' and textos:
                n_user += 1
                linhas.append(f'\n## 🧑 {{OPERADOR}} · {quando}\n\n' + '\n\n'.join(textos) + '\n')
            elif tipo == 'assistant':
                if textos:
                    n_asst += 1
                    linhas.append(f'\n**🤖 Claude · {quando}**\n\n' + '\n\n'.join(textos) + '\n')
                for ft in ferramentas:
                    linhas.append(f'- 🔧 {ft}')
    cab = (f'# Transcrição de sessão do Claude Code\n\n'
           f'> Fonte: `{src.replace(chr(92), "/").split("/")[-1]}` · exportada em {datetime.now(BRT):%d/%m/%Y %H:%M} '
           f'· {n_user} mensagens do usuário · {n_asst} respostas · resultados de ferramenta e raciocínio omitidos\n')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write(cab + '\n'.join(linhas) + '\n')
    print(f'ok: {dst} ({n_user} usuário, {n_asst} respostas)')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
