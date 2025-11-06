# Agendei

Aplicação Django com fluxo de autenticação (login, signup, recuperação), listagem de serviços e base PWA.

## Executar localmente (Docker produção)

1. `docker compose -f docker-compose.prod.yml up --build`
2. Acesse `http://localhost:8000/` (ou o IP da máquina: `http://SEU_IP:8000/`).

## Executar localmente (Python)

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
```

## Testar pelo GitHub (CI)

- Cada push/PR dispara o workflow em `.github/workflows/ci.yml`:
  - `manage.py check --deploy`
  - `collectstatic`
  - `manage.py test`
- Em "Actions" você pode acompanhar logs e status dos testes.

## Testar pelo GitHub Codespaces

1. No repositório, clique em "Code" → "Create codespace".
2. Aguarde a instalação automática das dependências.
3. No terminal do Codespaces:
   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```
4. Abra a porta 8000 (forwarded) e acesse a URL gerada pelo Codespaces.

## Variáveis de ambiente

- `SECRET_KEY` (obrigatória em produção)
- `DEBUG` (`0` ou `1`)
- `DATABASE_URL` (ex.: `postgresql://user:pass@host:5432/db`)
- `ALLOWED_HOSTS` (ex.: `*` para testes)
- `CSRF_TRUSTED_ORIGINS` (ex.: `http://seu-ip,http://seu-ip:8000`)

## Notas

- Whitenoise serve estáticos em produção após `collectstatic`.
- PWA básico com `manifest.json` e `service-worker.js`.

## Deploy no Render (Blueprint)

Este repositório inclui `render.yaml` para provisionar automaticamente:
- Serviço Web (`agendei01-web`) usando nosso `Dockerfile`.
- Banco Postgres gerenciado (`agendei01-db`).

Passos:
- No Render, crie um Blueprint apontando para este repositório.
- Render criará o banco e o serviço web; nas variáveis ficam:
  - `SECRET_KEY` (gerada automaticamente)
  - `DATABASE_URL` (do banco gerenciado)
  - `ALLOWED_HOSTS=*.onrender.com`
  - `CSRF_TRUSTED_ORIGINS=https://*.onrender.com`
- O serviço usará `PORT` definida pelo Render; o Dockerfile inicia Gunicorn com `0.0.0.0:${PORT:-8000}`.

Após deploy, acesse:
- `https://<seu-servico>.onrender.com/conta/signup/` (cadastro)
- `https://<seu-servico>.onrender.com/conta/login/` (login)
- `https://<seu-servico>.onrender.com/servicos/` (serviços)

### Migrações e SMTP

- Migrações: o blueprint executa automaticamente `python manage.py migrate` após cada deploy.
- SMTP: variáveis já previstas no `render.yaml` — ajuste no painel do Render:
  - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
  - `EMAIL_HOST` (ex.: `smtp.sendgrid.net`)
  - `EMAIL_PORT=587`
  - `EMAIL_USE_TLS=1`
  - `EMAIL_HOST_USER` (ex.: `apikey` no SendGrid)
  - `EMAIL_HOST_PASSWORD` (defina como Secret)
  - `DEFAULT_FROM_EMAIL` (ex.: `no-reply@seu-dominio.com`)