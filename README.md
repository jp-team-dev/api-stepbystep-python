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

## Novos recursos guiados

- A API agora organiza o conteúdo em `modules` → `lessons` → `cards`, permitindo criar trilhas de aprendizagem guiadas.
- Endpoints como `POST /learning/modules`, `GET /learning/lessons`, `GET /learning/cards?lesson_id=<id>` suportam filtros e relacionamentos.
- Cada card pode pertencer a uma lição e fornece um `sensory_cue` para experiências sensoriais controladas.
- O campo `sensory_focus` da entidade `Module` aceita agora uma lista com múltiplas opções de estímulo (ex: `["visual", "vocal"]`), mantendo o registro da combinação de canais.

---

O projeto Flutter está em `/home/hell/projects/flutter/app-stepbystep-flutter`.
# api-stepbystep-python
