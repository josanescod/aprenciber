#!/bin/bash
docker run --name aprenciber-postgres \
  --network aprenciber-net \
  -e POSTGRES_DB=aprenciber \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 127.0.0.1:5432:5432 \
  -d postgres:16