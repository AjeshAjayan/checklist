from pydantic import BaseModel

class Checklist(BaseModel):
    heading: str
    items: list[str]

class GetChecklistResponse(BaseModel):
    checklist: list[Checklist]
