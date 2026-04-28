#!/bin/bash
docker run --name aprenciber-pgadmin \
    --network aprenciber-net \
    -e PGADMIN_DEFAULT_EMAIL=aprenciber@local.dev \
    -e PGADMIN_DEFAULT_PASSWORD=pgadmin \
    -p 127.0.0.1:5433:80 \
    -d dpage/pgadmin4