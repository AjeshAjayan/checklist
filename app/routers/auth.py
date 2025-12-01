from fastapi import APIRouter
from datetime import datetime, timedelta
from app.models.request.login_request import LoginRequest
from database import db
from settings import settings
from app.models.response.login_response import LoginResponse
from app.utils.generate_otp import generate_otp
from datetime import datetime
from datetime import timedelta
from app.models.request.verify_otp_request import VerifyOtpRequest
from app.models.response.verify_otp_response import VerifyOtpResponse
from app.utils.generate_access_token import generate_access_token

router = APIRouter()

@router.post("/login")
async def login_or_signup(login_request: LoginRequest) -> LoginResponse:
    try:
        user = await db.users.find_one({"phone_number": login_request.phone_number})
        
        # If user exist, send OTP
        if user:
            otp = generate_otp()
            await db.users.update_one({
                "phone_number": login_request.phone_number
            }, {
                "$set": {
                    "otp": otp,
                    "expiry_time": datetime.now() + timedelta(minutes=5)
                }
            })
            return LoginResponse(otp=otp if settings.MOCK_OTP else "", mock_otp=settings.MOCK_OTP)
        else:
            # If user does not exist, create user and send OTP
            otp = generate_otp()
            await db.users.insert_one({
                "phone_number": login_request.phone_number,
                "otp": otp,
                "expiry_time": datetime.now() + timedelta(minutes=5)
            })
            return LoginResponse(otp=otp if settings.MOCK_OTP else "", mock_otp=settings.MOCK_OTP)
    except Exception as e:
        print(e)
        return LoginResponse(otp="", mock_otp=settings.MOCK_OTP)


@router.post("/verify")
async def verify_otp(verify_otp_request: VerifyOtpRequest) ->  VerifyOtpResponse:
    try:
        user = await db.users.find_one({"otp": verify_otp_request.otp})
        if user:
            jwt_token = generate_access_token({"phone_number": user["phone_number"]})
            return VerifyOtpResponse(jwt_token=jwt_token, is_success=True)
        else:
            return VerifyOtpResponse(jwt_token="", is_success=False)
    except Exception as e:
        print(e)
        return VerifyOtpResponse(jwt_token="", is_success=False)

