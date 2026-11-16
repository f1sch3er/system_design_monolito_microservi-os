# Spec 001 — Visão geral: monolito vs microserviços

## Objetivo
Entender o que vamos construir e por quê. Nenhuma linha de código ainda.

## Contexto
Pasta vazia. Só existe este repositório e o `README.md`.

## Passos
1. Ler o `README.md` inteiro.
2. Desenhar (em papel ou comentário) os 4 domínios: Usuários, Produtos,
   Pedidos, Pagamentos.
3. Responder mentalmente:
   - Quantos processos rodam num monolito?
   - Quantos bancos de dados um monolito usa?
   - Como dois microserviços conversam entre si?

## Critérios de aceite
- [ ] Você sabe a diferença entre "chamada de função" e "chamada via rede".
- [ ] Você sabe listar os 4 domínios do e-commerce.
- [ ] Você entendeu que vamos construir o MESMO sistema duas vezes.

## Conceito
A diferença central entre **monolito** e **microserviços** é o *boundary*:
no monolito os módulos conversam por chamada de função (mesmo processo);
nos microserviços conversam por rede (HTTP), cada um no seu processo.
