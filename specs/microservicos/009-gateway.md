# Spec 009 — Microserviços: API Gateway

## Objetivo
Criar um ponto único de entrada (API Gateway) que roteia para os serviços.

## Contexto
Os 4 serviços existem em portas separadas (specs 007–008).

## Passos
1. Criar `microservices/gateway/` (porta 8000).
2. O gateway expõe as mesmas rotas públicas, mas **redireciona** via HTTP
   para o serviço certo:
   - `/products/*` -> `http://localhost:8001`
   - `/users/*` -> `http://localhost:8002`
   - `/orders/*` -> `http://localhost:8003`
   - `/payments/*` -> `http://localhost:8004`
3. Testar: chamar `http://localhost:8000/products` deve retornar os produtos
   do serviço 8001, sem o cliente saber que existe um 8001.

## Critérios de aceite
- [ ] Gateway sobe na porta 8000.
- [ ] Todas as rotas funcionam passando pelo gateway.
- [ ] O cliente conversa **apenas** com `localhost:8000`.

## Conceito
No microserviço, o cliente não deve conhecer a topologia interna (8001, 8002,
...). O **API Gateway** centraliza isso: roteamento, e no mundo real também
autenticação, rate limit, agregação de respostas etc. É mais uma peça para
operar — mais um custo que o monolito não tinha.
