from __future__ import annotations

from fastapi import FastAPI
from fastapi.routing import APIRouter

from agno.agent.agent import Agent
from agno.app.settings import APIAppSettings
from agno.app.utils import generate_id
from agno.app.whatsapp.async_router import get_async_router
from agno.app.whatsapp.sync_router import get_sync_router
from agno.team.team import Team


class WhatsappAPI:
    def __init__(
        self,
        agent: Agent | None = None,
        team: Team | None = None,
        settings: APIAppSettings | None = None,
        api_app: FastAPI | None = None,
        router: APIRouter | None = None,
    ):
        if not agent and not team:
            raise ValueError("Either agent or team must be provided.")

        if agent and team:
            raise ValueError("Only one of agent or team can be provided.")

        self.agent: Agent | None = agent
        self.team: Team | None = team

        if self.agent:
            if not self.agent.agent_id:
                self.agent.agent_id = generate_id(self.agent.name)

        if self.team:
            if not self.team.team_id:
                self.team.team_id = generate_id(self.team.name)

        self.settings: APIAppSettings = settings or APIAppSettings()
        self.api_app: FastAPI | None = api_app
        self.router: APIRouter | None = router
        self.endpoints_created: set[str] = set()

    def get_router(self) -> APIRouter:
        return get_sync_router(agent=self.agent, team=self.team)

    def get_async_router(self) -> APIRouter:
        return get_async_router(agent=self.agent, team=self.team)

    def get_app(self, use_async: bool = True, prefix: str = "") -> FastAPI:
        if not self.api_app:
            self.api_app = FastAPI(
                title=self.settings.title,
                docs_url="/docs" if self.settings.docs_enabled else None,
                redoc_url="/redoc" if self.settings.docs_enabled else None,
                openapi_url="/openapi.json" if self.settings.docs_enabled else None,
            )

        if not self.api_app:
            raise Exception("API App could not be created.")

        if not self.router:
            self.router = APIRouter(prefix=prefix)

        if not self.router:
            raise Exception("API Router could not be created.")

        if use_async:
            self.router.include_router(self.get_async_router())
        else:
            self.router.include_router(self.get_router())

        self.api_app.include_router(self.router)

        return self.api_app
