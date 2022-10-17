import os

import streamlit as st
import subprocess
from datetime import datetime
from shutil import copyfile
from glob import glob
import random

DEVICE = 'cuda:0'

def download_files(dataset):
    if not os.path.isfile('weights/model.ckpt'):
        os.makedirs('weights', exist_ok=True)
        import wget
        wget.download('https://dl.dropboxusercontent.com/s/vg2wojrw91b97a3/sd-v1-4.ckpt?dl=0', 'weights/model.ckpt')


    if not os.path.isdir(f'regularization_images/{dataset}'):
        os.makedirs(f'regularization_images', exist_ok=True)
        p = subprocess.Popen(f"git clone https://github.com/djbielejeski/Stable-Diffusion-Regularization-Images-{dataset}.git regularization_images".split(" "))
        p.wait()

def save_uploadedfile(uploadedfile, path2save):
    with open(os.path.join(path2save, uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File:{uploadedfile.name} to {path2save}")


def main():

    os.makedirs('trained_models', exist_ok=True)
    st.header('You Can Be Anyone You Want')
    st.image('static/a_portrait.png')

    project_name = st.text_input('project name', value='superhero_project') + str(random.randint(10000, 99999))
    if not st.session_state.get('project_name', False):
        st.session_state['project_name'] = project_name
    training_images_folder = os.path.join('training_images', st.session_state['project_name'])
    os.makedirs(training_images_folder, exist_ok=True)
    class_word = st.selectbox(
        'What do you describe best',
        ('person', 'man', 'woman'))
    token = st.text_input('your name', value='AlbertEinstein').replace(' ', '').replace('-', '').replace('_', '')
    max_training_steps = st.number_input('number of training steps', min_value=1, max_value=100000, value=2000, step=100)
    dataset = st.selectbox(
        'Dataset for regularization images. Leave it unchanged if you dont know what it is',
        ("person_ddim", "man_euler", "man_unsplash", "woman_ddim", "blonde_woman"))

    st.text('Upload up to 5 photos with your face and push START TRAINING button. Note only one face per image is supported right now.')
    uploaded_files = st.file_uploader(label='face_images', type=['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG'], accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        save_uploadedfile(uploaded_file, training_images_folder)
        st.image(os.path.join(training_images_folder, uploaded_file.name))

    if not st.session_state.get('is_training_finished'):
        if st.button(label='START TRAINING'):
            st.text(f'Training concept {token} is in progress. Wait until it finished (~ 1 hour)')
            st.text(f'Do not close this browser tab')

            download_files(dataset)
            command = f"python main.py --base configs/stable-diffusion/v1-finetune_unfrozen.yaml -t --actual_resume weights/model.ckpt --reg_data_root regularization_images/{dataset} -n {st.session_state['project_name']}" + \
                      f" --gpus 0, --data_root {training_images_folder} --max_training_steps {max_training_steps} --class_word {class_word} --token {token} --no-test"
            print(command)
            p = subprocess.Popen(command.split(" "))
            p.wait()

            st.session_state.is_training_finished = True
            st.experimental_rerun()
    else:
        st.text(f'Training concept {token} is finished! Download it below.')

        # datetime object containing current date and time
        dt_string = datetime.now().strftime("%d_%m_%YT%H_%M_%S")
        file_name = dt_string + "_" + st.session_state['project_name'] + "_" + str(
            max_training_steps) + "_max_training_steps_" + token + "_token_" + class_word + "_class_word.ckpt"
        file_name = file_name.replace(" ", "_")
        l = [p for p in glob(f"logs/*/checkpoints/last.ckpt")]
        last_checkpoint_file = [p for p in l if st.session_state['project_name'] in p][0]
        copyfile(last_checkpoint_file, f"trained_models/{file_name}")


        with open(f"trained_models/{file_name}", 'rb') as f:
            st.download_button(f'Download {token} concept', f, file_name=f"trained_models/{file_name}")










if __name__ == '__main__':
    main()
