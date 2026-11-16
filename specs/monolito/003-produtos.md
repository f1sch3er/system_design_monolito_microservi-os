# Spec 003 — Monolito: módulo Produtos

## Objetivo
Criar o primeiro domínio (Produtos) dentro do monolito, com CRUD.

## Contexto
Monolito já sobe (spec 002). Ainda não há nenhum módulo de negócio.

## Passos
1. Criar `monolith/app/models.py` com o schema de Produto (ex.: `id`, `nome`,
   `preco`, `estoque`).
2. Criar `monolith/app/storage.py` com um "banco em memória" (dicionário)
   e funções de leitura/escrita.
3. Criar `monolith/app/routers/products.py` com:
   - `POST /products` -> cria produto
   - `GET /products` -> lista produtos
   - `GET /products/{id}` -> busca um produto
   - `PUT /products/{id}` -> atualiza produto
   - `DELETE /products/{id}` -> remove produto
4. Registrar o router no `main.py`.

## Critérios de aceite
- [ ] Criar, listar, buscar, atualizar e deletar produto funciona via `/docs`.
- [ ] Buscar um id inexistente retorna `404`.
- [ ] O produto fica salvo em memória (some ao reiniciar — isso é esperado).

## Conceito
Em um monolito, cada domínio vira um **módulo/package** dentro do mesmo
processo. O "banco de dados" aqui é um dicionário compartilhado: todos os
módulos enxergam os mesmos dados (a marca de um monolito).
