# -*- coding: UTF-8 -*-



import csv
import pandas
import numpy as np

csvFilePath = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport7\\scl90.csv'
columnList = ['QTH_PJ', 'QPZT_PJ', 'RJMG_PJ', 'YY_PJ', 'JL_PJ', 'DD_PJ', 'KB_PJ', 'PZ_PJ', 'JSB_PJ', 'QT_PJ', 'ZJF_PJ']
consLevelList = [1.37, 1.62, 1.65, 1.5, 1.39, 1.48, 1.23, 1.43, 1.29]

dfdtype = dict(ZF_YS='int64', ZJF_PJ='float64', YIXS_YS='int64', YAXS_YS='int64', YXPJ_PJ='float64', QTH_YS='int64',
               QTH_PJ='float64', QPZT_YS='int64', QPZT_PJ='float64', RJMG_YS='int64', RJMG_PJ='float64', YY_YS='int64',
               YY_PJ='float64', JL_YS='int64', JL_PJ='float64', DD_YS='int64', DD_PJ='float64', KB_YS='int64',
               KB_PJ='float64', PZ_YS='int64', PZ_PJ='float64', JSB_YS='int64', JSB_PJ='float64', QT_YS='int64',
               QT_PJ='float64')


def readAndfilt(csvFilePath):
    dataFrame = pandas.read_csv(csvFilePath, low_memory=False)
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

    dataFrame.drop(dropLine, inplace=True)

    dataFrame['AGE'] = dataFrame['AGE'].astype("int")
    for j in range(8, 12):
        dataFrame.iloc[:,j] = dataFrame.iloc[:,j].astype("float")
    for j in range(12, 33, 2):
        dataFrame.iloc[:, j] = dataFrame.iloc[:, j].astype("float")
    for j in range(13, 33, 2):
        dataFrame.iloc[:, j] = dataFrame.iloc[:, j].astype("int")

    dataFrame = dfRefined(dataFrame)

    return dataFrame


def selectByAGE(dataFrame):
    age1 = dataFrame[(dataFrame.AGE < 18)]
    age2 = dataFrame[(dataFrame.AGE > 18) & (dataFrame.AGE < 25)]
    age3 = dataFrame[(dataFrame.AGE > 25) & (dataFrame.AGE < 35)]
    age4 = dataFrame[(dataFrame.AGE > 35) & (dataFrame.AGE < 45)]
    age5 = dataFrame[(dataFrame.AGE > 45) & (dataFrame.AGE < 55)]
    age6 = dataFrame[(dataFrame.AGE > 55)]
    return age1, age2, age3, age4, age5, age6


def selectBySex(dataFrame):
    man = dataFrame[dataFrame.SEX == '男']
    woman = dataFrame[dataFrame.SEX == '女']
    return man, woman


def getItemMean(dataFrame, item):
    itemColumn = pandas.to_numeric(dataFrame[item],errors='coerce') #dataFrame[item].astype("float64")
    mean = itemColumn.mean()
    std = itemColumn.std()
    return mean, std


def getItemCount(dataFrame, item, consLevel):
    itemColumn = pandas.to_numeric(dataFrame[item],errors='coerce')
    selectColumn = itemColumn[itemColumn > consLevel]
    rate = .0
    rate += selectColumn.size/itemColumn.size
    return selectColumn.size, rate


def dfRefined(dataFrame):
    dataFrame.drop(columns=['NAME', 'INFO1', 'INFO2', 'INFO3', 'INFO4', 'INFO5', 'INFO6', '_NullFlags'], inplace=True)
    '''
    dataFrame['Sex_refined'] = 0
    dataFrame['Age_refined'] = 0
    sexColumn = dataFrame.SEX == '女'
    ageColumn = dataFrame.AGE
    for i in range(sexColumn.size):
        if sexColumn.iloc[i] == True:
            dataFrame.loc[i, 'Sex_refined'] = 1
    for i in range(ageColumn.size):
        if ageColumn.iloc[i] > 18 and ageColumn.iloc[i] < 25:
            dataFrame.loc[i, 'Age_refined'] = 1
        elif ageColumn.iloc[i] > 25 and ageColumn.iloc[i] < 35:
            dataFrame.loc[i, 'Age_refined'] = 2
        elif ageColumn.iloc[i] > 35 and ageColumn.iloc[i] < 45:
            dataFrame.loc[i, 'Age_refined'] = 3
        elif ageColumn.iloc[i] > 45 and ageColumn.iloc[i] < 55:
            dataFrame.loc[i, 'Age_refined'] = 4
        else:
            dataFrame.loc[i, 'Age_refined'] = 5

    # print(dataFrame['Sex_refined'].value_counts())
    # print(dataFrame['Age_refined'].value_counts())
    '''
    return dataFrame


def getItemCorr(dataFrame, item):

    result1 = dataFrame.corr(method='pearson')[item]
    return result1

    # dataFrameScore = dataFrame.iloc[:, 8:33]
    # result2 = dataFrame.corrwith(dataFrame[item])
    # return result2


if __name__ == '__main__':
    dataFrame = readAndfilt(csvFilePath)
    ageGroup = selectByAGE(dataFrame)
    sexGroup = selectBySex(dataFrame)

    # 输出性别10项指标均值情况
    # for column in columnList:
    #     for sex in sexGroup:
    #         mean, std = getItemMean(sex, column)
    #         print(column + " : ", mean, " +/- ", std)

    # 输出年龄10项指标均值情况
    # for column in columnList:
    #     for age in ageGroup:
    #         mean, std = getItemMean(age, column)
    #         print(column + " : ", mean, " +/- ", std)

    # 输出性别超标比例
    # for i in range(9):
    #     column = columnList[i]
    #     consLevel = consLevelList[i]
    #     for sex in sexGroup:
    #         count, rate = getItemCount(sex, column, consLevel)
    #         print(count, rate)

    # 输出10个因子，每个因子的相关性系数
    elementResult = []
    for element in columnList:
        elementResult.append(getItemCorr(dataFrame, element))

    # 输出整体的相关性系数
    corrResult = dataFrame.corr('pearson')
