import requests
from config import opt

responce = requests.post(f'http://0.0.0.0:{opt.inference_port}', data={'user_id':'nazarshmatko', 'prompt':'a photo of nazarshmatko person', 'imgs_names': ['sdjiu3f.jpg']})

print(responce)