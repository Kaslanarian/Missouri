import json
import numpy as np
import os
import torch
import torch.nn as nn 
import torch.nn.functional as F
import torch.utils.data as dt

class Conv1d(nn.Module):
    # 定义了卷积 - 激活
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, relu=True, same_padding=False):
        super(Conv1d, self).__init__()
        padding = int((kernel_size - 1) / 2) if same_padding else 0
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding=padding)

    def forward(self, x):
        x = self.conv(x)
        x = F.tanh(x)
        return x
        
class mycnn(nn.Module):
    def __init__(self):
        super(mycnn,self).__init__()
        self.branch1 = nn.Sequential(Conv1d(1, 8, 50, 25),
                                     nn.MaxPool1d(2), 
                                     Conv1d(8, 16, 3, same_padding=True),
                                     nn.MaxPool1d(2)
                                     )
        self.branch2 = nn.Sequential(Conv1d(1, 8, 75, 25),
                                     nn.MaxPool1d(3),
                                     Conv1d(8, 16, 3, same_padding=True),
                                     )
        self.branch3 = nn.Sequential(Conv1d(1, 8, 100, 25),
                                     nn.MaxPool1d(2), 
                                     Conv1d(8, 16, 3, same_padding=True),
                                     )
        self.layer1 = nn.Sequential(Conv1d(16, 8, 3, same_padding=True),
                                     nn.MaxPool1d(2), 
                                     )
        self.layer2 = nn.Sequential(Conv1d(8, 8, 3, same_padding=True),
                                     )

        self.linear1 = nn.Linear(8*42, 8*42)
        self.linear2 = nn.Linear(8*42, 16)
        self.linear3 = nn.Linear(16, 2)
    
    def forward(self, x):
        #print(x[:, :1, :].shape)
        x1_1 = self.branch1(x[:, :1, :])      
        x1_2 = self.branch2(x[:, :1, :])
        x1_3 = self.branch3(x[:, :1, :])
        #print(x1_1.shape, x1_2.shape, x1_3.shape)
        x1 = torch.cat((x1_1, x1_2, x1_3), 2)
        #print(x1.shape)
        x1 = self.layer1(x1)

        x2_1 = self.branch1(x[:, 1:2, :])
        x2_2 = self.branch2(x[:, 1:2, :])
        x2_3 = self.branch3(x[:, 1:2, :])
        x2 = torch.cat((x2_1, x2_2, x2_3), 2)
        x2 = self.layer1(x2)

        x3_1 = self.branch1(x[:, 2:, :])
        x3_2 = self.branch2(x[:, 2:, :])
        x3_3 = self.branch3(x[:, 2:, :])
        x3 = torch.cat((x3_1, x3_2, x3_3), 2)
        x3 = self.layer1(x3)

        x = torch.cat((x1, x2, x3), 2)
    
        x = self.layer2(x)
        #print(x.shape)
        x = x.view(-1, 8*42)
        
        x = F.tanh(self.linear1(x))
        x = F.tanh(self.linear2(x))
        x = F.tanh(self.linear3(x))
        return x
