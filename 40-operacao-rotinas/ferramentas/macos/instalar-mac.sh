#!/usr/bin/env bash
# instalar-mac.sh — prepara o repositório para rodar no macOS (e, com pequenas diferenças, no Linux).
#
#   ./40-operacao-rotinas/ferramentas/macos/instalar-mac.sh              confere tudo e instala o agendador
#   ./40-operacao-rotinas/ferramentas/macos/instalar-mac.sh --sem-agendador
#   ./40-operacao-rotinas/ferramentas/macos/instalar-mac.sh --desinstalar-agendador
#
# O que faz: confere git, python3, Chrome, ffmpeg (opcional), faster-whisper (opcional), weasyprint (opcional), pymupdf (opcional);
# dá permissão de execução aos .sh; instala o LaunchAgent do despachante (uma rodada por hora).
# Nada é instalado sem você ver a linha. O que faltar sai como instrução, não como erro silencioso.
set -uo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$AQUI/../../.." && pwd)"
PLIST_SRC="$AQUI/com.continuum.despachante.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.continuum.despachante.plist"
ok(){ printf '  ✅ %s\n' "$1"; }
falta(){ printf '  🔴 %s\n     → %s\n' "$1" "$2"; }
opc(){ printf '  🟡 %s\n     → %s\n' "$1" "$2"; }

echo "Repositório: $REPO"
echo
echo "1. Obrigatórios"
command -v git >/dev/null && ok "git $(git --version | cut -d' ' -f3)" || falta "git" "xcode-select --install"
if command -v python3 >/dev/null; then ok "python3 $(python3 --version | cut -d' ' -f2)"; PY="$(command -v python3)"; else falta "python3" "brew install python  (ou xcode-select --install)"; PY=python3; fi
command -v brew >/dev/null && ok "Homebrew" || opc "Homebrew" '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
if "$PY" "$REPO/40-operacao-rotinas/ferramentas/navegador.py" >/dev/null 2>&1; then ok "Chrome ($("$PY" "$REPO/40-operacao-rotinas/ferramentas/navegador.py"))"; else falta "Google Chrome (PDF, prancha, kit de marca)" "brew install --cask google-chrome  ou defina CHROME=<caminho>"; fi

echo
echo "2. Opcionais (só para as ferramentas que você for usar)"
command -v ffmpeg >/dev/null && ok "ffmpeg (transcrição e edição de vídeo)" || opc "ffmpeg" "brew install ffmpeg"
"$PY" -c "import faster_whisper" 2>/dev/null && ok "faster-whisper (transcrição local)" || opc "faster-whisper" "$PY -m pip install faster-whisper"
"$PY" -c "import weasyprint" 2>/dev/null && ok "weasyprint (pdf-continuum)" || opc "weasyprint" "brew install pango && $PY -m pip install weasyprint markdown"
"$PY" -c "import fitz" 2>/dev/null && ok "pymupdf (gerar_pdf.py)" || opc "pymupdf" "$PY -m pip install pymupdf"
"$PY" -c "import numpy" 2>/dev/null && ok "numpy" || opc "numpy (transcrição)" "$PY -m pip install numpy"
command -v docker >/dev/null && ok "Docker (OpenWA)" || opc "Docker (só para a captura de WhatsApp)" "brew install --cask docker"
command -v claude >/dev/null && ok "claude (Claude Code)" || opc "claude" "npm i -g @anthropic-ai/claude-code  (ou use o Codex: leia AGENTS.md)"
command -v codex >/dev/null && ok "codex" || opc "codex" "npm i -g @openai/codex"

echo
echo "3. Permissões de execução"
find "$REPO/40-operacao-rotinas" -name "*.sh" -exec chmod +x {} \; && ok "chmod +x em todos os .sh"

echo
echo "4. Agendador (launchd) do despachante — uma rodada por hora"
case "${1:-}" in
  --sem-agendador) echo "  pulado (--sem-agendador)";;
  --desinstalar-agendador)
    launchctl bootout "gui/$(id -u)" "$PLIST_DST" 2>/dev/null; rm -f "$PLIST_DST"; ok "LaunchAgent removido";;
  *)
    mkdir -p "$HOME/Library/LaunchAgents" "$REPO/40-operacao-rotinas/tarefas/log"
    sed -e "s#__REPO__#$REPO#g" -e "s#__PYTHON__#$PY#g" "$PLIST_SRC" > "$PLIST_DST"
    launchctl bootout "gui/$(id -u)" "$PLIST_DST" 2>/dev/null
    launchctl bootstrap "gui/$(id -u)" "$PLIST_DST" && ok "LaunchAgent instalado: $PLIST_DST (log em tarefas/log/launchd.*.log)" || falta "launchctl" "rode à mão: launchctl bootstrap gui/\$(id -u) $PLIST_DST"
    echo "     Para parar tudo sem desinstalar: touch \"$REPO/40-operacao-rotinas/tarefas/PAUSA\"";;
esac

echo
echo "5. Sincronia git (CLAUDE.md §11.6)"
echo "  Claude Code: os hooks em .claude/settings.json já chamam sincronizar.py ao abrir e fechar a sessão."
echo "  Codex ou outro agente sem hooks: rode ao fechar toda tarefa →  python3 40-operacao-rotinas/ferramentas/sincronizar.py"
echo "  Atalho:  git config alias.sync '!python3 40-operacao-rotinas/ferramentas/sincronizar.py'   →   git sync"
echo
echo "Pronto. Próximo passo: LEIA-ME-TEMPLATE.md §3 (o dia 1) e o roteiro de entrevista no README.md."
