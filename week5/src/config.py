from dataclasses import dataclass
import os

DEBUG = True

@dataclass
class Config:

    #general
    debug = DEBUG
    project_name = 'sd-concept-project'
    region = 'us-central1'
    checkpoints_storage_url = 'gs://sd-concept-checkpoints-storage'

    #buckets
    checkpoints_bucket_name = 'sd-concept-checkpoints-storage'
    results_bucket_name = 'sd-concept-results'

    #training
    training_container_uri = 'gcr.io/sd-concept-project/sd-concept-train-job:latest'
    dataset = 'person'
    token = 'NazarShmatko'
    training_images_folder = 'training_images'
    max_training_steps = 20 if DEBUG else 2000
    machine_type = "a2-highgpu-1g"
    accelerator_type = "NVIDIA_TESLA_A100"

    #potrs
    host_ip = "172.17.0.1" if DEBUG else os.environ['internal-url']
    infer_host_ip = "172.17.0.1" if DEBUG else os.environ['inference-url']
    web_server_port = 8000
    inference_port = 8283

    #inference
    n_samples = 1
    outdir = 'outdir'
    checkpoints_dir = 'checkpoints'



opt = Config()