# -*- coding:UTF-8 -*-

# function: 读取dbf格式文件，转化为excel格式
# author: wangchen

import os
import os.path
import dbfread
from easyExcel import *
from win32com import client
import csv

'''
def dbf2xls(dbfilename, exfilename):
    db = dbfread.DBF(dbfilename, load=True, encoding='cp936')
    ex = client.Dispatch('Excel.Application')

    ex.Visible = 0  # 后台运行，不显示，不警告
    ex.DisplayAlerts = 0

    wk = ex.Workbooks.Add()
    ws = wk.ActiveSheet

    r = 1
    c = 1
    for field in db.field_names:
        ws.Cells(r, c).Value = field
        c = c + 1
    r = 2
    for record in db:
        c = 1
        for field in db.field_names:
            ws.Cells(r, c).Value = str(record[field])
            c = c + 1
        r = r + 1
    wk.SaveAs(exfilename)
    wk.Close(False)
    ex.Application.Quit()
'''


def dbf2excel(dbfFileName, excelFileName):
    dbf = dbfread.DBF(dbfFileName, load=True, encoding='cp936', char_decode_errors='ignore')

    if os.path.exists(excelFileName) == True:
        excel = easyExcel(excelFileName)
        r = excel.getRowNumber
        for record in dbf:
            c = 1
            for field in dbf.field_names:
                excel.setCell('sheet1', r, c, record[field])
                c = c + 1
            r = r + 1
        excel.save()
    else:
        excel = easyExcel()
        r = 1
        c = 1
        for field in dbf.field_names:
            excel.setCell('sheet1', r, c, field)
            c = c + 1
        r = 2
        for record in dbf:
            c = 1
            for field in dbf.field_names:
                excel.setCell('sheet1', r, c, record[field])
                c = c + 1
            r = r + 1
        excel.save(excelFileName)
    excel.close()


def dbf2csv(dbfFileName, csvFileName):
    dbf = dbfread.DBF(dbfFileName, load=True, encoding='cp936', char_decode_errors='ignore')

    csvFile = open(csvFileName, mode='a', newline='')
    csvWriter = csv.writer(csvFile)

    csvWriter.writerow(dbf.field_names)
    for record in dbf:
        csvWriter.writerow(list(record.values()))



if __name__ == '__main__':
    print("Work begin...")
    dbffilename = "D:\\workData\\中山二院抑郁症项目\\惠诚数据\\data\\Database1\\bprs.dbf"
    xlsfilename = "E:\\workProjects\\NetLab530\\depression\\bprs.csv"
    dbf2csv(dbffilename, xlsfilename)
    print("Finish!")
