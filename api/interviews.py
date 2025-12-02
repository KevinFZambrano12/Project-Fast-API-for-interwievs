from fastapi import APIRouter, Depends
from app.core.dependencies import require_user

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.post("/create")
def create_interview(user = Depends(require_user(roles=["admin", "interviewer"]))):
    return {"message": f"Interview created by {user.email}"}

@router.get("/me")
def list_my_interviews(user = Depends(require_user())):
    return {"interviews": []}
