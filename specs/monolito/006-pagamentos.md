# Spec 006 — Monolito: módulo Pagamentos

## Objetivo
Adicionar o domínio Pagamentos, ligado a um Pedido.

## Contexto
Pedidos pronto (spec 005). Pagamentos completa o monolito.

## Passos
1. Adicionar o schema de Pagamento em `models.py`:
   - `id`, `order_id`, `valor`, `status` (`pendente` -> `pago`)
2. Criar `monolith/app/routers/payments.py` com:
   - `POST /payments` -> valida que o pedido existe e usa `order.total`
     como valor.
   - `GET /payments`
   - `POST /payments/{id}/pay` -> muda status para `pago` e atualiza o
     status do pedido para `pago`.
3. Registrar o router no `main.py`.

## Critérios de aceite
- [ ] Criar pagamento para pedido inexistente retorna erro.
- [ ] Pagar atualiza o pagamento **e** o pedido (transação entre módulos).
- [ ] `GET /payments` lista os pagamentos.

## Conceito
"Pagar" toca em **dois módulos ao mesmo tempo** (pagamento + pedido). No
monolito isso é trivial: as duas tabelas estão na mesma memória e você pode
atualizar as duas "na mesma transação". Em microserviços, isso vira um dos
problemas mais difíceis da área (transação distribuída).
