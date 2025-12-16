# .PHONY tells make that these are commands, not files
.PHONY: up down logs restart shell

# Start the Docker Engine, then build and start containers
up:
	@echo "Starting Docker Service..."
	sudo systemctl start docker
	@echo "Booting up containers..."
	sudo docker compose up --build -d
	@echo "Job Radar is online! 🚀"

# Stop containers, then stop the Docker Engine to save resources
down:
	@echo "Stopping containers..."
	sudo docker compose down
	@echo "Stopping Docker Service..."
	sudo systemctl stop docker
	@echo "System is resting. 💤"

# Full system reboot: Stops Docker engine, then starts everything fresh
reboot: down up

# Rebuilds containers without stopping the Docker Engine (Faster)
rebuild:
	@echo "Rebuilding containers..."
	rm -f poetry.lock
	sudo docker compose down
	sudo docker compose up --build -d
	@echo "Generating new lock file..."
	sudo docker compose exec web poetry lock
	@echo "Rebuild complete! 🛠️"

# View live logs from the python app
logs:
	sudo docker compose logs -f web

# View live logs from the background worker
worker-logs:
	sudo docker compose logs -f worker

# View live logs from the beat scheduler
beat-logs:
	sudo docker compose logs -f celery-beat

# View ALL logs (useful for seeing the interaction between api and worker)
logs-all:
	sudo docker compose logs -f

# Quick restart of just the containers (keeps Docker Engine running)
restart:
	sudo docker compose restart web

# Open a shell inside the running python container (for debugging)
shell:
	sudo docker compose exec web bash

# Run the automated test suite
test:
	sudo docker compose exec web python -m pytest -v

# Run static code analysis to find errors and style violations
lint:
	sudo docker compose exec web python -m ruff check .

# Auto-format code (adjusts spacing, indentation, and quotes)
format:
	sudo docker compose exec web python -m ruff format .

# Auto-fix linting issues (sorts imports, removes unused variables)
fix:
	sudo docker compose exec web python -m ruff check --fix .