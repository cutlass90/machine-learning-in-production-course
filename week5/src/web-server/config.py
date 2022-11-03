from dataclasses import dataclass

DEBUG = True

@dataclass
class Config:
    #general
    project_name = 'sd-concept-project'
    checkpoints_bucket_name = 'sd-concept-checkpoints-storage'

    #training
    dataset = 'person'
    token = 'ozkhqjxiusldandvccv'
    training_images_folder = 'training_images'
    max_training_steps = 20 if DEBUG else 2000
    web_server_port = 8000
    bucket_name = 'sd-concept-checkpoints-storage'

    #inference
    inference_port = 8283
    n_samples = 1



opt = Config()