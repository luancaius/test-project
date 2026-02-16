# User Service

[![cov](https://luancaius.github.io/test-project/badges/coverage.svg)](https://github.com/luancaius/test-project/actions)

A FastAPI microservice that exposes user profile data.

## Architecture

The service follows a **layered architecture** with clear separation between HTTP handling, business logic, and infrastructure. 
It uses a cross-cutting layer called `Shared` for Logging, Structure Logging and Settings.

### High-level layers
![general_architecture.png](assets/general_architecture.png)

![infra_layer.png](assets/infra_layer.png)

### Request flow (e.g. GET /v1/users/{id})

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Presentation
    participant SVC as UserService
    participant Repo as UserRepository
    participant Cache as Cache
    participant DB as Database

    C->>API: GET /v1/users/1
    API->>SVC: get_by_id(1)
    SVC->>Repo: get_by_id(1)
    Repo->>Cache: get(users:1)
    alt cache hit
        Cache-->>Repo: User
        Repo-->>SVC: User
    else cache miss
        Cache-->>Repo: None
        Repo->>DB: get(users, 1)
        DB-->>Repo: User or None
        opt user found
            Repo->>Cache: set(users:1, user)
        end
        Repo-->>SVC: User or None
    end
    SVC-->>API: User or None
    API-->>C: 200 + JSON or 404
```

### Layer responsibilities

| Layer | Location | Responsibility |
|-------|----------|----------------|
| **Presentation** | `src/presentation/api/v1/` | HTTP: FastAPI routers (`router.py`, `users.py`), request/response mapping, status codes (e.g. 404), and request-logging middleware. Depends only on the business layer via DI (`UserService`). |
| **Business** | `src/business/` | Application logic: `UserService` orchestrates the repository. Domain models and DTOs (`User`, `CreateUserRequest`, `UpdateUserRequest`) live in `business/models/`. No HTTP or storage details. |
| **Infrastructure** | `src/infra/` | **UserRepository** uses **Cache** (in-memory, TTL) and **Database** (persistent storage). Cache is checked first on reads; on miss, data is loaded from the database and written to the cache. Writes go to the database and refresh the cache. |
| **Shared** | `src/shared/` |  `settings` (env vars), dependency injection (`di`: structlog, cache, database, repository, service wiring, and FastAPI app factory). |

## Features

- **Endpoints:** `GET /v1/users`, `GET /v1/users/{user_id}`, `POST /v1/users`, `PATCH /v1/users/{user_id}`, and `GET /` (status).
- **Cache:** In-memory cache with configurable TTL (default 60s). GET-by-id checks the cache first; on miss, data is loaded from the database and stored in the cache. PATCH and POST refresh the cache for the affected user.
- **Database:** Persistent storage for users; the repository reads from and writes to the database, with the cache in front for GET-by-id.
- **Logging:** structlog (request start/finish in middleware; cache hits/misses, user operations, and errors in routes).

**Requirements:** Python 3.14+ (`mise` defaults to 3.14). Dependencies are managed with [uv](https://docs.astral.sh/uv/).

## Run locally

1. Install dependencies:

   ```bash
   mise run install
   ```

   or:

   ```bash
   uv sync
   ```

2. Start the application:

   ```bash
   mise run start
   ```

   The API is available at `http://localhost:8000`.  
   Swagger docs at `http://localhost:8000/docs`.

## Lint

```bash
mise run lint
```

## Test

```bash
mise run test
```

or:

```bash
pytest tests/ -v
```

### Test Coverage
```bash
mise run coverage
```


## Environment variables

| Variable              | Description                                   | Default   |
|-----------------------|-----------------------------------------------|-----------|
| `CACHE_TTL_SECONDS`   | TTL for in-memory user entries (seconds)      | 60        |
| `LOG_LEVEL`           | Logging level (e.g. INFO, DEBUG)              | INFO      |
| `SERVER_HOST`         | Bind host for uvicorn                         | 0.0.0.0   |
| `SERVER_PORT`         | Bind port                                     | 8000      |
| `SERVER_RELOAD`       | Enable uvicorn reload                         | true      |
| `APP_TITLE`           | Application title                             | User Service |

## API summary

| Method | Path                | Description                          |
|--------|---------------------|--------------------------------------|
| GET    | `/`                 | Status: `{"status": "ok", "service": "User Service"}` |
| GET    | `/v1/users`         | List all users                       |
| GET    | `/v1/users/{user_id}` | Get user by ID (404 if not found)  |
| POST   | `/v1/users`         | Create user (validates input)        |
| PATCH  | `/v1/users/{user_id}` | Partial update; repository refreshed for that entry |

## Data model

- **User:** `id` (int), `name` (str), `email` (EmailStr), `age` (optional int, > 0).
- **POST body (CreateUserRequest):** `name`, `email`, `age` (optional, > 0).
- **PATCH body (UpdateUserRequest):** any subset of `name`, `email`, `age` (optional, > 0).

---
