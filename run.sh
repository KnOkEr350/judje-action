#!/bin/bash
set -e

cat > /tmp/judge-compose.yml << EOF
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 2s
      timeout: 5s
      retries: 15

  student-app:
    image: ${IMAGE_SOLUTION}
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "curl -f -m 3 http://localhost:8080/ping || exit 1"]
      interval: 3s
      timeout: 10s
      retries: 30
      start_period: 15s

  judge:
    image: ${IMAGE_JUDGE}
    environment:
      BASE_URL: http://student-app:8080
    depends_on:
      student-app:
        condition: service_healthy
EOF

docker compose -f /tmp/judge-compose.yml up \
  --abort-on-container-exit \
  --exit-code-from judge