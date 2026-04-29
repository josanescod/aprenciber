#!/bin/bash
docker network create aprenciber-net 2>/dev/null || true
bash scripts/db/postgres.sh
bash scripts/db/pgadmin.sh
# docker start aprenciber-postgres
# docker start aprenciber-pgadmin
sleep 20
cd backend && source .venv/bin/activate && alembic upgrade head
cd ../
pnpm --prefix frontend dev &
#cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
cd backend && source .venv/bin/activate && fastapi dev