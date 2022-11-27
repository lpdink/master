import torch
from model import Transformer
from utils import config, en_tokenizer, logging

def get_vocab(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().split('\n')
    return {word:id for id, word in enumerate(lines)}, {id:word for id, word in enumerate(lines)}

zh_word2id, zh_id2word = get_vocab("./zh_vocab")
en_word2id, en_id2word = get_vocab("./en_vocab")

def get_input_tensor(sent):
    words = en_tokenizer(sent)
    # words.insert(0, "<bos>")
    # words.append("<eos>")
    tensor = torch.tensor([en_word2id[word] for word in words])
    return tensor


def main():
    sents = "More broadly, Japanese companies have to organize for performance and discipline."
    input_tensor = get_input_tensor(sents)
    model = Transformer(len(en_word2id), len(zh_word2id),config)
    logging.info(f"Loading weights from {config.model_path}")
    paras = torch.load(config.model_path)
    model.load_state_dict(paras)
    output_tensor = model.infer(input_tensor, 1, zh_word2id["<eos>"], 50)
    print(output_tensor)
    breakpoint()

if __name__=="__main__":
    main()