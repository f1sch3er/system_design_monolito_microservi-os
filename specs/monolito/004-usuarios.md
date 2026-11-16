# Spec 004 — Monolito: módulo Usuários

## Objetivo
Adicionar o domínio Usuários, seguindo o mesmo padrão de Produtos.

## Contexto
Produtos pronto (spec 003). O padrão de módulo já está estabelecido.

## Passos
1. Adicionar o schema de Usuário em `models.py` (ex.: `id`, `nome`, `email`).
2. Criar `monolith/app/routers/users.py` com:
   - `POST /users`
   - `GET /users`
   - `GET /users/{id}`
   - `PUT /users/{id}`
   - `DELETE /users/{id}`
3. Registrar o router no `main.py`.

## Critérios de aceite
- [ ] CRUD de usuário funciona via `/docs`.
- [ ] `GET /users/{id}` inexistente retorna `404`.
- [ ] O código segue o mesmo padrão de `products.py` (consistência).

## Conceito
Repetir o padrão de um módulo é o que faz um monolito **crescer rápido**:
você só adiciona um router novo, sem criar processo novo. É por isso que
monolitos são ótimos para começar.
