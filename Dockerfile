# Use an official Python runtime as the parent image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.5.1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION"

# Poetry configuration
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install project dependencies
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root --no-dev

# Copy the content of the local src directory to the working directory
COPY . /app/

# Specify the command to run on container start
ENTRYPOINT ["/bin/bash", "entry.sh"]
