format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8 .

test:
	poetry run python3 manage.py test

check-all: format lint
	poetry check

start:
	poetry run python3 manage.py runserver

shell:
	poetry run python3 manage.py shell

cls:
	poetry run python3 manage.py collectstatic


.PHONY: lint test check start startdb shell
