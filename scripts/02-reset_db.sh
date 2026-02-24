#!/usr/bin/env bash
set -euo pipefail

echo "Derrubando containers e removendo volumes..."
docker compose down -v

echo "Subindo containers limpos..."
docker compose up -d

echo "Aplicando migrations..."
docker compose exec backend alembic upgrade head

echo "Banco de dados resetado."
