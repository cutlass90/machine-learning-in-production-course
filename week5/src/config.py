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
    user_image_bucket_name = 'sd-concept-user-image'

    #training
    training_container_uri = 'gcr.io/sd-concept-project/sd-concept-train-job:latest'
    dataset = 'person_ddim'
    token = 'NazarShmatko'
    training_images_folder = 'training_images'
    steps = 2000
    machine_type = "a2-highgpu-1g"
    accelerator_type = "NVIDIA_TESLA_A100"

    #network
    if os.environ.get('redis-server-ip'): # k8s
        redis_ip = os.environ['redis-server-ip']
    elif os.path.isfile('/home/nazar/analyze_VGG.html'): #local
        redis_ip = '0.0.0.0'
    else: #docker
        redis_ip = "172.17.0.1"

    if os.environ.get('web-server-ip'): # k8s
        web_server_ip = os.environ['web-server-ip']
    elif os.path.isfile('/home/nazar/analyze_VGG.html'): #local
        web_server_ip = '0.0.0.0'
    else: #docker
        web_server_ip = "172.17.0.1"

    web_server_port = 8000
    redis_port = 6379

    #inference
    n_samples = 5
    outdir = 'outdir'
    checkpoints_dir = 'checkpoints'

    #redis
    task_queue_name = 'inference_tasks_queue' # uses for inference tasks
    train_queue_name = 'train_tasks_queue' # uses for training tasks



opt = Config()