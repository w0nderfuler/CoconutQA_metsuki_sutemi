import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from Cinescope.resources.roles import Roles


class RequestUserRegisterModel(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=12)
    passwordRepeat: str
    roles: list[Roles]

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        if "@" not in email:
            raise ValueError(f"Email {email} must contain @")
        return email

    @model_validator(mode="after")
    def validate_password_repeat(self) -> "RequestUserRegisterModel":
        if self.password != self.passwordRepeat:
            raise ValueError("Passwords do not match")
        return self


class ResponseUserRegisterModel(BaseModel):
    id: str
    email: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    )
    fullName: str
    verified: bool
    banned: bool | None = None
    roles: list[Roles]
    createdAt: str

    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError as error:
            raise ValueError("createdAt must use ISO 8601 format") from error
        return value


class UserCreateModel(BaseModel):
    email: str
    fullName: str
    password: str
    verified: bool = True
    banned: bool = False


class UserUpdateModel(BaseModel):
    roles: list[Roles]
    verified: bool
    banned: bool


class UserLoginModel(BaseModel):
    email: str
    password: str
