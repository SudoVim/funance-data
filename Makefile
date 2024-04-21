.PHONY: format
format:
	pipenv run black .

.PHONY: check
check:
	pipenv run black . --check
