## Simple educational implementation of paper [Denoising Diffusion Probabilistic Models](https://arxiv.org/pdf/2006.11239.pdf)

### Dataset
It uses a naive MNIST dataset, so one does not need to worry about it. It can be replaced with more complicated dataset easily.

### start training
```
python3 train.py
```

### to start training in docker container first build docker image
```angular2html
docker build -t sd-mnist:latest .
```
### then run training inside the container
```angular2html
docker run -it --gpu all sd-mnist:latest
```