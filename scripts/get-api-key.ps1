kubectl create serviceaccount my-service-account
kubectl apply -f "$PSScriptRoot/manifest/role.yml"
kubectl apply -f "$PSScriptRoot/manifest/rolebinding.yml"

$apiKey = kubectl create token my-service-account
echo "API Key: $apiKey"
