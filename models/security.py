from pydantic import BaseModel


class otp(BaseModel):
    value: str
