import random
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

QUESTIONS = [
    # ---------- SDD ----------
    {
        "q": "No SDD, o que vem ANTES do código?",
        "options": [
            "A especificação (spec)",
            "Os testes",
            "A documentação",
            "O deploy",
            "O docker-compose",
        ],
        "answer": "A especificação (spec)",
        "explain": "SDD = especificação antes do código: você pensa o problema antes da solução, em pedaços pequenos.",
    },
    {
        "q": "Qual campo de uma spec diz 'como sei que terminei'?",
        "options": [
            "Critérios de aceite",
            "Contexto",
            "Objetivo",
            "Conceito",
            "Passos",
        ],
        "answer": "Critérios de aceite",
        "explain": "Critérios de aceite são a lista de verificação que define 'pronto' — o coração do SDD.",
    },
    # ---------- Monolito vs Microserviços ----------
    {
        "q": "Quantos processos rodam num monolito?",
        "options": [
            "1",
            "2",
            "N (um por módulo)",
            "Depende do banco",
            "Sempre 5",
        ],
        "answer": "1",
        "explain": "Monolito = um único processo/artefato deployado; todos os módulos vivem dentro dele.",
    },
    {
        "q": "Como dois microserviços se comunicam?",
        "options": [
            "Chamada HTTP pela rede",
            "Chamada de função",
            "Variável global",
            "Arquivo compartilhado",
            "Não se comunicam",
        ],
        "answer": "Chamada HTTP pela rede",
        "explain": "Microserviços são processos separados; a ponte entre eles é a rede (HTTP/gRPC), com latência e falhas.",
    },
    {
        "q": "Quantos bancos de dados um monolito típico usa?",
        "options": [
            "1 compartilhado",
            "1 por serviço",
            "Nenhum",
            "Sempre 3",
            "1 por usuário",
        ],
        "answer": "1 compartilhado",
        "explain": "O monolito usa um banco compartilhado — é o que torna transações entre módulos triviais (mesma memória/banco).",
    },
    {
        "q": "Qual a principal vantagem dos microserviços?",
        "options": [
            "Deploy e escala independentes",
            "Menos complexidade",
            "Menos containers",
            "Sem rede",
            "Código mais curto",
        ],
        "answer": "Deploy e escala independentes",
        "explain": "A vitória real é deployar e escalar cada pedaço isolado, e organizar times por serviço.",
    },
    {
        "q": "Qual a desvantagem do monolito na hora de escalar?",
        "options": [
            "Escala o app inteiro junto",
            "Escala só o módulo pesado",
            "Nunca escala",
            "Usa mais rede",
            "Precisa de 5 containers",
        ],
        "answer": "Escala o app inteiro junto",
        "explain": "No monolito você replica o processo inteiro, mesmo que só um módulo (ex.: pagamento) esteja sobrecarregado.",
    },
    {
        "q": "Qual a alternativa entre 'monolito puro' e 'microserviços' para domínios que ainda não justificam o split?",
        "options": [
            "Monolito modular",
            "Serverless",
            "Big ball of mud",
            "Mainframe",
            "Nenhuma",
        ],
        "answer": "Monolito modular",
        "explain": "O monolito modular separa bem os módulos internos (boundaries claras) com deploy único — prepara uma futura extração sem pagar o custo de rede desde já.",
    },
    {
        "q": "No microserviço, 'pagar' atualiza o serviço de pagamento E o de pedidos. Como se chama esse problema e a solução padrão?",
        "options": [
            "Transação distribuída (resolvida com saga)",
            "Transação local (resolvida com commit)",
            "Deadlock (resolvido com lock)",
            "Índice (resolvido com B-tree)",
            "Cache (resolvido com Redis)",
        ],
        "answer": "Transação distribuída (resolvida com saga)",
        "explain": "No monolito era uma transação única no mesmo banco. Em microserviços vira transação distribuída, geralmente com padrão saga (passos + compensação).",
    },
    {
        "q": "Por que cada microserviço deve ter seu próprio banco?",
        "options": [
            "Evitar acoplamento via schema compartilhado",
            "Para gastar menos",
            "Para ter uma tabela global",
            "Obrigatório por lei",
            "Para evitar cache",
        ],
        "answer": "Evitar acoplamento via schema compartilhado",
        "explain": "Banco por serviço dá independência de evolução/deploy. O preço: joins viram chamadas de rede e transações distribuídas.",
    },
    {
        "q": "Qual opção é mais eficiente para comunicação INTERNA entre microserviços (binário, HTTP/2, contrato forte)?",
        "options": [
            "gRPC",
            "REST/JSON",
            "SOAP",
            "FTP",
            "WebSocket",
        ],
        "answer": "gRPC",
        "explain": "gRPC usa protobuf (binário) e HTTP/2 (multiplex) — mais leve e com contrato forte, comum em comunicação interna de alto volume.",
    },
    {
        "q": "Qual a principal vantagem de comunicação ASSÍNCRONA (fila) entre serviços?",
        "options": [
            "Desacoplamento e resiliência (não espera resposta)",
            "Latência menor que HTTP",
            "Garante consistência forte",
            "Substitui o banco de dados",
            "Mais simples de implementar",
        ],
        "answer": "Desacoplamento e resiliência (não espera resposta)",
        "explain": "Com fila/mensageria o produtor não bloqueia; se um serviço cai, a mensagem fica na fila e é processada depois.",
    },
    {
        "q": "Quando a atualização entre serviços acontece de forma assíncrona, qual consistência é normalmente aceita?",
        "options": [
            "Eventual",
            "Forte",
            "Linearizável",
            "Serializável",
            "Atomicidade total",
        ],
        "answer": "Eventual",
        "explain": "Em sistemas distribuídos aceita-se que os dados convergem depois de um tempo (eventual), em troca de disponibilidade e desacoplamento.",
    },
    {
        "q": "No teorema CAP, se você prioriza Consistência e Tolerância a Partição (CP), abre mão de?",
        "options": [
            "Disponibilidade",
            "Consistência",
            "Tolerância a partição",
            "Latência",
            "Segurança",
        ],
        "answer": "Disponibilidade",
        "explain": "CAP: sob partição de rede você escolhe entre consistência (CP) ou disponibilidade (AP). A partição em si não é opcional.",
    },
    # ---------- API Gateway ----------
    {
        "q": "Qual destas NÃO é uma responsabilidade típica do API Gateway?",
        "options": [
            "Armazenar o banco de dados dos serviços",
            "Roteamento",
            "Autenticação",
            "Rate limiting",
            "Agregação de respostas",
        ],
        "answer": "Armazenar o banco de dados dos serviços",
        "explain": "O gateway roteia, autentica, limita taxa e agrega — mas NÃO guarda dados de negócio.",
    },
    {
        "q": "Qual o risco de ter um ÚNICO API Gateway?",
        "options": [
            "Ponto único de falha",
            "Fica mais rápido",
            "Melhora a segurança sempre",
            "Remove a rede",
            "Nenhum risco",
        ],
        "answer": "Ponto único de falha",
        "explain": "Se o gateway cai, tudo cai. Em produção se mitiga com réplicas e failover — mais uma peça pra operar.",
    },
    {
        "q": "Qual técnica protege a API contra abuso e DoS?",
        "options": [
            "Rate limiting",
            "Cache",
            "Compressão",
            "Idempotência",
            "Service discovery",
        ],
        "answer": "Rate limiting",
        "explain": "Rate limiting limita requisições por janela de tempo (por IP/chave), tipicamente no gateway.",
    },
    # ---------- Containers ----------
    {
        "q": "O que é um Dockerfile?",
        "options": [
            "A receita que gera a imagem",
            "O container em execução",
            "O snapshot empacotado",
            "O orquestrador",
            "O banco de dados",
        ],
        "answer": "A receita que gera a imagem",
        "explain": "Dockerfile = receita; imagem = snapshot resultante; container = processo em execução.",
    },
    {
        "q": "O que faz o docker-compose?",
        "options": [
            "Orquestra vários containers (rede + healthcheck)",
            "Cria uma imagem",
            "Roda um único processo",
            "Compila o código",
            "Substitui o Python",
        ],
        "answer": "Orquestra vários containers (rede + healthcheck)",
        "explain": "docker-compose orquestra múltiplos containers: rede, dependências e healthchecks.",
    },
    {
        "q": "Na rede Docker, como um serviço encontra outro?",
        "options": [
            "Pelo nome do serviço (ex.: http://orders:8003)",
            "Por localhost",
            "Por IP público",
            "Por DNS externo",
            "Por sorte",
        ],
        "answer": "Pelo nome do serviço (ex.: http://orders:8003)",
        "explain": "Na rede Docker o hostname é o nome do serviço (service discovery do compose). IPs mudam a cada deploy.",
    },
    {
        "q": "Como um serviço descobre onde estão as instâncias dos outros em tempo real?",
        "options": [
            "Service discovery (DNS/Consul/k8s)",
            "IP fixo no código",
            "Arquivo de hosts manual",
            "Variável global",
            "Não precisa descobrir",
        ],
        "answer": "Service discovery (DNS/Consul/k8s)",
        "explain": "Em containers os IPs mudam a cada deploy. Service discovery mantém um registro atualizado (no seu caso, o compose fez isso por nome).",
    },
    {
        "q": "Escalar horizontalmente significa?",
        "options": [
            "Adicionar mais instâncias",
            "Aumentar CPU/RAM de uma máquina",
            "Trocar o banco",
            "Diminuir o número de serviços",
            "Mover pra nuvem",
        ],
        "answer": "Adicionar mais instâncias",
        "explain": "Horizontal = mais réplicas. Vertical = máquina maior. Microserviços favorecem o horizontal por serviço.",
    },
    {
        "q": "Por que serviços 'stateless' escalam melhor?",
        "options": [
            "Qualquer instância atende qualquer requisição",
            "Guardam sessão no servidor",
            "Não usam banco",
            "São mais rápidos em CPU",
            "Não precisam de rede",
        ],
        "answer": "Qualquer instância atende qualquer requisição",
        "explain": "Sem estado no servidor, o load balancer manda qualquer request pra qualquer réplica; o estado vai pro cliente/banco/cache.",
    },
    {
        "q": "Qual estratégia de deploy libera a nova versão para uma pequena fração de usuários primeiro?",
        "options": [
            "Canary",
            "Big bang",
            "Rollback",
            "Rebuild",
            "Blue-only",
        ],
        "answer": "Canary",
        "explain": "Canary expõe a mudança a um subconjunto, monitora e amplia. Blue-green é a variante com troca total entre dois ambientes.",
    },
    {
        "q": "Onde devem ficar configurações como API_KEY e URLs de serviços (12-factor)?",
        "options": [
            "Em variáveis de ambiente",
            "Hardcoded no código",
            "No banco de dados",
            "Num arquivo no repo",
            "No README",
        ],
        "answer": "Em variáveis de ambiente",
        "explain": "O 12-factor manda separar código de configuração. Env vars deixam o mesmo artefato rodar em qualquer ambiente sem mudar código.",
    },
    {
        "q": "Para reduzir chamadas ao serviço de produtos (dados que mudam pouco), qual técnica?",
        "options": [
            "Cache (ex.: Redis)",
            "Fila (RabbitMQ)",
            "Índice no banco",
            "Load balancer",
            "Circuit breaker",
        ],
        "answer": "Cache (ex.: Redis)",
        "explain": "Cache evita recomputar/refetch de dados quentes. O trade-off é lidar com invalidação (dado desatualizado).",
    },
    {
        "q": "Quando um serviço recebe mais requisições do que consegue processar, o que ajuda a não perder/sobrecarregar?",
        "options": [
            "Fila/mensageria (backpressure)",
            "Mais logs",
            "Criptografia",
            "Rate limiting inverso",
            "Comentários",
        ],
        "answer": "Fila/mensageria (backpressure)",
        "explain": "A fila absorve o pico e o consumidor processa no seu ritmo (backpressure), desacoplando produtor e consumidor.",
    },
    {
        "q": "Quais são os 3 pilares da observabilidade?",
        "options": [
            "Logs, métricas e tracing",
            "Logs, cache e fila",
            "CPU, RAM e disco",
            "Auth, rate limit e TLS",
            "Build, test e deploy",
        ],
        "answer": "Logs, métricas e tracing",
        "explain": "Logs (o que aconteceu), métricas (agregados numéricos) e tracing (caminho da requisição entre serviços) — essenciais em N serviços.",
    },
    {
        "q": "Qual padrão impede que uma falha num serviço vire cascata de falhas?",
        "options": [
            "Circuit breaker",
            "Load balancer",
            "Reverse proxy",
            "Cache",
            "Singleton",
        ],
        "answer": "Circuit breaker",
        "explain": "O circuit breaker 'abre' quando um serviço está doente e passa a falhar rápido (fail fast), sem continuar chamando.",
    },
    # ---------- Segurança ----------
    {
        "q": "O que é IDOR?",
        "options": [
            "Acessar recurso de outro usuário por ID, sem autorização",
            "Injeção de SQL",
            "Criptografia fraca",
            "Um tipo de firewall",
            "Uma assinatura digital",
        ],
        "answer": "Acessar recurso de outro usuário por ID, sem autorização",
        "explain": "IDOR = Insecure Direct Object Reference: trocar o ID na URL e acessar dado de outro usuário sem checagem de dono.",
    },
    {
        "q": "O que a imagem distroless remove?",
        "options": [
            "Shell e package manager",
            "O Python",
            "O kernel",
            "O código da app",
            "O Docker",
        ],
        "answer": "Shell e package manager",
        "explain": "Distroless remove shell e package manager -> menos superfície de ataque e menos CVEs.",
    },
    {
        "q": "Por que rodar o container como usuário non-root?",
        "options": [
            "Princípio do menor privilégio",
            "Mais performance",
            "É obrigatório no Docker",
            "Para ter shell",
            "Para instalar pip",
        ],
        "answer": "Princípio do menor privilégio",
        "explain": "Menor privilégio: se o container for comprometido, o invasor não roda como root.",
    },
    {
        "q": "Uma API key padrão fixa ('dev-api-key') em produção fere qual item do OWASP?",
        "options": [
            "A07 - Falhas de identificação/autenticação",
            "A03 - Injection",
            "A09 - Logging",
            "A02 - Falhas criptográficas",
            "Nenhum",
        ],
        "answer": "A07 - Falhas de identificação/autenticação",
        "explain": "Segredo fixo/default e sem autenticação robusta é falha de identificação/autenticação (A07).",
    },
    {
        "q": "Por que a operação de PAGAMENTO precisa ser idempotente?",
        "options": [
            "Para retry não cobrar duas vezes",
            "Para rodar mais rápido",
            "Para evitar cache",
            "Para criptografar o valor",
            "Para escalar horizontalmente",
        ],
        "answer": "Para retry não cobrar duas vezes",
        "explain": "Se a rede falha e o cliente reenvia, a operação idempotente garante o mesmo efeito uma única vez (crítico em dinheiro).",
    },
]


def ask(question):
    options = [(o, o == question["answer"]) for o in question["options"]]
    random.shuffle(options)

    print(f"\n{question['q']}")
    for i, (text, _) in enumerate(options, 1):
        print(f"  {i}) {text}")

    while True:
        try:
            raw = input("Resposta (1-5): ").strip()
            if not raw:
                continue
            n = int(raw)
            if 1 <= n <= 5:
                return options[n - 1][1], question["answer"]
            print("Digite um número entre 1 e 5.")
        except ValueError:
            print("Digite um número entre 1 e 5.")


def main():
    print("=" * 56)
    print("QUIZ - System Design (preparação para entrevistas)")
    print("Responda de 1 a 5. Ctrl+C para sair a qualquer momento.")
    print("=" * 56)

    questions = QUESTIONS[:]
    random.shuffle(questions)

    score = 0
    wrong = []

    for i, q in enumerate(questions, 1):
        correct, answer = ask(q)
        if correct:
            print("[Correto!]")
            score += 1
        else:
            print(f"[Errado] A correta era: {answer}")
            wrong.append((q["q"], answer))
        print(f"  -> {q['explain']}")

    total = len(questions)
    print("\n" + "=" * 56)
    print(f"RESULTADO: {score}/{total}")
    print("=" * 56)

    if wrong:
        print("\nVocê errou:")
        for q, answer in wrong:
            print(f"  - {q}  ->  {answer}")
    else:
        print("Perfeito, tudo certo!")

    if score == total:
        print("Domínio total dos conceitos.")
    elif score >= total * 0.7:
        print("Bom nível. Revisa os que errou.")
    else:
        print("Vale revisar as specs em specs/.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSaindo...")
        sys.exit(0)
