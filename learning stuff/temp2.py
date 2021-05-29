import torch
# x = torch.rand(5, 3)
# print(x)


# import numpa


print(torch.cuda.is_available())


X_train = torch.FloatTensor([0., 1., 2.])
X_train.is_cuda
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
