import json
import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
import os
dir = "D:\Missouri\model1\examples\\tutorial_api_python\example\\"
# x="data (5)_000000000000_keypoints.json"
# with open(dir + x, 'r') as f:
#     data = json.load(f)
#     print(data["people"])
#     if len(data["people"][0]['pose_keypoints_2d']) == 75 :
#         print(len(data["people"][0]['pose_keypoints_2d']))
k = [] 

for x in os.listdir(dir):
    with open(dir + x, 'r') as f:
        data = json.load(f)
        # print(data["people"][0]['pose_keypoints_2d'])
        if len(data["people"]) ==0 :
            continue 
        
        k.extend(data["people"][0]['pose_keypoints_2d'])
        # break
        f.close()
    os.remove(dir + x)  
# print(len(k))
dataframe = np.asarray(k).reshape(-1,75)

# print(dataframe.shape)
# repair the hollow

# print(np.sum(dataframe == 0))

rownum = 0
for row in dataframe:
    # print (rownum)
    
    for i in range(2,75,3):
        if row[i] == 0:
            if rownum < 15:
                dataframe[rownum,i-2:i+1] =np.asarray(np.mean( dataframe[0 : rownum+15,i-2:i+1],axis= 0) ).reshape(1,3)  
            
            elif rownum > dataframe.shape[0] -15:
                dataframe[rownum,i-2:i+1] =np.mean( dataframe[rownum-15 : dataframe.shape[0] ,i-2:i+1],axis= 0)   
            else: 
                dataframe[rownum,i-2:i+1] =np.mean( dataframe[rownum-15 : rownum+15,i-2:i+1],axis= 0)
    # print(dataframe[rownum])
    rownum += 1

# print(np.sum(dataframe == 0))
print("success")

# centralize
for i in range(25):
    if i == 1:
        continue
    dataframe[:,0+3*i]=dataframe[:,0+3*i] - dataframe[:,3]
    dataframe[:,1+3*i]=dataframe[:,0+3*i] - dataframe[:,4]
dataframe[:,3] = 0
dataframe[:,4] = 0
# print(np.sum(dataframe == np.NaN))
formal = len(os.listdir('D:\\data\\'))
before = len(os.listdir('D:\\test\\'))
test =True
# test =False
if not test:
    for a in range(int(dataframe.shape[0]/30)):
        data = dataframe[30*a:30*(a+1),:].flatten().tolist()
        # print(data)
        # 1 for fall  0 for abl
        jsonData = json.dumps({'data':data,'kind':0} )
        with open('D:\data\\' + str(a+formal) + '.json', 'w') as f:
            f.write(jsonData)
        f.close()
else:
    for a in range(int(dataframe.shape[0]/30)):
        data = dataframe[30*a:30*(a+1),:].flatten().tolist()
        # print(data)
        jsonData = json.dumps({'data':data} )
        with open('D:\\Missouri\\model2\\candidate' + str(a+before) + '.json', 'w') as f:
            f.write(jsonData)
        f.close()

