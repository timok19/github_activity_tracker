from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_injector import attach_injector, InjectorMiddleware, RequestScopeOptions
from injector import Injector
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from varname import nameof

from app.api.controllers.github_controller import GithubController
from app.di_compositor import AppModule
from app.lifespan_manager.lifespan_manager_abc import LifespanManagerABC
from app.options import ApiOptions


ENV_FILE_PATH: Path = Path.cwd() / ".env"

if not ENV_FILE_PATH.exists():
    raise EnvironmentError(".env file not found")

load_dotenv(dotenv_path=ENV_FILE_PATH, override=True, verbose=True)

injector: Injector = Injector([AppModule()])

lifespan_manager: LifespanManagerABC = injector.get(LifespanManagerABC)
api_options: ApiOptions = injector.get(ApiOptions)

app: FastAPI = FastAPI(
    title="GitHub Activity Tracker",
    lifespan=lifespan_manager.lifespan,
)

app.add_middleware(InjectorMiddleware, injector=injector)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.opt(exception=exc, colors=True, ansi=True).exception(
        "Request {method} {url}, StatusCode={status} - Exception:",
        method=request.method,
        url=request.url,
        status=exc.status_code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Error occurred: '{nameof(exc)}' with StatusCode={exc.status_code}"},
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.opt(exception=exc, colors=True, ansi=True).exception(
        "Request {method} {url}, StatusCode={status} - Exception:",
        method=request.method,
        url=request.url,
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )


app.include_router(GithubController.create_router())

attach_injector(app, injector, options=RequestScopeOptions(enable_cleanup=True))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=api_options.host,
        port=api_options.port,
        log_level="info",
        reload=True,
        use_colors=True,
    )
