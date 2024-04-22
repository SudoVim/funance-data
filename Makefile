.PHONY: format
format:
	pipenv run black .

.PHONY: check
check:
	pipenv run mypy .

.PHONY: test
test:
	pipenv run pytest
