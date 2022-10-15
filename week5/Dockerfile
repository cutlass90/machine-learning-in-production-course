FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime
RUN apt-get -y update
RUN apt-get -y install git gcc

COPY ./requirements.txt ./src/requirements.txt
WORKDIR ./src
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . ./

CMD ["streamlit", "run", "streamlit_demo.py", "--server.port", "1234"]
