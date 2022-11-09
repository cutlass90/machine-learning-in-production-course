import os
import time
import requests
from glob import glob

import streamlit as st
from PIL import Image
from config import opt
from google.cloud import storage


if os.path.isfile('secrets/sd-concept-project-14c11c803fff.json'):
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('secrets/sd-concept-project-14c11c803fff.json')
    storage_client = storage.Client(opt.project_name, credentials=credentials)
else:
    storage_client = storage.Client(opt.project_name)
results_bucket = storage_client.get_bucket(opt.results_bucket_name)

def main():
    st.set_page_config(layout="wide")
    st.header('You Can Be Anyone You Want')
    st.image('static/a_portrait.png')
    concept_is_ready = False

    inference, train = st.tabs(["Generate personalized portraits", "Create your own Concept"])

    with inference:
        st.header("Here you can generate personalized image arts using created earlier Concept")

        concepts_list = requests.get(f'http://{opt.host_ip}:{opt.web_server_port}/get-concepts')
        concepts_list = [i[1:-1] for i in concepts_list.text[1:-1].split(',')]
        concept = st.selectbox('choose your concept to use', concepts_list)

        style = st.selectbox('choose style', [os.path.basename(s) for s in sorted(glob('prompts/*'))])
        prompt = open(os.path.join('prompts', style, 'prompt'), 'r').read()
        images = sorted(glob(os.path.join('prompts', style, '*/*.jpeg')))
        st.image(images, width=200)

        if st.button('generate'):
            st.text('Generating your personal arts. Wait a moment.')
            data = {'prompt': prompt, 'concept':concept}
            responce = requests.post(f'http://{opt.host_ip}:{opt.web_server_port}/generate-images', data=data)
            if responce.status_code == 200:
                blob_names = responce.text[1:-1]
                if blob_names == 'task failed':
                    st.text('Your task failed. Something goes wrong, try again later')
                else:
                    blob_names = [i[1:-1] for i in blob_names.split(',')]
                    for blob_name in blob_names:
                        blob = results_bucket.blob(blob_name)
                        img = blob.download_as_bytes()
                        st.image(img)

    with train:
        st.header("Here you can crate your own Concept and then use it to unlimited personalized arts generation.")
        st.text("Version 1.3")

        st.text('Upload 5 photos with your face. Note only one face per image is supported right now.')
        uploaded_photos = [None] * 5
        for i in range(5):
            uploaded_photos[i] = st.file_uploader(label=f'Upload your photo #{i + 1}', type=['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'], key=i)
            if uploaded_photos[i]:
                st.image(Image.open(uploaded_photos[i]), width=300)
        if all(uploaded_photos):
            if st.button(label='CREATE CONCEPT'):
                my_bar = st.progress(0)
                st.text(f'Your Concept creation is in progress. Wait until it finished (~ 1 hour)')
                st.text(f'Important. Do not close or reload this browser tab until the end.')

                files = [('images_list', (uploaded_photo.name, uploaded_photo.getvalue(), 'image/png')) for i, uploaded_photo in enumerate(uploaded_photos)]
                response = requests.post(f'http://{opt.host_ip}:8000/train', files=files)
                st.write(response)

                ph = st.empty()
                for i in range(3600):
                    st.write(response)
                    percent_complete = i / 3600
                    my_bar.progress(percent_complete)
                    time.sleep(1)
                    mm, ss = (3600 - i) // 60, (3600 - i) % 60
                    ph.metric("Yor concept will be ready in", f"{mm:02d}:{ss:02d}")
        if concept_is_ready:
            st.text('Congratulation! Your Concept is ready. Go to the "Generate personalized portraits" tab an try it')


if __name__ == '__main__':
    main()
