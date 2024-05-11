.PHONY: all
all: check-format mypy test

.PHONY: run
run:
	docker-compose up

.PHONY: format
format:
	pipenv run black .

.PHONY: check-format
check-format:
	pipenv run black . --check

.PHONY: mypy
mypy:
	pipenv run mypy .

.PHONY: test
test:
	pipenv run pytest
