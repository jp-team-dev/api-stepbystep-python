#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Subindo containers..."
docker compose up -d

echo "[2/3] Aplicando migrations..."
docker compose exec backend alembic upgrade head

echo "[3/3] Logs do backend:"
docker compose logs -f backend
