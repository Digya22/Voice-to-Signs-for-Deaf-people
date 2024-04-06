from fastapi import FastAPI

# from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from functions import english_to_tokens, get_video_path, stream_video


class Text(BaseModel):
    text: str


app = FastAPI()


@app.get("/")
def root():
    return {"Success": 200}


@app.post("/video")
def video(text: Text):
    tokens = english_to_tokens(text.text).get("tokens")
    return stream_video(get_video_path(tokens))
