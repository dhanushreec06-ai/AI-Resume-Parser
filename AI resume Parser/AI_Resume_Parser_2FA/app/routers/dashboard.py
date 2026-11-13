from fastapi import APIRouter, Depends
from .profile import current_user
from ..models import User

router = APIRouter(tags=["Dashboard"])

@router.get("/api/v1/dashboard")
async def dashboard(user: User = Depends(current_user)):
    return {"user": user.name, "state": "active", "redirect_url": "/dashboard/student"}
