from __future__ import annotations

from typing import Any

from agno.aws.api_client import AwsApiClient
from agno.aws.resource.secret.manager import SecretsManager


def read_secrets(
    secrets: SecretsManager | list[SecretsManager],
    aws_client: AwsApiClient | None = None,
) -> dict[str, Any]:
    secret_dict: dict[str, str] = {}
    if secrets is not None:
        if isinstance(secrets, SecretsManager):
            _secret_dict = secrets.get_secrets_as_dict(aws_client=aws_client)
            if _secret_dict is not None and isinstance(_secret_dict, dict):
                secret_dict.update(_secret_dict)
        elif isinstance(secrets, list):
            for _secret in secrets:
                if isinstance(_secret, SecretsManager):
                    _secret_dict = _secret.get_secrets_as_dict(aws_client=aws_client)
                    if _secret_dict is not None and isinstance(_secret_dict, dict):
                        secret_dict.update(_secret_dict)
    return secret_dict
