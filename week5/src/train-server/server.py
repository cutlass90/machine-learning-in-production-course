import os
import random
import shutil
import subprocess
import time
from glob import glob
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile, Form

from config import opt

app = FastAPI()


def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    try:
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()


def download_files(dataset):
    if not os.path.isfile('weights/model.ckpt'):
        os.makedirs('weights', exist_ok=True)
        import wget
        wget.download('https://dl.dropboxusercontent.com/s/vg2wojrw91b97a3/sd-v1-4.ckpt?dl=0', 'weights/model.ckpt')

    if not os.path.isdir(f'regularization_images/{dataset}'):
        os.makedirs(f'regularization_images', exist_ok=True)
        p = subprocess.Popen(f"git clone https://github.com/djbielejeski/Stable-Diffusion-Regularization-Images-{dataset}.git regularization_images".split(" "))
        p.wait()


@app.post("/")
async def strarttraining(checkpoint_path: str = Form(...), images_list: List[UploadFile] = File(...)):
    print('checkpoint_path', checkpoint_path)
    project_name = 'project' + str(random.randint(10000, 99999))

    os.makedirs(opt.training_images_folder, exist_ok=True)
    for f in glob(os.path.join(opt.training_images_folder, '*')):
        os.remove(f)
    for i, f in enumerate(images_list):
        save_upload_file(f, os.path.join(opt.training_images_folder, f'image{i}.jpg'))

    time.sleep(20)


    # download_files(opt.dataset)
    # command = f"python main.py --base configs/stable-diffusion/v1-finetune_unfrozen.yaml -t --actual_resume weights/model.ckpt --reg_data_root regularization_images/{opt.dataset} -n project_name" + \
    #           f" --gpus 0, --data_root {opt.training_images_folder} --max_training_steps {opt.max_training_steps} --class_word person --token {opt.token} --no-test"
    # print(command)
    # p = subprocess.Popen(command.split(" "))
    # p.wait()
    #
    # l = [p for p in glob(f"logs/*/checkpoints/last.ckpt")]
    # last_checkpoint_file = [p for p in l if project_name in p][0]
    #
    # # save_checkpoint_to_storage(last_checkpoint_file, checkpoint_path)
    #
    # shutil.rmtree("logs", ignore_errors=True)
    # print('training has finished')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
