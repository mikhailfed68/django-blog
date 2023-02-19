format:
	poetry run isort .
	poetry run black .

lint:
	poetry run flake8 .

test:
	poetry run python3 manage.py test

check-all: format lint test

start:
	poetry run python3 manage.py runserver

start-in-docker:
	python3 -m manage pause_for_db
	python3 -m manage migrate
	python3 -m manage collectstatic --no-input
	python3 -m manage runserver 0.0.0.0:8000

shell:
	poetry run python3 manage.py shell

cls:
	poetry run python3 manage.py collectstatic


.PHONY: format lint test check start startdb shell cls
