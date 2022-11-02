from dataclasses import dataclass

DEBUG = True

@dataclass
class Config:
    outdir = 'outdir'
    project_name = 'sd-concept-project'
    bucket_name = 'sd-concept-checkpoints-storage'

    checkpoints_dir = 'checkpoints'


opt = Config()