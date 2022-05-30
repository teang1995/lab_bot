import json

from typing import Union
from fastapi import FastAPI, request, status

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/", status_code=status.HTTP_200_OK)
def hello_there():
    slack_event = json.loads(request.data)
    if "test" in slack_event:
        return {'message': f'ok, {slack_event}'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}