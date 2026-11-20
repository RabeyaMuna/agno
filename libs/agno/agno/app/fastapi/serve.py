from __future__ import annotations

from fastapi import FastAPI

from agno.utils.log import logger


def serve_fastapi_app(
    app: str | FastAPI,
    *,
    host: str = "localhost",
    port: int = 7777,
    reload: bool = False,
    **kwargs,
):
    import uvicorn

    logger.info(f"Starting API on {host}:{port}")

    uvicorn.run(app=app, host=host, port=port, reload=reload, **kwargs)
