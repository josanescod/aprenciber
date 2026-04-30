#!/bin/bash
docker network create aprenciber-net 2>/dev/null || true
bash scripts/db/postgres.sh
bash scripts/db/pgadmin.sh
bash scripts/labs/build-images.sh
sleep 60
cd backend && source .venv/bin/activate && alembic upgrade head
cd ../
pnpm --prefix frontend dev &
cd backend && source .venv/bin/activate && fastapi dev