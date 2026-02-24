# StepByStep FastAPI backend

Este projeto é o backend FastAPI do StepByStep, agora em seu próprio diretório.

## Como rodar (desenvolvimento)

1. Copie `.env.example` para `.env` e ajuste se necessário.

2. Comandos principais (use `make <comando>` ou scripts em `scripts/`):

| Comando                  | O que faz                                          |
| ------------------------ | -------------------------------------------------- |
| make up                  | Sobe containers backend e banco                    |
| make down                | Para e remove containers                           |
| make logs                | Mostra logs do backend                             |
| make migrate             | Aplica migrations Alembic                          |
| make shell               | Abre shell no container backend                    |
| make reset_db            | Reseta banco (remove volumes e reaplica migrações) |
| bash scripts/dev.sh      | Sobe tudo, aplica migrations e mostra logs         |
| bash scripts/reset_db.sh | Reseta banco e reaplica migrations                 |

3. Acesse a API em http://localhost:8000 e a documentação em http://localhost:8000/docs

---

O projeto Flutter está em `/home/hell/projects/flutter/app-stepbystep-flutter`.
# api-stepbystep-python
