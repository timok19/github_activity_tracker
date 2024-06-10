from fastapi import HTTPException
from fastapi_controllers import Controller, get
from fastapi_injector import Injected
from varname import nameof

from app.api.controllers.github_controller_abc import GithubControllerABC
from app.domains.domain_result import DomainResult, DomainResultDto
from app.domains.github_event.models import GithubRepoStatsResponseModel, GithubEventResponseModel
from app.domains.github_event.services.github_event_service_abc import GithubEventServiceABC


class GithubController(Controller, GithubControllerABC):
    prefix = "/api/github"
    tags = ["Github Events"]

    def __init__(self, github_service: GithubEventServiceABC = Injected(GithubEventServiceABC)) -> None:
        self.__github_service: GithubEventServiceABC = github_service

    @get("/fetch-events", name="Get Github events", response_model=DomainResultDto[list[GithubEventResponseModel]])
    async def fetch_events_async(self) -> DomainResultDto[list[GithubEventResponseModel]]:
        gh_events_result: DomainResult[list[GithubEventResponseModel]] = await self.__github_service.fetch_events_async()

        return gh_events_result.to_dto()

    @get("/get-repo-stats", name="Get Github repos statistics", response_model=DomainResultDto[GithubRepoStatsResponseModel])
    async def get_repo_stats_async(self, repo_name: str, event_type: str) -> DomainResultDto[GithubRepoStatsResponseModel]:
        if not repo_name or not event_type:
            raise HTTPException(
                status_code=400,
                detail=f"Missing {nameof(repo_name)} and {nameof(event_type)}",
            )

        event_stats_result: DomainResult[GithubRepoStatsResponseModel] = await self.__github_service.get_event_stats_async(
            repo_name=repo_name,
            event_type=event_type,
        )

        return event_stats_result.to_dto()
