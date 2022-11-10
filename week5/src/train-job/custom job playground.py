from google.cloud import aiplatform
from config import opt
from typing import List

def custom_training_job_sample(
    project: str,
    location: str,
    bucket: str,
    display_name: str,
    container_uri: str,
    replica_count: int,
    command: List[str]
):
    aiplatform.init(project=project, location=location, staging_bucket=bucket)

    job = aiplatform.CustomContainerTrainingJob(
        display_name=display_name,
        container_uri=container_uri,
        command=command
    )

    model = job.run(
        replica_count=replica_count, machine_type=opt.machine_type, accelerator_type=opt.accelerator_type,
        accelerator_count=1, sync=True
    )

    return model


if __name__ == "__main__":
    custom_training_job_sample(project=opt.project_name,
                               location=opt.region,
                               bucket=opt.checkpoints_storage_url,
                               display_name='display_name_nazar',
                               container_uri=opt.training_container_uri,
                               replica_count=1,
                               command=["python", "train.py", "--checkpoint-name", "testcustomjob.ckpt", "--imgs-list", "1.jpg", "2.jpg", "3.jpg", "--steps", "20"])
