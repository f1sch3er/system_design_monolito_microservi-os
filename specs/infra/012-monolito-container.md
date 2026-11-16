# Spec 012 — Containers: monolito em 1 container (comparação)

## Objetivo
Empacotar o monolito em **1 único container** e comparar com os 5 containers
dos microserviços.

## Contexto
Microserviços já rodam em 5 containers (spec 011). O monolito (specs 002–006)
nunca foi containerizado.

## Passos
1. Criar `monolith/Dockerfile` (mesma receita **multi-stage/distroless** da
   spec 010, porta 8000).
2. Criar `monolith/.dockerignore`.
3. Rodar o monolito num container único e testar as mesmas rotas.
4. Fazer a comparação lado a lado.

## Critérios de aceite
- [ ] `docker build` e `docker run` do monolito funcionam.
- [ ] As mesmas rotas funcionam num único container.

## Conceito
Aqui fica **visual** a diferença:

| | Monolito | Microserviços |
|---|---|---|
| Containers | 1 | 5 |
| Rede entre serviços | nenhuma (tudo no processo) | HTTP dentro da rede Docker |
| "Subir" tudo | 1 comando, 1 imagem | compose com 5 imagens |
| Escalar um módulo | escala tudo junto | escala só o container do módulo |

O monolito é mais simples de empacotar (1 imagem). Os microserviços custam
mais "empacotamento" (5 imagens, rede, healthcheck) — mas ganham deploy e
escala independentes. É o mesmo trade-off, agora medido em containers.
