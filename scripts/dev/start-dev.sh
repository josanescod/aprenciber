#!/bin/bash
docker network create aprenciber-net 2>/dev/null || true
docker start aprenciber-postgres
docker start aprenciber-pgadmin
pnpm --prefix frontend dev &
#cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
cd backend && source .venv/bin/activate && fastapi dev