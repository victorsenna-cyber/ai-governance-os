#!/usr/bin/env bash
# "Capturar WhatsApp" (macOS / Linux): sobe o Docker e o OpenWA se precisar e roda a captura.
# Equivalente do capturar.bat. A lógica toda mora no capturar.py; este arquivo só prepara o motor.
# Uso: ./capturar.sh --chat "<nome da conversa>"   (nunca sem --chat; a rodada completa é rodada.py)
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENWA="${OPENWA_DIR:-$AQUI/../../../../../repos-externos/OpenWA}"

if ! docker info >/dev/null 2>&1; then
  echo "Abrindo o Docker…"
  if [[ "$(uname)" == "Darwin" ]]; then open -a Docker; else sudo systemctl start docker 2>/dev/null || true; fi
  for _ in $(seq 1 40); do
    sleep 3
    docker info >/dev/null 2>&1 && break
  done
  docker info >/dev/null 2>&1 || { echo "O Docker não subiu em 2 minutos. Abra o Docker Desktop e tente de novo."; exit 1; }
fi

if [[ -d "$OPENWA" ]]; then
  ( cd "$OPENWA" && docker compose -f docker-compose.dev.yml up -d )
else
  echo "Motor OpenWA não encontrado em: $OPENWA (defina OPENWA_DIR). Seguindo só com a captura."
fi

python3 "$AQUI/capturar.py" "$@"
