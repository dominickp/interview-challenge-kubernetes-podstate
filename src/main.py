import os
from typing import Union
from fastapi import FastAPI

from kube_client import KubeClient

TARGET_POD_STATUS = os.environ.get("TARGET_POD_STATUS", "Running")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/kube")
def read_kube():
    client = KubeClient()
    pods = client._get_pods(pod_state=TARGET_POD_STATUS)
    return client.get_podlist_table(pods.to_dict())


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
