from typing import Generic, TypeVar, Optional

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class DomainResult(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    value: Optional[T] = Field(None)
    error_message: Optional[str] = Field(None)

    def is_success(self) -> bool:
        return self.error_message is None

    @staticmethod
    def success(value: T) -> "DomainResult[T]":
        return _SuccessResult(value=value)

    @staticmethod
    def error(error_message: str) -> "DomainResult[T]":
        return _ErrorResult(error_message=error_message)

    def to_dto(self) -> "DomainResultDto[T]":
        return DomainResultDto(value=self.value, error_message=self.error_message)


class _SuccessResult(DomainResult[T]):
    def __init__(self, value: T) -> None:
        super().__init__(value=value)


class _ErrorResult(DomainResult[T]):
    def __init__(self, error_message: str) -> None:
        super().__init__(error_message=error_message)


class DomainResultDto(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    value: Optional[T] = Field(None)
    error_message: Optional[str] = Field(None)
