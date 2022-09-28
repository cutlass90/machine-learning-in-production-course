FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
RUN apt-get -y update
RUN apt-get -y install git gcc

COPY ./requirements.txt ./src/requirements-lin.txt
WORKDIR ./src
RUN pip3 install --no-cache-dir -r requirements-lin.txt
COPY . .

CMD ["python3", "train.py"]
