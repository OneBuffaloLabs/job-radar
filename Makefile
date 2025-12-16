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

# View live logs from the python app
logs:
	sudo docker compose logs -f web

# Quick restart of just the containers (keeps Docker Engine running)
restart:
	sudo docker compose restart web

# Open a shell inside the running python container (for debugging)
shell:
	sudo docker compose exec web bash