FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv --no-cache-dir

# Copy dependency manifest first for layer caching
COPY pyproject.toml .

# Install dependencies (no editable install — source copied next)
RUN uv pip install --system --no-cache --no-project .

# Copy source tree
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
