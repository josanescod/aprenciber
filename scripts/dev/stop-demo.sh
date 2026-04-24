#!/bin/bash

docker rm -f aprenciber-attacker aprenciber-vuln-ftp 2>/dev/null || true
docker rmi aprenciber-ftp-attacker:demo 2>/dev/null || true
docker rmi aprenciber-ftp-target:demo 2>/dev/null || true
docker network rm aprenciber-ftp-creds-net 2>/dev/null || true


echo "[contenidors, imatges i xarxa esborrats]"