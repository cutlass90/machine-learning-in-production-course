1. [Done]streamlit app that do nothing. just page
2. [Done]deploy at cloudrun with CI
3. [Done]add training and inference
3.1 [Done]deploy at GKE with CI
4. add fast api with backend
5. add queues
6. add billing

## Useful commands:
### Enable ability to work with gcloud image registry
```angular2html
gcloud services enable containerregistry.googleapis.com
```
```angular2html
gcloud auth configure-docker
``` 

### Deploy in Cloud Run (GPU is not supported)
```angular2html
gcloud run deploy sd-concept-project --image=gcr.io/sd-concept-project/sd-concept:latest --max-instances=10 --min-instances=1 --port=1234 --region=us-east1 --cpu=4 --memory=8Gi
```
### Delete deployment in Cloud Run
```angular2html
gcloud run services delete sd-concept-project
```
### GKE Avialable resources lists
```angular2html
gcloud compute machine-types list --filter highgpu
```
```angular2html
gcloud compute accelerator-types list --filter p100
```


[GPU types description](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)
[GPU and machines type description](https://cloud.google.com/compute/docs/gpus)
[tutorail 1](https://cloud.google.com/kubernetes-engine/docs/quickstarts/deploy-app-container-image#python)
[tutorail 2](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#ubuntu)

### kubectl common commands
```angular2html
kubectl get nodes
```
```angular2html
kubectl apply -f deployment.yaml
```
```angular2html
kubectl get deployments
```
```angular2html
kubectl get pods
```
```angular2html
kubectl delete deployments sd-concept-cluster
```
```angular2html
kubectl apply -f service.yaml
```
```angular2html
kubectl exec -it sd-concept-cluster-f6fdccc45-nw7gx -- /bin/sh
```
```angular2html
kubectl logs -f <PODNAME>
```

<br>
нод пули треба для того щоб мати різні відеокарти<br>
регіон більше зони - для того щоб не падало і вічно жило<br>
регіон вміщує декілька зон<br>



TODO if user did not upload images do not start training
