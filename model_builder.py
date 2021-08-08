from Models.Embedding import Embeddings
from Models.Encoder import  TransformerEncoder
from Models.TokenCLS import TokenCLSModel


def build_embeddings(opt, src_Tokenizer, for_encoder=True):
    """
    Args:
        opt: the option in current environment.
        text_field(TextMultiField): word and feats field.
        for_encoder(bool): build Embeddings for encoder or decoder?
    """
    emb_dim = opt.src_word_vec_size if for_encoder else opt.tgt_word_vec_size
    word_padding_idx = src_Tokenizer.pad_token_id#通过tokenizer得到pad id
    num_word_embeddings= src_Tokenizer.vocab_size#通过Tokenizer得到词表大小

    emb = Embeddings(
        word_vec_size=emb_dim,
        position_encoding=opt.position_encoding,
        feat_merge="concat",
        feat_vec_exponent=0.7,
        feat_vec_size=-1,
        dropout=opt.dropout[0] if type(opt.dropout) is list else opt.dropout,
        word_padding_idx=word_padding_idx,
        feat_padding_idx=[],
        word_vocab_size=num_word_embeddings,
        feat_vocab_sizes=[],
        sparse= False,
        freeze_word_vecs=False
    )
    return emb
def build_Model(opt,src_Tokenizer):
    if opt.tokenCLS==False:
        emb=build_embeddings(opt,src_Tokenizer)
        encoder=TransformerEncoder.from_opt(opt,emb)
    else:
        emb = build_embeddings(opt, src_Tokenizer)
        encoder=TokenCLSModel.from_opt(opt,emb)
    return encoder