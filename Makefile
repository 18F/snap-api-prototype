install:
	pip install pipenv
	pipenv install

style-check:
	pipenv run flake8 --max-line-length=160

type-check:
	mypy snap_financial_factors

test:
	python3 -m pipenv run behave

check-all: style-check type-check test

# For now.
serve:
	env FLASK_APP=app.py FLASK_ENV=development flask run

serve-local:
	env FLASK_APP=app.py FLASK_ENV=development flask run
