from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/root", tags=["Root"])
def read_root():
    return JSONResponse({"Hello": "World"})