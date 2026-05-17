#!/bin/bash

docker build -t aprenciber-ftp-attacker:demo \
  scenarios/beginner/ftp-credentials/attacker
docker build -t aprenciber-ftp-target:demo \
  scenarios/beginner/ftp-credentials/target
docker build -t aprenciber-lfi-attacker:demo \
  scenarios/beginner/local-file-inclusion/attacker
docker build -t aprenciber-lfi-target:demo \
  scenarios/beginner/local-file-inclusion/target