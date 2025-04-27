# What The Feed

A programmable RSS Feed Mixer application that allows users to blend multiple RSS feeds into custom streams using rules for filtering, tagging, and transforming content.

## System Requirements

- Python 3.13 or higher
- Docker (optional, for containerized deployment)
- UV

## Project Overview

What The Feed is a flexible RSS feed aggregation and transformation system built with FastAPI. It enables users to:

- Aggregate content from multiple RSS feeds
- Apply custom filtering rules to feed items
- Transform content using various rule types
- Generate custom mixed feeds in different formats

## Key Features

- **Feed Management**: Add, update, and remove RSS feed sources
- **Mixer Creation**: Create custom feed mixers that combine multiple sources
- **Rule Engine**: Define rules for filtering and transforming feed content
- **Custom Transformations**: Apply various transformations to feed items
- **Multiple Output Formats**: Generate mixed feeds in different formats (RSS, JSON)


## How to Run the Project

### Setup

```bash
# Install dependencies using UV
make setup
```

This command creates a virtual environment, installs dependencies, and sets up pre-commit hooks.

### Run the Application

```bash
# Run the application locally
make run
```

The application will start on http://0.0.0.0:8001 with auto-reload enabled.

### Docker Deployment

```bash
# Run using Docker
make run-docker

# Run using Docker Compose
make run-compose
```

### Development Commands

```bash
# Update dependencies
make update

# Generate UV lock file
make lock

# Run tests
make test

# Run tests with coverage report
make test-coverage

# Lint the code
make lint

# Format the code
make format

# Clean the project
make clean

# Run database migrations
make migrate
```

## Makefile Commands

- `setup`: Install dependencies using UV
- `run`: Run the application locally
- `run-docker`: Run the application using Docker
- `run-compose`: Run the application with Docker Compose
- `update`: Update dependencies using UV
- `lock`: Generate UV lock file
- `test`: Run tests
- `test-coverage`: Run tests with coverage report
- `lint`: Lint the code using flake8
- `format`: Format the code using black
- `clean`: Clean the project (remove cache files, build artifacts, etc.)
- `migrate`: Run database migrations