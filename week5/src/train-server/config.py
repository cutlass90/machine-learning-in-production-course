from dataclasses import dataclass

@dataclass
class Config:
    dataset = 'person'
    token = 'ozkhqjxiusldandvccv'
    training_images_folder = 'training_images'
    max_training_steps = 2000

opt = Config()