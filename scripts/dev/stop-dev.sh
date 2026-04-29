#! /bin/bash
pkill -f "pnpm --prefix frontend dev"
pkill -f "fastapi dev"
docker stop aprenciber-postgres && docker rm -f aprenciber-postgres
docker stop aprenciber-pgadmin && docker rm -f aprenciber-pgadmin
docker network rm aprenciber-net
