import requests

responce = requests.post('http://0.0.0.0:8283', data={'user_id':'nazarshmatko', 'prompt':'a photo of nazarshmatko person', 'imgs_names': ['img1.jpg', 'img2.jpg']})

print(responce)