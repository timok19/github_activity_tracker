from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from injector import inject
from tortoise.contrib.fastapi import RegisterTortoise

from app.lifespan_manager.lifespan_manager_abc import LifespanManagerABC
from app.options import DatabaseOptions


class LifespanManager(LifespanManagerABC):
    @inject
    def __init__(self, database_options: DatabaseOptions) -> None:
        self.__database_options: DatabaseOptions = database_options

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator:
        async with RegisterTortoise(
            app,
            db_url=self.__database_options.connection_string,
            modules={"models": ["app.infrastructure.models"]},
            generate_schemas=True,
            add_exception_handlers=True,
        ):
            yield
