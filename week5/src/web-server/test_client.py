import requests
from config import opt

# files = [('images_list', (f'img{i}.jpg', open('/home/nazar/DATASETS/images/nazar_photo_croped512/20220721_161526.jpg', 'rb'), 'image/png')) for i in range(5)]
# response = requests.post('http://0.0.0.0:8000/train', files=files)
# print(response)

def test_get_concepts():
    concepts_list = requests.get(f'http://0.0.0.0:{opt.web_server_port}/get-concepts')
    concepts_list = [i[1:-1] for i in concepts_list.text[1:-1].split(',')]
    assert 'nazarshmatkocheckpoint.ckpt' in concepts_list

def test_generate_images():
    prompt = 'a photo of nazarshmatko person'
    concept = 'nazarshmatkocheckpoint.ckpt'
    responce = requests.post(f'http://0.0.0.0:{opt.web_server_port}/generate-images', data={'prompt': prompt, 'checkpoint_name': concept})
    assert len(responce) > 0
    assert responce.status_code == 200
    responce = [i[1:-1] for i in responce.text[1:-1].split(',')]
    assert len(responce[0]) == 40
    assert responce[0][-4:] == '.jpg'

if __name__ == "__main__":
    test_get_concepts()
    # test_generate_images()