import ray
from ray import serve
from transformers import pipeline
from predict import Predictor

ray.init(address="auto", namespace="serve")
serve.start(detached=True)


@serve.deployment
class PredictorDeployent(Predictor):
    def __init__(self, path2checkpoint):
        super().__init__(path2checkpoint)

    def __call__(self, request):
        txt = request.query_params["txt"]
        predicted = super().__call__(txt)
        return predicted


PredictorDeployent.deploy('checkpoints')