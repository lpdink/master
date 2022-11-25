import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
from utils import config, logging


class CorpusData:
    """
    单一语种，训练数据不大，直接读到内存里
    """

    def __init__(self, file_path, tokenizer) -> None:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        # 构建词表
        symbols = ["<bos>", "<eos>", "<pad>", "<unk>"]
        word2id = {word: id for id, word in enumerate(symbols)}
        id2word = {id: word for id, word in enumerate(symbols)}
        split_sents = []
        max_words = 0
        logging.info(f"loading {file_path}")
        for line in tqdm(lines):
            line = line.strip()
            words = tokenizer(line)
            max_words = max(max_words, len(words))
            split_sents.append(words)
            for word in words:
                if word not in word2id.keys():
                    id = max(id2word.keys()) + 1
                    word2id[word] = id
                    id2word[id] = word
        self._word2id = word2id
        self._id2word = id2word
        self._split_sents = split_sents
        self._vocab = None
        self.max_words = max_words

    def get_word(self, id):
        return self._id2word.get(id, None)

    def get_id(self, word):
        return self._word2id.get(word, None)

    def get_vocab(self):
        if self._vocab is None:
            self._vocab = sorted(
                list(self._word2id.keys()), key=lambda word: self._word2id[word]
            )
        return self._vocab

    def __len__(self):
        return len(self._split_sents)

    def __getitem__(self, index):
        return self._split_sents[index]


class TranslationData:
    def __init__(self, src_data_obj, dst_data_obj) -> None:
        self.src_data_obj = src_data_obj
        self.dst_data_obj = dst_data_obj
        assert len(src_data_obj) == len(
            dst_data_obj
        ), f"src_data_obj len {len(src_data_obj)} not eq to dst_data_obj len {len(dst_data_obj)}"
        self._process_data()

    def _process_data(self):
        """
        将sents转id
        """
        train_data, test_data, valid_data = [], [], []
        sent_num = len(self.src_data_obj)
        index = 0
        for src_words, dst_words in tqdm(zip(self.src_data_obj, self.dst_data_obj),total=len(self.src_data_obj)):
            src_tensor = torch.tensor(
                [self.src_data_obj.get_id("<bos>")]
                + [self.src_data_obj.get_id(word) for word in src_words]
                + [self.src_data_obj.get_id("<eos>")]
                + [self.src_data_obj.get_id("<pad>")]
                * (self.src_data_obj.max_words - len(src_words))
            )
            dst_tensor = torch.tensor(
                [self.dst_data_obj.get_id("<bos>")]
                + [self.dst_data_obj.get_id(word) for word in dst_words]
                + [self.dst_data_obj.get_id("<eos>")]
                + [self.dst_data_obj.get_id("<pad>")]
                * (self.dst_data_obj.max_words - len(dst_words))
            )
            if (index / sent_num) < config.train_pert:
                train_data.append((src_tensor, dst_tensor))
            elif (index / sent_num) < config.train_pert + config.test_pert:
                test_data.append((src_tensor, dst_tensor))
            else:
                valid_data.append((src_tensor, dst_tensor))
            index += 1
        self.train_data = train_data
        self.test_data = test_data
        self.valid_data = valid_data

    def get_data(self):
        train_loader = DataLoader(
            self.train_data, batch_size=config.batch_size, shuffle=True
        )
        test_loader = DataLoader(
            self.test_data, batch_size=config.batch_size, shuffle=True
        )
        valid_loader = DataLoader(
            self.valid_data, batch_size=config.batch_size, shuffle=True
        )
        return train_loader, test_loader, valid_loader
