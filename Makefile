# Makefile para facilitar comandos do backend StepByStep

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f backend

migrate:
	docker compose exec backend alembic upgrade head

shell:
	docker compose exec backend bash

ps:
	docker compose ps

reset_db:
	bash scripts/reset_db.sh
