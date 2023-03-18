import torch
import torch.nn as nn
import numpy as np
from utils import logging, get_dataset
from torch.utils.data import DataLoader

DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda:0"


class CNNModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)
        self.linear = nn.Linear(in_features=9216, out_features=128)
        self.output = nn.Linear(in_features=128, out_features=10)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = x.view(x.size(0), -1)
        x = torch.relu(self.linear(x))
        x = self.dropout2(x)
        x = self.output(x)
        return x


train_src, train_dst, test_src, test_dst = get_dataset(
    "/home/lpdink/github/master/course/high-ai/final_project/part1/resources/mnist"
)


class DataSet:
    def __init__(self, src, dst) -> None:
        self.src = src.reshape((-1, 1, 28, 28))
        self.dst = dst

    def __len__(self):
        return len(self.dst)

    def __getitem__(self, index):
        return (self.src[index], self.dst[index])


def main():
    train_dataset = DataSet(train_src, train_dst)
    test_dataset = DataSet(test_src, test_dst)
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    model = CNNModel().to(DEVICE)
    loss_fn = nn.CrossEntropyLoss().to(DEVICE)
    opt = torch.optim.Adam(params=model.parameters())
    epochs = 10
    model.train()
    for epoch in range(epochs):
        for src, dst in train_loader:
            src = src.to(DEVICE)
            dst = dst.to(DEVICE)
            output = model(src)
            loss = loss_fn(output, dst)
            opt.zero_grad()
            loss.backward()
            opt.step()
        logging.info(f"epoch:{epoch}  loss:{loss}")
        # eval
        model.eval()
        with torch.no_grad():
            test_output = model(torch.tensor(test_dataset.src).to(DEVICE))
            acc = np.sum(test_output.argmax(1).tolist() == test_dataset.dst) / len(
                test_dataset
            )
            logging.info(f"测试集准确率:{acc}")
        model.train()


if __name__ == "__main__":
    main()
