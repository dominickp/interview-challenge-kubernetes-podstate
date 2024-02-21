from prometheus_client import Counter

metric_kubernetes_api_requests = Counter(
    "kubernetes_api_requests", 
    "Number of requests to the Kubernetes API", 
    ["resource", "namespace"]
)
