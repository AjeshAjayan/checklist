from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    MOCK_OTP: bool
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    OPEN_ROUTER_API_KEY: str
    OPEN_WEATHER_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
