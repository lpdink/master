import struct
import numpy as np
import os
import logging
import datetime


def decode_idx3_ubyte(idx3_ubyte_file):
    with open(idx3_ubyte_file, "rb") as f:
        fb_data = f.read()

    offset = 0
    fmt_header = ">iiii"  # 以大端法读取4个 unsinged int32
    _, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, fb_data, offset)
    offset += struct.calcsize(fmt_header)
    fmt_image = ">" + str(num_rows * num_cols) + "B"
    images = np.empty((num_images, num_rows, num_cols))
    for i in range(num_images):
        im = struct.unpack_from(fmt_image, fb_data, offset)
        images[i] = np.array(im).reshape((num_rows, num_cols))
        offset += struct.calcsize(fmt_image)
    return images.astype(np.float32)  # [img_index, row, column] [10000, 28, 28]


def decode_idx1_ubyte(idx1_ubyte_file):
    with open(idx1_ubyte_file, "rb") as f:
        fb_data = f.read()

    offset = 0
    fmt_header = ">ii"  # 以大端法读取两个 unsinged int32
    _, label_num = struct.unpack_from(fmt_header, fb_data, offset)

    offset += struct.calcsize(fmt_header)
    labels = []

    fmt_label = ">B"  # 每次读取一个 byte
    for i in range(label_num):
        labels.append(struct.unpack_from(fmt_label, fb_data, offset)[0])
        offset += struct.calcsize(fmt_label)
    return np.array(labels).astype(np.int64)


def get_dataset(mnist_folder):
    file_names = [
        "train-images-idx3-ubyte",
        "train-labels-idx1-ubyte",
        "t10k-images-idx3-ubyte",
        "t10k-labels-idx1-ubyte",
    ]
    train_src_path, train_dst_path, test_src_path, test_dst_path = [
        os.path.join(mnist_folder, file_name) for file_name in file_names
    ]
    train_src = decode_idx3_ubyte(train_src_path)
    train_dst = decode_idx1_ubyte(train_dst_path)
    test_src = decode_idx3_ubyte(test_src_path)
    test_dst = decode_idx1_ubyte(test_dst_path)
    return train_src, train_dst, test_src, test_dst


LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../resources/log")
COLOR_DIC = {
    "ERROR": "31",
    "INFO": "37",
    "DEBUG": "34",
    "WARN": "33",
    "WARNING": "33",
    "CRITICAL": "35",
}


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt, use_color=False) -> None:
        super().__init__(fmt)
        self.use_color = use_color

    def format(self, record) -> str:
        color = COLOR_DIC[record.levelname]
        return (
            f"\033[{color}m{super().format(record)}\033[0m"
            if self.use_color
            else super().format(record)
        )


class Logger(logging.Logger):
    def __init__(self, name="log", level=0) -> None:
        super().__init__(name, level)
        stream_handler = logging.StreamHandler()
        fmt = "[%(asctime)s %(levelname)s %(pathname)s:%(lineno)d] %(message)s"
        color_formater = ColorFormatter(fmt, True)
        stream_handler.setFormatter(color_formater)
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_file_path = os.path.join(LOG_DIR, f"{now}.txt")
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_format = logging.Formatter(fmt)
        file_handler.setFormatter(file_format)
        self.addHandler(stream_handler)
        self.addHandler(file_handler)


logging = Logger()
