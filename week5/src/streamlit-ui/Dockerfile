FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install streamlit==1.13.0 Pillow==9.1.0

COPY . .


ENTRYPOINT ["streamlit", "run", "streamlit_ui.py", "--server.port=8501", "--server.maxUploadSize", "3000"]