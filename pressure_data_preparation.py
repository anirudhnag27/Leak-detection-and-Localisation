import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split

global train_df, test_df
train_df = pd.DataFrame(columns = ['Junc 10', 'Junc 11', 'Junc 12', 'Junc 13', 'Junc 21', 'Junc 22', 'Junc 23', 'Junc 31', 'Junc 32', 'condition']) 
#condition: 0=no leak. 1=leak present.

def addPressureToDF(filePath, leakStatus):
    df0 = pd.read_excel(filePath, skiprows=3, nrows=9)
    df0 = df0['psi             ']
    #making a list of excel sheet's pressures
    currentPressureArray = np.zeros(10, dtype=float)
    for i in range(9): 
        currentPressureArray[i] = df0[i]
    currentPressureArray[9] = leakStatus #0 is for no leak
    return train_df.append(pd.Series(currentPressureArray, index = train_df.columns), ignore_index=True)


def addNoLeakDataToDF(filePath):
    #creating balanced dataset:
    #inserting non-leak data into the dataset
    global train_df, test_df
    noLeakDF = pd.read_excel(filePath, skiprows=3, nrows=9)
    noLeakDF = noLeakDF['psi             ']
    currentPressureArray = np.zeros(10, dtype=float)
    for i in range(9): 
        currentPressureArray[i] = noLeakDF[i]
    currentPressureArray[9] = 0  #0 is for no leak
    for i in range(43): #43 = 0.8*54 i.e. 80%
        train_df = train_df.append(pd.Series(currentPressureArray, index = train_df.columns), ignore_index=True)
    for i in range(11):
        test_df = test_df.append(pd.Series(currentPressureArray, index = test_df.columns), ignore_index=True)

#adding the leak-case data to the dataframe
for leakDataFolder in os.listdir('.'): 
    if 'Leak Data ' in leakDataFolder:#eg. Leak Data 0100 Hrs
        dataHoursFolderList = os.listdir('./' + leakDataFolder) #eg. ./Leak Data 0100 Hrs/
        for i in dataHoursFolderList: #each i is when leak is at node i
            if 'Node ' in i: #eg. Node 11
                listOfExcelSheets = os.listdir('./' + leakDataFolder + '/' + i)
                for j in listOfExcelSheets: 
                    #each j is when different emitter coefficient is used for node i
                    if 'Nodes' in j: #eg.Nodes_160.xlsx
                        train_df = addPressureToDF('./' + leakDataFolder + '/' + i + '/' + j, 1)


#train-test split of leaking nodes data only. includes shuffling
train_df, test_df = train_test_split(train_df, test_size=0.2)
test_df = test_df.reset_index(drop = True)
train_df = train_df.reset_index(drop = True)

#adding the non-leaking data to train and test datafames 
# same ratio is used. Train dataset = 80% of total data
for leakDataFolder in os.listdir('.'): 
    if 'Leak Data ' in leakDataFolder:#eg. Leak Data 0100 Hrs
        addNoLeakDataToDF('./' + leakDataFolder + '/Nodes_0.xlsx')


#again shuffling both train and test dataset
train_df = train_df.sample(frac=1).reset_index(drop=True)
test_df = test_df.sample(frac=1).reset_index(drop=True)

x_train = train_df.drop(columns = ['condition'])
y_train = train_df['condition']

x_test = test_df.drop(columns = ['condition'])
y_test = test_df['condition']

#exporting prepared datasets as excel sheets
x_train.to_excel('x_train.xlsx',index=False)
y_train.to_excel('y_train.xlsx',index=False)
x_test.to_excel('x_test.xlsx',index=False)
y_test.to_excel('y_test.xlsx',index=False)