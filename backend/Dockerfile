# Build stage - compile psycopg2 and other C extensions
FROM python:3.11-alpine AS builder

RUN apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.11-alpine

RUN apk add --no-cache libpq

COPY --from=builder /install /usr/local

WORKDIR /app
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
