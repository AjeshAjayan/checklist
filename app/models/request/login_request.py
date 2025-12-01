from pydantic import BaseModel

class LoginRequest(BaseModel):
    phone_number: str
