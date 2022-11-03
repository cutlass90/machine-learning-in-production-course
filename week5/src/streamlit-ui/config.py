from dataclasses import dataclass

DEBUG = True

@dataclass
class Config:
    # general
    project_name = 'sd-concept-project'
    results_bucket_name = 'sd-concept-results'
    web_server_port = 8000
    checkpoints_bucket_name = 'sd-concept-checkpoints-storage'


opt = Config()