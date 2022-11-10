import argparse
import os
import shutil
import subprocess
from glob import glob

from google.cloud import storage

from config import opt


def download_images_from_cloud(blob_name, save_dir):
    storage_client = storage.Client(opt.project_name)
    bucket = storage_client.get_bucket(opt.bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(os.path.join(save_dir, os.path.basename(blob.path)))


def save_checkpoint_to_storage(last_checkpoint_file, checkpoint_path):
    storage_client = storage.Client(opt.project_name)
    bucket = storage_client.get_bucket(opt.bucket_name)
    blob = bucket.blob(checkpoint_path)
    blob.upload_from_filename(last_checkpoint_file, timeout=300)


def download_files(dataset):
    if not os.path.isfile('weights/model.ckpt'):
        os.makedirs('weights', exist_ok=True)
        import wget
        wget.download('https://dl.dropboxusercontent.com/s/vg2wojrw91b97a3/sd-v1-4.ckpt?dl=0', 'weights/model.ckpt')

    if not os.path.isdir(f'regularization_images/{dataset}'):
        os.makedirs(f'regularization_images', exist_ok=True)
        p = subprocess.Popen(f"git clone https://github.com/djbielejeski/Stable-Diffusion-Regularization-Images-{dataset}.git regularization_images".split(" "))
        p.wait()


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--imgs-list', nargs='+', required=True)
    parser.add_argument('--checkpoint-name', type=str, required=True)
    parser.add_argument('--steps', type=int, default=opt.steps)
    parser.add_argument('--gpu_id', type=int, default=0)

    args = parser.parse_args()

    os.makedirs(opt.training_images_folder, exist_ok=True)
    for f in glob(os.path.join(opt.training_images_folder, '*')):
        os.remove(f)
    for i, f in enumerate(args.imgs_list):
        download_images_from_cloud(f, opt.training_images_folder)

    download_files(opt.dataset)
    command = f"python main.py --base configs/stable-diffusion/v1-finetune_unfrozen.yaml -t --actual_resume weights/model.ckpt --reg_data_root regularization_images/{opt.dataset} -n project_name" + \
              f" --gpus {args.gpu_id}, --data_root {opt.training_images_folder} --max_training_steps {args.steps} --class_word person --token {opt.token} --no-test"
    print(command)
    p = subprocess.Popen(command.split(" "))
    p.wait()

    last_checkpoint_file = [p for p in glob(f"logs/*/checkpoints/last.ckpt")][0]

    save_checkpoint_to_storage(last_checkpoint_file, args.checkpoint_name)

    shutil.rmtree("logs", ignore_errors=True)
    print('training has finished')


if __name__ == "__main__":
    main()
