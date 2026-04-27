from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from sqlalchemy.orm import Session

from app.models.scenario import Scenario as ScenarioModel

SCENARIOS_DIR = (
    Path(__file__).resolve().parent.parent.parent.parent.parent / "scenarios"
)

REQUIRED_FIELDS = {"id", "name", "description", "difficulty", "tags", "containers"}


@dataclass
class NetworkConfig:
    driver: str = "bridge"


@dataclass
class ContainerConfig:
    image: str
    role: str
    networks: list[str] = field(default_factory=list)
    ports: list[int] = field(default_factory=list)


@dataclass
class FlagConfig:
    path: str


@dataclass
class Scenario:
    id: str
    name: str
    description: str
    difficulty: str
    tags: list[str]
    containers: dict[str, ContainerConfig]
    networks: dict[str, NetworkConfig] = field(default_factory=dict)
    hints: list[str] = field(default_factory=list)
    flag: FlagConfig | None = None
    active: bool = True
    yaml_path: str = ""


def _parse_networks(raw: dict[str, Any]) -> dict[str, NetworkConfig]:
    result = {}
    for name, config in raw.items():
        result[name] = NetworkConfig(
            driver=config.get("driver", "bridge"),
        )
    return result


def _parse_containers(raw: dict[str, Any]) -> dict[str, ContainerConfig]:
    result = {}
    for name, config in raw.items():
        missing = {"image", "role"} - config.keys()
        if missing:
            raise ValueError(f"Container '{name}' missing required fields: {missing}")
        result[name] = ContainerConfig(
            image=config["image"],
            role=config["role"],
            networks=config.get("networks", []),
            ports=config.get("ports", []),
        )
    return result


def _parse_flag(raw: dict[str, Any] | None) -> FlagConfig | None:
    if raw is None:
        return None

    if "path" not in raw:
        raise ValueError("Flag config missing required field: path")

    return FlagConfig(path=raw["path"])


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
        networks=_parse_networks(data.get("networks", {})),
        hints=data.get("hints", []),
        flag=_parse_flag(data.get("flag")),
        active=data.get("active", True),
        yaml_path=str(yaml_path),
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


def sync_scenarios_to_db(db: Session) -> int:
    count = 0
    for yaml_path in sorted(SCENARIOS_DIR.rglob("*.yaml")):
        try:
            scenario = load_scenario(yaml_path)
            tags_str = ",".join(scenario.tags) if scenario.tags else None
            existing = db.query(ScenarioModel).filter_by(slug=scenario.id).first()
            if existing:
                existing.title = scenario.name
                existing.description = scenario.description
                existing.difficulty = scenario.difficulty
                existing.tags = tags_str
                existing.is_active = scenario.active
                existing.yaml_path = str(yaml_path)
            else:
                db.add(
                    ScenarioModel(
                        slug=scenario.id,
                        title=scenario.name,
                        description=scenario.description,
                        difficulty=scenario.difficulty,
                        tags=tags_str,
                        yaml_path=str(yaml_path),
                        is_active=scenario.active,
                    )
                )
            count += 1
        except (ValueError, FileNotFoundError, KeyError) as exc:
            print(f"Warning: skipping {yaml_path}: {exc}")
    db.commit()
    return count
