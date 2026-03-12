from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserSchema):
    pass


class UserUpdateSchema(UserSchema):
    pass


__all__ = ["UserCreateSchema", "UserSchema", "UserUpdateSchema"]