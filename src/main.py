import os
import logging
from typing import Union
from fastapi import FastAPI

from kube_client import KubeClient
from response import create_pod_table_response, VALID_POD_STATUSES

POD_STATUS = os.environ.get("POD_STATUS", "Running")
if POD_STATUS not in VALID_POD_STATUSES:
    raise ValueError(f"Invalid pod status: '{POD_STATUS}' must be one of: {VALID_POD_STATUSES}")

app = FastAPI()

@app.get("/")
def get_pods_table():
    client = KubeClient()
    try:
        pods = client.get_pods("default")
        return create_pod_table_response(target_pod_state=POD_STATUS, podlist=pods)
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}
