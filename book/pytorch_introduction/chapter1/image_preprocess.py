# 读取图像到[图像高，图像宽，通道]
# conda install Pillow
# 对hsv改变幅度，且不超出范围，以进行数据增强。
from functools import reduce
from PIL import Image
import numpy as np
import os
import random

RAW_PATH = "./resources/img_raw"
PREPARED_PATH = "./resources/img_prepared"

TARGET_SIZE = (300, 300)
FILTER = Image.NEAREST

# 是否进行增强
ENHANCE = True
RANDOM_RANGE = 0.5 # 增强10%


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
        if ENHANCE:
            im_hsv = im.convert("HSV")
            width, height = im_hsv.size
            pixel_map = im_hsv.load()
            for w in range(width):
                for h in range(height):
                    pix_h, pix_s, pix_v = im_hsv.getpixel((w, h))
                    pixel_map[w, h] = (int(min(pix_h*(1+RANDOM_RANGE), 255)), 
                                        int(min(pix_s*(1+RANDOM_RANGE), 255)),
                                        int(min(pix_v*(1+RANDOM_RANGE), 255)))
            im = im_hsv.convert("RGB")
                    
        """
        在opencv中的范围如下，但在PIL中，H似乎也是255的。
        H = [0,179]
        L = [0,255]
        S = [0,255]

        H = [0,179]
        S = [0,255]
        V = [0,255]
        """
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
