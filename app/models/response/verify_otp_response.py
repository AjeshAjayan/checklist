from pydantic import BaseModel

class VerifyOtpResponse(BaseModel):
    jwt_token: str
    is_success: bool