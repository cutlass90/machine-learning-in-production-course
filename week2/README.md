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
```
kubectl create -f minio-standalone.yaml
```
### Port forwarding
```
kubectl port-forward svc/minio-ui 9001:9001
kubectl port-forward svc/minio-api 9000:9000
```

### Start minio local server
```
minio server ~/minio --console-address :9090
```
### Run minio tests
```angular2html
pytest  week2/test_minio_client.py
```