1. streamlit app that do nothing. just page
2. deploy at cloudrun with CI
3. add training and inference
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
Service URL: https://sd-concept-project-ylwlqo73vq-ue.a.run.app
```angular2html
gcloud run services delete sd-concept-project
```
