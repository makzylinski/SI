import numpy as np
import matplotlib.pyplot as pt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("datasets/cyfry.csv").values

#print(data)

clf = DecisionTreeClassifier()

# training

xtrain = data[0:100, 1:]
train_label = data[0:100, 0]

clf.fit(xtrain, train_label)
#print(xtrain)

# testing data

xtest = data[100:,1:]
actual_label = data[100:,0]     # 102 to aktualny indeks 0 (czyli czworka)

p = clf.predict(xtest)
#spr = xtest[0]
#pred_spr = clf.predict([spr])   # czworka,
#print(spr)
#print(pred_spr)

count = 0
for i in range(0,100):
    count += 1 if p[i] == actual_label[i] else 0

print("Accuracy =", (count/100)*100, "%")
