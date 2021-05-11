from Models.Embedding import Embeddings
from Models.Encoder import  TransformerEncoder
def build_embeddings(opt, src_Tokenizer, for_encoder=True):
    """
    Args:
        opt: the option in current environment.
        text_field(TextMultiField): word and feats field.
        for_encoder(bool): build Embeddings for encoder or decoder?
    """
    emb_dim = opt.src_word_vec_size if for_encoder else opt.tgt_word_vec_size
    word_padding_idx = src_Tokenizer.pad_token_id()#通过tokenizer得到pad id
    num_word_embeddings= src_Tokenizer.vocab_size()#通过Tokenizer得到vocab id

    freeze_word_vecs = opt.freeze_word_vecs_enc if for_encoder \
        else opt.freeze_word_vecs_dec

    emb = Embeddings(
        word_vec_size=emb_dim,
        position_encoding=opt.position_encoding,
        feat_merge=opt.feat_merge,
        feat_vec_exponent=opt.feat_vec_exponent,
        feat_vec_size=opt.feat_vec_size,
        dropout=opt.dropout[0] if type(opt.dropout) is list else opt.dropout,
        word_padding_idx=word_padding_idx,
        feat_padding_idx=[],
        word_vocab_size=num_word_embeddings,
        feat_vocab_sizes=[],
        sparse=opt.optim == "sparseadam",
        freeze_word_vecs=freeze_word_vecs
    )
    return emb
def build_Model(opt,src_Tokenizer):
    emb=build_embeddings(opt,src_Tokenizer)
    encoder=TransformerEncoder.from_opt(opt,emb)
    return encoder