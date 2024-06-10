from datetime import datetime
from typing import Type

from tortoise import models, fields
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    PydanticModel,
    pydantic_queryset_creator,
    PydanticListModel,
)


class GithubEvent(models.Model):
    id: int = fields.IntField(pk=True)
    event_id: str = fields.CharField(
        max_length=255,
        unique=True,
        null=False,
    )
    event_type: str = fields.CharField(max_length=255, null=False)
    repo_name: str = fields.CharField(max_length=255, null=False)
    created_at: datetime = fields.DatetimeField(null=False)

    def __str__(self) -> str:
        return self.event_id


# Pydantic Models
GithubEventModel: Type[PydanticModel] = pydantic_model_creator(GithubEvent)
GithubEventListModel: Type[PydanticListModel] = pydantic_queryset_creator(GithubEvent)
