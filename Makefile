install:
		pip install pipenv
		pipenv install

test:
		python3 -m pipenv run behave

serve-local:
		env FLASK_APP=app.py FLASK_ENV=development flask run