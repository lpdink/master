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
                src = src.transpose(0, 1).to(config.device)
                dst = dst.transpose(0, 1).to(config.device)
                src_padding_mask, dst_padding_mask = dataset.get_padding_mask(src, dst)
                src_padding_mask.to(config.device)
                dst_padding_mask.to(config.device)
                dst_mask = torch.nn.Transformer.generate_square_subsequent_mask(dst.shape[0]).to(config.device)
                # breakpoint()
                output = model(src, dst, dst_mask, src_padding_mask, dst_padding_mask)
                optimizer.zero_grad()
                loss = loss_fn(output.reshape(-1, len(zh_vocab)), dst.reshape(-1))
                loss.backward()
                lr_scheduler.step_and_update_lr()
                optimizer.step()
                losses += loss.item()
                logging.info(f"Epoch: {epoch}, Batch[{idx}/{len(train_loader)}], Train loss :{loss.item()}")
            if epoch % 5 == 0:
                state_dict = deepcopy(model.state_dict())
                torch.save(state_dict, config.model_path)
    except KeyboardInterrupt:
        state_dict = deepcopy(model.state_dict())
        torch.save(state_dict, config.model_path)



    breakpoint()




if __name__=="__main__":
    main()