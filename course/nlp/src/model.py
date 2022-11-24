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
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

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

        x = x + self.pe[:x.size(0), :]
        return self.dropout(x)


class Transformer(torch.nn.Module):
    def __init__(self, config) -> None:
        super().__init__()
        self.transformer = torch.nn.Transformer(config.d_model, config.nhead, config.encoder_layers, config.decoder_layers, config.dim_feedforward, config.dropout)
        self.decoder_mask = torch.nn.Transformer.generate_square_subsequent_mask(config.seq_length)
        self.pos_encoder = PositionalEncoding(config.d_model, config.dropout, config.seq_length)

    def forward(self, src, tgt, encoder_mask):
        """
            src: encoder输入，源语言序列，[sequence length, batch size, embed dim]
            tgt: decoder输入，目标语言序列，[sequence length, batch size, embed dim]
            src输入被padding到256，以便放入定长的tensor，对padding部分，进行-inf掩码
            tgt总是concat一个全0向量作为开始，再进行掩码
        """
        src = self.pos_encoder(src)
        return self.transformer(src, tgt, src_key_padding_mask=encoder_mask, tgt_key_padding_mask=self.decoder_mask)

    def infer(self):
        return 
