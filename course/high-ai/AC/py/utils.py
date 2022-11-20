import json
import os
import numpy as np
from functools import reduce

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


def get_config(config_path):
    with open(config_path, "r") as file:
        content = file.read()
    data = json.loads(content)
    return Config(**data)


config = get_config(CONFIG_PATH)

def abs_distance(dot1, dot2):
    x1, y1 = dot1
    x2, y2 = dot2
    return np.power((x1-x2)**2+(y1-y2)**2 , 0.5)

def get_path_length(path):
    # 计算path长度
    if len(path) in [0, 1]:
        return 0
    rst = 0
    for idx in range(len(path)-1):
        rst += abs_distance(path[idx], path[idx+1])
    return rst


if __name__ == "__main__":
    print(config)