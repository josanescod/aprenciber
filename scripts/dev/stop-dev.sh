#! /bin/bash
pkill -f "pnpm --prefix frontend dev"
pkill -f "fastapi dev"

docker stop aprenciber-postgres
docker stop aprenciber-pgadmin
