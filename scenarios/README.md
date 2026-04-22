# Scenarios - Aprenciber

Definició dels escenaris de ciberseguritat utilitzats per la plataforma.

### Objectiu

Permetre la creació dinàmica de laboratoris mitjançan fitxers YAML.

Cada escenari defineix:

- contenidors necessaris (màquina atacant + màquina/es vulnerables)
- configuració de l'entorn
- hints
- metadades (dificultat, tags, rols etc.)

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
description: "Accedeix a fitxers sensibles explotant un servidor web mal configurat"
difficulty: "easy"
tags: 
  - "file-intrusion"
  - "path-traversal"
  - "misconfiguration"
active: true
containers:
  attacker:
    image: "aprenciber-kali"
    role: "attacker"
  target:
    image: "aprenciber-vulnerable-web"
    role: "target"
    ports:
      - 80
      - 443
hints:
  - "Comprova les rutes i els fitxers exposats públicament"
  - "Intenta manipular els paràmetres que apunten als fitxers"
```

