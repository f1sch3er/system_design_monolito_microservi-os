# Spec 005 — Monolito: módulo Pedidos

## Objetivo
Criar o domínio Pedidos, que **integra** Usuário + Produto.

## Contexto
Produtos (003) e Usuários (004) prontos. Agora vem a primeira integração.

## Passos
1. Adicionar o schema de Pedido em `models.py`:
   - `id`, `user_id`, `product_id`, `quantidade`, `total`, `status`
2. Criar `monolith/app/routers/orders.py` com:
   - `POST /orders` -> valida que `user_id` e `product_id` existem,
     calcula `total = preco * quantidade` e cria o pedido.
   - `GET /orders`
   - `GET /orders/{id}` -> retorna o pedido com dados do usuário e do produto
     embutidos (join em memória).
3. Registrar o router no `main.py`.

## Critérios de aceite
- [ ] Criar pedido com usuário ou produto inexistente retorna erro (400/404).
- [ ] `total` é calculado a partir do preço do produto.
- [ ] `GET /orders/{id}` devolve os dados do usuário e do produto junto.

## Conceito
A integração no monolito é **uma chamada de função direta**: o módulo de
pedidos lê os dicionários de usuários e produtos que já estão na memória.
Sem rede, sem latência, sem serialização. Essa é a maior vantagem do monolito
— e a maior dificuldade de quebrá-lo depois.
