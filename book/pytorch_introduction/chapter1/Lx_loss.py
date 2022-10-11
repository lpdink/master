# L1及L2损失
# L1损失是假定误差服从拉普拉斯分布
# L2损失是假定误差服从正态分布，
# MAE 是L1损失/N
# MSE 是L2损失/N
# ============================
# 对比
# L2损失函数	        L1损失函数
# 不是非常的鲁棒（robust）	鲁棒
# 稳定解	             不稳定解
# 总是一个解	         可能多个解
# 鲁棒意味着，L1损失函数对异常值较多，且需要被考虑的情况比较好。
import numpy as np


def l1_loss(y, y_hat):
    """

    Args:
        y (np.array): true label
        y_hat (np.array): predict result

    Returns:
        np.array: l1_loss
    """
    return np.sum(np.abs(y - y_hat))


def l2_loss(y, y_hat):
    # y与y_hat当然是同shape的
    # 写成np.sum((y-y_hat)*(y-y_hat))应该也一样？
    return np.dot((y - y_hat), (y - y_hat).T)


def mae_loss(y, y_hat):
    assert y.size == y_hat.size
    return 1 / y.size * (np.sum(np.abs(y - y_hat)))


def mse_loss(y, y_hat):
    assert y.size == y_hat.size
    return 1 / y.size * (np.dot((y - y_hat), (y - y_hat).T))


if __name__ == "__main__":
    y = np.arange(10)
    # random range(-1, 1)
    y_hat = np.arange(10) + 2 * (np.random.random(10) - 0.5)
    print(
        f"L1 loss: {l1_loss(y, y_hat)}\nMae loss: {mae_loss(y, y_hat)}\nL2 loss: {l2_loss(y, y_hat)}\nMse loss: {mse_loss(y, y_hat)}"
    )
