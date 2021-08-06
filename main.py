from prenlp.tokenizer import NLTKMosesTokenizer
from torch.utils.data import DataLoader
import argparse
from Models.Util.DataIterator import create_examples
from Models.Util.Tokenizer import PretrainedTokenizer,Tokenizer,Defaulttokenizer
from trainer import Trainer
TOKENIZER_CLASSES = {'nltk_moses': NLTKMosesTokenizer}
def main(args):
    print(args)
    # Load tokenizer
    if args.tokenizer == 'sentencepiece':
        tokenizer = PretrainedTokenizer(pretrained_model=args.pretrained_model, vocab_file=args.vocab_file)
    elif args.tokenizer == 'default':
        tokenizer=Defaulttokenizer()
        tokenizer = Tokenizer(tokenizer=tokenizer, vocab_file=args.vocab_file)
    else:
        tokenizer = TOKENIZER_CLASSES[args.tokenizer]()
        tokenizer = Tokenizer(tokenizer=tokenizer, vocab_file=args.vocab_file)

    # Build DataLoader
    train_dataset = create_examples(args, tokenizer, mode='train')
    test_dataset = create_examples(args, tokenizer, mode='test')
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=True)

    # Build Trainer
    trainer = Trainer(args, train_loader, test_loader, tokenizer)

    # Train & Validate
    for epoch in range(1, args.epochs + 1):
        trainer.train(epoch)
        trainer.validate(epoch)
        trainer.save(epoch, args.output_model_prefix)

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--c1file_trn', default='c1file_trn', type=str, help='class1训练数据集')
    parser.add_argument('--c2file_trn', default='c2file_trn', type=str, help='class2训练数据集')
    parser.add_argument('--c1file_val', default='c1file_val', type=str, help='class1验证数据集')
    parser.add_argument('--c2file_val', default='c2file_val', type=str, help='class2验证数据集')
    parser.add_argument('--vocab_file',          default='',     type=str, help='词典位置')
    parser.add_argument('--tokenizer',           default='',  type=str, help='tokenizer to tokenize input corpus. available: sentencepiece, '+', '.join(TOKENIZER_CLASSES.keys()))
    parser.add_argument('--pretrained_model',    default='',     type=str, help='句向量的预训练模型。pretrained sentencepiece model path. used only when tokenizer=\'sentencepiece\'')
    parser.add_argument('--output_model_prefix', default='model',          type=str, help='输出模型的前缀名')
    # Input parameters
    parser.add_argument('--batch_size',     default=24,   type=int,   help='batch size')
    parser.add_argument('--max_seq_len',    default=512,  type=int,   help='the maximum size of the input sequence')
    # Train parameters
    parser.add_argument('--epochs',         default=20,   type=int,   help='the number of epochs')
    parser.add_argument('--lr',             default=1e-4, type=float, help='learning rate')
    parser.add_argument('--no_cuda',        action='store_true')
    # Model parameters
    parser.add_argument('--src_word_vec_size',default=256,type=int)
    parser.add_argument('--position_encoding', default=True, type=bool)
    parser.add_argument('--enc_rnn_size',         default=256,  type=int,   help='the number of expected features in the transformer')
    parser.add_argument('--enc_layers',       default=6,    type=int,   help='the number of heads in the multi-head attention network')
    parser.add_argument('--heads',   default=8,    type=int,   help='the number of multi-head attention heads')
    parser.add_argument('--dropout',        default=0.2,  type=float, help='the residual dropout value')
    parser.add_argument('--transformer_ff',     default=1024, type=int,   help='the dimension of the feedforward network')
    parser.add_argument('--attention_dropout', default=0.1, type=float, help='')
    parser.add_argument('--max_relative_positions',default=0,type=float,help='')



    args=parser.parse_args()
    main(args)