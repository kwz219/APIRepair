import torch.nn as nn
import torch
from Models.Encoder import EncoderBase, TransformerEncoderLayer
from Models.Util.Pos_ffn import ActivationFunction
from Models.Util.misc import sequence_mask


class TokenCLSModel(EncoderBase):
    """Transformer Encoder用于token classification
    Args:
        num_layers (int): number of encoder layers
        d_model (int): size of the model
        heads (int): number of heads
        d_ff (int): size of the inner FF layer
        dropout (float): dropout parameters
        embeddings (onmt.modules.Embeddings):
          embeddings to use, should have positional encodings
        pos_ffn_activation_fn (ActivationFunction):
            activation function choice for PositionwiseFeedForward layer
    Returns:
        (torch.FloatTensor, torch.FloatTensor):
        * embeddings ``(src_len, batch_size, model_dim)``
        * memory_bank ``(src_len, batch_size, model_dim)``
    """

    def __init__(self, num_layers, d_model, heads, d_ff, dropout,
                 attention_dropout, embeddings, max_relative_positions,
                 n_labels,pos_ffn_activation_fn=ActivationFunction.relu):
        super(TokenCLSModel, self).__init__()

        self.embeddings = embeddings
        self.transformer = nn.ModuleList(
            [TransformerEncoderLayer(
                d_model, heads, d_ff, dropout, attention_dropout,
                max_relative_positions=max_relative_positions,
                pos_ffn_activation_fn=pos_ffn_activation_fn)
             for i in range(num_layers)])
        self.layer_norm = nn.LayerNorm(d_model, eps=1e-6)
        # layers to classify
        self.n_labels=n_labels
        self.linear = nn.Linear(d_model, n_labels)


    @classmethod
    def from_opt(cls, opt, embeddings):
        """Alternate constructor."""
        return cls(
            opt.enc_layers,
            opt.enc_rnn_size,
            opt.heads,
            opt.transformer_ff,
            opt.dropout[0] if type(opt.dropout) is list else opt.dropout,
            opt.attention_dropout[0] if type(opt.attention_dropout)
            is list else opt.attention_dropout,
            embeddings,
            opt.max_relative_positions,
            opt.n_labels,
            pos_ffn_activation_fn=ActivationFunction.relu,
        )

    def forward(self, src, lengths=None):
        """See :func:`EncoderBase.forward()`"""
        src=src.transpose(0,1)
        self._check_args(src, lengths)

        emb = self.embeddings(src)

        out = emb.transpose(0, 1).contiguous()
        mask = ~sequence_mask(lengths).unsqueeze(1)
        # Run the forward pass of every layer of the tranformer.
        for layer in self.transformer:
            out = layer(out, mask)
        out = self.layer_norm(out)#[batch_size,sequence_len,hidden_dim]
        out, _ = torch.max(out, dim=1)
        print(out.size())
        out=self.softmax(self.linear(out))
        return emb, out, lengths

    def update_dropout(self, dropout, attention_dropout):
        self.embeddings.update_dropout(dropout)
        for layer in self.transformer:
            layer.update_dropout(dropout, attention_dropout)

