# Spec 008 — Microserviços: extrair Usuários, Pedidos e Pagamentos

## Objetivo
Extrair os três domínios restantes como serviços independentes.

## Contexto
Produtos já é microserviço (spec 007). Falta o resto.

## Passos
1. Criar `microservices/users/` (mesma estrutura do de produtos, porta 8002).
2. Criar `microservices/orders/` (porta 8003):
   - Aqui começa a mudança: para criar um pedido, o serviço de pedidos deve
     **chamar via HTTP** o serviço de usuários e o de produtos.
   - Use `httpx` para consultar `GET http://localhost:8002/users/{id}` e
     `GET http://localhost:8001/products/{id}`.
   - O serviço de pedidos guarda **só a referência** (`user_id`,
     `product_id`) e uma cópia mínima (nome do produto, nome do usuário)
     para não depender dos outros serviços a cada leitura.
3. Criar `microservices/payments/` (porta 8004):
   - Para criar/pagar um pagamento, chama via HTTP o serviço de pedidos.

## Critérios de aceite
- [ ] Os 4 serviços sobem em portas diferentes (8001–8004).
- [ ] Criar pedido falha se usuário/produto não existir nos outros serviços.
- [ ] `POST /orders` funciona quando usuário e produto existem.
- [ ] Pagar atualiza via HTTP o pedido correspondente.

## Conceito
Quando os módulos viram serviços separados, a integração **muda de chamada
de função para chamada HTTP**. Você ganha independência (cada serviço pode
ser deployado/reescrito sozinho), mas paga o custo: latência de rede, falhas
de rede, e dados duplicados (cópia mínima no pedido).
