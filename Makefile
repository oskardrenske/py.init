.ONESHELL:  # Everything in one shell to make it easier to use venv windows
.DEFAULT_GOAL := help  # Om du bara skriver make

# kör även om det inte finns en fil med samma namn som kommandot
.PHONY: all

# Indentering görs med tab i makefile, inte spaces
# topp-nivån är make-kommandon
# indenterat körs i ett shell
# 

# Remove old venv and cached files
# Create new venv and install dependencies
# Run tests so you know that they pass before you start working
install: clean setup_venv test
	@echo "** Installation complete **"

activate_venv:
	. .venv/bin/activate  # dot instead of source is make-specific

git-pull:
	git pull

refresh: clean git-pull install


setup_venv:
	uv venv  # skapa venv
	. .venv/bin/activate 
	uv sync  # Installera dependencies från uv.lock
	pre-commit install # konfigurera git hooks och installera 
	
# Ta bort ven voch cachade filer
clean:
	@echo "** Deleting venv and cached files **"
	rm -rf .venv/
	rm -rf __pycache__/
	rm -rf .pytest_cache

# Kör tester med coverage (cov-report i terminalen)
test:  activate_venv
	pytest --cov . tests

# köra ruff check
lint: activate_venv
	ruff check

# Formattera koden med ruff check
format: activate_venv
	ruff format

# Allt du vill göra innan en commit
commit: activate_venv lint format test
	
# Om du har docker kan du göra snabbkommandon
docker: commit
	docker build .

# conditions skall inte vara indenterade
windows:
	@echo "Check if you're running Windows"
ifeq ($(OS), Windows_NT)
	@echo "- You run windows"
endif
ifneq ($(OS), Windows_NT)
	@echo "- You don't run Windows"
endif

help:
	@echo "Kolla i Makefile vilka kommandon som finns"

h: help
