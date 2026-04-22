from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


SCENARIOS_DIR = Path(__file__).parent.parent.parent.parent / "scenarios"

REQUIRED_FIELDS = {"id", "name", "description", "difficulty", "tags", "containers"}


@dataclass
class ContainerConfig:
    image: str
    role: str
    ports: list[str] = field(default_factory=list)


@dataclass
class Scenario:
    id: str
    name: str
    description: str
    difficulty: str
    tags: list[str]
    containers: dict[str, ContainerConfig]
    hints: list[str] = field(default_factory=list)
    active: bool = True


def _parse_containers(raw: dict[str, Any]) -> dict[str, ContainerConfig]:  # verificar
    result = {}
    for name, config in raw.items():
        missing = {"image", "role"} - config.keys()
        if missing:
            raise ValueError(f"Container '{name}' missing required fields: {missing}")
        result[name] = ContainerConfig(
            image=config["image"],
            role=config["role"],
            ports=config.get("ports", []),
        )
    return result


def load_scenario(yaml_path: Path) -> Scenario:
    if not yaml_path.exists():
        raise FileNotFoundError(f"Scenario file not found: {yaml_path}")

    with yaml_path.open("r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML: {yaml_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML structure in {yaml_path}")

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Missing required fields {missing} in {yaml_path}")

    return Scenario(
        id=data["id"],
        name=data["name"],
        description=data["description"],
        difficulty=data["difficulty"],
        tags=data["tags"],
        containers=_parse_containers(data["containers"]),
        hints=data.get("hints", []),
        active=data.get("active", True),
    )


def load_all_scenarios() -> list[Scenario]:
    scenarios = []

    for yaml_path in sorted(SCENARIOS_DIR.rglob("*.yaml")):
        try:
            scenario = load_scenario(yaml_path)
            if scenario.active:
                scenarios.append(scenario)
        except (ValueError, FileNotFoundError, KeyError) as exc:
            print(f"Warning: skipping {yaml_path}: {exc}")

    return scenarios
