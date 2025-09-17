FROM python:3.11.7-slim-bookworm

ENV APP_HOME="/app"
WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for PySpark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

COPY scripts/uv-installer.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

# Spark environment variables
ENV SPARK_HOME="/app/.venv/lib/python3.11/site-packages/pyspark"
ENV PYTHONPATH="$SPARK_HOME/python:$PYTHONPATH"
ENV PYSPARK_PYTHON="/app/.venv/bin/python"
ENV PYSPARK_DRIVER_PYTHON="/app/.venv/bin/python"

COPY scripts/entrypoint.sh scripts/entrypoint.sh
RUN chmod +x scripts/entrypoint.sh

CMD ["bash", "scripts/entrypoint.sh"]