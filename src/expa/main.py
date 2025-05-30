import json
import logging.config

from fastapi import FastAPI
from dotenv import load_dotenv
from .routers.root import router as root_router
from .routers.converse import router as converse_router

load_dotenv()


def create_app() -> FastAPI:
    with open('logger_config.json', 'r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info("Application Started")
    app = FastAPI(title="Expa Voice Assistant", version="1.0")
    app.include_router(root_router)
    app.include_router(converse_router)
    return app

# if __name__ == "__main__":
#     print("Say something... (say 'exit' to quit)\n")
#     fileName = record_audio_vad()
#     with open(fileName , "rb") as f:
#         response = requests.post("http://localhost:8000/converse", files={"file": (fileName, f, "audio/wav")})
#         reply = ""
#         for chunk in response.json():
#             reply += chunk.text + " "
#         print(reply)
