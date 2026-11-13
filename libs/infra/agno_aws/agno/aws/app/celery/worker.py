from __future__ import annotations

from agno.aws.app.base import AwsApp, AwsBuildContext, ContainerContext  # noqa: F401


class CeleryWorker(AwsApp):
    # -*- App Name
    name: str = "celery-worker"

    # -*- Image Configuration
    image_name: str = "agnohq/celery-worker"
    image_tag: str = "latest"
    command: str | list[str] | None = "celery -A tasks.celery worker --loglevel=info"

    # -*- Workspace Configuration
    # Path to the workspace directory inside the container
    workspace_dir_container_path: str = "/app"
