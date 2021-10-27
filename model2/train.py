import json
import numpy as np
import os
import torch
import torch.nn as nn 
import torch.nn.functional as F
import torch.utils.data as dt
from model import mycnn

iteration=500
total=195
batchsize=182
frame_number=30
data=np.zeros((total, 3, 25*frame_number))
targets=np.zeros(total)
file=os.listdir("data/")

def load_data():
    print("Loading data...")
    for i in range(total):
        #if i < batchsize:
        name=''.join(["data/",file[i]])
        with open(name,'r',encoding='utf8') as fp:
            json_data=json.load(fp)
            key_points=json_data["data"]
            for j in range(25*frame_number):
                data[i, 0, j] = key_points[j*3]
                data[i, 1, j] = key_points[j*3+1]
                data[i, 2, j] = key_points[j*3+2]
        targets[i] = json_data["kind"]


load_data()
cor_lst=[]
correctness=0

for k in range(1,16):
    if (k-1)*13==0:
        train_data = data[k*13:,:,:]
        train_targets = targets[k*13:]
    elif k*13 == 104:
        train_data = data[:(k-1)*13,:,:]
        train_targets = targets[:(k-1)*13:]
    else:
        train_data = np.concatenate((data[k*13:,:,:],data[:(k-1)*13,:,:]),axis=0)
        train_targets = np.concatenate((targets[k*13:],targets[:(k-1)*13]),axis=0)
    model=mycnn()
    #print(model)
    optimizer=torch.optim.SGD(model.parameters(), lr=0.015)
    loss_function=torch.nn.CrossEntropyLoss()
    
    train_data = torch.Tensor(train_data)
    train_targets = torch.Tensor(train_targets).long()
    test_data = data[(k-1)*13:k*13,:,:]
    test_data = torch.Tensor(test_data)
    test_targets = targets[(k-1)*13:k*13]
    test_targets = torch.Tensor(test_targets).long()

    #last_correctness=0
    last_loss = None 
    for batch_no in range(1,8):
        correctness=0
        for i in range(iteration):
            #train_data_new = train_data[(batch_no-1)*13:batch_no*13,:,:]
            #train_targets_new = train_targets[(batch_no-1)*13:batch_no*13]
            train_data_new = train_data[:,:,:]
            train_targets_new = train_targets[:]
            print(k,"th validation", batch_no, "th batch",i,"th iteration", end="   ")
            output=model(train_data_new)
            #print(output.shape, train_targets_new.shape)
            loss=loss_function(output, train_targets_new)
            print("Loss:", loss.item(), end="   ")
            last_loss = loss.item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            pr=model(test_data)
            #print(pr.size())
            lstresult=[]
            for j in range(total-batchsize):
                if pr[j,0] > pr[j, 1]:
                    lstresult.append(0)
                else:
                    lstresult.append(1)
            result=np.array(lstresult)
            correctness = 1-np.count_nonzero(test_targets-result)/(total-batchsize)
            print("Correctness",correctness)
            if(loss.item()<0.01):
                break
            if last_loss != None:
                if i > 100 and last_loss-loss.item()<1e-5:
                    break
            '''print("LastCorrectness",last_correctness)
            if i>2000 and correctness<last_correctness:
                correctness = last_correctness
                break'''
    cor_lst.append(correctness)

print("Final mean correctness:", np.mean(np.array(cor_lst)))
torch.save(model, "nnmodel")
