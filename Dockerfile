FROM python:3.14-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /service/

#install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --locked --no-editable --no-install-project

COPY src ./src
RUN uv sync --no-dev --locked --no-editable



FROM python:3.14-alpine AS production

RUN apk add --no-cache gosu
RUN adduser -D -H worker

COPY --from=builder --chown=worker:worker /service/.venv /service/.venv
COPY --from=builder --chown=worker:worker /service/src /service/src
# Owner (worker): rwx, group (worker): rx, others: rx. or 755
RUN chmod -R u=rwx,go=rx /service

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENV PATH="/service/.venv/bin:$PATH"
WORKDIR /service
EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
