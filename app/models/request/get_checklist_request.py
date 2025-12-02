from pydantic import BaseModel

class GetChecklistRequest(BaseModel):
    prompt: str
