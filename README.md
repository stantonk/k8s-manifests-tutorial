```
curl http://$(minikube ip):30228
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