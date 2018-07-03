# -*- coding: UTF-8 -*-

import csv
import codecs
import pandas
import string

csvFilePath = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport7\\tanpermission.csv'

'''
with codecs.open(csvFilePath, mode='r', encoding='UTF-8') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        print(' ,'.join(row))
'''

'''
with open( csvFilePath, mode='r') as csvFile:
    reader = csv.reader(csvFile)
    head_row = next(reader)
    # print(head_row)
    # print(type(head_row))
    for row in reader:
        print(reader.line_num, row)
'''

# def readAndfilt(csvFilePath):
dataFrame = pandas.read_csv(csvFilePath, low_memory=False)
# print( dataFrame.head())
# print( dataFrame.tail())
dropLine = []
for index in dataFrame.index:
    curAge = dataFrame.loc[index, 'AGE']
    if curAge.isdigit() == False:
        dropLine.append(index)
    else:
        curAge = int(curAge)
        if curAge > 100:
            dropLine.append(index)
# print(dropLine)

dataFrame.drop(dropLine,inplace=True)
dataFrame['AGE'] = dataFrame['AGE'].astype(int)


def selectByAGE(dataFrame, symptom):
    dataFrame = dataFrame[dataFrame.TESTNAME == symptom]
    age1 = dataFrame[(dataFrame.AGE < 18)]
    age2 = dataFrame[(dataFrame.AGE > 18) & (dataFrame.AGE < 25)]
    age3 = dataFrame[(dataFrame.AGE > 25) & (dataFrame.AGE < 35)]
    age4 = dataFrame[(dataFrame.AGE > 35) & (dataFrame.AGE < 45)]
    age5 = dataFrame[(dataFrame.AGE > 45) & (dataFrame.AGE < 55)]
    age6 = dataFrame[(dataFrame.AGE > 55 )]
    return age1, age2, age3, age4, age5, age6


def selectBySex(dataFrame, symptom):
    dataFrame = dataFrame[dataFrame.TESTNAME == symptom]
    man = dataFrame[dataFrame.SEX == '男']
    women = dataFrame[dataFrame.SEX == '女']
    return man, women

def selectBySymptom(dataFrame, symptom):
    IDList = []
    dataFrame = dataFrame.set_index('NUMBERID')     # set index use NUMBERID
    dfGroupByID = dataFrame.groupby('NUMBERID')
    for ID, group in dfGroupByID:
        # print(ID, group)
        flag = False
        for element in group.TESTNAME:
            if element == '90项症状清单':
                flag = True
                break
        if flag == False:
            IDList.append(ID)
    # print(IDList)
    dataFrame.drop(IDList, inplace=True)

    return dataFrame[dataFrame.TESTNAME == symptom ]

if __name__ == '__main__':
    data = selectBySymptom(dataFrame, '焦虑自评量表')