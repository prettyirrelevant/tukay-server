LINT_PATHS = apps/ conf/ services/ utils/ manage.py

include .env.local

lint:
	isort $(LINT_PATHS) --diff --check-only
	ruff format $(LINT_PATHS) --check
	ruff $(LINT_PATHS)
	pylint $(LINT_PATHS)

format:
	isort $(LINT_PATHS)
	ruff format $(LINT_PATHS)
	ruff $(LINT_PATHS) --fix

test:
	@echo "Running tests..."
	python -Wa manage.py test --failfast

runserver:
	@echo 'Running flicks dev server...'
	python -X dev manage.py runserver

start-huey:
	./manage.py run_huey -w 2 -f

create-app:
	@mkdir apps/$(filter-out $@,$(MAKECMDGOALS)) && python manage.py startapp $(filter-out $@,$(MAKECMDGOALS)) apps/$(filter-out $@,$(MAKECMDGOALS))

%:
	@: