import os
import time
import requests
from glob import glob

import streamlit as st
from PIL import Image


def main():
    st.set_page_config(layout="wide")
    st.header('You Can Be Anyone You Want')
    st.image('static/a_portrait.png')
    concept_is_ready = False

    inference, train = st.tabs(["Generate personalized portraits", "Create your own Concept"])

    with inference:
        st.header("Here you can generate personalized image arts using created earlier Concept")

        concepts_list = ['concept1', 'concept2']
        concept = st.selectbox('choose your concept to use', concepts_list)

        style = st.selectbox('choose style', [os.path.basename(s) for s in sorted(glob('prompts/*'))])
        images = sorted(glob(os.path.join('prompts', style, '*/*.jpeg')))
        st.image(images, width=200)

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

                files = {'media': ('img', open('prompts/astronaut/einstein/e4ab357c9af988bf9f0b257242af19052e66026f032c20c10fbce1a1.jpeg', 'rb'))}
                response = requests.post('http://127.0.0.1:8000/train', files=files)
                print(response)


                ph = st.empty()
                for i in range(3600):
                    percent_complete = i / 3600
                    my_bar.progress(percent_complete)
                    time.sleep(1)
                    mm, ss = (3600 - i) // 60, (3600 - i) % 60
                    ph.metric("Yor concept will be ready in", f"{mm:02d}:{ss:02d}")
        if concept_is_ready:
            st.text('Congratulation! Your Concept is ready. Go to the "Generate personalized portraits" tab an try it')


if __name__ == '__main__':
    main()
