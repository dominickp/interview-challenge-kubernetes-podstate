# Uninstall any existing hello-world pods so I can re-run this script
helm uninstall my-hello-1 -n default
helm uninstall my-hello-2 -n default
helm uninstall my-hello-3 -n default

# Deploy 3 hello-world pods using the cloudecho/hello chart
helm repo add cloudecho https://cloudecho.github.io/charts/
helm repo update
helm install my-hello-1 cloudecho/hello -n default --version=0.1.2
helm install my-hello-2 cloudecho/hello -n default --version=0.1.2
helm install my-hello-3 cloudecho/hello -n default --version=0.1.2

# Wait for the pods to be ready
kubectl wait --for=condition=Ready pod -l app.kubernetes.io/name=hello --timeout=180s

# Display the pods
echo "### GET PODS ###"
kubectl get pods -l app.kubernetes.io/name=hello

# Port forward the pods so I can access them via localhost
$POD_NAME = $(kubectl get pods --namespace default -l "app.kubernetes.io/name=hello,app.kubernetes.io/instance=my-hello-1" -o jsonpath="{.items[0].metadata.name}")
$CONTAINER_PORT = $(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
Write-Host "Visit http://127.0.0.1:8080 to use your application"
kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
