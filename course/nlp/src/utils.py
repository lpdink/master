import json
import os
import logging
from torchtext.data.utils import get_tokenizer
from datetime import datetime

CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../resources/config.json"
)


class Config:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if type(v) == dict:
                v = Config(**v)
            if type(v) == list:
                for index, item in enumerate(v):
                    if type(item) == dict:
                        v[index] = Config(**item)
            self[k] = v

    def get(self, key, default=None):
        if key in self.__dict__.keys():
            return getattr(self, key)
        else:
            return default

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key):
        print(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __contains__(self, key):
        return key in self.__dict__

    def __repr__(self):
        return self.__dict__.__repr__()

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
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_file_path = os.path.join(LOG_DIR, f"{now}.txt")
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        file_format = logging.Formatter(fmt)
        file_handler.setFormatter(file_format)
        self.addHandler(stream_handler)
        self.addHandler(file_handler)


logging = Logger()


def get_config(config_path):
    with open(config_path, "r") as file:
        content = file.read()
    data = json.loads(content)
    return Config(**data)


config = get_config(CONFIG_PATH)
zh_tokenizer = get_tokenizer("spacy", "zh_core_web_sm")
en_tokenizer = get_tokenizer("spacy", "en_core_web_sm")


if __name__ == "__main__":
    print(config)