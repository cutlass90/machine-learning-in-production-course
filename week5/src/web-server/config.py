from dataclasses import dataclass

DEBUG = True

@dataclass
class Config:
    dataset = 'person'
    token = 'ozkhqjxiusldandvccv'
    training_images_folder = 'training_images'
    max_training_steps = 20 if DEBUG else 2000

    project_name = 'sd-concept-project'
    bucket_name = 'sd-concept-checkpoints-storage'


opt = Config()