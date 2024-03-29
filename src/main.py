import os
import logging
from fastapi import FastAPI
from prometheus_client import make_asgi_app
from kube_client import KubeClient
from response import create_pod_table_response, VALID_POD_STATUSES

# Create a runtime error if the app is misconfigured
POD_STATUS = os.environ.get("POD_STATUS", "Running")
if POD_STATUS not in VALID_POD_STATUSES:
    raise ValueError(f"Invalid pod status: '{POD_STATUS}' must be one of: {VALID_POD_STATUSES}")

app = FastAPI()

@app.get("/")
def get_pods_table():
    client = KubeClient()
    try:
        pods = client.get_pods(namespace="default")
        return create_pod_table_response(target_pod_state=POD_STATUS, podlist=pods)
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
