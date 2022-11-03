import requests

responce = requests.post('http://35.232.114.226', data={'user_id':'nazarshmatko', 'prompt':'a photo of nazarshmatko person', 'imgs_names': ['isdfsdfmg3.jpg', 'im3rsdfg4.jpg']})

print(responce)