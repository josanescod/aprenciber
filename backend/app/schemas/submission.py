from pydantic import BaseModel


class FlagSubmitRequest(BaseModel):
    flag: str


class FlagSubmitResponse(BaseModel):
    correct: bool
    message: str
