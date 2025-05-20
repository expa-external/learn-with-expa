from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", tags=["root"])
def read_root():
    return JSONResponse({"Hello": "World"})