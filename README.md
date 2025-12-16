# Job Radar 📡

> **High-performance job aggregation engine built with FastAPI, SQLAlchemy, and AsyncIO.**

![CI Status](https://github.com/OneBuffaloLabs/job-radar/actions/workflows/ci.yml/badge.svg)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/celery-%2337814A.svg?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)

## 📖 About

Job Radar is an asynchronous microservice designed to aggregate, normalize, and serve job posting data from multiple sources. It leverages modern Python type systems for validation and uses a distributed producer-consumer architecture for data ingestion. Heavy lifting (scraping) is offloaded to background Celery workers backed by Redis, ensuring the API remains non-blocking and responsive.

This project serves as an architectural reference for building scalable Python backends using **FastAPI** and **SQLModel**, paired with a modern **Next.js** frontend.

## 🛠 Tech Stack

- **Runtime:** Python 3.12+
- **Framework:** FastAPI (Async/Await)
- **Frontend:** Next.js (React / TypeScript)
- **Database:** PostgreSQL 15 (via Docker)
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Task Queue:** Celery
- **Message Broker:** Redis
- **HTTP Client:** HTTPX (Async)
- **Migrations:** Alembic
- **Dependency Management:** Poetry
- **Linting/Formatting:** Ruff

## 🚀 Getting Started

This project uses a containerized development environment for the backend and a local Node environment for the frontend.

### Prerequisites

- Docker & Docker Compose
- Make (Standard on Linux/Mac, install via Chocolatey/Winget on Windows)
- Node.js 18+ (For the frontend)

### Quick Start (Backend)

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

### 🖥️ Frontend Setup (UI)

The UI is a Next.js application located in the `ui/` directory.

1.  **Install Dependencies**

    ```bash
    cd ui
    npm install
    ```

2.  **Run Development Server**

    ```bash
    npm run dev
    ```

3.  **View Dashboard**
    Open [http://localhost:3000](http://localhost:3000) to view the job listings.

## ⚡ Data Ingestion

The system uses an event-driven architecture. Jobs are not fetched automatically on page load; they must be ingested into the database first.

### Manual Trigger

To force the system to fetch the latest jobs immediately, send a POST request to the ingestion endpoint:

```bash
curl -X POST http://localhost:8000/api/jobs/ingest
```

**What happens next?**

1. The API responds immediately with a Task ID.
2. A **Celery Worker** picks up the task in the background.
3. The worker fetches data from remote sources (e.g., Remotive).
4. Data is normalized and saved to PostgreSQL.
5. Refresh the **UI** to see the new listings.

###Automated ScheduleA **Celery Beat** scheduler is running in the background to automatically trigger ingestion at defined intervals (configured in `app/core/celery_app.py`).

##⚙️ Developer Command ReferenceWe use `make` to abstract complex Docker Compose commands.

| Command            | Description                                                             |
| ------------------ | ----------------------------------------------------------------------- |
| `make up`          | Start Docker Engine and boot up containers.                             |
| `make down`        | Stop containers and **stop Docker Engine** (saves battery/RAM).         |
| `make logs`        | Tail the logs of the API container (HTTP traffic).                      |
| `make worker-logs` | Tail the logs of the Celery Worker (Ingestion tasks).                   |
| `make beat-logs`   | Tail the logs of the Scheduler (Cron triggers).                         |
| `make logs-all`    | Tail logs from ALL services at once.                                    |
| `make restart`     | Restart the web container (use after code changes).                     |
| `make rebuild`     | Rebuild containers (use after adding dependencies in `pyproject.toml`). |
| `make reboot`      | Full system cycle: Stops Docker Engine, then starts fresh.              |
| `make test`        | Run the automated test suite (`pytest`).                                |
| `make shell`       | Open a bash shell inside the running container.                         |

##📂 Project Structure

```text
/
├── app/ # Python Backend (FastAPI)
│ ├── api/ # Route controllers
│ ├── core/ # App configuration & Database setup
│ ├── models/ # Internal Database Models (SQLModel)
│ ├── schemas/ # External Data Schemas (Pydantic)
│ ├── services/ # Business Logic & Ingestion Engine
│ ├── tasks.py # Celery Task Definitions (Worker entry point)
│ └── main.py # Application entry point
├── ui/ # Frontend Dashboard (Next.js)
│ ├── app/ # App Router Pages
│ └── public/ # Static assets
├── pyproject.toml # Poetry dependencies
├── docker-compose.yml # Infrastructure definition
└── Makefile # Command shortcuts
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

```

```
