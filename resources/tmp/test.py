# 对比学生模型和4号模型在4号训练集上的表现
import torch
import torch.nn as nn
import PIL
import os
import numpy as np

# model
from domainbed.algorithms.algorithms import ERM, ERMStudent
from domainbed.datasets import get_dataset
from config import config
from log import logging


data_set_idx = 3  # 四号数据集
assert torch.cuda.is_available()
device = "cuda:0"


def test():
    test_envs = [data_set_idx]
    dataset, in_splits, out_splits = get_dataset(
        test_envs, config.args, config.hparams, ERM
    )
    dataset_1 = in_splits[data_set_idx][0]
    dataset_2 = out_splits[data_set_idx][0]

    batch_input_tensor_1 = [dataset_1[idx]["x"] for idx in range(len(dataset_1.keys))]
    batch_input_tensor_2 = [dataset_2[idx]["x"] for idx in range(len(dataset_2.keys))]
    batch_input_tensor = batch_input_tensor_1 + batch_input_tensor_2
    batch_input_tensor = torch.stack(batch_input_tensor, 0).to(device)
    true_batch_1 = [dataset_1[idx]["y"] for idx in range(len(dataset_1.keys))]
    true_batch_2 = [dataset_2[idx]["y"] for idx in range(len(dataset_2.keys))]
    true_batch = torch.tensor(true_batch_1 + true_batch_2).to(device)
    # breakpoint()
    for loop_idx in ["1000", "2000", "3000", "4000", "5000"]:
        t_model_path = f"/home/zhidan/zhidan/codes_Distill/train_output/PACS/230301_09-43-01_exp_name/checkpoints/TE3_{loop_idx}.pth"

        t_model = ERM(
            dataset.input_shape,
            dataset.num_classes,
            num_domains=3,
            hparams=config.hparams,
        ).to(device)
        ckpt = torch.load(t_model_path)
        t_model.load_state_dict(ckpt["model_dict"])
        t_model.eval()
        with torch.no_grad():
            # breakpoint()
            i_batches = batch_input_tensor.chunk(100, dim=0)
            o_batches = true_batch.chunk(100, dim=0)
            point = 0
            for i_batch, o_batch in zip(i_batches, o_batches):
                predict_rst = t_model.predict(i_batch)
                # breakpoint()
                point += sum(predict_rst.argmax(1) == o_batch).item()
            logging.warning(
                f"step:{loop_idx} T-model 准确率：{point/len(true_batch)}  point:{point} in {len(true_batch)}"
            )

        s_model = ERMStudent(
            dataset.input_shape,
            dataset.num_classes,
            num_domains=3,
            hparams=config.hparams,
        ).to(device)
        s_model_path = f"/home/zhidan/xiaozeyu/zhou_project/miro/resources/student_model/S_ERM_{loop_idx}.pt"

        s_model.load_state_dict(torch.load(s_model_path))
        s_model.eval()
        with torch.no_grad():
            i_batches = batch_input_tensor.chunk(100, dim=0)
            o_batches = true_batch.chunk(100, dim=0)
            point = 0
            for i_batch, o_batch in zip(i_batches, o_batches):
                predict_rst = s_model.predict(i_batch)
                point += sum(predict_rst.argmax(1) == o_batch).item()
            logging.warning(
                f"step:{loop_idx} S-model 准确率：{point/len(true_batch)}  point:{point} in {len(true_batch)}"
            )


if __name__ == "__main__":
    test()
