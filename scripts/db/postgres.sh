#!/bin/bash
docker run --name aprenciber-postgres \
  --network aprenciber-net \
  --restart=unless-stopped \
  -e POSTGRES_DB=aprenciber \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 127.0.0.1:5432:5432 \
  -v aprenciber_pgdata:/var/lib/postgresql/data \
  -d postgres:16-alpine \
  
  