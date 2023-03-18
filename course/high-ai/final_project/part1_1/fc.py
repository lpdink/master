import numpy as np
from copy import deepcopy
from utils import get_dataset, logging

train_src, train_dst, test_src, test_dst = get_dataset(
    "/home/lpdink/github/master/course/high-ai/final_project/part1/resources/mnist"
)


class MyLinear:
    def __init__(self, shape):
        self.weight = np.random.randn(*shape) * (2 / shape[0] ** 0.5)
        self.bias = np.zeros(shape[-1])
        self.weight_grad = None
        self.bias_grad = None

    def infer(self, x):
        tmp = np.dot(x, self.weight)
        tmp += self.bias
        return tmp

    def forward(self, x):
        self.x = x
        tmp = np.dot(x, self.weight)
        tmp += self.bias
        return tmp

    def backward(self, grad):
        batch_size = grad.shape[0]
        self.weight_grad = np.einsum("ji,jk->ik", self.x, grad) / batch_size
        self.bias_grad = np.einsum("i...->...", grad, optimize=True) / batch_size
        return np.einsum("ij,kj->ik", grad, self.weight, optimize=True)

    def step(self):
        lr = 0.0001
        self.weight.data -= lr * self.weight_grad
        self.bias.data -= lr * self.bias_grad


class MyRelu:
    def __init__(self) -> None:
        self.x = None

    def forward(self, x):
        self.x = x
        return np.maximum(0, x)

    def infer(self, x):
        return np.maximum(0, x)

    def backward(self, eta):
        eta[self.x < 0] = 0
        return eta

    def step(self):
        pass


def softmax(x):
    v = np.exp(x - x.max(axis=-1, keepdims=True))
    return v / v.sum(axis=-1, keepdims=True)


class MyModel:
    def __init__(self, hidden_nodes) -> None:
        self.layers = [
            MyLinear((28 * 28, hidden_nodes)),
            MyRelu(),
            MyLinear((hidden_nodes, 100)),
            MyRelu(),
            MyLinear((100, 10)),
        ]

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def infer(self, x):
        for layer in self.layers:
            x = layer.infer(x)
        return x

    def backward(self, grad):
        now_grad = deepcopy(grad)
        for layer in self.layers[::-1]:
            now_grad = layer.backward(now_grad)
        return now_grad

    def step(self):
        for layer in self.layers:
            layer.step()


def logloss(y_true, y_pred, eps=1e-15):
    p = np.clip(y_pred, eps, 1 - eps)
    loss = np.sum(-y_true * np.log(p) - (1 - y_true) * np.log(1 - p))

    return loss / len(y_true), softmax(y_pred) - y_true


def main():
    global train_src, train_dst
    train_dst_pad = np.zeros((len(train_dst), 10))
    for i in range(len(train_dst)):
        train_dst_pad[i][train_dst[i]] = 1
    epochs = 3
    batch_size = 128
    model = MyModel(1000)
    train_src = train_src.reshape(train_src.shape[0], -1)
    for epoch in range(epochs):
        i = 0
        while i <= len(train_dst) - batch_size:
            x = train_src[i : i + batch_size]
            y = train_dst_pad[i : i + batch_size]
            i += batch_size
            # breakpoint()
            output = model.forward(x)
            loss, grad = logloss(y, output)
            # breakpoint()
            model.backward(grad)
            model.step()
            # logging.info(f"epoch:{epoch}, loss:{loss}")
            test_acc = sum(
                model.infer(test_src.reshape(test_src.shape[0], -1)).argmax(1)
                == test_dst
            ) / len(test_dst)
            logging.info(f"epoch:{epoch}, loss:{loss}, acc:{test_acc}")
        # exit()


if __name__ == "__main__":
    main()
