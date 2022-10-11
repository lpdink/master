# 读取图像到[图像高，图像宽，通道]
# conda install Pillow
from functools import reduce
from PIL import Image
import numpy as np
import os

RAW_PATH = "./resources/img_raw"
PREPARED_PATH = "./resources/img_prepared"

TARGET_SIZE = (300, 300)
FILTER = Image.NEAREST


def resize_jpgs(dir_path=RAW_PATH):
    rst = []
    jpgs = [
        os.path.join(dir_path, file_path)
        for file_path in os.listdir(dir_path)
        if file_path.endswith(".jpg")
    ]
    for jpg_path in jpgs:
        im = Image.open(jpg_path)
        im = im.resize(TARGET_SIZE, FILTER)
        im.save(os.path.join(PREPARED_PATH, "prepared_" + os.path.basename(jpg_path)))
        im_np = np.array(im)
        # 在axis=0升一维，表示文件索引
        im_np = im_np.reshape(1, *im_np.shape)
        rst.append(im_np)
    # concatenate的开销恐怕很大，不知道是否有别的方法。
    return reduce(lambda a, b: np.concatenate((a, b)), rst)


if __name__ == "__main__":
    im_nps = resize_jpgs()
    print(im_nps.shape)
    breakpoint()
