# Setup
### Start cluster
```
minikube start
```
### Start dashboard
```
minikube dashboard
```

# MINIO
### Deploy
```angular2html
kubectl create -f minio-standalone.yaml
```
### Port forwarding
```
kubectl port-forward svc/minio-ui 9001:9001
kubectl port-forward svc/minio-api 9000:9000
```
