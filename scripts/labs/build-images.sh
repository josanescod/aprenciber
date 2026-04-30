#!/bin/bash

docker build -t aprenciber-ftp-attacker:demo \
  scenarios/beginner/ftp-credentials/attacker
docker build -t aprenciber-ftp-target:demo \
  scenarios/beginner/ftp-credentials/target