#!/bin/bash
docker network create aprenciber-net 2>/dev/null || true
bash scripts/db/postgres.sh
bash scripts/db/pgadmin.sh
bash scripts/labs/build-images.sh
echo "Waiting Postgres..."
until pg_isready -h 127.0.0.1 -p 5432 -U postgres; do
  sleep 2
done
echo "Postgres ready!"
cd backend && source .venv/bin/activate && alembic upgrade head
cd ../
pnpm --prefix frontend dev &
cd backend && source .venv/bin/activate && fastapi dev