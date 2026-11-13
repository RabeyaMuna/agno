from __future__ import annotations

from agno.docker.app.base import ContainerContext, DockerApp


class FastApi(DockerApp):
    # -*- App Name
    name: str = "fastapi"

    # -*- Image Configuration
    image_name: str = "agnohq/fastapi"
    image_tag: str = "0.104"
    command: str | list[str] | None = "uvicorn main:app --reload"

    # -*- App Ports
    # Open a container port if open_port=True
    open_port: bool = True
    port_number: int = 8000

    # -*- Workspace Configuration
    # Path to the workspace directory inside the container
    workspace_dir_container_path: str = "/app"
    # Mount the workspace directory from host machine to the container
    mount_workspace: bool = False

    # -*- Uvicorn Configuration
    uvicorn_host: str = "0.0.0.0"
    # Defaults to the port_number
    uvicorn_port: int | None = None
    uvicorn_reload: bool | None = None
    uvicorn_log_level: str | None = None
    web_concurrency: int | None = None

    def get_container_env(self, container_context: ContainerContext) -> dict[str, str]:
        container_env: dict[str, str] = super().get_container_env(container_context=container_context)

        if self.uvicorn_host is not None:
            container_env["UVICORN_HOST"] = self.uvicorn_host

        uvicorn_port = self.uvicorn_port
        if uvicorn_port is None and self.port_number is not None:
            uvicorn_port = self.port_number
        if uvicorn_port is not None:
            container_env["UVICORN_PORT"] = str(uvicorn_port)

        if self.uvicorn_reload is not None:
            container_env["UVICORN_RELOAD"] = str(self.uvicorn_reload)

        if self.uvicorn_log_level is not None:
            container_env["UVICORN_LOG_LEVEL"] = self.uvicorn_log_level

        if self.web_concurrency is not None:
            container_env["WEB_CONCURRENCY"] = str(self.web_concurrency)

        return container_env
