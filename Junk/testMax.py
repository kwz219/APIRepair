import torch
def test_torchmax():
    x=torch.randn(3,3,3)
    print(x)
    max_d0=torch.max(x,dim=0)[0]
    max_d1 = torch.max(x, dim=1)[0]
    max_d2 = torch.max(x, dim=2)[0]
    print(max_d0)
    print(max_d1)
    print(max_d2)
test_torchmax()
