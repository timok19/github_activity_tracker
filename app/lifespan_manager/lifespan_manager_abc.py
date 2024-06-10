from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI


class LifespanManagerABC(ABC):
    @asynccontextmanager
    @abstractmethod
    async def lifespan(self, _app: FastAPI) -> AsyncGenerator:
        pass
