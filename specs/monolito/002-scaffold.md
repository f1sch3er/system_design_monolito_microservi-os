# Spec 002 — Monolito: scaffold do projeto FastAPI

## Objetivo
Ter um app FastAPI mínimo rodando na pasta `monolith/`.

## Contexto
Só existe o `README.md` e a spec 001. Ainda não há código.

## Passos
1. Criar a pasta `monolith/`.
2. Criar `monolith/requirements.txt` com:
   ```
   fastapi
   uvicorn[standard]
   ```
3. Criar `monolith/app/__init__.py` (vazio).
4. Criar `monolith/app/main.py` com um app FastAPI e uma rota de saúde que
   reporta cada módulo:
   - `GET /health` -> `{"status": "ok", "modules": { ... }}`
   - cada módulo reporta `ok` (alcançável) e a quantidade de registros.
5. Rodar e testar no Swagger (`/docs`).

## Critérios de aceite
- [ ] `uvicorn app.main:app --reload` sobe sem erro.
- [ ] `GET /health` responde `200` com `status: ok` e um bloco `modules`.
- [ ] `/docs` abre o Swagger.

## Conceito
Um **monolito** começa com *um único* processo (um `main.py`, um `uvicorn`).
Todas as rotas futuras vão morar aqui dentro. Um `/health` por módulo já
adianta a ideia de que, mais tarde, cada módulo terá que reportar sua própria
saúde quando virar um microserviço.
