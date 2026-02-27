# Makefile para facilitar comandos do backend StepByStep

TEST_VENV=.venv-test
TEST_PY=$(TEST_VENV)/bin/python3
TEST_PIP=$(TEST_VENV)/bin/pip
DATABASE_URL?=postgresql://postgres:198870@localhost:5433/stepbystep
TEST_DATABASE_URL?=postgresql://postgres:198870@localhost:5433/stepbystep_test

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

$(TEST_VENV):
	python3 -m venv $(TEST_VENV)
	$(TEST_PIP) install -r requirements.txt

test: $(TEST_VENV)
	@echo ">> (env) TEST_DATABASE_URL=$(TEST_DATABASE_URL)"
	@echo ">> TEST_DATABASE_URL=$(TEST_DATABASE_URL)"
	@echo ">> Validating virtualenv $(TEST_VENV)"
	@echo ">> Using python interpreter $(TEST_PY)"
	@echo ">> Running pytest..."
	@PYTHONPATH=$(PWD) TEST_DATABASE_URL=$(TEST_DATABASE_URL) $(TEST_PY) -m pytest app/test_learning_api.py
