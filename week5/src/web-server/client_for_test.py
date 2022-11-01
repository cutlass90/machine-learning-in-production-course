import requests

files = [('images_list', (f'img{i}.jpg', open('/home/nazar/DATASETS/images/nazar_photo_croped512/20220721_161526.jpg', 'rb'), 'image/png')) for i in range(5)]
response = requests.post('http://0.0.0.0:8000/train', files=files)
print(response)