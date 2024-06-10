from datetime import datetime, timedelta, UTC

from async_lru import alru_cache
from github import Github
from github.Event import Event
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from injector import inject
from tortoise.transactions import in_transaction

from app.domains.domain_result import DomainResult
from app.infrastructure.models import GithubEvent
from app.domains.github_event.models import GithubRepoStatsResponseModel, GithubEventResponseModel
from app.options import GithubOptions
from app.domains.github_event.services.github_event_service_abc import GithubEventServiceABC


class GithubEventService(GithubEventServiceABC):
    @inject
    def __init__(self, github_options: GithubOptions) -> None:
        self.__github_client: Github = Github(github_options.auth_token)
        self.__github_repo_names: list[str] = github_options.repo_names

    @alru_cache(ttl=300, maxsize=1024)
    async def fetch_events_async(self) -> DomainResult[list[GithubEventResponseModel]]:
        results: list[GithubEventResponseModel] = []

        for repo_name in self.__github_repo_names:
            repo: Repository = self.__github_client.get_repo(repo_name)
            events: PaginatedList[Event] = repo.get_events()

            await self.__store_events_for_repo(events, repo_name)

            results.extend(
                [
                    GithubEventResponseModel(
                        id=event.id,
                        repo_name=repo_name,
                        type=event.type,
                        created_at=event.created_at,
                    )
                    for event in events
                ]
            )

        return DomainResult.success(results)

    @staticmethod
    async def __store_events_for_repo(events: PaginatedList[Event], repo_name: str) -> None:
        new_gh_events: list[GithubEvent] = []

        async with in_transaction():
            for event in events:
                if not await GithubEvent.filter(event_id=event.id).exists():
                    new_gh_events.append(
                        GithubEvent(
                            event_id=event.id,
                            event_type=event.type,
                            repo_name=repo_name,
                            created_at=event.created_at,
                        )
                    )

            if len(new_gh_events) > 0:
                await GithubEvent.bulk_create(new_gh_events)

    async def get_event_stats_async(self, repo_name: str, event_type: str) -> DomainResult[GithubRepoStatsResponseModel]:
        window_start: datetime = datetime.now(tz=UTC) - timedelta(days=7)

        events: list[GithubEvent] = await GithubEvent.filter(
            repo_name=repo_name,
            event_type=event_type,
            created_at__gte=window_start,
        ).order_by("created_at")

        len_events: int = len(events)

        if len_events > 500:
            events = events[:500]

        if len_events < 2:
            error_message: str

            if len_events == 0:
                error_message = f"No events '{event_type}' were found for repo '{repo_name}'."
            else:
                error_message = f"Only one event '{event_type}' was found for repo '{repo_name}'."

            return DomainResult.error(error_message)

        time_deltas_in_seconds: list[float] = [(events[i].created_at - events[i - 1].created_at).total_seconds() for i in range(1, len_events)]

        avg_time_in_seconds: float = round(sum(time_deltas_in_seconds) / len(time_deltas_in_seconds), 1)

        return DomainResult.success(
            GithubRepoStatsResponseModel(
                repo_name=repo_name,
                event_type=event_type,
                average_time_between_events=avg_time_in_seconds,
            )
        )
