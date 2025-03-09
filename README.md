A fully annotated Kubernetes manifest to help people understand what all the
fields are in each object and how they fit together.

### initial setup
```
alias k=kubectl
```

### get things started and deployed
```
minikube delete
minikube start
eval $(minikube docker-env)
docker build -t rest-api:latest .
eval $(minikube docker-env -u)
k apply -f rest-api.yaml
```

### Connecting to the service

Wait until everything is started, you'll know when the pod's state is Running:

```
k get pods
NAME                        READY   STATUS    RESTARTS   AGE
rest-api-6dd7948584-vfkkl   1/1     Running   0          127m
```

Get the details of the `NodePort` rest-api service:
```
k get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        133m
rest-api     NodePort    10.103.97.199   <none>        80:32707/TCP   132m
```

#### MacOS + Minikube + Docker for Mac
If you're on MacOS and using Minikube via Docker for Mac, you can't curl the service directly at the
Minikube ip and the bound NodePort (i.e. `curl http://$(minikube ip):32707`). Instead you'll have to
do:

```
minikube service rest-api --url
```

Then you'll see:

```
http://127.0.0.1:56242
❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.
```

Then in another terminal, `curl http://127.0.0.1:SOMEPORT`

See [here](https://minikube.sigs.k8s.io/docs/handbook/accessing/#nodeport-access) for more details on why.

#### MacOS + Minikube + Parallels
If you're on MacOS and using Minikube via Parallels (`minikube start --driver=parallels`, you can just curl the service
normally, like so:

```
curl http://$(minikube ip):32707

{
  "greeting": "Hello, Homer"
}
```

### Build & Deploy

Because of how images get cached in Minikube, we need to either remove the image for `rest-api:latest` or we
need to tag each image with a different version and update the `rest-api.yaml` mainfest accordingly.

It's easier to just remove the `rest-api:latest` image and rebuild it and redeploy:

```
eval $(minikube docker-env)
docker rmi rest-api:latest
docker build -t rest-api:latest .
eval $(minikube docker-env -u)
k apply -f rest-api.yaml
```

### ConfigMap

Notice that the greeting says "Hello, Homer", which matches the ConfigMap's `name` field in the `config.yaml` file.
It is mounted into the rest-api's container at `/etc/config` (see `rest-api.yaml` k8s manifest).

```
k exec -it $(k get pods -o json | jq -r '.items[0].metadata.name') -- cat /etc/config/config.yaml
name: "Homer"
```

**Important Note: You have to redeploy the pods for a configmap change to be seen**