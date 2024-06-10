from abc import ABC, abstractmethod
from pathlib import Path


class BaseTestCaseABC(ABC):
    @classmethod
    @abstractmethod
    def get_test_env_file_path(cls) -> Path:
        pass

    @classmethod
    @abstractmethod
    def load_test_env_file(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def remove_test_env_file(cls) -> None:
        pass
