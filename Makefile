.PHONY: lint format cov

lint:
	python3 -m flake8 --exclude=.git/,.direnv/,.pyenv/ --ignore=E203,E501,W503
	python3 -m isort --check-only --skip-glob .pyenv --profile black .
	python3 -m black --check --exclude '/(\.git|\.direnv|\.pyenv)/' .

format:
	python3 -m black --exclude '/(\.git|\.direnv|\.pyenv)/' .
	python3 -m isort --skip-glob .pyenv --profile black .

cov:
	python3 -m coverage run --source='.' --omit '.pyenv/*' manage.py test
	python3 -m coverage report -m
