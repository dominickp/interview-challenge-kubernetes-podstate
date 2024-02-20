from typing import Union
from fastapi import FastAPI

from kube_client import KubeClient


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/kube")
def read_kube():
    client = KubeClient()
    return client.get_pods()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
