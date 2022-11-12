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
    user_email = st.text_input('Enter your email here', value='example@gmail.com')
    if st.button('Login'):
        st.session_state['user_email'] = user_email
    if st.session_state.get('user_email'):
        st.text(f"Welcome {st.session_state['user_email']}")

    inference, train = st.tabs(["Generate personalized portraits", "Create your own Concept"])

    with inference:
        st.header("Here you can generate personalized image arts using created earlier Concept")

        concepts_list = requests.get(f'http://{opt.web_server_ip}:{opt.web_server_port}/get-concepts')
        concepts_list = [i[1:-1] for i in concepts_list.text[1:-1].split(',')]
        concept = st.selectbox('choose your concept to use', concepts_list)

        style = st.selectbox('choose style', [os.path.basename(s) for s in sorted(glob('prompts/*'))])
        prompt = open(os.path.join('prompts', style, 'prompt'), 'r').read()
        images = sorted(glob(os.path.join('prompts', style, '*/*.jpeg')))
        st.image(images, width=200)

        if st.button('generate'):
            st.text('Generating your personal arts. Wait a moment.')
            data = {'prompt': prompt, 'concept':concept}
            responce = requests.post(f'http://{opt.web_server_ip}:{opt.web_server_port}/generate-images', data=data)
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

        st.text('Upload 5 photos with your face. Note only one face per image is supported right now.')
        uploaded_photos = st.file_uploader(label=f'Upload your photos', type=['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'], accept_multiple_files=True)
        if uploaded_photos:
            st.image([Image.open(i) for i in uploaded_photos], width=300)
        if uploaded_photos and st.session_state.get('user_email'):
            if st.button(label='CREATE CONCEPT'):
                my_bar = st.progress(0)
                st.text(f'Your Concept creation is in progress. Wait until it finished (~ 1 hour)')
                st.text(f'Important. Do not close or reload this browser tab until the end.')

                files = [('images_list', (uploaded_photo.name, uploaded_photo.getvalue(), 'image/png')) for i, uploaded_photo in enumerate(uploaded_photos)]
                response = requests.post(f'http://{opt.web_server_ip}:{opt.web_server_port}/train', files=files)
                st.write(response)
                if response.status_code == 200:
                    ph = st.empty()
                    for i in range(3600):
                        st.write(response)
                        percent_complete = i / 3600
                        my_bar.progress(percent_complete)
                        time.sleep(1)
                        mm, ss = (3600 - i) // 60, (3600 - i) % 60
                        ph.metric("Yor concept will be ready in", f"{mm:02d}:{ss:02d}")


if __name__ == '__main__':
    main()
