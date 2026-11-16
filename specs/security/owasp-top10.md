# Spec Security — Hardening OWASP Top 10 (2021)

Achados da análise de segurança do monolito + correções aplicadas.
Cada item mapeia para o OWASP Top 10.

---

## A01 — Broken Access Control (CRÍTICO)

**Achado:**
- Nenhuma autenticação/autorização.
- IDOR: IDs sequenciais (`1`, `2`, `3`...) previsíveis, permitindo enumerar
  e manipular qualquer recurso (`GET /users/1`, `DELETE /products/1`,
  `POST /payments/3/pay`) sem checagem de dono.

**Correção aplicada:**
- Adicionada **API Key** (`monolith/app/auth.py`) exigida em todas as rotas
  de negócio (`X-API-Key`), com comparação em tempo constante
  (`secrets.compare_digest`).
- IDs agora usam **UUID v4** (`storage.py`), eliminando a enumeração.
- *Limitação honesta:* a API key é única/compartilhada. Proteção por
  usuário (multi-tenant) exige identidade por usuário — spec futura.

## A07 — Identification and Authentication Failures (CRÍTICO)

**Achado:** sem login/senha/token. Qualquer um "pagava" qualquer pedido.

**Correção aplicada:**
- Camada de autenticação via API key em todos os routers (via `Depends`).
- `/health` permanece público (padrão de health check).

## A04 — Insecure Design / validação de negócio (ALTO)

**Achado:** aceitava `preco` negativo, `estoque` negativo, `quantidade`
zero/negativa (gerava `total` negativo) e email sem formato.

**Correção aplicada (`models.py`):**
- `preco > 0` (`Field(gt=0)`).
- `estoque >= 0` (`Field(ge=0)`).
- `quantidade > 0` (`Field(gt=0)`).
- `email` validado com `EmailStr` (dependência `email-validator`).

## A06 — Vulnerable and Outdated Components (ALTO)

**Achado:** dependências sem versão fixada.

**Correção aplicada (`requirements.txt`):**
- Versões pinadas (`fastapi==0.135.3`, `uvicorn[standard]==0.42.0`,
  `email-validator==2.4.0`).

## A05 — Security Misconfiguration (MÉDIO)

**Achado:** sem security headers, sem `trusted_hosts`, `--reload` em produção.

**Correção aplicada (`main.py`):**
- Middleware de security headers: `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`.
- `TrustedHostMiddleware` com `ALLOWED_HOSTS` configurável.
- *Não aplicado aqui (nível de deploy):* HTTPS/TLS e desligar `--reload`.

## A09 — Security Logging and Monitoring (MÉDIO)

**Achado:** zero logs de eventos de segurança.

**Correção aplicada:**
- Logging configurado (`logging.basicConfig`) no `main.py`.
- Eventos de segurança logados: falha de autenticação (`auth.py`),
  criação/exclusão de recursos e pagamentos (`payments.py`, routers).

---

## Fora do Top 10 (tratados)

- **PII:** `GET /users` ainda lista emails, mas agora exige API key.
- **DoS / rate limit:** recomendado em camada de deploy (API Gateway /
  proxy reverso). Será tema natural na spec 009 (microserviços/gateway).

## Não aplicável (nota)

- **A03 (Injection):** sem SQL ainda (dados em memória). Ponto de atenção
  ao trocar por banco real (usar consultas parametrizadas).

---

## Critérios de aceite

- [ ] `GET /products` sem `X-API-Key` retorna `401`.
- [ ] Com `X-API-Key: dev-api-key` as rotas funcionam.
- [ ] Criar produto com `preco: -1` retorna `422`.
- [ ] Criar pedido com `quantidade: 0` retorna `422`.
- [ ] Criar usuário com email inválido retorna `422`.
- [ ] `/health` continua público e funcionando.
- [ ] IDs dos recursos são UUIDs (não sequenciais).

## Como testar

```bash
cd monolith
uvicorn app.main:app --reload
```

Swagger: adicione o header `X-API-Key` com valor `dev-api-key` (botão
"Authorize").
