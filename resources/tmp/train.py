import torch
import torch.nn as nn
import PIL
import os
import numpy as np

from torch.utils.data import Dataset, DataLoader
from domainbed.algorithms.algorithms import ERMStudent
from domainbed.datasets import get_dataset
from config import config
from log import logging

assert torch.cuda.is_available(), "GPU can't use!"
device = "cuda:0"
# device = "cpu"

model_save_path = "./resources/student_model"
if not os.path.isdir(model_save_path):
    os.makedirs(model_save_path)


class DisDataset(Dataset):
    def __init__(self, x, y, teacher_pred) -> None:
        self.x = x.to(device)
        self.y = y.to(device)
        self.teacher_pred = teacher_pred.to(device)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.x[idx, :, :, :], self.y[idx], self.teacher_pred[idx, :]


def train():
    input_shape = (3, 224, 224)
    num_classes = 7
    num_domines = 3
    batch_size = 32

    # step指喂入多少次batch_size大小的数据
    # 很少这样做，为了与本repo保持一致.
    total_steps = 5000
    save_steps = 1000

    model = ERMStudent(
        input_shape=input_shape,
        num_classes=num_classes,
        num_domains=num_domines,
        hparams=config.hparams,
    ).to(device)
    input_dataset = torch.load("./in_.pt")
    true_dataset = torch.load("./out_.pt")
    pred_dataset = torch.load("./pre_.pt")

    dis_dataset = DisDataset(input_dataset, true_dataset, pred_dataset)
    data_loader = DataLoader(dis_dataset, batch_size)

    step_idx = 0
    while True:
        for i_tensor, o_tensor, p_tensor in data_loader:
            loss = model.update(i_tensor, o_tensor, p_tensor)
            logging.info(f"{loss} at step {step_idx+1}")
            if (step_idx + 1) % save_steps == 0:
                save_path = os.path.join(model_save_path, f"S_ERM_{step_idx+1}.pt")
                torch.save(model.state_dict(), save_path)
                logging.warning(f"model save at {save_path}")
            step_idx += 1
            if step_idx > total_steps:
                break
        if step_idx > total_steps:
            break
    logging.warning("all work done.")
    # breakpoint()


if __name__ == "__main__":
    train()
