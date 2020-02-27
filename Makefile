install:
	pip install pipenv
	pipenv install

check-style:
	pipenv run flake8 --max-line-length=160

test:
	python3 -m pipenv run behave

# For now.
serve:
	env FLASK_APP=app.py FLASK_ENV=development flask run

serve-local:
	env FLASK_APP=app.py FLASK_ENV=development flask run
