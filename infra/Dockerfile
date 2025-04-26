FROM python:3.12-slim

ENV USER="what-the-feed" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a new user and set up locales
RUN useradd -m $USER \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        ca-certificates \
        locales \
    && locale-gen en_US.UTF-8 \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Set working directory
WORKDIR /home/$USER

# Install UV
RUN pip install --no-cache-dir uv

# Copy the project files and set the correct ownership
COPY ./src ./
COPY pyproject.toml ./

COPY --chown=$USER:$USER . .

RUN uv pip compile pyproject.toml -o uv.lock && uv pip install -e .

EXPOSE 8003

ENTRYPOINT ["sh", "./src/boot.sh"]
#CMD ["python", "./src/main.py"]
