from __future__ import annotations

from agno.docker.app.base import ContainerContext, DockerApp  # noqa: F401


class CeleryWorker(DockerApp):
    # -*- App Name
    name: str = "celery-worker"

    # -*- Image Configuration
    image_name: str = "agnohq/celery-worker"
    image_tag: str = "latest"
    command: str | list[str] | None = "celery -A tasks.celery worker --loglevel=info"

    # -*- Workspace Configuration
    # Path to the workspace directory inside the container
    workspace_dir_container_path: str = "/app"
    # Mount the workspace directory from host machine to the container
    mount_workspace: bool = False
