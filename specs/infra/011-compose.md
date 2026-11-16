# Spec 011 — Containers: docker-compose orquestrando os serviços

## Objetivo
Subir os 5 serviços juntos com um único `docker-compose.yml`, com rede
interna e healthcheck.

## Contexto
Cada serviço já tem seu `Dockerfile` (spec 010). Agora falta orquestrar.

## Passos
1. Criar `microservices/docker-compose.yml` com 5 serviços:
   - `products`, `users`, `orders`, `payments`, `gateway`.
   - cada um com `build:` apontando para sua pasta.
   - `environment:` passando `API_KEY` e as URLs dos outros serviços.
2. **Rede interna:** as URLs passam a usar o **nome do serviço** como hostname
   (ex.: `http://orders:8003`), não `localhost`.
3. Publicar **apenas** a porta do gateway para o host (`8000:8000`).
4. Adicionar `healthcheck` em cada serviço usando o endpoint `/health` que já
   existe.
   - Como a imagem é **distroless** (sem shell), o healthcheck usa `python3`
     (não `curl`/`wget`).
5. Subir com `docker compose up --build`.

Exemplo (trecho):
```yaml
services:
  orders:
    build: ./orders
    environment:
      API_KEY: dev-api-key
      USERS_URL: http://users:8002
      PRODUCTS_URL: http://products:8001
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8003/health')"]
      interval: 10s
      timeout: 5s
      retries: 3

  gateway:
    build: ./gateway
    ports:
      - "8000:8000"
    environment:
      PRODUCTS_URL: http://products:8001
      USERS_URL: http://users:8002
      ORDERS_URL: http://orders:8003
      PAYMENTS_URL: http://payments:8004
```

## Critérios de aceite
- [ ] `docker compose up --build` sobe os 5 serviços.
- [ ] O cliente acessa tudo por `localhost:8000` (só o gateway é exposto).
- [ ] Criar pedido/pagamento funciona com os serviços se achando **por nome**.
- [ ] `docker compose ps` mostra os serviços `healthy`.

## Conceito
O `docker-compose.yml` vira o "orquestrador" que substitui os 5 `uvicorn`
manuais. A mudança mais importante de mentalidade é o **service discovery**:
dentro da rede de containers, o hostname de um serviço é o seu **nome** no
compose (`orders`, `users`...), não `localhost`. O gateway continua sendo a
única porta aberta para fora — o mesmo desenho da spec 009, só que agora a
rede é do Docker, não do seu SO.
