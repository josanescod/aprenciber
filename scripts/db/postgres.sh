#!/bin/bash
docker run --name aprenciber-postgres \
  -e POSTGRES_DB=aprenciber \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:16