# Spec 007 — Microserviços: extrair Produtos

## Objetivo
Transformar o módulo de Produtos em um microserviço independente.

## Contexto
Monolito completo (specs 002–006). Agora começamos a **quebrar** ele.

## Passos
1. Criar `microservices/products/` com estrutura própria:
   - `app/main.py` (app FastAPI só de produtos)
   - `app/models.py` (só o schema de Produto)
   - `app/storage.py` (só o dicionário de produtos)
   - `requirements.txt`
2. Copiar as rotas de Produtos para esse serviço.
3. Rodar o serviço de produtos **em outra porta** (ex.: 8001).
4. Confirmar que `/docs` dele só tem Produtos.

## Critérios de aceite
- [ ] Serviço de produtos sobe sozinho na porta 8001.
- [ ] CRUD de produtos funciona via `/docs` do serviço novo.
- [ ] O monolito antigo continua funcionando (não quebramos nada).

## Conceito
Um microserviço é **um processo separado com sua própria memória**. Os
produtos que estão no serviço de produtos NÃO são visíveis para outros
serviços — para acessar, outro serviço terá que fazer **chamada HTTP**.
