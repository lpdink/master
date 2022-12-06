from .base import BaseDataSet
from common import objfactory

@objfactory("dataset.cv.mnist")
class Mnist(BaseDataSet):
    def __init__(self, train_img_path, train_label_path, test_img_path, test_label_path) -> None:
        super().__init__()