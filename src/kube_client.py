import os
from kubernetes import client, config

SECRET_KUBE_API_KEY = os.environ.get("SECRET_KUBE_API_KEY")
if not SECRET_KUBE_API_KEY:
    raise ValueError("Required envvar 'SECRET_KUBE_API_KEY' is not set")
KUBERNETES_SERVICE_HOST = os.environ.get("KUBERNETES_SERVICE_HOST", "localhost")
KUBERNETES_SERVICE_PORT = os.environ.get("KUBERNETES_SERVICE_PORT", "6443")
TARGET_POD_STATUS = os.environ.get("TARGET_POD_STATUS", "Running")

class KubeClient:

    def __init__(self) -> None:
        configuration = client.Configuration()
        configuration.api_key['authorization'] = SECRET_KUBE_API_KEY
        configuration.host = f"https://{KUBERNETES_SERVICE_HOST}:{KUBERNETES_SERVICE_PORT}"
        configuration.verify_ssl = False
        with client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            self.api = client.CoreV1Api(api_client)
            
    
    def get_pods(self):
        return self.api.list_namespaced_pod(namespace='default')
    