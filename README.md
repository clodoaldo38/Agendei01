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