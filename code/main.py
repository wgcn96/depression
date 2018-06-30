# -*- coding: UTF-8 -*-

import os
import sys
sys.path.append('E:\\workProjects\\NetLab530\\depression\\code')
import os.path
from fileTree import getAllDBF
from convertFile import *
import logging

print('begin')
workDir = 'D:\\workData\\中山二院抑郁症项目\\惠诚数据\\data'
outputDir = 'E:\\workProjects\\NetLab530\\depression\\output\\originTransport'
fileList = getAllDBF(workDir)
count = 0
throwCount = 0
for item in fileList:
    curDataPath, curFileName = os.path.split(item)
    curFileName, curFileExtension = os.path.splitext(curFileName)

    if curFileExtension == '.dbf' or curFileExtension == '.DBF':
        print('current file: ', curFileName + curFileExtension)
        outFileName = curFileName + '.csv'
        outputFile = os.path.join(outputDir, outFileName)
        try:
            dbf2csv(item, outputFile)
            count += 1
        except BaseException as e:
            logging.exception(e)
            print('dealing with ', curFileName + curFileExtension, 'thrown an error, pass it!')
            throwCount += 1
            continue
print('Finish!, total deal with {0} files, throw error {1} files'.format(count,throwCount))
