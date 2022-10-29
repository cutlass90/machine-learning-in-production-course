import os
import uuid
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile
from google.cloud import aiplatform
from google.cloud import storage

from config import opt


def write_image(source_file, destination_blob_name):
    storage_client = storage.Client(opt.project_name)
    bucket = storage_client.get_bucket(opt.bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(source_file)


def create_custom_job_sample(
        project: str,
        display_name: str,
        container_image_uri: str,
        location: str = "us-central1",
        api_endpoint: str = "us-central1-aiplatform.googleapis.com",
        args=[]
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.JobServiceClient(client_options=client_options)
    custom_job = {
        "display_name": display_name,
        "job_spec": {
            "worker_pool_specs": [
                {
                    "machine_spec": {
                        "machine_type": "a2-highgpu-1g",
                        "accelerator_type": aiplatform.gapic.AcceleratorType.NVIDIA_TESLA_A100,
                        "accelerator_count": 1,
                    },
                    "replica_count": 1,
                    "container_spec": {
                        "image_uri": container_image_uri,
                        "command": ["python train.py "],
                        "args": args,
                    },
                }
            ]
        },
    }
    parent = f"projects/{project}/locations/{location}"
    response = client.create_custom_job(parent=parent, custom_job=custom_job)
    print("response:", response)


app = FastAPI()


@app.post("/train")
async def strarttraining(images_list: List[UploadFile] = File(...)):
    user_id = uuid.uuid4()
    blob_names = [str(user_id) + f'_img{i}' + os.path.splitext(img.filename)[1].lower() for i, img in enumerate(images_list)]
    for i, (img, blob) in enumerate(zip(images_list, blob_names)):
        write_image(img.file, blob)
    args = ['--checkpoint-name', str(user_id) + 'checkpoint.ckpt', '--imgs-list'] + blob_names
    create_custom_job_sample(
        project=opt.project_name,
        display_name='train' + str(user_id),
        container_image_uri='gcr.io/sd-concept-project/sd-concept-train-job:latest',
        location="us-central1",
        api_endpoint="us-central1-aiplatform.googleapis.com",
        args=args
    )

    return str(user_id)


@app.get("/generate-image")
def generate_image(prompt_id):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
