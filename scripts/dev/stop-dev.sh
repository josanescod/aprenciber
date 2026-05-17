#! /bin/bash
set -e
pkill -f "pnpm --prefix frontend dev"
pkill -f "fastapi dev"
docker stop aprenciber-postgres && docker rm -f aprenciber-postgres
docker stop aprenciber-pgadmin && docker rm -f aprenciber-pgadmin
docker rmi aprenciber-ftp-target:demo aprenciber-ftp-attacker:demo dpage/pgadmin4:latest
docker network rm aprenciber-net
docker volume rm aprenciber_pgdata
PID=$(ss -ltnp 2>/dev/null | grep ":5173" | awk -F',' '{print $2}' | awk -F'=' '{print $2}')

if [ -n "$PID" ]; then
    echo "Kill the process on port 5173 (PID: $PID)"
    kill -9 "$PID"
else
    echo "No processes on port 5173"
fi