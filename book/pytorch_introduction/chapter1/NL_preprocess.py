# 中文分词的常见方法是THULAC和Jieba
# 本P演示英文的word to vec过程。(使用Numpy 正态分布)
from math import sqrt
import numpy as np

with open("./resources/text.txt", encoding="utf-8") as file:
    TEXT = file.read()
    TEXT = (
        TEXT.replace(",", "")
        .replace("′", "")
        .replace("?", "")
        .replace("(", "")
        .replace(")", "")
        .replace('"', "")
    )


def get_word_vec(word_bag):
    # 有n个单词，每个单词对应m长度的向量，n与m的关系，依照经验满足：m的大小与n的四次方根成正比，比例系数1-10，且为2的整数次方
    n = len(word_bag)  # n=117，四次方根约等于3.2，取8作为m的长度
    m = 8
    word2vec = np.random.normal(size=(n, m)).tolist()
    word2vec = {word: vec for word, vec in zip(word_bag, word2vec)}
    return word2vec


if __name__ == "__main__":
    word_bag = list({word for lines in TEXT.split("\n") for word in lines.split()})
    word2vec = get_word_vec(word_bag)
    print(word2vec)
    breakpoint()
