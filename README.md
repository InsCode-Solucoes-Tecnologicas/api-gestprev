# api-gestprev

API da plataforma **GestPrev** — Django + Django REST Framework. Primeiro módulo: Calculadora Previdenciária.

O front fica no repositório [ui-gestprev](https://github.com/InsCode-Solucoes-Tecnologicas/ui-gestprev). Os dois conversam pelo contrato OpenAPI publicado em `/api/schema/`.

## Subir o ambiente completo (um comando)

Clone os dois repositórios lado a lado:

```
natalprev/
├── api-gestprev/
└── ui-gestprev/
```

```bash
cd api-gestprev
cp .env.example .env
docker compose up --build
```

| Endereço | O quê |
| --- | --- |
| http://localhost:8080 | Front |
| http://localhost:8080/api/docs/ | Documentação da API (Swagger) |
| http://localhost:8080/api/schema/ | Contrato OpenAPI |
| http://localhost:8080/api/admin/ | Admin do Django |

Carga inicial (ente Natal e, com `DJANGO_DEBUG=1`, o usuário `dev` com perfil Analista). Pode rodar mais de uma vez:

```bash
docker compose exec api python manage.py carga_inicial
```

A senha do `dev` vem de `DEV_USER_PASSWORD` no `.env`; se vazia, é gerada e mostrada na saída. O CNPJ do ente vem de `ENTE_CNPJ` (obrigatório com `DJANGO_DEBUG=0`).

Administrador:

```bash
docker compose exec api python manage.py createsuperuser
```

## Desenvolvimento só da API (sem Docker)

```bash
uv venv -p 3.12 .venv
uv pip install -p .venv -r requirements-dev.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Sem `POSTGRES_HOST` definido, usa SQLite local.

## Qualidade

```bash
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -q
```

O CI (GitHub Actions) roda os mesmos passos e o build da imagem em todo push e PR.

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `config/` | Settings, URLs, WSGI |
| `apps/core/` | Ente (multi-ente), perfis, autenticação por sessão |
| `apps/calculadora/` | Módulo da Calculadora Previdenciária |
| `deploy/nginx/` | Proxy reverso: front em `/`, API em `/api/` |

## Autenticação

Sessão por cookie no mesmo domínio (nginx na frente), sem JWT e sem CORS.

1. `GET /api/auth/csrf/` — recebe o cookie `csrftoken`
2. `POST /api/auth/login/` com o header `X-CSRFToken`
3. `GET /api/auth/eu/` — usuário logado e perfis
4. `POST /api/auth/logout/`

Perfis (grupos criados pela migração): Analista, Revisor, Consulta, Administrador.

## Regras

- Configurações e senhas só por variável de ambiente; `.env` nunca vai para o git.
- Container roda sem root; só o nginx publica porta.
- Valores monetários em `Decimal`, nunca `float`.
