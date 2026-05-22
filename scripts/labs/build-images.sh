#!/bin/bash
set -e

SCENARIOS_DIR="scenarios"

echo "Buscant escenaris escenaris a $SCENARIOS_DIR..."

for yaml in $(find "$SCENARIOS_DIR" -name "scenario.yaml" | sort); do
    scenario_dir=$(dirname "$yaml")
    echo "[build] Processant: $yaml"

    for role in attacker target; do
        context="$scenario_dir/$role"
        if [ -d "$context" ]; then
            image_name=$(grep "image:" "$yaml" | grep "$role" -A0 | head -1 | awk '{print $2}' | tr -d '"')
            if [ -n "$image_name" ]; then
                echo "Building $image_name from $context"
                docker build -t "$image_name" "$context"
            fi
        fi
    done
done

echo "OK"