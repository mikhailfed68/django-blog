install:
	poetry install

lint:
	poetry run flake8 django_blog

test:
	poetry run pytest django_blog

test-cov:
	poetry run pytest --cov=django_blog

check-pyproject:
	poetry check

check: check-pyproject lint test

build: check
	poetry build

start: startdb
	poetry run python3 manage.py runserver

startdb:
	cat ~/.password_root | sudo service postgresql start

shell: startdb
	poetry run python3 manage.py shell

.PHONY: install lint test check build start startdb shell