# -*- coding: UTF-8 -*-



import csv
import pandas
import numpy as np
import __init__


csvFilePath = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport7\\scl90.csv'
sasFilePath = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport7\\sas.csv'
sdsFilePath = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport7\\sds.csv'
psqiFilePath = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport7\\Psqi.csv'
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
    dataFrame.drop(columns=['INFO1', 'INFO2', 'INFO3', 'INFO4', 'INFO5', 'INFO6', '_NullFlags'], inplace=True)
    dataFrame = dataFrame[dataFrame['NAME'].notnull()]
    dataFrame = dataFrame.drop_duplicates('NAME')
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


def readSAS(filePath):
    sas = pandas.read_csv(filePath, low_memory=False)
    sas = sas[['NAME', 'YS']]
    sas = sas[sas['NAME'].notnull()]
    sas = sas.drop_duplicates('NAME')
    sas['YS'] = sas['YS'].astype('int')
    # dataFrame = dataFrame[dataFrame['NAME'].notnull()]
    # dataFrame = dataFrame.drop_duplicates('NAME')
    return sas


def readSDS(filePath):
    sds = pandas.read_csv(filePath, low_memory=False)
    sds = sds[['NAME', 'ZF']]
    sds = sds[sds['NAME'].notnull()]
    sds = sds.drop_duplicates('NAME')
    sds['ZF'] = sds['ZF'].astype('int')
    return sds


def diagramCorr(scl90, another):
    df = pandas.merge(left=scl90, right=another, on='NAME', how='inner')
    return df.corr()

if __name__ == '__main__':
    dataFrame = readAndfilt(csvFilePath)
    # ageGroup = selectByAGE(dataFrame)
    # sexGroup = selectBySex(dataFrame)

    # 输出性别10项指标均值情况
    # fileName = "E:\\workProjects\\NetLab530\\depression\\output\\result\\性别对scl9010个因子的影响.xlsx"
    # excel = easyExcel(fileName)
    # i = j = 1
    # for column in columnList:
    #     i = 1
    #     j = j + 1
    #     excel.setCell('sheet1', i, j, column)
    #     for sex in sexGroup:
    #         i = i + 1
    #         mean, std = getItemMean(sex, column)
    #         str = column + " : ", mean, " +/- ", std
    #         print(str)
    #         excel.setCell('sheet1', i, j, mean)
    #         excel.setCell('sheet1', i + 3, j, std)
    # excel.save(fileName)
    # excel.close()

    # 输出年龄10项指标均值情况
    # fileName = "E:\\workProjects\\NetLab530\\depression\\output\\result\\年龄对scl9010个因子的影响.xlsx"
    # excel = easyExcel(fileName)
    # i = j = 1
    # for column in columnList:
    #     i = 1
    #     j = j + 1
    #     excel.setCell('sheet1', i, j, column)
    #     for age in ageGroup:
    #         i = i + 1
    #         mean, std = getItemMean(age, column)
    #         str = column + " : ", mean, " +/- ", std
    #         print(str)
    #         excel.setCell('sheet1', i, j, mean)
    #         excel.setCell('sheet1', i + 8, j, std)
    # excel.save(fileName)
    # excel.close()

    # 输出性别超标比例
    # j = 1
    # fileName = "E:\\workProjects\\NetLab530\\depression\\output\\result\\性别对scl9010个因子的影响.xlsx"
    # excel = easyExcel(fileName)
    # for k in range(9):
    #     i = 7
    #     j = j + 1
    #     column = columnList[k]
    #     consLevel = consLevelList[k]
    #     for sex in sexGroup:
    #         i = i + 3
    #         count, rate = getItemCount(sex, column, consLevel)
    #         print(count, rate)
    #         excel.setCell('sheet1', i, j, count)
    #         excel.setCell('sheet1', i + 1, j, rate)
    # excel.save(fileName)
    # excel.close()

    # 输出年龄超标比例
    # j = 1
    # fileName = "E:\\workProjects\\NetLab530\\depression\\output\\result\\年龄对scl9010个因子的影响.xlsx"
    # excel = easyExcel(fileName)
    # for k in range(9):
    #     i = 19
    #     j = j + 1
    #     column = columnList[k]
    #     consLevel = consLevelList[k]
    #     for age in ageGroup:
    #         i = i + 2
    #         count, rate = getItemCount(age, column, consLevel)
    #         print(count, rate)
    #         excel.setCell('sheet1', i, j, count)
    #         excel.setCell('sheet1', i + 1, j, rate)
    # excel.save(fileName)
    # excel.close()

    # 输出10个因子，每个因子的相关性系数
    # elementResult = []
    # for element in columnList:
    #     elementResult.append(getItemCorr(dataFrame, element))

    # 输出整体的相关性系数
    # corrResult = dataFrame.corr('pearson')

    # 表与表之间的关联
    dataFrame.drop(columns=['NUMBER', 'AGE', 'SEX', 'EDUCATION', 'MARRIAGE', 'DATE', 'LAST', 'YYSTR2', 'YYSTR1'], inplace=True)
    # scl90 = dataFrame[columnList]
    sas = readSAS(sasFilePath)
    sds = readSDS(sdsFilePath)
    psqi = readSDS(psqiFilePath)
    result = []
    result1 = diagramCorr(dataFrame, sas)['YS']
    result.append(result1)
    result2 = diagramCorr(dataFrame, sds)['ZF']
    result.append(result2)
    result3 = diagramCorr(dataFrame, psqi)['ZF']
    result.append(result3)

