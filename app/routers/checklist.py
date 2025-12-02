from fastapi import APIRouter, Depends
from app.middlewares.verify_token import verify_token
from app.utils.launch_checklist_assistant import launch_checklist_assistant
from app.models.request.get_checklist_request import GetChecklistRequest
from app.models.response.get_checklist_response import GetChecklistResponse

router = APIRouter()

@router.post("/")
async def get_checklist(request: GetChecklistRequest, _: dict = Depends(verify_token)) -> GetChecklistResponse:
    try:
        response = launch_checklist_assistant(request.prompt)
        return GetChecklistResponse(checklist=response)
    except Exception as e:
        print(e)
        return GetChecklistResponse(checklist=[])
