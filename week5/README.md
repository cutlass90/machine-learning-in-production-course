1. [Done]streamlit app that do nothing. just page
2. [Done]deploy at cloudrun with CI
3. [in progress]add training and inference
4. add fast api with backend
5. add queues
6. add billing


```angular2html
docker build --progress=plain -t sd-concept:latest ./
```
```angular2html
docker run -p 1234:1234 --gpus all -d sd-concept:latest
```
```angular2html
gcloud services enable containerregistry.googleapis.com
```
```angular2html
gcloud auth configure-docker
``` 
```angular2html
docker push gcr.io/sd-concept-project/sd-concept:latest
```
```angular2html
gcloud run deploy sd-concept-project --image=gcr.io/sd-concept-project/sd-concept:latest --max-instances=10 --min-instances=1 --port=1234 --region=us-east1 --cpu=4 --memory=8Gi
```
```angular2html
docker run -p 1234:1234 --gpus all -it -v /home/nazar/machine_learning_in_production_course/week5/weights:/workspace/src/weights sd-concept:latest /bin/bash
```
```angular2html
gcloud run services delete sd-concept-project
```
```angular2html
gcloud compute machine-types list --filter highgpu
```
```angular2html
gcloud compute accelerator-types list --filter p100
```
```angular2html
gcloud container clusters create sd-concept-cluster --zone us-central1-a --accelerator type=nvidia-tesla-a100,count=1 --machine-type a2-highgpu-1g --num-nodes 1
```
```angular2html
gcloud container clusters create sd-concept-cluster --zone us-central1-c --accelerator type=nvidia-tesla-p100,count=1 --machine-type n1-standard-8 --num-nodes 1
```
опис відеокарт
https://cloud.google.com/kubernetes-engine/docs/how-to/gpus
опис машин і відеокарт
https://cloud.google.com/compute/docs/gpus
```angular2html
/home/nazar/google-cloud-sdk/bin/kubectl get nodes
```
```angular2html
/home/nazar/google-cloud-sdk/bin/kubectl apply -f deployment.yaml
```


questions:
differents with 3 cluster creation methods
(https://cloud.google.com/kubernetes-engine/docs/how-to/gpus)

що з квотами?

