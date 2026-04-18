# Scenarios - Aprenciber

Definició dels escenaris de ciberseguritat utilitzats per la plataforma.

### Objectiu

Permetre la creació dinàmica de laboratoris mitjançan fitxers YAML.

Cada escenari defineix:

- contenidors necessaris (màquina atacant + màquina/es vulnerables)
- configuració de l'entorn
- hints
- metadades (dificultat, tags, etc.)

### Estructura

```txt
src/
└── beginner/
    └── file_intrusion_vulnerability/
        ├── scenario.yaml
        ├── instructions.md
        ├── init/
        └── setup.sh
```

## Exemple d'escenari

```yaml
id: "file_intrusions_01"
name: "Exposed File Intrusion"
description: "Access sensitive files by exploiting a misconfigured server"
difficulty: "easy"
tags: ["file-intrusion", "path-traversal", "misconfiguration"]

containers:
  attacker:
    image: "kali-lite"
  victim:
    image: "vulnerable-web"

hints:
  - "Check publicly exposed paths and files."
  - "Try manipulating parameters that point to files."
```

