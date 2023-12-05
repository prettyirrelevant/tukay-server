LINT_PATHS = apps/ common/ conf/ services/ manage.py

include .env.local

lint:
	isort $(LINT_PATHS) --diff --check-only
	ruff $(LINT_PATHS)
	pylint $(LINT_PATHS)
	mypy $(LINT_PATHS) --install-types --non-interactive

format:
	isort $(LINT_PATHS)
	ruff $(LINT_PATHS) --fix
	black $(LINT_PATHS)

test:
	@echo "Running tests..."
	python -Wa manage.py test --failfast

runserver:
	@echo 'Running Tukay development server...'
	python -X dev manage.py runserver

start-huey:
	./manage.py run_huey -w 2 -f

create-app:
	@mkdir apps/$(filter-out $@,$(MAKECMDGOALS)) && python manage.py startapp $(filter-out $@,$(MAKECMDGOALS)) apps/$(filter-out $@,$(MAKECMDGOALS))

%:
	@: