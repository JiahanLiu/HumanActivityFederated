import torch as torch
import torch.nn as nn
import torch.nn.functional as F 
import torch.optim as optim

class NetFC_1(nn.Module):

    def __init__(self):
        super(NetFC_1, self).__init__()

        self.z1 = nn.Linear(784, 30)
        self.z2_output = nn.Linear(30, 10)

    def forward(self, x):
        x = x.reshape(-1, 784)
        x = F.relu(self.z1(x))
        x = self.z2_output(x)
        x = F.log_softmax(x, dim=1)

        return x

class NetCNN_conv2_relu3(nn.Module):
    def __init__(self):
        super(NetCNN_conv2_relu3, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        x = F.log_softmax(x, dim=1)
        return x

class NetCNN_convrelu3_relu3(nn.Module):
    def __init__(self):
        super(NetCNN_convrelu3_relu3, self).__init__()

        self.conv_block = nn.Sequential(
                nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(inplace=True),
                nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(64),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2, stride=2),
                nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(128),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2, stride=2) 
            )

        self.linear_block = nn.Sequential(
                nn.Dropout(p=0.5),
                nn.Linear(128*7*7, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(inplace=True),
                nn.Dropout(0.5),
                nn.Linear(128, 64),
                nn.BatchNorm1d(64),
                nn.ReLU(inplace=True),
                nn.Dropout(0.5),
                nn.Linear(64, 10)
            )

    def forward(self, x):
        x = self.conv_block(x)
        x = x.view(x.size(0), -1)
        x = self.linear_block(x)
        x = F.log_softmax(x, dim=1)
        
        return x    

def parameter_init(model):
    if type(model) == nn.Linear:
        torch.nn.init.kaiming_uniform_(model.weight, nonlinearity='relu')
        model.bias.data.fill_(0.01)