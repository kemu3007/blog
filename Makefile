genlock:
	pip freeze > requirements.txt
fmt:
	black src/ && isort src/
lint:
	black --check src/ && isort --check-only --diff src/ && flake8 src/
