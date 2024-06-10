from abc import ABC, abstractmethod

from app.domains.domain_result import DomainResult
from app.domains.github_event.models import GithubRepoStatsResponseModel, GithubEventResponseModel


class GithubEventServiceABC(ABC):
    @abstractmethod
    async def fetch_events_async(self) -> DomainResult[list[GithubEventResponseModel]]:
        pass

    @abstractmethod
    async def get_event_stats_async(self, repo_name: str, event_type: str) -> DomainResult[GithubRepoStatsResponseModel]:
        pass
