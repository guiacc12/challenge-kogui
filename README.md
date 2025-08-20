## Challenge Kogui

Um ambiente simples e completo para coletar leads: um formulário em Django grava no Postgres e dispara um webhook para um workflow no n8n. Tudo roda em containers com Docker.

### O que você encontra aqui
- Aplicação Django com um formulário de leads (nome, e‑mail e telefone opcional)
- Banco PostgreSQL para persistência
- n8n com workflow de recebimento e validação do webhook
- Servidor via Gunicorn e arquivos estáticos servidos pelo WhiteNoise

## Requisitos
- Docker e Docker Compose instalados
- Porta 8000 livre (app web) e 5678 livre (n8n)

## Como executar

1) Clonar o repositório
```bash
git clone <repository-url>
cd challenge-kogui
```

2) Criar um arquivo `.env` na raiz do projeto (exemplo mínimo)
```bash
# Django
SECRET_KEY=change-me
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco de dados
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=challenge
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=challenge_db
POSTGRES_PORT=5432

# n8n
N8N_WEBHOOK_URL=http://challenge_n8n:5678/webhook/lead
```

3) Subir os serviços
```bash
docker compose up -d --build
```

4) Acessar a aplicação
- App: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`

5) Criar um superusuário (opcional)
```bash
docker compose exec challenge_web python manage.py createsuperuser --username admin --email admin@example.com
```

Observação: o container da web aguarda o banco iniciar, coleta estáticos, roda migrações e inicia o Gunicorn automaticamente (veja `scripts/commands.sh`).

## Workflow no n8n
- Abrir o n8n em `http://localhost:5678`
- Importar `challenge_n8n/workflow-leads.json`
- Ativar o workflow
- Garantir que a variável `N8N_WEBHOOK_URL` no `.env` aponte para o endpoint do n8n (no compose: `http://challenge_n8n:5678/webhook/lead`)

Quando um lead é criado pelo formulário, o sistema envia um POST para o webhook do n8n com os campos `name`, `email` e `telefone`. O workflow valida e responde com sucesso (200) quando os dados estão corretos.

## Testando
- Acesse `http://localhost:8000` e envie o formulário
- Verifique no n8n (aba "Executions") as chamadas recebidas
- Se preferir inspecionar requests, use um serviço de teste de webhooks e aponte `N8N_WEBHOOK_URL` para a URL fornecida pelo serviço

## Estrutura do projeto (resumo)
```
challenge-kogui
├── challenge_web            # Aplicação Django
│   ├── leads                # App de Leads
│   ├── challenge_web        # Projeto Django
│   └── static               # CSS e imagens
├── challenge_db             # Dados persistentes (Postgres, n8n, static/media)
├── challenge_n8n            # Workflow do n8n (JSON)
├── docker-compose.yml       # Orquestração dos serviços
├── Dockerfile               # Build do container web
└── README.md                # Este guia
```

## Variáveis de ambiente importantes
- `SECRET_KEY`: chave do Django
- `DEBUG`: 1 para desenvolvimento, 0 para produção
- `ALLOWED_HOSTS`: hosts permitidos, separados por vírgula
- `DB_ENGINE`: engine do Django (ex.: `django.db.backends.postgresql`)
- `POSTGRES_*`: configurações do banco (nome, usuário, senha, host, porta)
- `N8N_WEBHOOK_URL`: URL do webhook que receberá os leads

## Dicas e solução de problemas
- Portas em uso: ajuste mapeamentos em `docker-compose.yml` se necessário
- Logs: `docker compose logs -f`
- Healthcheck da web: `http://localhost:8000/health/`
- Erro de conexão com banco: confirme `DB_ENGINE` e credenciais no `.env`

---

Feito para ser simples de rodar e fácil de entender. Se algo não funcionar como esperado, abra os logs e verifique as variáveis de ambiente — geralmente a solução está por lá.
 