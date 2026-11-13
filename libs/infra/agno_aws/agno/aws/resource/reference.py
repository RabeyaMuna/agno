from __future__ import annotations

from agno.aws.api_client import AwsApiClient


class AwsReference:
    def __init__(self, reference):
        self.reference = reference

    def get_reference(self, aws_client: AwsApiClient | None = None):
        return self.reference(aws_client=aws_client)
