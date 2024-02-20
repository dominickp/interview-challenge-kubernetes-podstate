import os
from kubernetes import client, config

SECRET_KUBE_API_KEY = os.environ.get("SECRET_KUBE_API_KEY")
if not SECRET_KUBE_API_KEY:
    raise ValueError("Required envvar 'SECRET_KUBE_API_KEY' is not set")
KUBERNETES_SERVICE_HOST = os.environ.get("KUBERNETES_SERVICE_HOST", "localhost")
KUBERNETES_SERVICE_PORT = os.environ.get("KUBERNETES_SERVICE_PORT", "6443")

class KubeClient:

    def __init__(self) -> None:
        configuration = client.Configuration()
        configuration.api_key['authorization'] = f"Bearer {SECRET_KUBE_API_KEY}"
        configuration.host = f"https://{KUBERNETES_SERVICE_HOST}:{KUBERNETES_SERVICE_PORT}"
        configuration.verify_ssl = False
        with client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            self.api = client.CoreV1Api(api_client)
    
    def _get_pods(self, pod_state: str, namespace="default"):
        # List all pods in the default namespace that have the matching pod state
        return self.api.list_namespaced_pod(namespace, field_selector=f"status.phase={pod_state}")
    
    @staticmethod
    def get_podlist_table(podlist: dict) -> dict:
        result = {"pods": []}
        for pod in podlist.get("items", []):
            name = pod.get("metadata", {}).get("name")
            status = pod.get("status", {}).get("phase")
            instance_name = pod.get("metadata", {}).get("labels", {}).get("app.kubernetes.io/instance")
            restarts = pod.get("status", {}).get("containerStatuses", [{}])[0].get("restartCount", 0)
            result["pods"].append({
                "podName": name,
                "instanceName": instance_name,
                "status": status,
                "restarts": restarts
            })
        
        return result