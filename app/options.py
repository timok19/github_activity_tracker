import os
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GithubOptions(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    @property
    def repo_names(self) -> list[str]:
        repos_str: Optional[str] = os.getenv("GITHUB_REPOSITORIES")
        separator: Optional[str] = os.getenv("LIST_SEPARATOR")

        if repos_str is None or separator is None:
            raise ValueError("GITHUB_REPOSITORIES or LIST_SEPARATOR environment variable is not set")

        return repos_str.split(separator)

    @property
    def auth_token(self) -> str:
        if (github_token := os.getenv("GITHUB_TOKEN")) is None:
            raise ValueError("GITHUB_TOKEN environment variable is not set")

        return github_token


class DatabaseOptions(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    @property
    def connection_string(self) -> str:
        if (conn_str := os.getenv("CONNECTION_STRING")) is None:
            raise ValueError("CONNECTION_STRING environment variable is not set")

        return conn_str


class ApiOptions(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    @property
    def host(self) -> str:
        if (api_host := os.getenv("API_HOST")) is None:
            return "127.0.0.1"

        return api_host

    @property
    def port(self) -> int:
        if (api_port := os.getenv("API_PORT")) is None:
            return 8000

        return int(api_port)
