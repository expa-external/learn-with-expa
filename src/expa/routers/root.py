from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/home", tags=["home"])
def read_root():
    return JSONResponse({"Hello": "World"})