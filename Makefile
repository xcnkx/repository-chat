include .env
export

IMAGE_NAME := tensaku_app:latest
CONTAINER_NAME := tensaku_app

.PHONY: fmt
fmt:
	poetry run black app tests
	poetry run ruff check app --fix-only --exit-zero

.PHONY: lint
lint:
	poetry run ruff app tests
	poetry run mypy app 

.PHONY: test
test:
	poetry run pytest tests

.PHONY: help
help:
	@echo "make lint"
	@echo "make fmt"
	@echo "make test"

.PHONY: qa
qa: 
	poetry run python app/main.py --repo-path $(REPO_PATH) --question $(QUESTION)

