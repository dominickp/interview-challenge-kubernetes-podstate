import os
from kubernetes import client, config

SECRET_KUBE_API_KEY = os.environ.get("SECRET_KUBE_API_KEY")
KUBERNETES_SERVICE_HOST = os.environ.get("KUBERNETES_SERVICE_HOST", "localhost")
KUBERNETES_SERVICE_PORT = os.environ.get("KUBERNETES_SERVICE_PORT", "6443")

class KubeClient:

    def __init__(self) -> None:
        configuration = client.Configuration()
        if SECRET_KUBE_API_KEY:
            # For local development with docker-compose, run .\scripts\get-api-key.ps1 
            # and save the API key in the .env file like this:
            #   SECRET_KUBE_API_KEY=the-api-key
            #   KUBERNETES_SERVICE_HOST=192.168.1.68    # I couldn't get the docker DNS name of k0s to work
            #   KUBERNETES_SERVICE_PORT=6443
            configuration.api_key['authorization'] = f"Bearer {SECRET_KUBE_API_KEY}"
            configuration.host = f"https://{KUBERNETES_SERVICE_HOST}:{KUBERNETES_SERVICE_PORT}"
            configuration.verify_ssl = False
            with client.ApiClient(configuration) as api_client:
                self.api = client.CoreV1Api(api_client)
        else:
            # Load the in-cluster configuration when running on actual Kubernetes
            config.load_incluster_config()
            self.api = client.CoreV1Api()

    def get_pods(self, namespace: str) -> list:
        """"
        Returns a list of pods in the specified namespace.

        Parameters:
        namespace (str): The namespace to list pods from.

        Returns:
        list: A list of Kubernetes pods.
        """
        podlist = self.api.list_namespaced_pod(namespace=namespace)
        items = podlist.to_dict().get("items", [])
        return items
