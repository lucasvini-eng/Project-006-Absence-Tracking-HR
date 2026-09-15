# Gerenciamento de Ausências - RH

Projeto de portfólio que simula um sistema de gestão de ausências (férias,
atestados, licenças) para RH, combinando:

- **Django** (`admin_service`) — back-office administrativo. RH cadastra
  funcionários, departamentos e tipos de ausência via Django Admin, e é o
  responsável pelo schema do banco (migrations).
- **FastAPI** (`api_service`) — API pública consumida por colaboradores e
  gestores para solicitar, aprovar ou rejeitar ausências, com documentação
  automática (Swagger).
- **PostgreSQL** — banco de dados compartilhado entre os dois serviços.

## Arquitetura

```
                ┌─────────────────┐
                │   PostgreSQL     │
                │  (banco único)   │
                └───────┬─────────┘
          ┌─────────────┴─────────────┐
          │                           │
┌─────────▼─────────┐       ┌─────────▼─────────┐
│  Django (admin)    │       │  FastAPI (api)     │
│  porta 8000        │       │  porta 8001        │
│  - Django Admin    │       │  - Solicitar        │
│  - Dono do schema  │       │  - Aprovar/Rejeitar │
│  - Cadastros base  │       │  - Consultar        │
└────────────────────┘       └─────────────────────┘
```

O Django roda as migrations e é o "dono" da estrutura das tabelas. A API
FastAPI mapeia essas mesmas tabelas via SQLAlchemy (sem gerar migrations
próprias) e cuida da regra de negócio de solicitação/aprovação.

## Como rodar

1. Copie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```

2. Suba os containers:
   ```bash
   docker compose up --build
   ```

3. Em outro terminal, crie um superusuário para acessar o Django Admin:
   ```bash
   docker compose exec admin_service python manage.py createsuperuser
   ```

4. Acesse:
   - Django Admin: http://localhost:8000/admin
   - FastAPI Swagger: http://localhost:8001/docs

## Fluxo de uso sugerido

1. No Django Admin, cadastre `Departamento`, `TipoAusencia` (Férias,
   Atestado, Licença) e os `Funcionario` (definindo quem é gestor de quem).
2. Via FastAPI (`POST /ausencias/`), o colaborador solicita uma ausência.
3. O gestor aprova (`POST /ausencias/{id}/aprovar`) ou rejeita
   (`POST /ausencias/{id}/rejeitar`).
4. Se for do tipo "Férias", o saldo de dias do funcionário é debitado
   automaticamente na aprovação.

## Próximos passos (evolução do projeto)

- Autenticação/autorização (JWT) diferenciando papéis: RH, gestor, colaborador.
- Notificação por e-mail ao aprovar/rejeitar (automação de processos).
- Exportação periódica dos dados para um Data Warehouse (BigQuery) para
  alimentar um dashboard de absenteísmo no Power BI.
- Pipeline de CI/CD (GitHub Actions) rodando testes e build das imagens.
