import numpy as np
import json


def random_input():
    objs = np.random.randint(1,100,(100,3))
    # breakpoint()
    with open("../resources/input.json", "w") as file:
        dic = {"input": objs.tolist()}
        json.dump(dic, file, indent=4)

if __name__=="__main__":
    random_input()