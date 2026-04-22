#!/bin/bash
docker start aprenciber-postgres
pnpm --prefix frontend dev &
#cd backend && source .venv/bin/activate && uvicorn app.main:app --reload
cd backend && source .venv/bin/activate && fastapi dev