from dataclasses import dataclass
import os


@dataclass
class Config:

    #general
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
    max_training_steps = 2000
    machine_type = "a2-highgpu-1g"
    accelerator_type = "NVIDIA_TESLA_A100"

    #potrs
    host_ip = os.environ['internal-url'] if os.environ.get('internal-url') else "172.17.0.1"
    infer_host_ip = os.environ['inference-url'] if os.environ.get('inference-url') else "172.17.0.1"
    web_server_port = 8000
    inference_port = 8283

    #inference
    n_samples = 1
    outdir = 'outdir'
    checkpoints_dir = 'checkpoints'



opt = Config()