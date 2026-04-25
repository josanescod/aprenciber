#!/bin/bash

echo "[stopping] Eliminant contenidors de labs actius..."

# Eliminar tots els contenidors amb prefix del provisioner
docker ps -a --format '{{.Names}}' | grep '^aprenciber-lab-' | xargs -r docker rm -f

# Eliminar totes les xarxes amb prefix del provisioner
docker network ls --format '{{.Name}}' | grep '^aprenciber-lab-' | xargs -r docker network rm

echo "[Contenidors i xarxes eliminats. Les imatges es conserven]"