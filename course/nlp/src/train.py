import torch
import os
from copy import deepcopy
from dataset import CorpusData, TranslationData
from model import Transformer
from utils import config, zh_tokenizer, en_tokenizer, logging

class ScheduledOptim:
    # reference from https://github.com/jadore801120/attention-is-all-you-need-pytorch/blob/master/transformer/Optim.py
    '''A simple wrapper class for learning rate scheduling'''

    def __init__(self, optimizer, lr_mul, d_model, n_warmup_steps):
        self._optimizer = optimizer
        self.lr_mul = lr_mul
        self.d_model = d_model
        self.n_warmup_steps = n_warmup_steps
        self.n_steps = 0


    def step_and_update_lr(self):
        "Step with the inner optimizer"
        self._update_learning_rate()
        self._optimizer.step()


    def zero_grad(self):
        "Zero out the gradients with the inner optimizer"
        self._optimizer.zero_grad()


    def _get_lr_scale(self):
        d_model = self.d_model
        n_steps, n_warmup_steps = self.n_steps, self.n_warmup_steps
        return (d_model ** -0.5) * min(n_steps ** (-0.5), n_steps * n_warmup_steps ** (-1.5))


    def _update_learning_rate(self):
        ''' Learning rate scheduling per step '''

        self.n_steps += 1
        lr = self.lr_mul * self._get_lr_scale()

        for param_group in self._optimizer.param_groups:
            param_group['lr'] = lr

def accuracy(logits, y_true, PAD_IDX):
    """
    :param logits:  [tgt_len,batch_size,tgt_vocab_size]
    :param y_true:  [tgt_len,batch_size]
    :param PAD_IDX:
    :return:
    """
    y_pred = logits.transpose(0, 1).argmax(axis=2).reshape(-1)
    # 将 [tgt_len,batch_size,tgt_vocab_size] 转成 [batch_size, tgt_len,tgt_vocab_size]
    y_true = y_true.transpose(0, 1).reshape(-1)
    # 将 [tgt_len,batch_size] 转成 [batch_size， tgt_len]
    acc = y_pred.eq(y_true)  # 计算预测值与正确值比较的情况
    mask = torch.logical_not(y_true.eq(PAD_IDX))  # 找到真实标签中，mask位置的信息。 mask位置为FALSE，非mask位置为TRUE
    acc = acc.logical_and(mask)  # 去掉acc中mask的部分
    correct = acc.sum().item()
    total = mask.sum().item()
    return float(correct) / total, correct, total


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
    model = Transformer(len(en_vocab),len(zh_vocab),config).to(config.device)
    if os.path.isfile(config.model_path):
        paras = torch.load(config.model_path)
        model.load_state_dict(paras)
        logging.warning(f"load weights from {config.model_path}")
    loss_fn = torch.nn.CrossEntropyLoss(ignore_index=dataset.src_data_obj.get_id("<pad>"))
    optimizer = torch.optim.Adam(model.parameters(),
                                 lr=0.,
                                 betas=(config.beta1, config.beta2), eps=config.epsilon)
    lr_scheduler = ScheduledOptim(optimizer, 1, config.d_model, 4000)
    model.train()
    try:
        for epoch in range(config.epochs):
            losses = 0
            for idx, (src, dst) in enumerate(train_loader):
                src = src.to(config.device)
                dst = dst.to(config.device)
                dst_input = dst[:-1, :]
                # breakpoint()
                src_padding_mask, dst_padding_mask = dataset.get_padding_mask(src, dst_input)
                src_padding_mask.to(config.device)
                dst_padding_mask.to(config.device)
                dst_mask = torch.nn.Transformer.generate_square_subsequent_mask(dst_input.shape[0]).to(config.device)
                output = model(src, dst_input, dst_mask, src_padding_mask, dst_padding_mask)
                optimizer.zero_grad()
                dst_hat = dst[1:,:]
                loss = loss_fn(output.reshape(-1, len(zh_vocab)), dst_hat.reshape(-1))
                # breakpoint()
                # logging.info(output)
                # logging.info(output.shape)
                # logging.info(dst)
                # exit()
                loss.backward()
                lr_scheduler.step_and_update_lr()
                optimizer.step()
                acc, _, _ = accuracy(output, dst_hat, zh_corpus.get_id("<pad>"))
                losses += loss.item()
                logging.info(f"Epoch: {epoch}, Batch[{idx}/{len(train_loader)}], Train loss :{loss.item()}, acc:{acc}")
            if epoch % 5 == 0:
                state_dict = deepcopy(model.state_dict())
                # model_path = config.model_path#f"{config.model_path}_{epoch}"
                model_path = f"{config.model_path}_{epoch}"
                torch.save(state_dict, model_path)
    except KeyboardInterrupt:
        state_dict = deepcopy(model.state_dict())
        torch.save(state_dict, config.model_path)



    breakpoint()




if __name__=="__main__":
    main()