import numpy as np
from copy import deepcopy
from utils import get_dataset, logging

train_src, train_dst, test_src, test_dst = get_dataset(
    "/home/lpdink/github/master/course/high-ai/final_project/part1/resources/mnist"
)


class MyLinear(object):
    def __init__(self, in_channel, out_channel, lr=0.001):
        self.weight = (np.random.randn(in_channel, out_channel) * 0.1).astype(
            np.float64
        )
        self.bias = np.zeros((out_channel,), dtype=np.float64)
        self.in_data = np.zeros((1, in_channel))
        self.out_data = None
        self.weight_grad = None
        self.bias_grad = None
        self.lr = lr

    def forward(self, data):
        self.in_data = data
        self.out_data = np.dot(data, self.weight) + self.bias
        return self.out_data

    def backward(self, grad):
        N = self.in_data.shape[0]
        data_grad = np.dot(grad, self.weight.T)  # 当前层的梯度
        self.weight_grad = np.dot(self.in_data.T, grad) / N  # 当前层权重的梯度
        self.bias_grad = np.sum(grad, axis=0) / N  # 当前层偏置的梯度
        return data_grad

    def step(self):
        self.weight += self.weight_grad * self.lr
        self.bias += self.bias_grad * self.lr


class MyRelu():
    def __init__(self) -> None:
        self.x=None

    def forward(self, x):
        self.x = x
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
        self.layers = [MyLinear(28 * 28, hidden_nodes), MyRelu(), MyLinear(hidden_nodes, 100), MyRelu(), MyLinear(100, 10)]

    def forward(self, x):
        for layer in self.layers:
            x=layer.forward(x)
        return x
    
    def backward(self, grad):
        now_grad = deepcopy(grad)
        for layer in self.layers[::-1]:
            now_grad=layer.backward(now_grad)
        return now_grad
    
    def step(self):
        for layer in self.layers:
            layer.step()
    
def logloss(y_true, y_pred, eps=1e-15):
    p = np.clip(y_pred, eps, 1-eps)
    loss = np.sum(- y_true * np.log(p) - (1 - y_true) * np.log(1-p))

    return loss / len(y_true), softmax(y_pred)-y_true

def main():
    global train_src, train_dst
    train_dst_pad = np.zeros((len(train_dst), 10))
    for i in range(len(train_dst)):
        train_dst_pad[i][train_dst[i]]=1
    epochs=500
    batch_size=12800
    model = MyModel(500)
    train_src = train_src.reshape(train_src.shape[0], -1)
    for epoch in range(epochs):
        i = 0
        while i <= len(train_dst) - batch_size:
            x = train_src[i:i+batch_size]
            y = train_dst_pad[i:i+batch_size]
            i += batch_size
            # breakpoint()
            output = model.forward(x)
            loss, grad = logloss(y, output)
            breakpoint()
            model.backward(grad)
            model.step()
        test_acc = sum(model.forward(test_src.reshape(test_src.shape[0],-1)).argmax(1)==test_dst)/len(test_dst)
        # breakpoint()
        logging.info(f"epoch:{epoch}, loss:{loss}, acc:{test_acc}")
        # exit()



if __name__=="__main__":
    main()
