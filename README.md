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
docker build -t rest-api .
eval $(minikube docker-env -u)
k apply -f example.yaml
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

Hello, World!
```

### ConfigMap
```
k exec -it $(k get pods -o json | jq -r '.items[0].metadata.name') -- cat /etc/config/config.yaml
some: "config"
more: "config
enabled: true
```

You have to redeploy the pods for a configmap change to be seen
```
➜ k exec -it $(k get pods -o json | jq -r '.items[0].metadata.name') -- cat /etc/config/config.yaml
some: "config"
more: "config
enabled: true

k8s-service-alb at ☸️ minikube
➜ k get pods
NAME                                READY   STATUS    RESTARTS        AGE
nginx-deployment-69d9f88474-9lqqf   1/1     Running   0               47s
nginx-deployment-69d9f88474-d89ww   1/1     Running   0               46s
nginx-deployment-69d9f88474-snxmq   1/1     Running   0               45s
shell                               1/1     Running   1 (6m42s ago)   26h

k8s-service-alb at ☸️ minikube
➜ k delete pod nginx-deployment-69d9f88474-9lqqf
pod "nginx-deployment-69d9f88474-9lqqf" deleted

k8s-service-alb at ☸️ minikube
➜ k delete pod nginx-deployment-69d9f88474-d89ww
pod "nginx-deployment-69d9f88474-d89ww" deleted

k8s-service-alb at ☸️ minikube
➜ k delete pod nginx-deployment-69d9f88474-snxmq
pod "nginx-deployment-69d9f88474-snxmq" deleted

k8s-service-alb at ☸️ minikube
➜ k exec -it $(k get pods -o json | jq -r '.items[0].metadata.name') -- cat /etc/config/config.yaml
some: "config"
more: "config
enabled: true
moreconfig: 5
```