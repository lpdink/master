from common import logging, hps, objfactory
from framework import BaseModel
import argparse

def train():
    objs = objfactory.create_objs(hps)
    mnist = objs.get("mnist")
    models = [model for model in objs.get_objs() if isinstance(model, BaseModel)]
    for model in models:
        model.train(mnist)


def infer():
    pass

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group() # 互斥组
    group.add_argument("-t", "--train", action="store_true")
    group.add_argument("-i", "--infer", action="store_true")
    args = parser.parse_args()
    if args.train:
        train()
    elif args.infer:
        infer()
    else:
        logging.warning("Run script with --train or --infer.")

    


if __name__=="__main__":
    main()