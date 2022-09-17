FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
RUN apt-get -y update
RUN apt-get -y install git gcc

COPY ./ ./src
WORKDIR ./src
RUN pip3 install --no-cache-dir -r requirements-lin.txt
RUN pip3 uninstall -y torchtext

CMD ["python3", "scripts/dream.py", "--web", "--port", "9090", "--host", "0.0.0.0"]
