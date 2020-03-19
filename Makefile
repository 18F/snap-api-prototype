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

feature-check:
	python3 -m pipenv run behave

test:
	python3 -m pipenv run pytest tests -v

check-all: style-check type-check security-check feature-check test

serve: serve-local

serve-local:
	pipenv run gunicorn "app:create_app()" --reload

serve-prod: install-prod
	pipenv run gunicorn "app:create_app()"

deploy: deploy-cf

deploy-cf:
	cf push

logs: logs-cf

logs-cf:
	./set_app_name.sh
	cf logs ${APP_NAME}
