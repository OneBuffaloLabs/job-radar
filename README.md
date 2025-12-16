# Job Radar 📡

> **High-performance job aggregation engine built with FastAPI, SQLAlchemy, and AsyncIO.**

![CI Status](https://github.com/OneBuffaloLabs/job-radar/actions/workflows/ci.yml/badge.svg)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📖 About

Job Radar is an asynchronous microservice designed to aggregate, normalize, and serve job posting data from multiple sources. It leverages modern Python type systems for validation and uses an event-driven architecture for data ingestion.

This project serves as an architectural reference for building scalable Python backends using **FastAPI** and **SQLModel**.

## 🛠 Tech Stack

- **Runtime:** Python 3.12+
- **Framework:** FastAPI (Async/Await)
- **Database:** PostgreSQL 15 (via Docker)
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **HTTP Client:** HTTPX (Async)
- **Migrations:** Alembic
- **Dependency Management:** Poetry
- **Linting/Formatting:** Ruff

## 🚀 Getting Started

This project uses a containerized development environment. You do not need Python or Postgres installed on your host machine—only **Docker** and **Make**.

### Prerequisites

- Docker & Docker Compose
- Make (Standard on Linux/Mac, install via Chocolatey/Winget on Windows)

### Quick Start

The project includes a `Makefile` to handle the lifecycle of the application and the Docker daemon.

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/OneBuffaloLabs/job-radar.git](https://github.com/OneBuffaloLabs/job-radar.git)
    cd job-radar
    ```

2.  **Start the environment**
    This command will start the Docker service (systemd), build the containers, and run them in the background.

    ```bash
    make up
    ```

3.  **Verify Status**
    View the live logs to ensure the application is running:

    ```bash
    make logs
    ```

4.  **Access the API**
    - **API Root:** [http://localhost:8000](http://localhost:8000)
    - **Interactive Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
    - **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Developer Command Reference

We use `make` to abstract complex Docker Compose commands.

| Command        | Description                                                             |
| :------------- | :---------------------------------------------------------------------- |
| `make up`      | Start Docker Engine and boot up containers.                             |
| `make down`    | Stop containers and **stop Docker Engine** (saves battery/RAM).         |
| `make logs`    | Tail the logs of the running web container.                             |
| `make restart` | Restart the web container (use after code changes).                     |
| `make rebuild` | Rebuild containers (use after adding dependencies in `pyproject.toml`). |
| `make reboot`  | Full system cycle: Stops Docker Engine, then starts fresh.              |
| `make test`    | Run the automated test suite (`pytest`).                                |
| `make shell`   | Open a bash shell inside the running container.                         |

## 📂 Project Structure

```text
/
├── app/
│   ├── api/          # Route controllers
│   ├── core/         # App configuration & Database setup
│   ├── models/       # Internal Database Models (SQLModel)
│   ├── schemas/      # External Data Schemas (Pydantic)
│   ├── services/     # Business Logic & Ingestion Engine
│   └── main.py       # Application entry point
├── pyproject.toml    # Poetry dependencies
├── docker-compose.yml# Infrastructure definition
└── Makefile          # Command shortcuts
```

##🧪 DevelopmentThe project is configured for rapid iteration.

- **Hot Reloading:** The `web` container mounts the local directory, so changes to `app/` are reflected immediately.
- **Linting & Formatting:** We use `ruff` to enforce code quality.

```bash
# Check for linting errors
make lint

# Auto-fix linting errors (imports, unused variables)
make fix

# Auto-format code (spacing, quotes)
make format
```

---

_Built by [@bana0615](https://www.google.com/search?q=https://github.com/bana0615) as an experimental tool for [One Buffalo Labs](https://github.com/OneBuffaloLabs)._

**License**
[MIT](https://www.google.com/search?q=LICENSE)
