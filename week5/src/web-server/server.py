import os
import time
import uuid
from typing import List

import requests
import pickle
import uvicorn
from fastapi import FastAPI, File, UploadFile
# from google.cloud import aiplatform
from google.cloud import storage
import redis

from config import opt

# client = aiplatform.gapic.JobServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})
if os.path.isfile('secrets/sd-concept-project-14c11c803fff.json'):
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('secrets/sd-concept-project-14c11c803fff.json')
    storage_client = storage.Client(opt.project_name, credentials=credentials)
else:
    storage_client = storage.Client(opt.project_name)

app = FastAPI()
r = redis.Redis(host=opt.redis_ip, port=opt.redis_port, db=0)


def concept2checkpoint(concept):
    return concept + 'checkpoint.ckpt'

def checkpoint2concept(checkpoint):
    return checkpoint.replace('checkpoint.ckpt', '')


# def write_image(source_file, destination_blob_name):
#     storage_client = storage.Client(opt.project_name)
#     bucket = storage_client.get_bucket(opt.bucket_name)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_file(source_file)


# def create_custom_job_sample(project: str, display_name: str, container_image_uri: str, location: str = "us-central1", args=()):
#     custom_job = {
#         "display_name": display_name,
#         "job_spec": {
#             "worker_pool_specs": [
#                 {
#                     "machine_spec": {
#                         "machine_type": "e2-standard-4",
#                         # "machine_type": "a2-highgpu-1g",
#                         # "accelerator_type": aiplatform.gapic.AcceleratorType.NVIDIA_TESLA_A100,
#                         # "accelerator_count": 1,
#                     },
#                     "replica_count": 1,
#                     "container_spec": {
#                         "image_uri": container_image_uri,
#                         # "command": ["python train.py "],
#                         "args": args,
#                     },
#                 }
#             ]
#         },
#     }
#     parent = f"projects/{project}/locations/{location}"
#     response = client.create_custom_job(parent=parent, custom_job=custom_job)
#     print("response:", response)




# @app.post("/train")
# async def strarttraining(images_list: List[UploadFile] = File(...)):
#     user_id = uuid.uuid4()
#     blob_names = [str(user_id) + f'_img{i}' + os.path.splitext(img.filename)[1].lower() for i, img in enumerate(images_list)]
#     for i, (img, blob) in enumerate(zip(images_list, blob_names)):
#         write_image(img.file, blob)
#     args = ['--checkpoint-name ' + str(user_id) + 'checkpoint.ckpt',
#             '--imgs-list ' + ' '.join(blob_names)]
#     args = ["--checkpoint-name=sdaklfnljksdh.ckpt"]
#
#     print('args', args)
#     create_custom_job_sample(
#         project=opt.project_name,
#         display_name='train' + str(user_id),
#         container_image_uri='gcr.io/sd-concept-project/sd-concept-train-job:latest',
#         location="us-central1",
#         # api_endpoint="us-central1-aiplatform.googleapis.com",
#         args=args
#     )
#
#     return str(user_id)

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
