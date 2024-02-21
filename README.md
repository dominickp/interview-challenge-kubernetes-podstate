# interview-challenge-kubernetes-podstate
This repo contains a Python service that uses the Kubernetes API to display a list of pods running with a certain state. GitHub Actions is setup to build and push the docker image to GHCR. Some scripts are included along with a pre-configured k0s that runs inside of Docker (with docker-compose) which facilitate end-to-end testing the service on Kubernetes.

```sh
curl -s http://localhost:8000/ | jq
```
```json
{
  "pods": [
    {
      "podName": "indico-chart-7987cfdb48-8lpgx",
      "state": "Running",
      "instanceName": "indico-chart",
      "restarts": 0
    },
    {
      "podName": "my-hello-1-6d4cd8686d-b7rwg",
      "state": "Running",
      "instanceName": "my-hello-1",
      "restarts": 0
    },
    {
      "podName": "my-hello-2-bf74b54ff-7xqdj",
      "state": "Running",
      "instanceName": "my-hello-2",
      "restarts": 0
    },
    {
      "podName": "my-hello-3-5f4fd4b6fd-trnpv",
      "state": "Running",
      "instanceName": "my-hello-3",
      "restarts": 0
    }
  ]
}
```

## Challenge
> #### Description
> You are to build a Python based Kubernetes Service that looks for pods that are in a designated status state. Status should be a parameter to this program, passed in via environment > variable POD_STATUS and can be one of: Terminating, Error, Completed, Running or CreateContainerConfigError. The program should produce a table listing of all pods in the specified state.
> 
> Step 1 – Program Development
> Build and debug the program using an IDE (Visual Studio Code or something else).   To test your program you can use Kind, K3s or any other Kubernetes that you are currently connected to.
> 
> Step 2 - Containerize
> Build a Dockerfile for your program.
> 
> Step 3 – Deploy your Container
> Deploy your container (preferably using Helm) into your cluster.    This can be either a K8s Job, Deployment or Pod.

## Local development
This project utilizes on-container development: where the container we ship is re-utilized as the development environment.

To run the container, it should be as simple as:
```sh
docker-compose up --build app
```

The app should be available here: http://localhost:8000/ And any time code changes are detected, the server will hot-reload.

But to connect to Kubernetes, you'll have to get k0s running first:
```
docker-compose up --build k0s
```
One that's up, use this command to get an admin kube config:
```sh
docker exec k0s cat /var/lib/k0s/pki/admin.conf
```
Then save that file in the right place (`C:\Users\Dom\.kube` for me on Windows). Now `kubectl get pods` should be working.

Now you can get a k8s API key for use in local development:
```sh
.\scripts\get-api-key.ps1
```
Then create a .env file and copy the contents of the API key into it:

```sh
# Run .\scripts\get-api-key.ps1 to get a new one when this expires
SECRET_KUBE_API_KEY=my-api-key
KUBERNETES_SERVICE_HOST=192.168.1.68
KUBERNETES_SERVICE_PORT=6443
```
Set your local IP address of the Docker host as `KUBERNETES_SERVICE_HOST`. So the networking goes out of the app container and back through the host itself to the port we bound to in `docker-compose` (I couldn't get the internal Docker DNS name working). Restart the container when changing this file since it's a change in the container's run context.

### Deploy to Kubernetes
To test the app inside of a Kubernetes cluster, I've created a helm chart which will pull the latest image from GHCR and deploy it into k0s.

The below script will deploy 3 dummy pods (they will probably be stuck pending due to a taint):
```sh
.\scripts\deploy-hello-world-pods.ps1
```
```
PS C:\Users\Dom\Documents\GitHub\interview-challenge-indico> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
my-hello-1-6d4cd8686d-vgj6d   0/1     Pending   0          10s
my-hello-2-bf74b54ff-ldv7w    0/1     Pending   0          10s
my-hello-3-5f4fd4b6fd-298wl   0/1     Pending   0          8s
```

```
Warning  FailedScheduling  5m26s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/master: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling..
```


Then the below script deploys the helm chart for this Python application. It also applies some other Kubernetes manifests needed for the service account and removes the taint on the master node.

```sh
.\scripts\deploy-indico-app.ps1
```

If all goes well, the app should be port forwarded and available here: http://localhost:9001/

```
PS C:\Users\Dom\Documents\GitHub\interview-challenge-indico> kubectl get pods                     
NAME                            READY   STATUS    RESTARTS   AGE
indico-chart-7987cfdb48-8lpgx   1/1     Running   0          20m
my-hello-1-6d4cd8686d-b7rwg     1/1     Running   0          28m
my-hello-2-bf74b54ff-7xqdj      1/1     Running   0          28m
my-hello-3-5f4fd4b6fd-trnpv     1/1     Running   0          28m
```

### Example deployment that puts a pod in a bad state

```sh
helm install indico-badstate-chart .\helm\indicoapp-badstate\ --values .\helm\indicoapp-badstate\values.yaml
```
```sh
helm uninstall indico-badstate-chart
```
