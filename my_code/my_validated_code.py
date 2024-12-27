from pydantic import BaseModel
from pydantic.types import StrictInt, StrictStr
from loguru import logger


class Numbers(BaseModel):
    arg_1: StrictInt
    arg_2: StrictInt


class Name(BaseModel):
    name: StrictStr


class Init(BaseModel):
    name: str

    def __init__(self, name):
        super().__init__(name=name)
        logger.info("INIT")


class StringOrNone(BaseModel):
    var: str | None


# bash deactivate
