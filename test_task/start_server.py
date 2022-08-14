import ray
from ray import serve
from predict import Predictor
from fastapi import FastAPI

app = FastAPI()
ray.init(address="auto", namespace="serve")
serve.start(detached=True)


@serve.deployment
@serve.ingress(app)
class PredictorDeployent(Predictor):
    def __init__(self, path2checkpoint):
        super().__init__(path2checkpoint)

    @app.get("/")
    def get(self, txt:str):
        predicted = self.predict(txt)
        return predicted

    @app.get("/max100")
    def get(self, txt: str):
        txt = txt[:100]
        predicted = self.predict(txt)
        return predicted



PredictorDeployent.deploy('checkpoints')