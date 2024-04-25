import uuid as pyuuid

from pydantic import BaseModel, ConfigDict, StringConstraints, TypeAdapter
from typing_extensions import Annotated, List


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: pyuuid.UUID
    username: Annotated[str, StringConstraints(max_length=50)]
    password: Annotated[str, StringConstraints(max_length=50)]
    total: int
    wins: int 