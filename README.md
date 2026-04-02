# Apache Superset Docker Setup

A containerized Apache Superset project with PostgreSQL and Redis, ready for local development and easy deployment to a public GitHub repository.

## What This Project Includes

- Apache Superset running in Docker
- PostgreSQL as the metadata database
- Redis for caching
- A bootstrap container that runs database migrations, creates permissions, and creates the initial admin user
- Local configuration support through `superset_config.py`

## Project Stack

- Apache Superset
- PostgreSQL 14
- Redis 7
- Docker and Docker Compose

## Prerequisites

Before running this project, make sure you have:

- Docker installed
- Docker Compose installed
- A terminal or shell with access to the project folder

## Setup

1. Copy the environment template:

   ```bash
   copy .env.example .env
   ```

   On macOS or Linux:

   ```bash
   cp .env.example .env
   ```

2. Open `.env` and replace every placeholder value with your own secure credentials.

3. Build and start the stack:

   ```bash
   docker compose up -d --build
   ```

4. Open Superset in your browser:

   ```text
   http://localhost:8088
   ```

## Initial Bootstrap

The `superset-init` service automatically runs the following steps during startup:

- `superset db upgrade`
- `superset fab create-permissions`
- `superset fab security-converge`
- `superset fab create-admin`
- `superset init`

This means the project should be ready after the first `docker compose up -d --build`.

## Environment Variables

Use `.env` for local secrets and credentials. The repository includes `.env.example` as a safe template.

Required variables:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `SUPERSET_SECRET_KEY`
- `SUPERSET_ADMIN_USERNAME`
- `SUPERSET_ADMIN_FIRSTNAME`
- `SUPERSET_ADMIN_LASTNAME`
- `SUPERSET_ADMIN_EMAIL`
- `SUPERSET_ADMIN_PASSWORD`

## Default Behavior

- Superset is exposed on port `8088`
- PostgreSQL data is stored in a Docker volume named `db_data`
- Redis data is stored in a Docker volume named `redis_data`
- Local Superset settings are loaded from `superset_config.py`

## Security Notes

If you plan to publish this repository publicly:

- Never commit your `.env` file
- Keep `SUPERSET_SECRET_KEY` private and rotate it if it was ever exposed
- Use a strong `POSTGRES_PASSWORD`
- Use a strong `SUPERSET_ADMIN_PASSWORD`
- Treat any data stored in your local Docker volumes as local-only; it is not part of the Git repository

## Useful Commands

Stop the stack:

```bash
docker compose down
```

Stop the stack and remove volumes:

```bash
docker compose down -v
```

Rebuild after changing the Dockerfile or requirements:

```bash
docker compose up -d --build
```

View logs:

```bash
docker logs -f superset_app
```

Run the Superset init commands manually if needed:

```bash
docker exec -it superset_app superset db upgrade
docker exec -it superset_app superset fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password admin
docker exec -it superset_app superset init
```

## Troubleshooting

### 500 Internal Server Error on login or welcome page

If the UI shows `500 Internal Server Error` or permission-related errors, try:

```bash
docker exec -it superset_app superset fab create-permissions
docker exec -it superset_app superset fab security-converge
```

Then refresh the browser or log in again.

### Missing database driver

If Superset cannot connect to PostgreSQL, rebuild the image:

```bash
docker compose up -d --build
```

The Dockerfile installs `psycopg2-binary` into the Superset runtime environment.

### Fresh reset

If you want a completely clean local environment:

```bash
docker compose down -v
docker compose up -d --build
```

## Repository Structure

- `docker-compose.yml` - Service definitions for Superset, PostgreSQL, and Redis
- `Dockerfile` - Custom image used to add Python dependencies
- `requirements.txt` - Additional Python dependencies
- `superset_config.py` - Local Superset configuration
- `.env.example` - Safe template for local secrets

## Notes

This repository is designed for local development and portfolio/demo use. If you want to use it in production, review the Superset security settings, database credentials, and network exposure before deploying.
