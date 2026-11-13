from __future__ import annotations

from typing import Any

from agno.aws.api_client import AwsApiClient
from agno.aws.resource.base import AwsResource
from agno.aws.resource.ec2.subnet import Subnet
from agno.cli.console import print_info
from agno.utils.log import logger


class TargetGroup(AwsResource):
    """
    Reference:
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/create_target_group.html
    """

    resource_type: str | None = "TargetGroup"
    service_name: str = "elbv2"

    # Name of the Target Group
    name: str
    protocol: str | None = None
    protocol_version: str | None = None
    port: int | None = None
    vpc_id: str | None = None
    subnets: list[str | Subnet] | None = None
    health_check_protocol: str | None = None
    health_check_port: str | None = None
    health_check_enabled: bool | None = None
    health_check_path: str | None = None
    health_check_interval_seconds: int | None = None
    health_check_timeout_seconds: int | None = None
    healthy_threshold_count: int | None = None
    unhealthy_threshold_count: int | None = None
    matcher: dict[str, str] | None = None
    target_type: str | None = None
    tags: list[dict[str, str]] | None = None
    ip_address_type: str | None = None

    def _create(self, aws_client: AwsApiClient) -> bool:
        """Creates the Target Group

        Args:
            aws_client: The AwsApiClient for the current Target Group
        """
        print_info(f"Creating {self.get_resource_type()}: {self.get_resource_name()}")

        # create a dict of args which are not null, otherwise aws type validation fails
        not_null_args: dict[str, Any] = {}

        # Get vpc_id
        vpc_id = self.vpc_id
        if vpc_id is None and self.subnets is not None:
            from agno.aws.resource.ec2.subnet import get_vpc_id_from_subnet_ids

            subnet_ids = []
            for subnet in self.subnets:
                if isinstance(subnet, Subnet):
                    subnet_ids.append(subnet.name)
                elif isinstance(subnet, str):
                    subnet_ids.append(subnet)
            vpc_id = get_vpc_id_from_subnet_ids(subnet_ids, aws_client)
        if vpc_id is not None:
            not_null_args["VpcId"] = vpc_id

        if self.protocol is not None:
            not_null_args["Protocol"] = self.protocol
        if self.protocol_version is not None:
            not_null_args["ProtocolVersion"] = self.protocol_version
        if self.port is not None:
            not_null_args["Port"] = self.port
        if self.health_check_protocol is not None:
            not_null_args["HealthCheckProtocol"] = self.health_check_protocol
        if self.health_check_port is not None:
            not_null_args["HealthCheckPort"] = self.health_check_port
        if self.health_check_enabled is not None:
            not_null_args["HealthCheckEnabled"] = self.health_check_enabled
        if self.health_check_path is not None:
            not_null_args["HealthCheckPath"] = self.health_check_path
        if self.health_check_interval_seconds is not None:
            not_null_args["HealthCheckIntervalSeconds"] = self.health_check_interval_seconds
        if self.health_check_timeout_seconds is not None:
            not_null_args["HealthCheckTimeoutSeconds"] = self.health_check_timeout_seconds
        if self.healthy_threshold_count is not None:
            not_null_args["HealthyThresholdCount"] = self.healthy_threshold_count
        if self.unhealthy_threshold_count is not None:
            not_null_args["UnhealthyThresholdCount"] = self.unhealthy_threshold_count
        if self.matcher is not None:
            not_null_args["Matcher"] = self.matcher
        if self.target_type is not None:
            not_null_args["TargetType"] = self.target_type
        if self.tags is not None:
            not_null_args["Tags"] = self.tags
        if self.ip_address_type is not None:
            not_null_args["IpAddressType"] = self.ip_address_type

        # Create TargetGroup
        service_client = self.get_service_client(aws_client)
        try:
            create_response = service_client.create_target_group(
                Name=self.name,
                **not_null_args,
            )
            logger.debug(f"Response: {create_response}")
            resource_dict = create_response.get("TargetGroups", {})

            # Validate resource creation
            if resource_dict is not None:
                self.active_resource = create_response
                return True
        except Exception as e:
            logger.error(f"{self.get_resource_type()} could not be created.")
            logger.error(e)
        return False

    def _read(self, aws_client: AwsApiClient) -> Any | None:
        """Returns the TargetGroup

        Args:
            aws_client: The AwsApiClient for the current TargetGroup
        """
        from botocore.exceptions import ClientError

        logger.debug(f"Reading {self.get_resource_type()}: {self.get_resource_name()}")
        service_client = self.get_service_client(aws_client)
        try:
            describe_response = service_client.describe_target_groups(Names=[self.name])
            logger.debug(f"Describe Response: {describe_response}")
            resource_list = describe_response.get("TargetGroups", None)

            if resource_list is not None and isinstance(resource_list, list):
                for resource in resource_list:
                    if resource.get("TargetGroupName") == self.name:
                        self.active_resource = resource
        except ClientError as ce:
            logger.debug(f"ClientError: {ce}")
        except Exception as e:
            logger.error(f"Error reading {self.get_resource_type()}.")
            logger.error(e)
        return self.active_resource

    def _delete(self, aws_client: AwsApiClient) -> bool:
        """Deletes the TargetGroup

        Args:
            aws_client: The AwsApiClient for the current TargetGroup
        """
        print_info(f"Deleting {self.get_resource_type()}: {self.get_resource_name()}")

        service_client = self.get_service_client(aws_client)
        self.active_resource = None

        try:
            tg_arn = self.get_arn(aws_client)
            if tg_arn is None:
                logger.error(f"TargetGroup {self.get_resource_name()} not found.")
                return True
            delete_response = service_client.delete_target_group(TargetGroupArn=tg_arn)
            logger.debug(f"Delete Response: {delete_response}")
            return True
        except Exception as e:
            logger.error(f"{self.get_resource_type()} could not be deleted.")
            logger.error("Please try again or delete resources manually.")
            logger.error(e)
        return False

    def _update(self, aws_client: AwsApiClient) -> bool:
        """Update EcsService"""
        print_info(f"Updating {self.get_resource_type()}: {self.get_resource_name()}")

        tg_arn = self.get_arn(aws_client=aws_client)
        if tg_arn is None:
            logger.error(f"TargetGroup {self.get_resource_name()} not found.")
            return True

        # create a dict of args which are not null, otherwise aws type validation fails
        not_null_args: dict[str, Any] = {}
        if self.health_check_protocol is not None:
            not_null_args["HealthCheckProtocol"] = self.health_check_protocol
        if self.health_check_port is not None:
            not_null_args["HealthCheckPort"] = self.health_check_port
        if self.health_check_enabled is not None:
            not_null_args["HealthCheckEnabled"] = self.health_check_enabled
        if self.health_check_path is not None:
            not_null_args["HealthCheckPath"] = self.health_check_path
        if self.health_check_interval_seconds is not None:
            not_null_args["HealthCheckIntervalSeconds"] = self.health_check_interval_seconds
        if self.health_check_timeout_seconds is not None:
            not_null_args["HealthCheckTimeoutSeconds"] = self.health_check_timeout_seconds
        if self.healthy_threshold_count is not None:
            not_null_args["HealthyThresholdCount"] = self.healthy_threshold_count
        if self.unhealthy_threshold_count is not None:
            not_null_args["UnhealthyThresholdCount"] = self.unhealthy_threshold_count
        if self.matcher is not None:
            not_null_args["Matcher"] = self.matcher

        service_client = self.get_service_client(aws_client)
        try:
            response = service_client.modify_target_group(
                TargetGroupArn=tg_arn,
                **not_null_args,
            )
            logger.debug(f"Update Response: {response}")
            resource_dict = response.get("TargetGroups", {})

            # Validate resource creation
            if resource_dict is not None:
                print_info(f"TargetGroup updated: {self.get_resource_name()}")
                self.active_resource = response
                return True
        except Exception as e:
            logger.error(f"{self.get_resource_type()} could not be created.")
            logger.error(e)
        return False

    def get_arn(self, aws_client: AwsApiClient) -> str | None:
        tg = self._read(aws_client)
        if tg is None:
            return None
        tg_arn = tg.get("TargetGroupArn", None)
        return tg_arn
