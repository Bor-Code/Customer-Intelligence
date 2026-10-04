.PHONY: install format lint test build up down

install:
	uv pip install --system -e .

format:
	ruff format .
	ruff check --fix .

lint:
	ruff check .
	mypy .

test:
	pytest tests/ -v

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down
