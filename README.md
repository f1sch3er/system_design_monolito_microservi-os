# System Design: Monolito vs Microserviços

Projeto didático para entender **dois conceitos ao mesmo tempo**:

1. **SDD (Spec-Driven Development)** — a forma de organizar o trabalho em
   *specs* (especificações) pequenas, uma por vez, antes de escrever código.
2. **Monolito vs Microserviços** — o mesmo sistema construído das duas formas,
   para comparar na prática.

---

## O que é SDD?

SDD (Spec-Driven Development) é um jeito de trabalhar em que **a especificação
vem antes do código**. Em vez de "sair codando", você:

1. Escreve uma **spec** (um documento curto) dizendo *o quê* fazer e *por quê*.
2. Implementa o mínimo necessário para **satisfazer os critérios de aceite**.
3. Revisa e parte para a próxima spec.

A spec é pequena o suficiente para caber na cabeça de uma vez. Isso evita
"paralisia diante de um projeto grande" e te obriga a pensar no problema antes
de pensar na solução.

### Anatomia de uma spec (nosso padrão)

Toda spec em `specs/` segue este formato:

| Campo | O que responde |
|-------|----------------|
| Objetivo | O que vamos entregar nesta task |
| Contexto | O que já existe até agora |
| Passos | Como fazer, em pedaços pequenos |
| Critérios de aceite | Como saber que terminou (lista de verificação) |
| Conceito | O conceito de system design que esta task ensina |

> Regra de ouro: **nunca pule uma spec**. Cada uma ensina um pedaço.

---

## Monolito vs Microserviços (em 1 minuto)

| | Monolito | Microserviços |
|---|---|---|
| Quantos processos | 1 | N (um por serviço) |
| Comunicação | Chamada de função (em processo) | Rede (HTTP/gRPC) |
| Banco de dados | 1 banco compartilhado | 1 banco por serviço |
| Deploy | Deploy único (tudo junto) | Deploy independente |
| Escalar | Escala o app inteiro | Escala só o serviço pesado |
| Complexidade | Baixa no início, cresce | Alta no início, estável |

**A ideia do projeto:** construímos o *mesmo* e-commerce de duas formas e
sentimos a diferença.

---

## O sistema (e-commerce simples)

Quatro módulos/domínios:

```
Usuários  ->  quem compra
Produtos  ->  o que é vendido
Pedidos   ->  junta usuário + produto(s)
Pagamentos->  ligado a um pedido
```

Cada módulo expõe uma pequena API REST (FastAPI).

---

## Estrutura do projeto

```
system_design/
├── README.md               <- você está aqui
├── specs/                  <- SDD: uma spec = uma task pequena
│   ├── 001-visao-geral.md  <- visão geral (monolito vs microserviços)
│   ├── monolito/           <- specs do monolito (002-006)
│   ├── microservicos/      <- specs dos microserviços (007-009)
│   ├── infra/              <- specs de containers (010-012)
│   └── security/           <- hardening OWASP Top 10
├── monolith/               <- versão 1: tudo em um único processo
└── microservices/          <- versão 2: um processo por serviço
```

---

## Roadmap (as tasks, em ordem)

| Spec | Título | Entrega |
|------|--------|---------|
| 001 | Visão geral | Entender o plano |
| 002 | Scaffold do monolito | App FastAPI no ar |
| 003 | Módulo Produtos | CRUD de produtos |
| 004 | Módulo Usuários | CRUD de usuários |
| 005 | Módulo Pedidos | Pedidos integrando usuário+produto |
| 006 | Módulo Pagamentos | Pagamento ligado a pedido |
| 007 | Extrair Produtos | Primeiro microserviço |
| 008 | Extrair o resto | Usuários, Pedidos, Pagamentos |
| 009 | API Gateway | Roteamento + comunicação HTTP |
| 010 | Dockerfile por serviço | Empacotar cada serviço em imagem |
| 011 | docker-compose | Orquestrar os 5 serviços + rede interna |
| 012 | Monolito em 1 container | Comparação 1 vs 5 containers |

> **Plus (fora do curso):** a parte de segurança — `specs/security/` com
> `owasp-top10.md` (hardening OWASP Top 10 aplicado) e `distroless.md`
> (imagens de container mínimas) — foi solicitada por fora do curso, como
> conteúdo extra/bônus.

---

## Como rodar (monolito)

```bash
cd monolith
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Depois acesse `http://127.0.0.1:8000/docs` (Swagger) para testar a API.

---

## Regras do jogo

- Implementamos **primeiro o monolito** (specs 002–006), depois o **split**
  (specs 007–009).
- Armazenamento **em memória** (dicionários Python) para não complicar.
- Uma spec por vez. Se uma spec não estiver clara, melhore a spec antes de
  codar.
