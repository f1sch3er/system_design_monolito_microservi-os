# Security — Imagens seguras (Distroless)

## Objetivo
Usar imagens de container **mínimas** (distroless) como base dos serviços,
reduzindo a superfície de ataque.

## Contexto
Hardening OWASP já aplicado (`owasp-top10.md`). As specs 010–012 usavam
`python:3.12-slim` como base. Vamos trocar a **runtime** por distroless.

## O que é distroless
- Imagem só com o **runtime** (Python) e as dependências do app.
- **Sem** shell (`/bin/sh`), **sem** package manager (apt/pip), **sem**
  utilitários (curl, bash, cat...).
- Roda como usuário **non-root** por padrão.

## Por que usar (vínculo com OWASP)

| OWASP | Como ajuda |
|-------|-----------|
| A06 — Componentes vulneráveis | menos pacotes = menos CVEs conhecidos |
| A05 — Security Misconfiguration | sem shell reduz o que um invasor faz após explorar algo |
| A01 — Broken Access Control | non-root = menos privilégio (princípio do menor privilégio) |

## Como fazer (multi-stage build)
A imagem distroless **não tem pip**. Então a receita vira dois estágios:
1. **builder**: imagem completa (só para instalar dependências).
2. **runtime**: distroless, copiando o código + o venv do builder.

```dockerfile
# Estágio 1 (builder): imagem completa só para instalar dependências
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Estágio 2 (runtime): distroless — sem shell, sem pip, usuário non-root
FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /venv /venv
COPY app ./app
ENV PATH="/venv/bin:$PATH" \
    PYTHONPATH="/venv/lib/python3.11/site-packages" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
EXPOSE 8001
ENTRYPOINT ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

> Nota: a versão do Python precisa **casar** entre builder e runtime
> (`debian12` = Python 3.11). Ajuste o `PYTHONPATH` conforme a imagem.

## Trade-offs

- **Debug mais difícil:** não dá `docker exec -it <id> bash` (não existe
  shell). Diagnóstico vira via logs (`docker logs`) e healthcheck.
- **Receita mais longa:** exige multi-stage porque a runtime não tem pip.

## Critérios de aceite

- [ ] `Dockerfile` usa multi-stage (builder completo + runtime distroless).
- [ ] A imagem final **não** contém `/bin/sh` nem pip.
- [ ] O container sobe como usuário **non-root**.
- [ ] `docker inspect` mostra a imagem final menor que a `python:3.11-slim`.

## Conceito

Imagem mínima é **defesa em profundidade**: se o app for comprometido, o
invasor encontra um ambiente sem ferramentas para se mover (sem shell, sem
curl, sem apt). É o mesmo raciocínio do `/health` por serviço: cada peça
menor e mais enxuta é mais fácil de auditar e de proteger.
