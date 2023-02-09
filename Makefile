format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8 .

test:
	poetry run python3 manage.py test

check-all: format lint test
	poetry check

start:
	poetry run python3 manage.py runserver

shell:
	poetry run python3 manage.py shell

.PHONY: lint test check start startdb shell
