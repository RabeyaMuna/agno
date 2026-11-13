from __future__ import annotations

import sys
from typing import Any

from agno.utils.log import logger


class AwsApiClient:
    def __init__(
        self,
        aws_region: str | None = None,
        aws_profile: str | None = None,
    ):
        super().__init__()
        self.aws_region: str | None = aws_region
        self.aws_profile: str | None = aws_profile

        # aws boto3 session
        self._boto3_session: Any | None = None
        logger.debug("**-+-** AwsApiClient created")

    def create_boto3_session(self) -> Any | None:
        """Create a boto3 session"""
        import boto3

        logger.debug("Creating boto3.Session")
        try:
            self._boto3_session = boto3.Session(
                region_name=self.aws_region,
                profile_name=self.aws_profile,
            )
            logger.debug("**-+-** boto3.Session created")
            logger.debug(f"\taws_region: {self._boto3_session.region_name}")
            logger.debug(f"\taws_profile: {self._boto3_session.profile_name}")
        except Exception as e:
            logger.error("Could not connect to aws. Please confirm aws cli is installed and configured")
            logger.error(e)
            sys.exit(0)
        return self._boto3_session

    @property
    def boto3_session(self) -> Any | None:
        if self._boto3_session is None:
            self._boto3_session = self.create_boto3_session()
        return self._boto3_session
