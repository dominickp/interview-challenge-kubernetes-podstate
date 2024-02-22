
import pytest
from src.response import get_pod_state, create_pod_table_response

EXAMPLE_PODS = {
    "CreateContainerConfigError": {
        "status": {"container_statuses": [{"state": {"waiting": {"reason": "CreateContainerConfigError"}}}]},
        "metadata": {"labels": {"app.kubernetes.io/instance": "instance1"}, "name": "pod1"}
    },
    "Error": {
        "status": {"container_statuses": [{"state": {"waiting": {"reason": "Error"}}}]}, 
        "metadata": {
            "deletionTimestamp": "2021-07-01T00:00:00Z", 
            "labels": {"app.kubernetes.io/instance": "instance2"}, 
            "name": "pod2"
        }
    },
    "Completed": {"status": {"phase": "Succeeded"}},
    "Running": {"status": {"phase": "Running"}},
    "Terminating": {
        "status": {"container_statuses": [{"state": {"waiting": {}}}], "phase": "Running"}, 
        "metadata": {"deletionTimestamp": "2021-07-01T00:00:00Z"}
    }
}

@pytest.mark.parametrize("pod, expected_state", [
    (EXAMPLE_PODS["CreateContainerConfigError"], "CreateContainerConfigError"),
    (EXAMPLE_PODS["Error"], "Error"),
    (EXAMPLE_PODS["Completed"], "Completed"),
    (EXAMPLE_PODS["Running"], "Running"),
    (EXAMPLE_PODS["Terminating"], "Terminating"),
])
def test_get_pod_state(pod, expected_state):
    """
    Test that get_pod_state returns the expected state for a given pod.
    """
    assert get_pod_state(pod) == expected_state

@pytest.mark.parametrize("target_pod_state, podlist, expected_result", [
    (
        "CreateContainerConfigError", [
            EXAMPLE_PODS["Completed"],
            EXAMPLE_PODS["CreateContainerConfigError"],
            EXAMPLE_PODS["Terminating"],
        ], {
            "pods": [
                {"podName": "pod1", "state": "CreateContainerConfigError", "instanceName": "instance1", "restarts": 0}
            ]
        }
    ),
    (
        "Error", [
            EXAMPLE_PODS["Completed"],
            EXAMPLE_PODS["CreateContainerConfigError"],
            EXAMPLE_PODS["Error"],
        ], {
            "pods": [
                {"podName": "pod2", "state": "Error", "instanceName": "instance2", "restarts": 0}
            ]
        }
    ),
])
def test_create_pod_table_response_filters_by_state(target_pod_state, podlist, expected_result):
    """
    Test that create_pod_table_response returns the expected result when filtering by pod state.
    """
    assert create_pod_table_response(target_pod_state, podlist) == expected_result
