from pathlib import Path
from uuid import uuid4

from docker import DockerClient
from docker.errors import ImageNotFound

from app.infrastructure.scenarios.scenario_loader import Scenario


class LabProvisioner:
    def __init__(self, docker_client: DockerClient):
        self.docker_client = docker_client

    def start_lab(self, scenario: Scenario) -> dict:
        lab_short_id = str(uuid4())[:12]

        created_containers = {}
        created_networks = {}

        try:
            created_networks = self._create_networks(lab_short_id, scenario)
            created_containers = self._create_containers(
                lab_short_id, scenario, created_networks
            )

            return {
                "lab_short_id": lab_short_id,
                "status": "running",
                "containers_info": created_containers,
                "networks_info": created_networks,
            }

        except Exception as exc:
            self.cleanup(
                containers_info=created_containers,
                networks_info=created_networks,
            )
            raise RuntimeError(f"Error creating lab: {exc}") from exc

    def _create_networks(self, lab_short_id: str, scenario: Scenario) -> dict:
        networks_info = {}

        for logical_name, net_config in scenario.networks.items():
            docker_network_name = f"aprenciber-lab-{lab_short_id}-{logical_name}"

            network = self.docker_client.networks.create(
                name=docker_network_name,
                driver=net_config.driver,
            )

            networks_info[logical_name] = {
                "name": docker_network_name,
                "id": network.id,
                "driver": net_config.driver,
            }

        return networks_info

    def _ensure_image_exists(
        self,
        image: str,
        scenario_path: Path,
        build_context: str | None,
        dockerfile: str,
    ) -> None:
        try:
            self.docker_client.images.get(image)
            print(f"[docker] Image already exists: {image}")
            return
        except ImageNotFound:
            if not build_context:
                raise RuntimeError(
                    f"Image '{image}' does not exist and no build_context was provided"
                )

            context_path = scenario_path / build_context
            if not context_path.exists():
                raise RuntimeError(f"Build context not found: {context_path}")

            print(f"[docker] Building image: {image}")
            self.docker_client.images.build(
                path=str(context_path),
                dockerfile=dockerfile,
                tag=image,
                rm=True,
                forcerm=True,
            )

    def _create_containers(
        self,
        lab_short_id: str,
        scenario: Scenario,
        networks_info: dict,
    ) -> dict:
        containers_info = {}
        scenario_path = (
            Path(scenario.yaml_path).parent
            if hasattr(scenario, "yaml_path")
            else Path()
        )

        for logical_name, container_config in scenario.containers.items():
            image = container_config.image
            role = container_config.role
            container_networks = container_config.networks

            if not container_networks:
                raise RuntimeError(
                    f"Container '{logical_name}' has no networks configured"
                )

            self._ensure_image_exists(
                image=image,
                scenario_path=scenario_path,
                build_context=None,
                dockerfile="Dockerfile",
            )

            container_name = f"aprenciber-lab-{lab_short_id}-{logical_name}"
            first_network_name = networks_info[container_networks[0]]["name"]

            container = self.docker_client.containers.run(
                image=image,
                name=container_name,
                network=first_network_name,
                detach=True,
                tty=role == "attacker",
                stdin_open=role == "attacker",
            )

            for extra_network in container_networks[1:]:
                self.docker_client.networks.get(
                    networks_info[extra_network]["name"]
                ).connect(container)

            containers_info[logical_name] = {
                "name": container_name,
                "id": container.id,
                "image": image,
                "role": role,
                "networks": container_networks,
            }

        return containers_info

    def cleanup(self, containers_info: dict, networks_info: dict) -> None:

        errors: list[str] = []

        for container_info in containers_info.values():
            container_name = container_info.get("name")

            if not container_name:
                continue

            try:
                container = self.docker_client.containers.get(container_name)
                container.remove(force=True)
            except Exception as exc:
                if (
                    "404" not in str(exc).lower()
                    and "not found" not in str(exc).lower()
                ):
                    errors.append(f"Container {container_name}: {exc}")

        for network_info in networks_info.values():
            network_name = network_info.get("name")

            if not network_name:
                continue

            try:
                network = self.docker_client.networks.get(network_name)
                network.remove()
            except Exception as exc:
                if (
                    "404" not in str(exc).lower()
                    and "not found" not in str(exc).lower()
                ):
                    errors.append(f"Network {network_name}: {exc}")

        if errors:
            raise RuntimeError("Errors during lab cleanup: " + " | ".join(errors))
