import os
import logging
from typing import Union
from fastapi import FastAPI

from kube_client import KubeClient
from response import get_podlist_table, VALID_POD_STATUSES

POD_STATUS = os.environ.get("POD_STATUS", "Error")
if POD_STATUS not in VALID_POD_STATUSES:
    raise ValueError(f"Invalid pod status: '{POD_STATUS}' must be one of: {VALID_POD_STATUSES}")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/kube")
def read_kube():
    client = KubeClient()
    try:
        pods = client.get_pods("default")
        return get_podlist_table(target_pod_state=POD_STATUS, podlist=pods)
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}
    


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
