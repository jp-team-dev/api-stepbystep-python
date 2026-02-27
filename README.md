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
- Lessons, modules e cards usam Pydantic v2 (`ConfigDict(from_attributes=True)`) para respostas consistentes com relacionamentos carregados via SQLModel.

---

O projeto Flutter está em `/home/hell/projects/flutter/app-stepbystep-flutter`.
# Testes automatizados

- Antes de rodar `make test`, suba o banco PostgreSQL (`make up` ou `docker compose up -d db`) para que `TEST_DATABASE_URL` (default `postgresql://postgres:postgres@localhost:5432/stepbystep_test`) esteja pronto.
- Como os testes usam o clone `stepbystep_test`, mantenha esse banco atualizado copiando a estrutura/dados do banco principal:
  1. Pelo **pgAdmin**: faça backup de `stepbystep`, crie `stepbystep_test` e restaure o `.backup/.sql`.
  2. Pela linha de comando: `createdb -T stepbystep stepbystep_test` (ou `pg_dump stepbystep | psql stepbystep_test`).
- O alvo `make test` cria `.venv-test`, instala as dependências e executa `PYTHONPATH=$(PWD) python -m pytest app/test_learning_api.py`.
- Os testes usam PostgreSQL porque o schema depende de arrays (`sensory_focus`), então o SQLite falhava com `visit_ARRAY`. Dessa forma eles usam o mesmo banco usado pela API.

# Ambientes Python

- Use `.venv` para desenvolvimento normal e `.venv-test` apenas para executar os testes automatizados.
- No VS Code, selecione o interpretador `.../api-stepbystep-python/.venv-test/bin/python3` (Paleta > *Python: Select Interpreter*) quando for abrir `app/test_learning_api.py` ou qualquer arquivo de teste para garantir que o editor reconhece `pytest` e as dependências instaladas naquele ambiente.
- O `Makefile` já injeta `TEST_DATABASE_URL` no alvo `test` e imprime qual valor está em uso, mas se houver outro terminal configurado com `TEST_DATABASE_URL` diferente, o `@echo` mostra isso logo no início da execução.

# PyCharm

- Ao abrir o projeto no PyCharm, configure o intérprete do projeto com o mesmo `.venv` ou `.venv-test` usado no terminal. Isso evita falso-positivos nos imports e permite rodar os testes direto pela IDE.
- Após apontar o intérprete correto, habilite o Codex Chat IA (se disponível) para ter acesso ao mesmo histórico de suporte, mas lembre que esta conversa permanece registrada neste Codex CLI, então cole trechos úteis em notas do PyCharm se precisar.
- Para a suíte de testes integrados no PyCharm, defina `TEST_DATABASE_URL` na configuração de execução (Run Configuration > Environment variables) igual a `postgresql://postgres:198870@localhost:5433/stepbystep_test`, e garanta que o serviço `docker compose up -d db` esteja rodando com a porta 5433 aberta.

# api-stepbystep-python
