import os
import time
import uuid
from typing import List

import requests
from datetime import datetime
import pickle
import uvicorn
from fastapi import FastAPI, File, UploadFile
# from google.cloud import aiplatform
from google.cloud import storage
import redis

from config import opt

if os.path.isfile('secrets/sd-concept-project-14c11c803fff.json'):
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('secrets/sd-concept-project-14c11c803fff.json')
    storage_client = storage.Client(opt.project_name, credentials=credentials)
else:
    storage_client = storage.Client(opt.project_name)

app = FastAPI()
r = redis.Redis(host=opt.redis_ip, port=opt.redis_port, db=0)
user_imgs_bucket = storage_client.get_bucket(opt.user_image_bucket_name)


def concept2checkpoint(concept):
    return concept + 'checkpoint.ckpt'

def checkpoint2concept(checkpoint):
    return checkpoint.replace('checkpoint.ckpt', '')


def write_image(source_file, destination_blob_name):
    blob = user_imgs_bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file)


@app.post("/train")
def strarttraining(user_email: str = File(...), images_list: List[UploadFile] = File(...)):
    blob_names = [str(user_email) + f'_img{i}' + os.path.splitext(img.filename)[1].lower() for i, img in enumerate(images_list)]
    for i, (img, blob) in enumerate(zip(images_list, blob_names)):
        write_image(img.file, blob)
    task = {
        'save_checkpoint_path_blob': f'{user_email}_{datetime.now().strftime("%d.%m.%Y_%H:%M")}checkpoint.ckpt',
        'user_imgs_blobs_list': blob_names
    }
    print(task)
    r.rpush(opt.train_queue_name, pickle.dumps(task))


@app.get("/get-concepts")
def get_concepts():
    blobs = storage_client.list_blobs(opt.checkpoints_bucket_name)
    checkpoints = [blob.name for blob in blobs]
    concepts = [checkpoint2concept(ch) for ch in checkpoints]
    return concepts

@app.post("/generate-images")
def generate_images(prompt: str=File(...), concept: str=File(...)):
    imgs_names = [f'{str(uuid.uuid4())}.jpg' for _ in range(opt.n_samples)]
    task = {
        'taskid': str(uuid.uuid4()),
        'prompt': prompt,
        'checkpoint_name': concept2checkpoint(concept),
        'imgs_names': imgs_names
    }
    print(task)
    r.rpush(opt.task_queue_name, pickle.dumps(task))
    while True:
        time.sleep(0.5)
        task_status = r.get(task['taskid'])
        if task_status:
            task_status = task_status.decode()
            r.delete(task['taskid'])
            if task_status == 'done':
                return imgs_names
            elif task_status == 'fail':
                return 'task failed'



if __name__ == "__main__":
    # uvicorn.run("server:app", host=f"{opt.host_ip}", port=opt.web_server_port, reload=True, access_log=False)
    uvicorn.run("server:app", host=f"localhost", port=opt.web_server_port)
