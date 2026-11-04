# Rodar no macOS (e Linux)

> Parte das ferramentas foi escrita primeiro para Windows. **Tudo o que é texto, método e git roda igual em qualquer sistema.** O que era específico de Windows foi traduzido; esta pasta é o ponto de entrada no Mac.

## Começo

```bash
git clone <url do repo> && cd <pasta>
./40-operacao-rotinas/ferramentas/macos/instalar-mac.sh      # confere git, python3, Chrome, opcionais; instala o agendador
```

Depois: `LEIA-ME-TEMPLATE.md` §3 (o dia 1) e o roteiro de entrevista no `README.md`.

## Equivalências

| No Windows | No macOS / Linux |
|---|---|
| `py script.py` | `python3 script.py` (toda a documentação já usa `python3`; `py` também funciona se você criar o alias `alias py=python3`) |
| Agendador de Tarefas (`continuum-despachante`, 1 rodada/hora) | LaunchAgent `com.continuum.despachante` (instalado pelo `instalar-mac.sh`; `launchctl list | grep continuum` para conferir; arquivo `PAUSA` em `tarefas/` para tudo) |
| `openwa/capturar.bat` | `openwa/capturar.sh` (abre o Docker Desktop com `open -a Docker`) |
| Chrome em `C:\Program Files\…` | `navegador.py` acha o Chrome em `/Applications/…`; ou `export CHROME=<caminho>` |
| `servir.py --atalho` (atalho `.lnk` na área de trabalho) | sem equivalente automático: `python3 servir.py` abre o painel no navegador; para um "app", **Automator → Aplicativo → Executar Shell Script** com a mesma linha |
| atalhos na área de trabalho (OpenWA, Painel de Resultado, tela offline) | os mesmos `python3 …`; para um ícone, Automator → Aplicativo → Executar Shell Script, ou alias no shell |
| PowerShell nos READMEs | os mesmos comandos em bash (os READMEs trazem os dois) |
| `winget install Gyan.FFmpeg` | `brew install ffmpeg` |
| CRLF | o repo é LF (`.gitattributes`); nada a fazer |

## Agente principal sem hooks (Codex e outros)

Os hooks de `.claude/settings.json` só existem no Claude Code. Com Codex (`AGENTS.md`), a sincronia git é o **último ato de toda tarefa**, à mão:

```bash
python3 40-operacao-rotinas/ferramentas/sincronizar.py        # commita, mescla a main, regenera AGENTS.md, publica
```

Ou `git config alias.sync '!python3 40-operacao-rotinas/ferramentas/sincronizar.py'` e depois só `git sync`.

O despachante (`despachar.py`) lança os workers N2–N5 pelo `claude -p`. Sem Claude Code instalado, defina `WORKER_CLI` com o comando do seu agente, com `{modelo}` e `{prompt_stdin}` opcionais — por exemplo `WORKER_CLI="codex exec --model {modelo} -"` — ou deixe N2–N5 para rodar na sessão principal e use o despachante só para N0 (scripts) e N1.

## Caminhos com espaço e acento

Os nomes de pasta do repo têm espaço e acento (`execução Codex/`, `960-referências criativos/`). No shell, sempre entre aspas. O git no macOS normaliza Unicode (NFD) em alguns nomes; se um `git status` mostrar pasta "renomeada" sem você ter mexido, rode `git config core.precomposeunicode true` uma vez.
