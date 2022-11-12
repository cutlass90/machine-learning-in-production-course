import os
import pickle
import shutil
import subprocess
import time
from glob import glob
from typing import List

import redis
from config import opt
from google.cloud import storage

if os.path.isfile('secrets/sd-concept-project-14c11c803fff.json'):
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file('secrets/sd-concept-project-14c11c803fff.json')
    storage_client = storage.Client(opt.project_name, credentials=credentials)
else:
    storage_client = storage.Client(opt.project_name)

user_image_bucket = storage_client.get_bucket(opt.user_image_bucket_name)
checkpoints_bucket = storage_client.get_bucket(opt.checkpoints_bucket_name)
r = redis.Redis(host=opt.redis_ip, port=opt.redis_port, db=0)


def upload_user_photo(blob, save_path):
    blob = checkpoints_bucket.blob(blob)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    blob.download_to_filename(save_path)


def download_files():
    if not os.path.isfile('weights/model.ckpt'):
        os.makedirs('weights', exist_ok=True)
        import wget
        wget.download('https://dl.dropboxusercontent.com/s/vg2wojrw91b97a3/sd-v1-4.ckpt?dl=0', 'weights/model.ckpt')

    if not os.path.isdir(f'regularization_images/{opt.dataset}'):
        os.makedirs(f'regularization_images', exist_ok=True)
        p = subprocess.Popen(f"git clone https://github.com/djbielejeski/Stable-Diffusion-Regularization-Images-{opt.dataset}.git regularization_images".split(" "))
        p.wait()


def save_checkpoint_to_storage(last_checkpoint_file, checkpoint_path):
    blob = checkpoints_bucket.blob(checkpoint_path)
    blob.upload_from_filename(last_checkpoint_file, timeout=300)


def strarttraining(save_checkpoint_path_blob: str, user_imgs_blobs_list: List[str]):
    os.makedirs(opt.training_images_folder, exist_ok=True)
    for f in glob(os.path.join(opt.training_images_folder, '*')):
        os.remove(f)
    for i, f in enumerate(user_imgs_blobs_list):
        upload_user_photo(f, os.path.join(opt.training_images_folder, f'image{i}.jpg'))

    download_files()
    command = f"python main.py --base configs/stable-diffusion/v1-finetune_unfrozen.yaml -t --actual_resume weights/model.ckpt --reg_data_root regularization_images/{opt.dataset} -n project_name" + \
              f" --gpus 0, --data_root {opt.training_images_folder} --max_training_steps {opt.max_training_steps} --class_word person --token {opt.token} --no-test"
    print(command)
    p = subprocess.Popen(command.split(" "))
    p.wait()

    last_checkpoint_file = [p for p in glob(f"logs/*/checkpoints/last.ckpt")][0]

    save_checkpoint_to_storage(last_checkpoint_file, save_checkpoint_path_blob)

    shutil.rmtree("logs", ignore_errors=True)
    print('training has finished')


def main():
    print('train server started')
    while True:
        if r.llen(opt.train_queue_name) > 0:
            task = r.lpop(opt.train_queue_name)
            task = pickle.loads(task)
            print('start train task', task)
            strarttraining(task['save_checkpoint_path_blob'], task['user_imgs_blobs_list'])
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()
