from abc import ABC, abstractmethod

from app.domains.domain_result import DomainResultDto
from app.domains.github_event.models import GithubRepoStatsResponseModel, GithubEventResponseModel


class GithubControllerABC(ABC):
    @abstractmethod
    async def fetch_events_async(self) -> DomainResultDto[tuple[GithubEventResponseModel]]:
        """
        Asynchronously fetch GitHub events from the configured repositories.

        :returns:
            ``DomainResultDto[List[GithubEventResponseModel]]``: A result with list of fetched GitHub events.
        """

    @abstractmethod
    async def get_repo_stats_async(self, repo_name: str, event_type: str) -> DomainResultDto[GithubRepoStatsResponseModel]:
        """
        Get repository statistics for a specific event type.

        :argument repo_name: Github repository name
        :argument event_type: Github event type

        :returns:
            DomainResultDto[GithubRepoStatsResponseModel]: A result of the repository statistics.
        """
