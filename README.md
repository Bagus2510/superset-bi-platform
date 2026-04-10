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

## GitLab Deployment

This repository includes deployment templates:

- `.env.example.deployment`
- `docker-compose-deployment.yml.example`
- `superset_config_deployment.py`

Recommended GitLab flow:

1. Store all sensitive values in GitLab CI/CD Variables (Masked + Protected), not in files.
2. In your deploy job, write variables into a temporary `.env` file on the runner.
3. Deploy using:

```bash
docker compose --env-file .env -f docker-compose-deployment.yml.example up -d --build
```

This repository also includes a ready pipeline file: `.gitlab-ci.yml`.
It uses runner tag `docker-shell` by default, so update the tag if your GitLab runner uses a different name.

Variables required in GitLab:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `SUPERSET_SECRET_KEY`
- `GUEST_TOKEN_JWT_SECRET`
- `SUPERSET_ADMIN_USERNAME`
- `SUPERSET_ADMIN_FIRSTNAME`
- `SUPERSET_ADMIN_LASTNAME`
- `SUPERSET_ADMIN_EMAIL`
- `SUPERSET_ADMIN_PASSWORD`
- `ALLOWED_CORS_ORIGINS`
- `SESSION_COOKIE_SECURE`
- `SESSION_COOKIE_NAME` (optional, default `superset_session`)
- `SESSION_COOKIE_SAMESITE` (optional, default `None`)
- `SESSION_COOKIE_DOMAIN` (optional)
- `PERMANENT_SESSION_LIFETIME` (optional, default `86400`)
- `ENABLE_PROXY_FIX` (optional, default `True`)
- `LOGOUT_REDIRECT_URL` (optional, default `/login/`)

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

## Public Access & Roles
This project is configured to allow public viewing of specific dashboards:
- **Public Role:** The `Public` role is configured to have `Gamma` permissions by default (as defined in `superset_config.py`).
- **Access Control:** To make a dashboard public, you must manually grant `can read on Chart` and `can read on Dashboard` permissions to the `Public` role in the Superset UI (Security -> List Roles -> Public).

## Repository Structure

- `docker-compose.yml` - Service definitions for Superset, PostgreSQL, and Redis
- `Dockerfile` - Custom image used to add Python dependencies
- `requirements.txt` - Additional Python dependencies
- `superset_config.py` - Local Superset configuration
- `.env.example` - Safe template for local secrets

## Notes

This repository is designed for local development and portfolio/demo use. If you want to use it in production, review the Superset security settings, database credentials, and network exposure before deploying.
