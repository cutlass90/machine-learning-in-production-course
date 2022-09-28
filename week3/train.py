import os

import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.utils import save_image, make_grid
from tqdm import tqdm

from src.networks import SimpleAE
from src.models import DDPM
from configs.mnist_v1 import opt
import wandb




def main():
    wandb.init(config = opt.__dict__)
    print(opt)
    os.makedirs(os.path.join(opt.checkpoint_dir, 'tf_logs'), exist_ok=True)
    os.makedirs(os.path.join(opt.checkpoint_dir, 'weights'), exist_ok=True)
    writer = SummaryWriter(os.path.join(opt.checkpoint_dir, 'tf_logs'))
    tf = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.0,), (1.0))]
    )
    dataset = MNIST("./data", train=True, download=True, transform=tf)
    dataloader = DataLoader(dataset, batch_size=opt.batch_size, shuffle=True, num_workers=0, drop_last=True)

    diffusor = SimpleAE(in_channels=1, filters=opt.filters).to(opt.device)
    ddpm = DDPM(diffusor=diffusor).to(opt.device)
    if opt.load_path:
        ddpm.load_state_dict(torch.load(opt.load_path))
        print(f'weights were loaded', opt.load_path)
    optim = torch.optim.Adam(ddpm.parameters(), lr=opt.lr)
    step = 0
    for i in range(opt.n_epoch):
        ddpm.train()
        for _, img in tqdm(enumerate(dataloader)):
            img = img[0].to(opt.device)
            loss = ddpm(img)
            optim.zero_grad()
            loss.backward()
            optim.step()
            if step % opt.log_freq == 0:
                writer.add_scalar('mse loss', loss.item(), step)
                wandb.log({"mse loss": loss.item()}, step=step)
                wandb.watch(diffusor)
                print(loss.item())
            if (step + 1) % opt.save_freq == 0:
                torch.save(ddpm.state_dict(), os.path.join(opt.checkpoint_dir, 'weights', 'latest.pth'))

            step += 1


        ddpm.eval()
        samples = ddpm.sample(16, (1, 28, 28))
        save_image(make_grid(samples, nrow=4, value_range=(-1, 1)), f"{opt.checkpoint_dir}/epoch{i}_sample.png")
        wandb.log({"generated images": wandb.Image(f"{opt.checkpoint_dir}/epoch{i}_sample.png")},
                  step=step)
        print()


if __name__ == "__main__":
    main()
