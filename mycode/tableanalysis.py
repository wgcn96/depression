import pandas
import numpy
from mycode.statistic.readSCL90 import readAndfilt

columns = [0, 1, 2, 3, 8, 9, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
columns_name = ['NUMBER', 'NAME', 'AGE', 'SEX', '总分', '总均分', '阳性项目数',
                '阳性项目均分', '躯体化', '强迫', '人际关系', '抑郁', '焦虑',
                '敌对', '恐怖', '偏执', '精神病性']

data = readAndfilt('../output/originTransport7/scl90.csv')

df = data[data['AGE'] < 100]
print('scl90总数据:')
print(df.shape)
#df = df[df.duplicated('NUMBER')==False]
df = df.drop_duplicates('NUMBER', keep=False)
print(df.shape)
df = df.dropna(how='any')
df = df.drop_duplicates('NAME', keep=False)
print(df.shape)

number_list = df['NAME'].tolist()
#print(number_list)
#number_list = list(map(int, number_list))
#print(number_list)

print(df.groupby('SEX').size())

df_male = []    #男性
df_female = []  #女性

for name, group in df.groupby('SEX'):
    if name == '男':
        df_male = group
        print(df_male.shape)
    elif name == '女':
        df_female = group
        print(df_female.shape)

from scipy import stats
col = ['总均分', '阳性项目均分', '躯体化', '强迫', '人际关系', '抑郁', '焦虑', '敌对', '恐怖', '偏执', '精神病性']
col2 = ['AGE','总分', '总均分', '阳性项目数', '阳性项目均分', '躯体化', '强迫',
        '人际关系', '抑郁', '焦虑', '敌对', '恐怖', '偏执', '精神病性']

X = df_male[col]    #男
Y = df_female[col]  #女
corr_result = df[col].corr()
corr_result.to_excel('SCL90各因子之间的相关性.xls')
print(corr_result)
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
plt.title('SCL90各因子相关性分析')
sns.heatmap(corr_result, cmap="YlGnBu")
plt.show()
# print(X.describe())
# print(Y.describe())
# print(X.mean().tolist())
#print(stats.ttest_ind(X, Y))
from scipy.stats import levene
#print(levene(df_male['总分'], df_female['总分']))

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
plt.figure(figsize=(8, 5))
xlen = list(range(len(X.mean().tolist())))
total_width, n = 0.8, 2
width = total_width / n

plt.bar(xlen, X.mean().tolist(), width=width, label='male', tick_label=col, fc='steelblue')
for i in range(len(xlen)):
    xlen[i] = xlen[i] + width
plt.bar(xlen, Y.mean().tolist(), width=width, label='female', fc='r')
plt.title('SCL90按性别分组各因子均值比较')
plt.legend()
plt.show()

def groupbyage(dataframe):
    b = []
    #print(dataframe.head(2))
    for a in dataframe.AGE:
        if a < 18:
            b.append(1)
        elif 18 <= a < 25:
            b.append(2)
        elif 25 <= a < 35:
            b.append(3)
        elif 35 <= a < 45:
            b.append(4)
        elif 45 <= a < 55:
            b.append(5)
        elif a >= 55:
            b.append(6)
        #print(a)
    print(dataframe.groupby(b).size())
    return dataframe.groupby(b)

data_age_group = groupbyage(df)

df_18 = []      # <18
df_25 = []      # 18~25
df_35 = []      # 25~35
df_45 = []      # 35~45
df_55 = []      # 45~55
df_gt55 = []    # >55

for name, group in data_age_group:
    if name == 1:
        df_18 = group[col]
    elif name == 2:
        df_25 = group[col]
    elif name == 3:
        df_35 = group[col]
    elif name == 4:
        df_45 = group[col]
    elif name == 5:
        df_55 = group[col]
    elif name == 6:
        df_gt55 = group[col]

plt.figure(figsize=(12, 6))
xlen = list(range(len(df_18.mean().tolist())))
total_width, n = 0.8, 6
width = total_width / n

plt.bar(xlen, df_18.mean().tolist(), width=width, label='<18', fc='lightskyblue')
for i in range(len(xlen)):
    xlen[i] = xlen[i] + width
plt.bar(xlen, df_25.mean().tolist(), width=width, label='18~25', fc='gray')
for i in range(len(xlen)):
    xlen[i] = xlen[i] + width
plt.bar(xlen, df_35.mean().tolist(), width=width, label='25~35', tick_label=col, fc='yellowgreen')
for i in range(len(xlen)):
    xlen[i] = xlen[i] + width
plt.bar(xlen, df_45.mean().tolist(), width=width, label='35~45', fc='orange')
for i in range(len(xlen)):
    xlen[i] = xlen[i] + width
plt.bar(xlen, df_55.mean().tolist(), width=width, label='45~55', fc='steelblue')
for i in range(len(xlen)):
    xlen[i] = xlen[i] + width
plt.bar(xlen, df_gt55.mean().tolist(), width=width, label='>55', fc='red')
plt.title('SCL90按年龄分组各因子均值比较')
plt.legend()
plt.show()

def corranalysis(columns_sds, columns_name_sds, filename, df90, name1, name2='SCL90', yinzi='抑郁标准分'):
    data_sds = pandas.read_csv(filename, encoding='utf-8',  usecols=columns_sds, names=columns_name_sds, header=0)
    data_sds['AGE'].astype(int)
    data_sds['NAME'].astype(numpy.str)
    data_sds = data_sds[data_sds['AGE'] < 100]
    #print(name1 + '总数据:')
    #print(data_sds.shape)
    data_sds = data_sds.drop_duplicates('NAME', keep=False)
    #print(data_sds.shape)
    data_sds = data_sds.dropna(how='any')


    tmp_data_sds = data_sds[data_sds['NAME'].isin(number_list)]
    number_list_sds = tmp_data_sds['NAME'].tolist()
    tmp_data_scl90 = df90[df90['NAME'].isin(number_list_sds)]

    tmp_data_sds = tmp_data_sds.sort_values(by = 'NAME',axis = 0,ascending = True)
    tmp_data_scl90 = tmp_data_scl90.sort_values(by = 'NAME',axis = 0,ascending = True)
    # print(tmp_data_sds.head(5))
    # print(tmp_data_scl90.head(5))
    df_corr = pandas.merge(tmp_data_sds[['NAME', yinzi]], tmp_data_scl90, how='inner', on='NAME')
    col3 = [yinzi, 'AGE', '总分', '总均分', '阳性项目数', '阳性项目均分', '躯体化', '强迫',
            '人际关系', '抑郁', '焦虑', '敌对', '恐怖', '偏执', '精神病性']
    df_corr = df_corr[col3]

    corr_list = []
    #print(df_corr.corr()[yinzi])
    corr_list = df_corr.corr()[yinzi].tolist()
    corr_list.pop(0)
    print(corr_list)
    # print(name1 + '与' + name2 + '各项因子的相关性分析：')
    # for a in col2:
    #     cl = tmp_data_sds[yinzi].corr(tmp_data_scl90[a])
    #     print(a + ': ' + str(cl))
    #     corr_list.append(cl)
    return corr_list

columnsSds = [0, 1, 2, 3, 8, 9]
columnsNameSds = ['NUMBER', 'NAME', 'SEX', 'AGE', '抑郁总分', '抑郁标准分']
corr_list1 = corranalysis(columnsSds, columnsNameSds, 'csv/sds.csv', df, 'SDS标准总分', yinzi='抑郁标准分')

columnsSds = [0, 1, 2, 3, 8, 9]
columnsNameSds = ['NUMBER', 'NAME', 'AGE', 'SEX', '焦虑总分', '焦虑标准分']
corr_list2 = corranalysis(columnsSds, columnsNameSds, 'csv/sas.csv', df, 'SAS标准总分', yinzi='焦虑标准分')

columnsSds = [0, 1, 2, 3, 8]
columnsNameSds = ['NUMBER', 'NAME',  'SEX', 'AGE', '睡眠质量指数总分']
corr_list3 = corranalysis(columnsSds, columnsNameSds, 'csv/Psqi.csv', df, 'Psqi总分', yinzi='睡眠质量指数总分')

result = pandas.DataFrame([corr_list1, corr_list2, corr_list3], index=['SDS标准总分', 'SAS标准总分', 'Psqi总分'], columns=col2)
result.to_excel('SCL90与SDS、SAS、Psqi相关性.xls')
plt.title('SCL90与SDS、SAS、Psqi相关性分析')
sns.heatmap(result, cmap="YlGnBu", vmin=-1, vmax=1)
plt.show()

# df1=pandas.DataFrame({'key':['a','b','c', 'd'],'data1':range(3)})
# print(df1)
# df2=pandas.DataFrame({'key':['b','c', 'a'],'data2':range(3)})
# print(df2)
# print(pandas.merge(df1,df2, how='inner', on='key'))