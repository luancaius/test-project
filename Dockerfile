FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

WORKDIR /app

COPY . .
RUN uv sync

EXPOSE 8000

ENV SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8000 \
    SERVER_RELOAD=false

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
