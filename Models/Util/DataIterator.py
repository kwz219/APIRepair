from typing import Iterable, Union, List
from prenlp.data import IMDB
from DataProcess.IOHelper import read_lines
import torch
from torch.utils.data import TensorDataset

DATASETS_CLASSES = {'imdb': IMDB}

class APIMU_Example(object):
    def __init__(self,code,mu_index,correct_api):
        super(APIMU_Example, self).__init__()
        self.codetext=code
        self.mu_index=mu_index
        self.correct_api=correct_api


class InputExample:
    """A single training/test example for text classification.
    """

    def __init__(self, text: str, label: str):
        self.text = text
        self.label = label


class InputFeatures:
    """A single set of features of data.
    """

    def __init__(self, input_ids: List[int], label_id: int):
        self.input_ids = input_ids
        self.label_id = label_id


def convert_examples_to_features(examples: List[InputExample],
                                 label_dict: dict,
                                 tokenizer,
                                 max_seq_len: int) -> List[InputFeatures]:
    pad_token_id = tokenizer.pad_token_id

    features = []
    src_lengths=[]
    for i, example in enumerate(examples):
        tokens = tokenizer.tokenize(example.text)
        tokens = tokens[:max_seq_len]

        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        padding_length = max_seq_len - len(input_ids)
        input_ids = input_ids + ([pad_token_id] * padding_length)
        label_id = label_dict.get(example.label)

        feature = InputFeatures(input_ids, label_id)
        features.append(feature)
        src_lengths.append(len(input_ids))

    return features,src_lengths


def create_examples(args,
                    tokenizer,
                    mode: str = 'train') -> Iterable[Union[List[InputExample], dict]]:
    if mode == 'train':
        dataset = read_dataset(args.c1file_trn,args.c2file_trn)
    elif mode == 'test':
        dataset = read_dataset(args.c1file_val,args.c2file_val)

    examples = []
    for text, label in dataset:
        example = InputExample(text, label)
        examples.append(example)

    labels = sorted(list(set([example.label for example in examples])))
    label_dict = {label: i for i, label in enumerate(labels)}
    # print('[{}]\tLabel dictionary:\t{}'.format(mode, label_dict))

    features,src_lengths = convert_examples_to_features(examples, label_dict, tokenizer, args.max_seq_len)

    #获得src长度
    all_input_lengths=torch.tensor([length for length in src_lengths], dtype=torch.long)
    all_input_ids = torch.tensor([feature.input_ids for feature in features], dtype=torch.long)
    all_label_ids = torch.tensor([feature.label_id for feature in features], dtype=torch.long)

    dataset = TensorDataset(all_input_ids, all_label_ids,all_input_lengths)

    return dataset

def read_dataset(bepath,afpath):
    dataset=[]
    bes=read_lines(bepath)
    afs=read_lines(afpath)
    for b in bes:
        dataset.append((b,0))
    for af in afs:
        dataset.append((af,1))
    return dataset
