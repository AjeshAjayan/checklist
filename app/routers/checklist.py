from fastapi import APIRouter, Depends
from app.middlewares.verify_token import verify_token

router = APIRouter()

@router.get("/")
async def get_checklist(user: dict = Depends(verify_token)):
    try:
        return {"message": "Checklist", "user": user}
    except Exception as e:
        print(e)
        return {"message": "Checklist", "user": None}

