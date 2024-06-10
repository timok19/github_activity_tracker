from datetime import datetime

from pydantic import BaseModel, ConfigDict, StrictStr, StrictFloat, AwareDatetime


class GithubRepoStatsResponseModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    repo_name: StrictStr
    event_type: StrictStr
    average_time_between_events: StrictFloat


class GithubEventResponseModel(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    id: StrictStr
    type: StrictStr
    repo_name: StrictStr
    created_at: AwareDatetime
