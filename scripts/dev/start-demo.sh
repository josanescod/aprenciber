#!/bin/bash

set -e # bash no ignora errors i s'atura

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$PROJECT_ROOT"

docker network create --driver bridge \
  --subnet=172.20.0.0/24 \
  --gateway=172.20.0.1 \
  aprenciber-ftp-credentials-net || true # si existeix la xarxa l'script continua

docker build -t aprenciber-ftp-attacker:demo \
  scenarios/beginner/ftp-credentials/attacker
docker build -t aprenciber-ftp-target:demo \
  scenarios/beginner/ftp-credentials/target

docker run -d \
  --name aprenciber-vuln-ftp \
  --network aprenciber-ftp-credentials-net \
  aprenciber-ftp-target:demo

docker run -it \
  --name aprenciber-attacker \
  --network aprenciber-ftp-credentials-net \
  aprenciber-ftp-attacker:demo

echo "[contenidors i xarxa preparats]"