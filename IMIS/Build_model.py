import pandas as pd
from datetime import date,datetime
from numpy import array
from scipy.signal import detrend
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional
import pickle
import pyodbc as odbc

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
c.execute("select * from LichSuGD")
dfLSGD=c.fetchall()
data =[]
for i in dfLSGD:
    i=tuple(i)
    data.append(i)
names = [ x[0] for x in c.description]
dfLSGD = pd.DataFrame(data, columns=names)
df1 = dfLSGD[dfLSGD['Đơn giá'].astype(str).str.len() == 9]
current_year = datetime.datetime.now().year
df1 = df1[df1['Ngày tính tồn kho'].dt.year < current_year]
df1=df1.rename(columns={'Số lượng':'Demand','Ngày tính tồn kho':'Date'})
# Chuyển đổi cột ngày tháng sang định dạng datetime
df1['Date'] = pd.to_datetime(df1['Date'])
# split a univariate sequence
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
# Define a list to store your models
models = {}
min=pd.to_datetime(date(2022,1,1))
max=pd.to_datetime(date(2022,12,31))
# Tạo một chuỗi ngày tháng liên tục từ ngày nhỏ nhất đến ngày lớn nhất
date_range = pd.date_range(start=min, end=max)
# Tạo một DataFrame mới với cột ngày tháng liên tục
new_df = pd.DataFrame({'Date': date_range})
for name, group in df1.groupby(["Mã hàng"]):
    # Sử dụng hàm merge để kết hợp hai DataFrame
    group = pd.merge(new_df, group, on='Date', how='left')
    group['Demand'] = group['Demand'].fillna(0)
    group['Month']=group['Date'].dt.month
    group = group.groupby(['Month']).agg({'Demand': 'sum'}).reset_index()
    detrended = detrend(group['Demand'], type='linear')
    detrended = pd.Series(detrended, index=group.index)
    # define input sequence
    raw_seq = detrended
    # choose a number of time steps
    n_steps = 3
    # split into samples
    X, y = split_sequence(raw_seq, n_steps)
    q_80 = int(len(X) * .8)
    X_train, y_train = X[:q_80], y[:q_80]
    X_test, y_test = X[q_80:], y[q_80:]
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)
    # reshape from [samples, timesteps] into [samples, timesteps, features]
    n_features = 1
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], n_features))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], n_features))
    # define model
    model = Sequential()
    model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(n_steps, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X_train, y_train, epochs=200, verbose=0)
    # Append the trained model to the list
    models[name]=model
# Save the list of models using pickle
with open('models.pkl', 'wb') as f:
    pickle.dump(models, f)
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1]))
X_test = scaler.inverse_transform(X_test)
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1],n_features))
yhat = model.predict(X_test, verbose=0)
print(yhat)