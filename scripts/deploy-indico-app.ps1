# Uninstall any existing indico-app pod
helm uninstall indico-chart

# Deploy indico app
helm install indico-chart .\helm\indicoapp\ --values .\helm\indicoapp\values.yaml

# Wait for the pods to be ready
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=indico-app --timeout=180s

# Display the pods
echo "### GET PODS ###"
kubectl get pods -l app.kubernetes.io/name=indico-app

# Port forward the pods so I can access them via localhost
$POD_NAME = $(kubectl get pods --namespace default -l "app.kubernetes.io/name=indico-app,app.kubernetes.io/instance=indico-chart" -o jsonpath="{.items[0].metadata.name}")
$CONTAINER_PORT = $(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
Write-Host "Visit http://127.0.0.1:9001 to use your application"
kubectl --namespace default port-forward $POD_NAME 9001:$CONTAINER_PORT
