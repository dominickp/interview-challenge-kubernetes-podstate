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
        else:
            configuration.load_incluster_config()
        configuration.verify_ssl = False
        with client.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            self.api = client.CoreV1Api(api_client)

    def _matches_pod_state(self, pod: dict, pod_state: str) -> bool:
        return True
    
    def _get_pods(self, pod_state: str, namespace="default"):
        """
        Running: This is equivalent to status.phase being "Running".
        Terminating: This can be derived if metadata.deletionTimestamp is not null.
        Completed: This is equivalent to status.phase being "Succeeded".
        Error: This can be derived if any of the status.containerStatuses have state.waiting.reason as "Error".
        CreateContainerConfigError: This can be derived if any of the status.containerStatuses have state.waiting.reason as "CreateContainerConfigError".
        """
        # List all pods in the default namespace that have the matching pod state
        podlist = self.api.list_namespaced_pod(namespace=namespace)
        items = podlist.to_dict().get("items", [])
        # print(items)
        # Filter the list of pods to only include those with the matching pod state
        return [pod for pod in items if self._matches_pod_state(pod, pod_state)]
    
    @staticmethod
    def get_podlist_table(podlist: list) -> dict:
        result = {"pods": []}
        # print(podlist)
        for pod in podlist:
            name = pod.get("metadata", {}).get("name")
            instance_name = pod.get("metadata", {}).get("labels", {}).get("app.kubernetes.io/instance")
            restarts = pod.get("status", {}).get("containerStatuses", [{}])[0].get("restartCount", 0)
            result["pods"].append({
                "podName": name,
                "instanceName": instance_name,
                "restarts": restarts
            })
        
        return result