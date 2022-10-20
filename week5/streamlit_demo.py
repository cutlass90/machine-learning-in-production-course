import os

import streamlit as st
import subprocess
from datetime import datetime
from shutil import copyfile
from glob import glob
import random
from PIL import Image

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
    trained_models_folder = 'trained_models'
    os.makedirs(trained_models_folder, exist_ok=True)
    st.set_page_config(layout="wide")
    st.header('You Can Be Anyone You Want')
    st.image('static/a_portrait.png')

    train, inference = st.tabs(["Create your own Concept", "Generate personalized portraits"])

    with train:
        st.header("Here you can crate your own Concept and then use it to unlimited personalized arts generation.")
        st.text("Version 1.2")

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
            st.image(os.path.join(training_images_folder, uploaded_file.name), width=400)

        if glob(os.path.join(training_images_folder, '*.*')): # if user upload images then draw "create concept" button
            if st.button(label='CREATE CONCEPT'):
                st.text(f'Creating Concept {token} is in progress. Wait until it finished (~ 1 hour)')
                st.text(f'Do not close this browser tab')
                with st.spinner('Creating...'):
                    download_files(dataset)
                    command = f"python main.py --base configs/stable-diffusion/v1-finetune_unfrozen.yaml -t --actual_resume weights/model.ckpt --reg_data_root regularization_images/{dataset} -n {st.session_state['project_name']}" + \
                              f" --gpus 0, --data_root {training_images_folder} --max_training_steps {max_training_steps} --class_word {class_word} --token {token} --no-test"
                    print(command)
                    p = subprocess.Popen(command.split(" "))
                    p.wait()

                    st.session_state.is_training_finished = True
                st.success('Done!')

                st.text(f'Training concept {token} is finished! Download it below.')

                # datetime object containing current date and time
                dt_string = datetime.now().strftime("%d_%m_%YT%H_%M_%S")
                file_name = dt_string + "_" + st.session_state['project_name'] + "_" + str(
                    max_training_steps) + "_max_training_steps_" + token + "_token_" + class_word + "_class_word.ckpt"
                file_name = file_name.replace(" ", "_")
                l = [p for p in glob(f"logs/*/checkpoints/last.ckpt")]
                last_checkpoint_file = [p for p in l if st.session_state['project_name'] in p][0]
                copyfile(last_checkpoint_file, f"{trained_models_folder}/{file_name}")

                with open(f"{trained_models_folder}/{file_name}", 'rb') as f:
                    st.download_button(f'Download {token} concept', f, file_name=f"{trained_models_folder}/{file_name}")

    with inference:
        COL_N = 5
        st.header("Here you can generate personalized image arts using created earlier Concept")

        st.text('Have your Concept locally? Upload it!')
        uploaded_file = st.file_uploader(label='Upload Concept', type=['ckpt'], accept_multiple_files=False, )
        if uploaded_file:
            save_uploadedfile(uploaded_file, trained_models_folder)

        checkpoints = sorted(glob(f'{trained_models_folder}/*.ckpt'))
        if checkpoints:
            checkpoint = st.selectbox(
                'Select your Concept',
                checkpoints)
            token = os.path.basename(checkpoint).split('_token_')[0].split('_max_training_steps_')[1]
            class_word = os.path.basename(checkpoint).split('_class_word.ckpt')[0].split('_token_')[1]



        prompt = st.text_input("Enter your text prompt here", value=f"{token} {class_word} as a masterpiece portrait painting by John Singer Sargent in the style of Rembrandt")



        outdir = 'outputs'
        if st.button(label='GENERATE'):
            with st.spinner('Generaiting...'):
                command = ["python", "scripts/stable_txt2img.py", "--ddim_eta", "0.0", "--n_samples", "1", "--n_iter", "10", "--scale", "7.0", "--ddim_steps", "50",
                           "--ckpt", f"{checkpoint}", f"--prompt", f"\"{prompt}\"", f"--outdir", f"{outdir}/{prompt[:100].replace(' ', '_') + str(random.randint(10000, 99999))}"]
                p = subprocess.Popen(command)
                p.wait()
            st.success('Done!')

        out_dirs = sorted(glob(f'{outdir}/*'), key=lambda x: os.path.getmtime(x), reverse=True)
        if out_dirs:
            out_dir = st.selectbox(
                'select results to view',
                out_dirs)
            images = glob(os.path.join(out_dir, '*.png'))
            columns = st.columns(COL_N)

            for i, img in enumerate(images):
                columns[i%COL_N].image(Image.open(img))






if __name__ == '__main__':
    main()
