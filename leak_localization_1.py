import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split

global noLeakDF
noLeakDF = pd.DataFrame(columns = ['Junc 10', 'Junc 11', 'Junc 12', 'Junc 13', 'Junc 21', 'Junc 22', 'Junc 23', 'Junc 31', 'Junc 32', 'Time']) 
testDF = pd.DataFrame(columns = ['Junc 10', 'Junc 11', 'Junc 12', 'Junc 13', 'Junc 21', 'Junc 22', 'Junc 23', 'Junc 31', 'Junc 32', 'Time', 'Leak Node', 'Prediction']) 


def addPressureToDF(filePath, currentTime):
    global noLeakDF
    df0 = pd.read_excel(filePath, skiprows=3, nrows=9)
    df0 = df0['psi             ']
    #making a list of excel sheet's pressures
    currentPressureArray = np.zeros(10, dtype=float)
    for i in range(9): 
        currentPressureArray[i] = df0[i]
    currentPressureArray[9] = currentTime
    return noLeakDF.append(pd.Series(currentPressureArray, index = noLeakDF.columns), ignore_index=True)


#adding the no leak data
for currentFolder in os.listdir('.'): 
    if 'Leak Data ' in currentFolder:#eg. Leak Data 0100 Hrs
        currentTime = currentFolder.split(' ')[2]
        noLeakDF = addPressureToDF('./' + currentFolder + '/Nodes_0.xlsx', currentTime)

def localiseLeak(filePath, currentTime):
    global noLeakDF
    df0 = pd.read_excel(filePath, skiprows=3, nrows=9)
    df0 = df0['psi             ']
    #making a list of excel sheet's pressures
    currentPressureArray = np.zeros(10, dtype=float)
    for i in range(9): 
        currentPressureArray[i] = df0[i]
    currentPressureArray[9] = float(currentTime)
    for i in range(6):
        iterTime = float(noLeakDF['Time'][i])
        if (currentTime==iterTime):
            noLeakPressureList = noLeakDF.iloc[i]
            pressureDifferenceList = np.zeros(9, dtype=float)
            for j in range(9):
                pressureDifferenceList[j] = abs(noLeakPressureList[j] - currentPressureArray[j])
            index_max = np.argmax(pressureDifferenceList)
            return float(noLeakDF.columns[index_max].split(' ')[1])


def addTest(filePath, currentTime_, leakNode):
    df0 = pd.read_excel(filePath, skiprows=3, nrows=9)
    df0 = df0['psi             ']
    #making a list of excel sheet's pressures
    currentPressureArray = np.zeros(12, dtype=float)
    for i in range(9): 
        currentPressureArray[i] = df0[i]
    currentPressureArray[9] = int(currentTime_)
    currentPressureArray[10] = leakNode
    currentPressureArray[11] = localiseLeak(filePath, currentTime_)
    return testDF.append(pd.Series(currentPressureArray, index = testDF.columns), ignore_index=True)


def getAccuracy():
    global testDF
    sizeOfDF = len(testDF['Prediction'])
    wrongPredictionCount = 0
    wrong_prediction_df = pd.DataFrame(columns = ['Junc 10', 'Junc 11', 'Junc 12', 'Junc 13', 'Junc 21', 'Junc 22', 'Junc 23', 'Junc 31', 'Junc 32', 'Time', 'Leak Node', 'Prediction']) 
    for i in range(sizeOfDF):
        if(testDF['Leak Node'][i] != testDF['Prediction'][i]):
            wrongPredictionCount += 1
    #         tempList = testDF.loc[i].to_list()
    #         wrong_prediction_df = wrong_prediction_df.append(pd.Series(tempList, index = testDF.columns), ignore_index=True)
    # for col in wrong_prediction_df:  
    #     if col != 'condition':
    #         plt.scatter('condition', col , data=combinedDF)
    #         plt.ylabel(col +  'pressure')
    #         plt.xlabel('0=no leak, 1=leak')
    #         plt.axis([-0.1, 1.1, 0, 140])
    #         plt.show()
    return float(sizeOfDF-wrongPredictionCount)/sizeOfDF


#adding the leak-case data to the dataframe
for leakDataFolder in os.listdir('.'): 
    if 'Leak Data ' in leakDataFolder:#eg. Leak Data 1 Hrs
        currentTime = float(leakDataFolder.split(' ')[2])
        dataHoursFolderList = os.listdir('./' + leakDataFolder) #eg. ./Leak Data 0100 Hrs/
        for i in dataHoursFolderList: #each i is when leak is at node i
            if 'Node ' in i: #eg. Node 11
                leakNode = float(i.split(' ')[1])
                listOfExcelSheets = os.listdir('./' + leakDataFolder + '/' + i)
                for j in listOfExcelSheets: 
                    #each j is when different emitter coefficient is used for node i
                    if 'Nodes' in j: #eg.Nodes_160.xlsx
                        testDF = addTest('./' + leakDataFolder + '/' + i + '/' + j, currentTime, leakNode)

print(testDF.head(10))
print("\nData available:")
print(len(testDF['Junc 10']))
# print(type(localiseLeak('./Leak Data 0100 Hrs/Node 10/Nodes_200.xlsx', 100)))
print("\n\n\nThe accuracy is:")
print(getAccuracy())