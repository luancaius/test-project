# Senior Software Engineer Assessment

## Objective

Build a microservice exposing user profile data. The service must demonstrate:

1. Well-structured Python code
2. FastAPI best practices
3. Caching (in-memory with TTL)
4. Logging (structured)
5. Unit testing
6. Documentation
7. Kubernetes deployability

---

## Task Description

Create a FastAPI service with the following endpoints:

| Endpoint           | Method | Description                                                                 |
|--------------------|--------|-----------------------------------------------------------------------------|
| `/users/{user_id}` | GET    | Returns user data by ID. Returns 404 if not found.                         |
| `/users`           | GET    | Returns all users.                                                         |
| `/users`           | POST   | Creates a new user. Validates input.                                       |
| `/users/{user_id}` | PATCH  | Updates a user's data partially and refreshes the cache.                   |

---

## Data Model

```python
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = None
```

---

## Requirements

### 1. Python Code Standards

1. Use PEP8 style and type hints.
2. Modular structure.

### 2. Caching

1. Use an in-memory cache with TTL to cache `GET /users/{user_id}` for **60 seconds**.
2. When a user is updated via PATCH, **refresh the cache immediately**.
3. Log cache hits, misses, and refreshes.

### 3. Logging

1. Use **structured JSON logs**.
2. Log incoming requests, errors, cache hits/misses, cache refresh events, and startup events.

### 4. Unit Testing

1. Use **pytest**.
2. Test `GET /users/{user_id}`, `GET /users`, `POST /users`, and `PATCH /users/{user_id}`.
3. Include **cache refresh behavior** in tests.

### 5. Deployment

1. Provide a **Dockerfile** to run the service.
2. **Kubernetes deployment:**
   - Deployment with **2 replicas**
   - Service to expose the API
   - Optional **ConfigMap** for cache configuration

### 6. Documentation

1. **README** with instructions to run locally, test, build Docker, and deploy to Kubernetes.

---

## Deliverables

1. Source code with proper structure.
2. Dockerfile.
3. Kubernetes manifests (Deployment, Service, ConfigMap).
4. README with instructions.
5. Unit tests demonstrating coverage, including cache refresh.
