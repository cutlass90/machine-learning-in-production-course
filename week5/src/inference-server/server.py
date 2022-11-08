import os
import random
import subprocess
from glob import glob
from shutil import rmtree
from typing import List

import uvicorn
from fastapi import FastAPI, File
from google.cloud import storage

from config import opt

app = FastAPI()
if os.path.isfile('secrets/sd-concept-project-14c11c803fff.json'):
    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('secrets/sd-concept-project-14c11c803fff.json')
    storage_client = storage.Client(opt.project_name, credentials=credentials)
else:
    storage_client = storage.Client(opt.project_name)
results_bucket = storage_client.get_bucket(opt.results_bucket_name)
checkpoints_bucket = storage_client.get_bucket(opt.checkpoints_bucket_name)


def save_img_to_storage(blob_name, path2img):
    blob = results_bucket.blob(blob_name)
    blob.upload_from_filename(path2img)


def download_checkpoint(user_id, save_path):
    blob = checkpoints_bucket.blob(user_id + 'checkpoint.ckpt')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    blob.download_to_filename(save_path)


def get_checkpoint(user_id: str):
    path2ckpt = os.path.join(opt.checkpoints_dir, user_id + 'checkpoint.ckpt')
    if not os.path.isfile(path2ckpt):
        download_checkpoint(user_id, path2ckpt)
    return path2ckpt


def make_inference(user_id, prompt, n_images, outdir):
    checkpoint = get_checkpoint(user_id)
    command = ["python", "scripts/stable_txt2img.py", "--ddim_eta", "0.0", "--n_samples", "1", "--n_iter", str(n_images), "--scale", "7.0", "--ddim_steps", "50",
               "--ckpt", f"{checkpoint}", f"--prompt", f"\"{prompt}\"", f"--outdir", outdir, "--skip_grid", "--seed", str(random.randint(1, 9999999))]
    print(command)
    p = subprocess.Popen(command)
    p.wait()
    return glob(os.path.join(outdir, 'samples/*.jpg'))


@app.post("/")
def inference(user_id: str = File(...), prompt: str = File(...), imgs_names: List[str] = File(...)):
    n_images = len(imgs_names)
    outdir = f"{opt.outdir}/{user_id}/{prompt[:100].replace(' ', '_') + str(random.randint(10000, 99999))}"
    img_paths = make_inference(user_id, prompt, n_images, outdir)
    for p, blob_name in zip(img_paths, imgs_names):
        save_img_to_storage(blob_name, p)
    rmtree(outdir, ignore_errors=True)


if __name__ == "__main__":
    uvicorn.run("server:app", host=f"{opt.host_ip}", port=opt.inference_port)
    # make_inference('nazarshmatko', 'a photo of nazarshmatko person', '2')
