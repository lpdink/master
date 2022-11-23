# NLP大作业：基于Transformer的英译中机器翻译

这是笔者的NLP大作业。笔者并非NLP方向的，仅有一些深度学习基础，这里提供一个从零开始的“基于Transformer的英译中机器翻译”任务的笔记，可供新手参考。  

## 数据集

我们以“中文” “机器翻译” “数据集”作为关键词在搜索引擎或github搜索，很容易发现一个大小良好的数据集 [WMT18(108M)](http://data.statmt.org/wmt18/translation-task/training-parallel-nc-v13.tgz)，包含多种语料，我们只关心zh-en的，解压后大小约64M。

## 数据预处理

先打开中文的文件，发现：

- 有部分句子含有乱码，
- 包含了部分&开头的非中文字符，显然是爬虫没删干净。
- 有很多（）指向的特定名词，在英文中没有，这将干扰翻译模型的训练。

由于我们的训练数据很多，这里直接删除含有这三种case的语句(在中英文语料中同时删除)，代码在preprocess/clean.py。  
删除非法语句后，我们总共有227196条语句。  

## 预训练词向量

我们使用spacy预训练的词向量模型获取中英文词向量。  

### conda安装spacy

```sh
conda install -c conda-forge spacy
```

### 下载预训练模型

下载 [中英文预训练模型](https://github.com/explosion/spacy-models/releases)，spacy提供效率和精确度两种版本的预训练模型。但由于我们要使用词向量，这里不得不选择lg模型。  
官方推荐使用以下命令下载并安装：

```sh
python -m spacy download en_core_web_lg
python -m spacy download zh_core_web_lg
```

两个模型加起来大约有1GB左右，由于网络问题，我们选择科学上网，从github-release处下载两个模型:  
[英文模型](https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.4.1/en_core_web_lg-3.4.1-py3-none-any.whl)  
[中文模型](https://github.com/explosion/spacy-models/releases/download/zh_core_web_lg-3.4.0/zh_core_web_lg-3.4.0-py3-none-any.whl)  

### 安装预训练模型

```sh
# 这里虽然版本号不一样，但是没有影响.
pip install zh_core_web_lg-3.4.0-py3-none-any.whl
pip install en_core_web_lg-3.4.1-py3-none-any.whl
```

### 使用预训练模型获取词向量

```python
import spacy
nlp_en = spacy.load("en_core_web_lg")
nlp_zh = spacy.load("zh_core_web_lg")

# 两种方式
# 第一种
nlp_en.vocab.get_vector("apple")
# 第二种
zh_tokens = nlp_zh("唯一的归宿是安宁。")
zh_tokens[0].vector
```

对于oov字，据官方称将返回全0数组。  
spacy为我们提供的词向量的维度是300，我们的模型将根据这个维度搭建。  

### 词向量还原为单词

我们的模型将接受一组维度为300的单词，将他们翻译为另一组维度为300的单词，我们需要知道模型的翻译结果是哪些单词，所以需要将词向量解析为单词：

参考自 [mapping-word-vector-to-the-most-similar-closest-word-using-spacy](https://stackoverflow.com/questions/54717449/mapping-word-vector-to-the-most-similar-closest-word-using-spacy)

```python
# Imports
from scipy.spatial import distance
import spaCy

# Load the spacy vocabulary
nlp = spacy.load("en_core_web_lg")

# Format the input vector for use in the distance function
# In this case we will artificially create a word vector from a real word ("frog")
# but any derived word vector could be used
input_word = "frog"
p = np.array([nlp.vocab[input_word].vector])

# Format the vocabulary for use in the distance function
ids = [x for x in nlp.vocab.vectors.keys()]
vectors = [nlp.vocab.vectors[x] for x in ids]
vectors = np.array(vectors)

# *** Find the closest word below ***
closest_index = distance.cdist(p, vectors).argmin()
word_id = ids[closest_index]
output_word = nlp.vocab[word_id].text
# output_word is identical, or very close, to the input word
```

## 模型

TODO