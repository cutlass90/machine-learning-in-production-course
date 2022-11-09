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

    #network
    if os.environ.get('internal-url'): # k8s
        host_ip = os.environ['internal-url']
    elif os.path.isfile('/home/nazar/analyze_VGG.html'): #local
        host_ip = '0.0.0.0'
    else: #docker
        host_ip = "172.17.0.1"
    web_server_port = 8000
    redis_port = 8123

    #inference
    n_samples = 1
    outdir = 'outdir'
    checkpoints_dir = 'checkpoints'

    #redis
    task_queue_name = 'tasks_queue'



opt = Config()