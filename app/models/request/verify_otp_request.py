from pydantic import BaseModel

class VerifyOtpRequest(BaseModel):
    otp: str
    phone_number: str