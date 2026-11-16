# Spec 010 — Containers: Dockerfile por serviço

## Objetivo
Empacotar cada serviço em uma **imagem Docker** (um `Dockerfile` por serviço).
Ainda **sem** orquestrar — só criar as imagens.

## Contexto
Microserviços prontos (specs 007–009), cada um com `requirements.txt`, `app/`
e rodando via `uvicorn`. Nenhum container ainda.

## Passos
1. Em cada serviço (`products`, `users`, `orders`, `payments`, `gateway`),
   criar um `Dockerfile` com **multi-stage** (builder + runtime distroless):
   - estágio **builder**: imagem `python:3.11-slim` só para instalar deps
   - estágio **runtime**: `gcr.io/distroless/python3-debian12` (sem shell)
   - copiar o código (`app/`) e o `venv` do builder
   - `EXPOSE` a porta do serviço
   - `ENTRYPOINT` com `uvicorn` em `--host 0.0.0.0`
2. Criar um `.dockerignore` em cada serviço (excluir `__pycache__`, `.venv`, `*.pyc`).
3. Fazer `docker build` de um serviço (ex.: `products`) e rodar.

Exemplo de `Dockerfile` (products):
```dockerfile
# Estágio 1 (builder): imagem completa só para instalar dependências
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Estágio 2 (runtime): distroless — sem shell, sem pip, usuário non-root
FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /venv /venv
COPY app ./app
ENV PATH="/venv/bin:$PATH" \
    PYTHONPATH="/venv/lib/python3.11/site-packages" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
EXPOSE 8001
ENTRYPOINT ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

> Detalhes e trade-offs do distroless: ver `specs/security/distroless.md`.

## Critérios de aceite
- [ ] Cada serviço tem seu próprio `Dockerfile` e `.dockerignore`.
- [ ] `docker build` de `products` termina sem erro.
- [ ] O container sobe e responde `GET /health`.
- [ ] A imagem final é **menor** que `python:3.11-slim` e **sem** shell.

## Conceito
Um **container** é um processo com *filesystem e rede isolados*. A **imagem**
é o snapshot empacotado; o **Dockerfile** é a receita. Dois pontos-chave que
mudam do "rodar local" para "rodar em container":
- `--host 0.0.0.0` (o container escuta em todas as interfaces, senão a rede
  de containers não alcança).
- o container tem **porta própria** e o acesso externo é controlado na hora
  de publicar a porta (no compose/`docker run -p`).
