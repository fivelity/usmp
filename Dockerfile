FROM python:3.11-slim-bookworm AS base

WORKDIR /app

# Install Poetry - using the recommended installation method
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

# Copy source code
COPY . .

FROM node:18-alpine AS frontend-builder

WORKDIR /app

COPY client/package*.json ./
RUN npm install

COPY client/. .
RUN npm run build

FROM base AS final

COPY --from=frontend-builder /app/build /app/client/build

CMD ["python", "-m", "uvicorn", "server.app.main:app", "--host", "0.0.0.0", "--port", "8100"]
