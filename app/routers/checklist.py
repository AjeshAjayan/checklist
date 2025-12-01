from fastapi import APIRouter, Depends
from app.middlewares.verify_token import verify_token
from app.utils.launch_checklist_assistant import launch_checklist_assistant

router = APIRouter()

@router.get("/{prompt}")
async def get_checklist(prompt: str, user: dict = Depends(verify_token)):
    try:
        response = launch_checklist_assistant(prompt)
        return {"message": "Checklist", "user": user, "response": response}
    except Exception as e:
        print(e)
        return {"message": "Checklist", "user": None}
