from fastapi import APIRouter, Depends
from app.middlewares.verify_token import verify_token
from app.agents.checklist_agent import checklist_agent
from app.models.request.get_checklist_request import GetChecklistRequest
from app.models.response.get_checklist_response import GetChecklistResponse

router = APIRouter()

@router.post("/")
async def get_checklist(request: GetChecklistRequest, _: dict = Depends(verify_token)) -> GetChecklistResponse:
    try:
        response = await checklist_agent(request.prompt)
        return GetChecklistResponse(checklist=response)
    except Exception as e:
        print(e)
        return GetChecklistResponse(checklist=[])
