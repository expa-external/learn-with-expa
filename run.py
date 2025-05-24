import uvicorn
from src.expa.main import create_app

if __name__ == "__main__":
    uvicorn.run("src.expa.main:create_app", factory=True, host="0.0.0.0", port=8000, reload=True)
