
VALID_POD_STATUSES = frozenset(["Terminating", "Error", "Completed", "Running", "CreateContainerConfigError"])


def get_pod_state(pod: dict) -> str:
    """
    Returns the state of a Kubernetes pod based on its status and metadata.

    Parameters:
    pod (dict): A dictionary representing a Kubernetes pod.

    Returns:
    str: The state of the pod ('CreateContainerConfigError', 'Error', 'Terminating', 'Completed', or 'Running').
    """
    for stat in pod.get("status", {}).get("container_statuses", []):
        waiting = stat.get("state", {}).get("waiting", {})
        if not waiting:
            continue
        if waiting.get("reason") == "CreateContainerConfigError":
            return "CreateContainerConfigError"
        if waiting.get("reason"):
            return "Error"

    if pod.get("metadata", {}).get("deletionTimestamp"):
        return "Terminating"
    if pod.get("status", {}).get("phase") == "Succeeded":
        return "Completed"
    return "Running"

def create_pod_table_response(target_pod_state: str, podlist: list) -> dict:
    """
    Returns a dictionary containing a list of pods with the matching pod state.

    Parameters:
    target_pod_state (str): The pod state to match.
    podlist (list): A list of dicts representing Kubernetes pods.
    
    Returns:
    dict: A dictionary containing a list of pods with the matching pod state.
    """
    result = {"pods": []}
    for pod in podlist:
        name = pod.get("metadata", {}).get("name")
        instance_name = pod.get("metadata", {}).get("labels", {}).get("app.kubernetes.io/instance")
        restarts = pod.get("status", {}).get("containerStatuses", [{}])[0].get("restartCount", 0)
        pod_state = get_pod_state(pod)
        if pod_state == target_pod_state:
            result["pods"].append({
                "podName": name,
                "state": pod_state,
                "instanceName": instance_name,
                "restarts": restarts
            })
    
    return result
