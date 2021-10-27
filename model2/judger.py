import json
import numpy as np
import os
import torch
import torch.nn as nn 
import torch.nn.functional as F
import torch.utils.data as dt
from model import mycnn
model=mycnn()
model=torch.load("nnmodel")

frame_number=30
data=np.zeros((1, 3, 25*frame_number))
with open("candidate.json",'r',encoding='utf8') as fp:
    json_data=json.load(fp)
    key_points=json_data["data"]
    for j in range(25*frame_number):
        data[0, 0, j] = key_points[j*3]
        data[0, 1, j] = key_points[j*3+1]
        data[0, 2, j] = key_points[j*3+2]

data=torch.Tensor(data)
pr=model(data)
if(pr[0,0]>pr[0,1]):
    print("No danger")
else:
    print("Danger!")