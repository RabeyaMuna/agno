from __future__ import annotations

from typing import Any

from agno.aws.resource.base import AwsResource
from agno.utils.log import logger


class EcsVolume(AwsResource):
    """
    Reference:
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html
    """

    resource_type: str | None = "EcsVolume"
    service_name: str = "ecs"

    name: str
    host: dict[str, Any] | None = None
    docker_volume_configuration: dict[str, Any] | None = None
    efs_volume_configuration: dict[str, Any] | None = None
    fsx_windows_file_server_volume_configuration: dict[str, Any] | None = None

    def get_volume_definition(self) -> dict[str, Any]:
        volume_definition: dict[str, Any] = {}

        if self.name is not None:
            volume_definition["name"] = self.name
        if self.host is not None:
            volume_definition["host"] = self.host
        if self.docker_volume_configuration is not None:
            volume_definition["dockerVolumeConfiguration"] = self.docker_volume_configuration
        if self.efs_volume_configuration is not None:
            volume_definition["efsVolumeConfiguration"] = self.efs_volume_configuration
        if self.fsx_windows_file_server_volume_configuration is not None:
            volume_definition["fsxWindowsFileServerVolumeConfiguration"] = (
                self.fsx_windows_file_server_volume_configuration
            )

        return volume_definition

    def volume_definition_up_to_date(self, volume_definition: dict[str, Any]) -> bool:
        if self.name is not None and volume_definition.get("name") != self.name:
            logger.debug("{} != {}".format(self.name, volume_definition.get("name")))
            return False
        if self.host is not None and volume_definition.get("host") != self.host:
            logger.debug("{} != {}".format(self.host, volume_definition.get("host")))
            return False
        if self.docker_volume_configuration is not None:
            if volume_definition.get("dockerVolumeConfiguration") != self.docker_volume_configuration:
                logger.debug(
                    "{} != {}".format(
                        self.docker_volume_configuration,
                        volume_definition.get("dockerVolumeConfiguration"),
                    )
                )
                return False
        if self.efs_volume_configuration is not None:
            if volume_definition.get("efsVolumeConfiguration") != self.efs_volume_configuration:
                logger.debug(
                    "{} != {}".format(
                        self.efs_volume_configuration,
                        volume_definition.get("efsVolumeConfiguration"),
                    )
                )
                return False
        if self.fsx_windows_file_server_volume_configuration is not None and (
            volume_definition.get("fsxWindowsFileServerVolumeConfiguration")
            != self.fsx_windows_file_server_volume_configuration
        ):
            logger.debug(
                "{} != {}".format(
                    self.fsx_windows_file_server_volume_configuration,
                    volume_definition.get("fsxWindowsFileServerVolumeConfiguration"),
                )
            )
            return False

        return True
