[doc("Show the recipes")]
default:
    @just --list

# show recipe for example 'just show start'
show name:
    @just --show {{name}}


start: docker-build docker-up

docker-build:
    docker compose build

docker-up:
    docker compose up

test:
    uv run pytest -s

#oneliner for checking linter format
format: ruff-check ruff-format

ruff-check:
    uv run ruff check .

ruff-check-autofix:
    uv run ruff check --fix .

ruff-format:
    uv run ruff format --check .

ruff-format-autofix:
    uv run ruff format .
