import pyodbc as odbc
import pandas as pd
DRIVER_NAME='SQL Server'
SERVER_NAME='DESKTOP-TF6BQMV\SQLEXPRESS01'
DATABASE_NAME='SCM'
connection_string= f"""
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
Trust_Connection=yes;
"""
conn=odbc.connect(connection_string)
c=conn.cursor()
# c.execute("select LichSuGD.MaHang,TenHang,NgayXK, sum(SLXuat) as NhuCau from LichSuGD,HangHoa where LichSuGD.MaHang=HangHoa.MaHang group by LichSuGD.MaHang,TenHang,DonGia,NgayXK")
# df1=c.fetchall()
# data =[]
# for i in df1:
#     i=tuple(i)
#     data.append(i)
# names = [ x[0] for x in c.description]
# df1 = pd.DataFrame(data, columns=names)
# a = df1.groupby(['MaHang']).NhuCau.agg(['mean', lambda x: x.std(ddof=0)])
# a.columns=['mean','std']
# a['std']=a['std'].apply(lambda x: round(x, 2))
# a['mean']=a['mean'].apply(lambda x: round(x, 2))
# a=a.reset_index()
# dfABC=AppFunction.ABCAnalysis(self)
# df=pd.merge(a,dfABC,on='MaHang',how='inner')
# df['ServiceLevel']=np.where(df['Class']=='A',80,np.where(df['Class']=='B',90,99))
# df['R']= np.round(norm.ppf(df['ServiceLevel'],df['mean'],df['std']),decimals=2)
# df['z']=(df['R']-df['mean'])/df['std']
# df['SS']=df['z']*df['std']
# c.execute("select B048.MaHang,TenHang,TongTon from B048,HangHoa where B048.MaHang=HangHoa.MaHang")
# dfB048=c.fetchall()
# data1 =[]
# for i in dfB048:
#     i=tuple(i)
#     data1.append(i)
# names1 = [ x[0] for x in c.description]
# dfB048 = pd.DataFrame(data1, columns=names1)
# dfB048=dfB048.groupby(['MaHang','TenHang'])['TongTon'].sum()
# dfB048=dfB048.reset_index()
# df=pd.merge(df,dfB048,on='MaHang',how='inner')
# df=df[df['TongTon']<df['SS']]
# df['Ty le']=df['TongTon']/df['SS']
# df["Ty le"] = df["Ty le"].apply(lambda x: x * 100)
# df["Ty le"] = df["Ty le"].round(1)
# df1=df[['MaHang','TenHang','TongTon','SS','Ty le']]
# import numpy as np
# from scipy.stats import norm
# print(norm.ppf(0.95,loc=50))
# import pandas as pd
# df1 = pd.DataFrame({'lkey': [0, '02-12-2023', '01-01-2024', '02-01-2024'],
#                     'value': [1, 2, 3, 5]})
# df2 = pd.DataFrame({'lkey': ['foo1', 'bar1', 'baz1', 'foo'],
#                     'value': [5, 6, 7, 8]})
# df=df1.merge(df2,on='lkey',how='left')
# t = pd.to_datetime(0)
# a='02/12/2023'
# b=pd.to_datetime(df1['lkey'])
import copy

# main_list = [29, 49, ["Q", "R"]]
# shallow_copy = copy.copy(main_list)

# Chỉnh sửa danh sách lồng nhau
# shallow_copy[2][0] = 99
# main_list[2][1] = 100
# print(f"The main list: {main_list}") #[29, 49, [99, 100]]
# print(f"The shallow copy list: {shallow_copy}") #[29, 49, [99, 100]]
# Chỉnh sửa các mục bên ngoài
# shallow_copy[0] = "M"
# main_list[1] = "N"
# print(f"The main list: {main_list}") #[29, 'N', ['Q', 'R']]  
# print(f"The shallow copy list: {shallow_copy}") #['M', 49, ['Q', 'R']]
### DEEPCOPY
# main_list = [200, 300, ["I", "J"]]
# deep_copy = copy.deepcopy(main_list)
# # Chỉnh sửa danh sách bên trong và bên ngoài
# deep_copy[2][0] = "K"
# main_list[0] = 500
# print(f"The main list: {main_list}") #[500, 300, ['I', 'J']]
# print(f"The deep copy list: {deep_copy}") #[200, 300, ['K', 'J']]
# import pandas as pd

# df = pd.DataFrame({'col': [10, 20, 30, 40, 50, 60, 70, 80, 90]})
# df = df.T
# print(df)
# a=[1,1,2,3]
# print(set(a))
import pandas as pd
import numpy as np
from datetime import date
from numpy import array
from scipy.signal import detrend
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional
import pickle

# c.execute("select LichSuGD.MaHang,TenHang,NgayXK,SLXuat as NhuCau from LichSuGD,HangHoa where LichSuGD.MaHang=HangHoa.MaHang")
# df1=c.fetchall()
# data =[]
# for i in df1:
#     i=tuple(i)
#     data.append(i)
# names = [ x[0] for x in c.description]
# df1 = pd.DataFrame(data, columns=names)
df1=pd.read_excel(r'D:\IMIS\Dashboard\LSGD T1-T10.xlsx')
df1=df1.rename(columns={'Mã hàng':'MaHang','Ngày tính tồn kho':'NgayXK','Số lượng':'NhuCau'})
with open('models.pkl', 'rb') as f:
    models = pickle.load(f)
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)
mh=[]
tbinh=[]
dlc=[]
min=pd.to_datetime(date(2022,1,1))
max=pd.to_datetime(date(2022,12,31))
gtrilon=list(models.keys())
# Tạo một chuỗi ngày tháng liên tục từ ngày nhỏ nhất đến ngày lớn nhất
date_range = pd.date_range(start=min, end=max)
# Tạo một DataFrame mới với cột ngày tháng liên tục
new_df = pd.DataFrame({'NgayXK': date_range})
for name, group in df1.groupby(["MaHang"]):
    #Sử dụng hàm merge để kết hợp hai DataFrame
    mh.append(name[0])
    group['NgayXK']=pd.to_datetime(group['NgayXK'])
    group = pd.merge(new_df, group, on='NgayXK', how='left')
    group['NhuCau'] = group['NhuCau'].fillna(0)
    group['Month']=group['NgayXK'].dt.month
    group = group.groupby(['Month']).agg({'NhuCau': 'sum'}).reset_index()
    # define input sequence
    raw_seq = group['NhuCau'].values
    if name in gtrilon:
        model=models.get(name)
        n_steps = 3
        # split into samples
        X, y = split_sequence(raw_seq, n_steps)
        #demonstrate prediction for the 12 months
        x_input=X[-1].reshape((3,))
        temp_input=list(x_input)
        list_output=[]
        i=0
        while (i<12):
            if len(temp_input)>3:
                x_input=array(temp_input[1:])
                x_input=x_input.reshape((1,n_steps,1))
                yhat=model.predict(x_input,verbose=0)
                temp_input.append(yhat[0][0])
                temp_input=temp_input[1:]
                list_output.append(yhat[0][0])
                i+=1
            else:
                x_input=x_input.reshape((1,n_steps,1))
                yhat=model.predict(x_input,verbose=0)
                temp_input.append(yhat[0][0])
                list_output.append(yhat[0][0])
                i+=1
            # print(list_output)
        tb=np.round(np.average(list_output)/24,2)
        dl=np.round(np.std(list_output)/24,2)
        tbinh.append(tb)
        dlc.append(dl)
    else:
        tb=np.round(np.average(raw_seq)/24,2)
        dl=np.round(np.std(raw_seq)/24,2)
        tbinh.append(tb)
        dlc.append(dl)
# a = df1.groupby(['MaHang']).NhuCau.agg(['mean', lambda x: x.std(ddof=0)])
# a.columns=['mean','std']
# a['std']=a['std'].apply(lambda x: round(x, 2))
# a['mean']=a['mean'].apply(lambda x: round(x, 2))
# a=a.reset_index()
datadf = {
    'MaHang': mh,
    'mean': tbinh,
    'std': dlc}
a = pd.DataFrame(datadf)
print(a)
