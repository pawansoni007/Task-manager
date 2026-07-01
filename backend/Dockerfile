FROM python:3.11-slim

WORKDIR /app

# Install system build dependencies required for compiling pydantic-core and
# other wheels that need native compilation.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust toolchain (non-interactive) so maturin/cargo can build
# pydantic-core if a wheel isn't available for the platform.
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Upgrade pip tools and install maturin so pip can build Rust-backed wheels.
RUN pip install --no-cache-dir --upgrade pip setuptools wheel maturin

# Install Python dependencies. Keep requirements in the backend directory.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files.
COPY . .

# Render (and most platforms) provide the port via $PORT.
ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
