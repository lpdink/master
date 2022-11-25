import torch
from dataset import CorpusData, TranslationData
from utils import config, zh_tokenizer, en_tokenizer

def main():
    zh_corpus = CorpusData(config.zh_path, zh_tokenizer)
    en_corpus = CorpusData(config.en_path, en_tokenizer)
    dataset = TranslationData(en_corpus, zh_corpus)
    train_loader, test_loader, valid_loader = dataset.get_data()
    zh_vocab = zh_corpus.get_vocab()
    en_vocab = en_corpus.get_vocab()
    with open("./zh_vocab", "w", encoding="utf-8") as file:
        file.write("\n".join(zh_vocab))
    with open("./en_vocab", "w", encoding="utf-8") as file:
        file.write("\n".join(en_vocab))
    breakpoint()




if __name__=="__main__":
    main()