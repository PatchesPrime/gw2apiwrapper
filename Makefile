init:
	pip install pipenv
	pipenv install --dev
	pipenv install

test:
	pipenv run py.test tests
