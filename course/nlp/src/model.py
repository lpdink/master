import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import config


class PositionalEncoding(nn.Module):
    # 参考自torch的example: https://github.com/pytorch/examples/blob/main/word_language_model/model.py
    r"""Inject some information about the relative or absolute position of the tokens in the sequence.
        The positional encodings have the same dimension as the embeddings, so that the two can be summed.
        Here, we use sine and cosine functions of different frequencies.
    .. math:
        \text{PosEncoder}(pos, 2i) = sin(pos/10000^(2i/d_model))
        \text{PosEncoder}(pos, 2i+1) = cos(pos/10000^(2i/d_model))
        \text{where pos is the word position and i is the embed idx)
    Args:
        d_model: the embed dim (required).
        dropout: the dropout value (default=0.1).
        max_len: the max. length of the incoming sequence (default=5000).
    Examples:
        >>> pos_encoder = PositionalEncoding(d_model)
    """

    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer("pe", pe)

    def forward(self, x):
        r"""Inputs of forward function
        Args:
            x: the sequence fed to the positional encoder model (required).
        Shape:
            x: [sequence length, batch size, embed dim]
            output: [sequence length, batch size, embed dim]
        Examples:
            >>> output = pos_encoder(x)
        """

        x = x + self.pe[: x.size(0), :]
        return self.dropout(x)


class Transformer(torch.nn.Module):
    def __init__(self, src_vocab_num, dst_vocab_num, config) -> None:
        super().__init__()
        self.transformer = torch.nn.Transformer(
            config.d_model,
            config.n_head,
            config.encoder_layers,
            config.decoder_layers,
            config.dim_feedforward,
            config.dropout,
        )
        self.pos_encoder = PositionalEncoding(config.d_model, config.dropout)
        self.encoder_embedding = nn.Embedding(src_vocab_num, config.d_model)
        self.decoder_embedding = nn.Embedding(dst_vocab_num, config.d_model)
        self.linear = nn.Linear(config.d_model, dst_vocab_num)

    def forward(self, src, dst, dst_mask, src_padding_mask, dst_padding_mask):
        """
        机器翻译任务的特性，源语言在推理时是完全可见的，无需padding
        """
        src = self.encoder_embedding(src)
        src = self.pos_encoder(src)
        dst = self.decoder_embedding(dst)
        dst = self.pos_encoder(dst)
        transformer_out = self.transformer(
            src,
            dst,
            tgt_mask=dst_mask,
            src_key_padding_mask=src_padding_mask,
            tgt_key_padding_mask=dst_padding_mask,
            memory_key_padding_mask=src_padding_mask
        )
        output = self.linear(transformer_out)

        return output

    def infer(self, src, start_id, end_id, max_len):
        self.eval()
        with torch.no_grad():
            src = src.reshape((-1, 1)) # batch=1
            src_embed = self.encoder_embedding(src)
            src_embed = self.pos_encoder(src_embed)
            encoder_out = self.transformer.encoder(src_embed)
            decoder_input = torch.ones((1,), dtype=torch.int).fill_(start_id)
            for _ in range(max_len):
                decoder_input = decoder_input.reshape(-1, 1)
                dst_embed = self.decoder_embedding(decoder_input)
                dst_embed = self.pos_encoder(dst_embed)
                # 取decoder的最后一位输出
                decoder_out = self.transformer.decoder(dst_embed, encoder_out)
                decoder_out = decoder_out[-1:]
                y_hat = torch.argmax(self.linear(decoder_out))
                # breakpoint()
                decoder_input = torch.concat((decoder_input, y_hat.unsqueeze(0).reshape(-1, 1)))
                if y_hat.item()==end_id:
                    break
        return decoder_input
