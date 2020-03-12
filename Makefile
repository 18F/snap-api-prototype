install: install-dev

install-dev:
	pip install pipenv
	pipenv install --dev

install-prod:
	pip install pipenv
	pipenv install

style-check:
	pipenv run flake8 --max-line-length=160

type-check:
	python3 -m pip install mypy --user
	mypy snap_financial_factors

security-check:
	pipenv run bandit -r snap_financial_factors

test:
	python3 -m pipenv run behave

check-all: style-check type-check security-check test

serve: serve-local

serve-local:
	pipenv run gunicorn "app:create_app()" --reload

serve-prod: install-prod
	pipenv run gunicorn "app:create_app()"
