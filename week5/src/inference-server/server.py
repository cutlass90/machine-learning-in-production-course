import os
import pickle
import random
import subprocess
import time
from glob import glob
from shutil import rmtree
from typing import List

from google.cloud import storage

from config import opt
import redis


if os.path.isfile('secrets/sd-concept-project-14c11c803fff.json'):
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('secrets/sd-concept-project-14c11c803fff.json')
    storage_client = storage.Client(opt.project_name, credentials=credentials)
else:
    storage_client = storage.Client(opt.project_name)

results_bucket = storage_client.get_bucket(opt.results_bucket_name)
checkpoints_bucket = storage_client.get_bucket(opt.checkpoints_bucket_name)
r = redis.Redis(host=opt.host_ip, port=opt.redis_port, db=0)


def save_img_to_storage(blob_name, path2img):
    blob = results_bucket.blob(blob_name)
    blob.upload_from_filename(path2img)


def download_checkpoint(checkpoint, save_path):
    blob = checkpoints_bucket.blob(checkpoint)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    blob.download_to_filename(save_path)


def get_checkpoint(checkpoint: str):
    path2ckpt = os.path.join(opt.checkpoints_dir, checkpoint)
    if not os.path.isfile(path2ckpt):
        download_checkpoint(checkpoint, path2ckpt)
    return path2ckpt


def make_inference(checkpoint, prompt, n_images, outdir):
    checkpoint = get_checkpoint(checkpoint)
    command = ["python", "scripts/stable_txt2img.py", "--ddim_eta", "0.0", "--n_samples", "1", "--n_iter", str(n_images), "--scale", "7.0", "--ddim_steps", "50",
               "--ckpt", f"{checkpoint}", f"--prompt", f"\"{prompt}\"", f"--outdir", outdir, "--skip_grid", "--seed", str(random.randint(1, 9999999))]
    print(command)
    p = subprocess.Popen(command)
    p.wait()
    return glob(os.path.join(outdir, 'samples/*.jpg'))



def inference(checkpoint: str, prompt: str, imgs_names: List[str]):
    n_images = len(imgs_names)
    outdir = f"{opt.outdir}/{prompt[:100].replace(' ', '_') + str(random.randint(10000, 99999))}"
    img_paths = make_inference(checkpoint, prompt, n_images, outdir)
    for p, blob_name in zip(img_paths, imgs_names):
        save_img_to_storage(blob_name, p)
    rmtree(outdir, ignore_errors=True)

def main():
    print('inference server started')
    while True:
        if r.llen(opt.task_queue_name) > 0:
            task = r.lpop(opt.task_queue_name)
            task = pickle.loads(task)
            print('start task', task)
            inference(task['checkpoint_name'], task['prompt'], task['imgs_names'])
            r.set(task['taskid'], 'done')
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()
