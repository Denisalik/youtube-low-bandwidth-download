from pathlib import Path

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.core.image import DockerImage


@pytest.fixture(scope="session")
def backend_server():
    with DockerImage(
        path=".",
        tag="yout-low-bandwidth-download-app-backend:test",
        dockerfile_path="Dockerfile",
        target="production",
        clean_up=False,
    ) as image:
        container = DockerContainer(image=str(image)).with_exposed_ports(8000)

        project_root = Path.cwd()
        data_volume = project_root / "data"
        container.with_volume_mapping(
            host=str(data_volume / "files"), container="/data/files", mode='rw'
        )
        container.with_volume_mapping(
            host=str(data_volume / "sql"), container="/data/sql", mode='rw'
        )
        container.waiting_for(LogMessageWaitStrategy("Uvicorn running on"))
        container.start()
        with container:
            host = container.get_container_host_ip()
            port = container.get_exposed_port(8000)
            yield f"http://{host}:{port}"
