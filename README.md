# Job Radar 📡

> **A scalable, non-blocking job aggregation engine.**

![CI Status](https://github.com/OneBuffaloLabs/job-radar/actions/workflows/ci.yml/badge.svg)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.112-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📖 The "Why"

Building a job board sounds simple until you have to scale it. **Job Radar** isn't just a scraper; it's an architectural reference for how to build high-concurrency Python backends.

I built this to solve the **"blocking problem."** Most simple scrapers halt the entire API while fetching data. Job Radar uses a distributed producer-consumer architecture:

1.  **FastAPI** handles the request instantly.
2.  **Celery & Redis** handle the heavy lifting (scraping/normalizing) in the background.
3.  **Next.js** renders the results in a snappy, client-side dashboard.

**Core Tech:** Python 3.12, FastAPI, PostgreSQL, Celery, Redis, Next.js 14.

## 🚀 Quick Start

This project uses a heavily customized `Makefile` to abstract away the complexity of Docker networking and volume management.

### 1. Backend (The Engine)

```bash
# Clone & Enter
git clone [https://github.com/OneBuffaloLabs/job-radar.git](https://github.com/OneBuffaloLabs/job-radar.git)
cd job-radar

# Boot the System
# (Starts Docker, builds containers, runs migrations, starts Redis/Celery)
make up

# Verify it's alive
# API should be at http://localhost:8000
make logs

```

### 2. Frontend (The Dashboard)

The UI is a separate Next.js app in the `ui/` folder.

```bash
cd ui
npm install
npm run dev
# Open http://localhost:3000

```

## ⚡ How it works (Ingestion)

Unlike basic CRUD apps, this system is **event-driven**. Jobs don't appear until you trigger an ingestion event.

1. **Trigger:** You hit the "Ingest" button (or API endpoint).
2. **Queue:** The API returns a `202 Accepted` immediately. It doesn't wait.
3. **Process:** A Celery worker wakes up, fetches data from sources (like Remotive), normalizes the JSON, and upserts it into Postgres.
4. **View:** The Frontend polls the read-optimized API endpoints to display new jobs.

**Manual Trigger:**

```bash
curl -X POST http://localhost:8000/api/jobs/ingest

```

## ⚙️ Developer Command Reference

I wrote a `Makefile` so I wouldn't have to remember Docker Compose flags.

| Command            | What it does                                                       |
| ------------------ | ------------------------------------------------------------------ |
| `make up`          | Starts the entire stack (API, DB, Redis, Worker).                  |
| `make down`        | Stops containers and **shuts down Docker Engine** to save battery. |
| `make logs`        | Tails the API logs.                                                |
| `make worker-logs` | Tails the Celery worker (Best for debugging scraping).             |
| `make shell`       | Drops you into a bash shell inside the running container.          |

## 📂 Project Structure

- **`app/core/celery_app.py`**: The background worker configuration.
- **`app/services/ingestion.py`**: The business logic for fetching and cleaning data.
- **`ui/app`**: Next.js App Router structure.
- **`docker-compose.yml`**: Orchestrates the 4 services (Web, Db, Redis, Worker).

---

<<<<<<< HEAD
_Built by [@bana0615](https://www.google.com/search?q=https://github.com/bana0615) as an experimental tool for [One Buffalo Labs](https://github.com/OneBuffaloLabs)._

**License**
[MIT](https://www.google.com/search?q=LICENSE) - Copyright (c) 2025 One Buffalo Labs
=======
_Built by **Andrew Elbaneh** @ [One Buffalo Labs](https://onebuffalolabs.com)._
**License** [MIT](https://www.google.com/search?q=LICENSE)
>>>>>>> f1cc89d (docs: refactor README for portfolio context)
