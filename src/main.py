import os
import logging
from typing import Union
from fastapi import FastAPI

from kube_client import KubeClient

POD_STATUS = os.environ.get("POD_STATUS", "Error")
VALID_POD_STATUSES = frozenset(["Terminating", "Error", "Completed", "Running", "CreateContainerConfigError"])
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
        pods = client._get_pods(pod_state=POD_STATUS)
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}
    return client.get_podlist_table(pods)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
