FROM apache/superset:latest

USER root

# Copy file requirements ke folder temporary
COPY requirements.txt /tmp/

# Install library tambahan
RUN uv pip install -p /app/.venv/bin/python -r /tmp/requirements.txt

USER superset