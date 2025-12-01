from pydantic import BaseModel

class LoginResponse(BaseModel):
    otp: str
    mock_otp: bool