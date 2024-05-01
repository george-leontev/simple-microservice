from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(prefix="", tags=["Root"])


@router.get("/")
async def default():
    return RedirectResponse("/docs")
