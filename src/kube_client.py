import os
from kubernetes import client, config

SECRET_KUBE_API_KEY = os.environ.get("SECRET_KUBE_API_KEY")
KUBERNETES_SERVICE_HOST = os.environ.get("KUBERNETES_SERVICE_HOST", "localhost")
KUBERNETES_SERVICE_PORT = os.environ.get("KUBERNETES_SERVICE_PORT", "6443")

class KubeClient:

    def __init__(self) -> None:
        configuration = client.Configuration()
        if SECRET_KUBE_API_KEY:
            configuration.api_key['authorization'] = f"Bearer {SECRET_KUBE_API_KEY}"
            configuration.host = f"https://{KUBERNETES_SERVICE_HOST}:{KUBERNETES_SERVICE_PORT}"
            configuration.verify_ssl = False
            with client.ApiClient(configuration) as api_client:
                self.api = client.CoreV1Api(api_client)
        else:
            config.load_incluster_config()
            self.api = client.CoreV1Api()

    def _matches_pod_state(self, pod: dict, pod_state: str) -> bool:
        return True
    
    def get_pods(self, namespace: str):

        # List all pods in the default namespace that have the matching pod state
        podlist = self.api.list_namespaced_pod(namespace=namespace)
        items = podlist.to_dict().get("items", [])
        # print(items)
        # Filter the list of pods to only include those with the matching pod state
        return items
    
  