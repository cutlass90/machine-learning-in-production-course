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
 