# interview-challenge-indico


## Challenge
You have 1-2 days to complete this exercise, email it back to us (as a .zip file), then we will schedule a time to review it online.

Description
You are to build a Python based Kubernetes Service that looks for pods that are in a designated status state. Status should be a parameter to this program, passed in via environment variable POD_STATUS and can be one of: Terminating, Error, Completed, Running or CreateContainerConfigError. The program should produce a table listing of all pods in the specified state.

Step 1 – Program Development
Build and debug the program using an IDE (Visual Studio Code or something else).   To test your program you can use Kind, K3s or any other Kubernetes that you are currently connected to.

Step 2 - Containerize
Build a Dockerfile for your program.

Step 3 – Deploy your Container
Deploy your container (preferably using Helm) into your cluster.    This can be either a K8s Job, Deployment or Pod.

## Setup

Create a .env file:

```sh
# Run .\scripts\get-api-key.ps1 to get a new one when this expires
SECRET_KUBE_API_KEY=
KUBERNETES_SERVICE_HOST=192.168.1.68
KUBERNETES_SERVICE_PORT=6443
```
### k0s
Start `k0s` and then run:
```sh
docker exec k0s cat /var/lib/k0s/pki/admin.conf
```
Paste the contents into kube conf

### Helm
Install it


### Get some services running

FIXME: run `.\scripts\deploy-hello-world-pods.ps1`

https://artifacthub.io/packages/helm/cloudecho/hello
```
helm repo add cloudecho https://cloudecho.github.io/charts/
helm repo update
helm install my-hello-1 cloudecho/hello -n default --version=0.1.2
helm install my-hello-2 cloudecho/hello -n default --version=0.1.2
helm install my-hello-3 cloudecho/hello -n default --version=0.1.2
```

1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=hello,app.kubernetes.io/instance=my-hello-2" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT

Then check the status:

```
PS C:\Users\Dom\Documents\GitHub\interview-challenge-indico> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
my-hello-1-6d4cd8686d-vgj6d   0/1     Pending   0          10s
my-hello-2-bf74b54ff-ldv7w    0/1     Pending   0          10s
my-hello-3-5f4fd4b6fd-298wl   0/1     Pending   0          8s
my-hello-5c4f755fc4-bxzxm     0/1     Pending   0          2m19s
```

```
  Warning  FailedScheduling  5m26s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/master: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
```

Why aren't they running?
```
kubectl describe pod my-hello-1-6d4cd8686d-vgj6d
```
Remove taint from the `k0s` node
`kubectl taint nodes k0s node-role.kubernetes.io/master-`

```
PS C:\Users\Dom\Documents\GitHub\interview-challenge-indico> kubectl get pods
NAME                             READY   STATUS    RESTARTS   AGE
my-hello-1-6d4cd8686d-vgj6d      1/1     Running   0          9m59s
my-hello-2-bf74b54ff-ldv7w       1/1     Running   0          9m59s
my-hello-3-5f4fd4b6fd-298wl      1/1     Running   0          9m57s
my-hello-5c4f755fc4-bxzxm        1/1     Running   0          12m
my-helloworld-6d569969c6-q4scc   1/1     Running   0          7m26s
```


### Deploying app into local kube
`helm install indico-chart .\helm\indicoapp\ --values .\helm\indicoapp\values.yaml`

Uninstall
`helm uninstall indico-chart`


### bad state example

`helm install indico-badstate-chart .\helm\indicoapp-badstate\ --values .\helm\indicoapp-badstate\values.yaml`
`helm uninstall indico-badstate-chart`


## Todo
- Add tests for different state conditions
- Cleanup/readme
- Refine code