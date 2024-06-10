import time

from app.domains.domain_result import DomainResult
from app.domains.github_event.models import GithubRepoStatsResponseModel, GithubEventResponseModel
from app.options import GithubOptions
from tests.base_test_case import BaseTestCase


class GithubEventServiceTestCase(BaseTestCase):
    tortoise_test_modules = ["app.infrastructure.models"]

    async def test_event_fetch_speed(self):
        # Arrange
        times: list[tuple[float, list[GithubEventResponseModel]]] = []

        # Act
        for i in range(0, 3):
            start: float = time.time()
            result: list[GithubEventResponseModel] = (await self._github_event_service.fetch_events_async()).value
            end: float = time.time()

            times.append((end - start, result))

        # Assert
        self.assertGreater(times[0][0], times[1][0])
        self.assertGreater(times[0][0], times[2][0])

        self.assertListEqual(times[0][1], times[1][1])
        self.assertListEqual(times[0][1], times[2][1])

    async def test_success_fetch_events(self):
        # Act
        gh_events_result: DomainResult[list[GithubEventResponseModel]] = await self._github_event_service.fetch_events_async()

        # Assert
        self.assertIsNotNone(gh_events_result)
        self.assertIsNotNone(gh_events_result.value)
        self.assertIsNone(gh_events_result.error_message)

        self.assertGreater(len(gh_events_result.value), 0)

    async def test_fail_get_repo_stats(self):
        # Arrange
        gh_options: GithubOptions = self._injector_mock.get(GithubOptions)

        repo_name: str = gh_options.repo_names[0]
        event_type: str = "PushEvent"

        # Act
        gh_repo_stats_result: DomainResult[GithubRepoStatsResponseModel] = await self._github_event_service.get_event_stats_async(
            repo_name=repo_name,
            event_type=event_type,
        )

        # Assert
        self.assertIsNotNone(gh_repo_stats_result)
        self.assertIsNone(gh_repo_stats_result.value)
        self.assertIsNotNone(gh_repo_stats_result.error_message)

        self.assertGreater(len(gh_repo_stats_result.error_message), 0)
