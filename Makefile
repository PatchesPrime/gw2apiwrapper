init:
	pip install pipenv
	pipenv install --dev
	pipenv install

test:
	pipenv run py.test --cov=GW2API tests
	coveralls
