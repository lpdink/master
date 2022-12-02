import torch
from model import Transformer
from utils import config, en_tokenizer, logging

def get_vocab(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.read().split('\n')
    return {word:id for id, word in enumerate(lines)}, {id:word for id, word in enumerate(lines)}

# zh_word2id, zh_id2word = get_vocab("/mnt/data/xiaozeyu/master/course/nlp/resources/zh_vocab")
# en_word2id, en_id2word = get_vocab("/mnt/data/xiaozeyu/master/course/nlp/resources/en_vocab")

zh_word2id, zh_id2word = get_vocab("./zh_vocab")
en_word2id, en_id2word = get_vocab("./en_vocab")

def get_input_tensor(sent):
    words = en_tokenizer(sent)
    # words.insert(0, "<bos>")
    # words.append("<eos>")
    tensor = torch.tensor([en_word2id[word] for word in words])
    return tensor

def load_model():
    model = Transformer(len(en_word2id), len(zh_word2id),config)
    logging.info(f"Loading weights from {config.model_path}")
    paras = torch.load("/mnt/data/xiaozeyu/master/course/nlp/resources/all_model/en2zh.pkl_10")
    model.load_state_dict(paras)
    return model

def infer_with_model(sents, model):
    input_tensor = get_input_tensor(sents)
    # print(input_tensor)
    output_tensor = model.infer(input_tensor, zh_word2id["<bos>"], zh_word2id["<eos>"], 50)
    # print(output_tensor)
    rst_sent = [zh_id2word[idx] for idx in output_tensor.reshape(-1).tolist()]
    rst_sent = "".join(rst_sent)
    print(rst_sent)


def main():
    model = load_model()
    # sent = "More broadly, Japanese companies have to organize for performance and discipline."
    # sent = "China apple Japan."
    # sent = "A Climate Deal is Not Enough"
    sents = [
        "More broadly, Japanese companies have to organize for performance and discipline.",
        "China apple Japan.",
        "A Climate Deal is Not Enough",
        "In many emerging markets, a lack of political freedom adds to the combustible mix.",
        "The combination of corruption, inequality, and political repression builds up enormous pressure, and there are no institutional channels through which to release it.",
        "But freer political regimes are not a panacea.",
        "In a democracy like India’s, the politically well-connected benefit from skewed growth, thus increasing the resentment of those left behind.",
        "The opportunity to “throw the rascals out” in each election cycle helps to let off some steam, but it does not resolve the problems that are generating it.",
        "It is difficult to predict what triggers popular protest, but economic factors are key.",
        "For example, rising food prices tend to hurt the poor, especially the urban poor, who spend a large share of their income on food; unlike agricultural workers, they receive none of the benefits of higher food prices."
    ]
    for sent in sents:
        infer_with_model(sent, model)
    breakpoint()

if __name__=="__main__":
    main()