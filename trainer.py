from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from model_builder import build_Model

class Trainer(object):
    def __init__(self, args, train_loader, test_loader, tokenizer):
        self.args = args
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.vocab_size = tokenizer.vocab_size
        self.pad_id = tokenizer.pad_token_id
        self.device = 'cuda' if torch.cuda.is_available() and not args.no_cuda else 'cpu'

        self.model = build_Model(args,tokenizer)
        self.model.to(self.device)

        "优化器采用Adam,损失函数采用交叉熵"
        self.optimizer = optim.Adam(self.model.parameters(), args.lr)
        self.criterion = nn.CrossEntropyLoss()

    def train(self, epoch):
        losses, accs = 0, 0
        n_batches, n_samples = len(self.train_loader), len(self.train_loader.dataset)

        self.model.train()
        for i, batch in enumerate(self.train_loader):
            inputs, labels = map(lambda x: x.to(self.device), batch)
            # |inputs| : (batch_size, seq_len), |labels| : (batch_size)

            outputs, attention_weights,lengthes = self.model(inputs)
            # |outputs| : (batch_size, 2), |attention_weights| : [(batch_size, n_attn_heads, seq_len, seq_len)] * n_layers

            loss = self.criterion(outputs, labels)
            losses += loss.item()
            acc = (outputs.argmax(dim=-1) == labels).sum()
            accs += acc.item()

            "参数更新"
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            if i % (n_batches // 5) == 0 and i != 0:
                print('Iteration {} ({}/{})\tLoss: {:.4f} Acc: {:4f}%'.format(
                    i, i, n_batches, losses / i, accs / (i * self.args.batch_size) * 100.))

        print('Train Epoch: {}\t>\tLoss: {:.4f} / Acc: {:.1f}%'.format(epoch, losses / n_batches,
                                                                       accs / n_samples * 100.))

    def validate(self, epoch):
        losses, accs = 0, 0
        n_batches, n_samples = len(self.test_loader), len(self.test_loader.dataset)

        self.model.eval()
        with torch.no_grad():
            for i, batch in enumerate(self.test_loader):
                inputs, labels = map(lambda x: x.to(self.device), batch)
                # |inputs| : (batch_size, seq_len), |labels| : (batch_size)

                outputs, attention_weights,lengthes = self.model(inputs)
                # |outputs| : (batch_size, 2), |attention_weights| : [(batch_size, n_attn_heads, seq_len, seq_len)] * n_layers

                loss = self.criterion(outputs, labels)
                losses += loss.item()
                acc = (outputs.argmax(dim=-1) == labels).sum()
                accs += acc.item()

        print('Valid Epoch: {}\t>\tLoss: {:.4f} / Acc: {:.1f}%'.format(epoch, losses / n_batches,
                                                                       accs / n_samples * 100.))

    def save(self, epoch, model_prefix='model', root='.model'):
        path = Path(root) / (model_prefix + '.ep%d' % epoch)
        if not path.parent.exists():
            path.parent.mkdir()

        torch.save(self.model, path)