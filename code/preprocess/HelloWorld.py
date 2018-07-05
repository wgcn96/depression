# -*- coding:UTF-8 -*-

import dbfread
from dbfread import DBF

print("Hello World")
table = DBF("D:\\workData\\中山二院抑郁症项目\\惠诚数据\\data\\Database1\\16pf.dbf", encoding='cp936')


for record in table:
    print(record)

for e in record:
    print(e)


print(table.field_names)

print(len(table))