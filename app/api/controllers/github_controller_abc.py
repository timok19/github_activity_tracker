from abc import ABC, abstractmethod

from app.domains.domain_result import DomainResultDto
from app.domains.github_event.models import GithubRepoStatsResponseModel, GithubEventResponseModel


class GithubControllerABC(ABC):
    @abstractmethod
    async def fetch_events_async(self) -> DomainResultDto[list[GithubEventResponseModel]]:
        pass

    @abstractmethod
    async def get_repo_stats_async(self, repo_name: str, event_type: str) -> DomainResultDto[GithubRepoStatsResponseModel]:
        pass
