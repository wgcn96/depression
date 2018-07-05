# -*- coding: UTF-8 -*-

# function: 在指定根目录下建立搜索树，返回列表类型
# author: wangchen

import os
import os.path



def getAllDBF(workDir):
    filePathList = []
    for parent, dirNames, fileNames in os.walk(workDir):
        '''
        for dirName in dirNames:
            print(parent,dirName)
        '''

        for fileName in fileNames:
            # if fileName.endswith('.dbf') or fileName.endswith('.DBF'):
            currentPath = os.path.join(parent, fileName)
            filePathList.append(currentPath)

    return filePathList


if __name__ == '__main__':
    workDir = 'D:\\workData\\中山二院抑郁症项目\\惠诚数据\\data'
    fileList = getAllDBF(workDir)
    print(fileList)
