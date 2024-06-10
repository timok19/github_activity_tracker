from fastapi_injector import request_scope
from injector import Module, Binder, singleton

from app.lifespan_manager.lifespan_manager import LifespanManager
from app.lifespan_manager.lifespan_manager_abc import LifespanManagerABC
from app.options import GithubOptions, DatabaseOptions, ApiOptions
from app.domains.github_event.services.github_event_service import GithubEventService
from app.domains.github_event.services.github_event_service_abc import GithubEventServiceABC


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(LifespanManagerABC, to=LifespanManager, scope=singleton)
        binder.bind(GithubEventServiceABC, to=GithubEventService, scope=request_scope)
        binder.bind(GithubOptions, to=GithubOptions(), scope=singleton)
        binder.bind(DatabaseOptions, to=DatabaseOptions(), scope=singleton)
        binder.bind(ApiOptions, to=ApiOptions(), scope=singleton)
