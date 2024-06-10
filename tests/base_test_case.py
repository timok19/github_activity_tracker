from pathlib import Path

from dotenv import load_dotenv
from injector import Injector, singleton
from tortoise.contrib.test import IsolatedTestCase

from app.domains.github_event.services.github_event_service import GithubEventService
from app.domains.github_event.services.github_event_service_abc import GithubEventServiceABC
from app.options import DatabaseOptions, GithubOptions
from tests.base_test_case_abc import BaseTestCaseABC

PATH_TO_TEST_ENV_FILE: Path = Path.cwd() / "tests" / ".env.test"

load_dotenv(dotenv_path=PATH_TO_TEST_ENV_FILE, verbose=True)


class BaseTestCase(IsolatedTestCase, BaseTestCaseABC):
    @classmethod
    def get_test_env_file_path(cls) -> Path:
        return Path.cwd() / "tests" / ".env.test"

    @classmethod
    def load_test_env_file(cls) -> None:
        env_file_path: Path = cls.get_test_env_file_path()
        if not load_dotenv(dotenv_path=env_file_path, verbose=True):
            raise EnvironmentError("Unable to load %r file" % str(env_file_path))

    @classmethod
    def remove_test_env_file(cls) -> None:
        NotImplementedError("Not used yet")

    @classmethod
    def setUpClass(cls):
        cls.load_test_env_file()

    def setUp(self):
        self._injector_mock: Injector = Injector()
        self._injector_mock.binder.bind(DatabaseOptions, to=DatabaseOptions(), scope=singleton)
        self._injector_mock.binder.bind(GithubEventServiceABC, to=GithubEventService, scope=singleton)
        self._injector_mock.binder.bind(GithubOptions, to=GithubOptions(), scope=singleton)

        self._github_event_service: GithubEventServiceABC = self._injector_mock.get(GithubEventServiceABC)

    def tearDown(self):
        self._injector_mock = None
        del self._injector_mock
