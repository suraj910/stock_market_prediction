# %%
import yfinance as yf
import pandas as pd


# %%
import math
import pandas_datareader as web
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
from keras.layers import Dropout
from keras.layers import *
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
from datetime import date,timedelta
today = date.today()
#print("Today's date:", today)
tomorrow = date.today()+timedelta(days=1)
print(tomorrow)

# %%
df = web.DataReader('^NSEI',data_source='yahoo',start='2018-01-01',end=today)
df

# %%
df.shape

# %%
plt.figure(figsize=(16,8))
plt.title('Closing Price')
plt.plot(df['Close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Closing price',fontsize=18)
plt.show()


# %%
data=df.filter(['Close'])
#convert dataframe into numpy array
dataset=data.values
#getting number of rows for training
training_data_len=math.ceil(len(dataset)*0.8)
training_data_len



# %%
#scale the data
scaler=MinMaxScaler(feature_range=(0,1))
#transform data into (0,1)
scaled_data = scaler.fit_transform(dataset) #computes the minimum and maximum values and scales all the values accordingly
scaled_data

# %%
#create the scaled training dataset
train_data=scaled_data[0:training_data_len,:]
#split the datainto x_train and y_train
x_train=[]
y_train=[]

for i in range (60, len(train_data)):
    x_train.append(train_data[i-60:i,0])  #not including i and it will contain first 60 values(0 to 59)
    y_train.append(train_data[i,0])    #this will contain the 61st value(60th position) that we want out model to predict
    if i <=61:
        print(x_train)
        print(y_train)
        print()

# %%
#convert x_train y_train to numpy array so we can use them to train Lstm model
x_train,y_train = np.array(x_train), np.array(y_train)

# %%
#reshape the xtrain data --> lstm network expects input to be 3d 
x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))    #(1168,60,1)
x_train.shape

# %%
#create LSTM model
model=Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.1))

model.add(LSTM(50, return_sequences=True))
model.add(Dropout(0.1))

model.add(LSTM(50, return_sequences=True))
model.add(Dropout(0.1))

model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.1))

#model.add(Dense(25))
model.add(Dense(1))


# %%
#COMPILE MODEL
model.compile(optimizer='adam',loss='mean_squared_error')

# %%
#train the model
model.fit(x_train,y_train,batch_size=32,epochs=25) #epoch is number of iteration 

# %%
#create the testing dataset
#creating new array containing scaled values from index 1168 to 1228
test_data = scaled_data[training_data_len-60:, :]
#create datasets x_test y test
x_test=[]
y_test=dataset[training_data_len:, :]   #this will consist the values that we want our model to predict
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i,0])    #x_test contains the past 60 values

# %%
#convert data to numpy array
x_test = np.array(x_test)

# %%
#reshape the data
x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

# %%
#get the model predicted price value
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)    #unscaling the values back from 0 and 1 to original value

# %%
#get the RMS error --> shows accuracy (lower the value better the model)
rmse = np.sqrt(np.mean(predictions - y_test)**2)
rmse

# %%
#plot data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions'] = predictions
#visualise the data
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price',fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.legend(['Train','Val','Predictions'],loc='lower right')
plt.savefig('static/assets/images/predict.png')
plt.show()

# %%
#show the valid and predicted price
valid

# %%
#get the quote
nifty_quote = web.DataReader('^NSEI',data_source='yahoo',start='2016-01-01',end=today)
#create a new dataframe
new_df = nifty_quote.filter(['Close'])
#get the last 60 day closing price values and convert the dataframe to an array 
last_60_days = new_df[-60:].values
#scale the data to be values between 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)
#create an empty list
X_test = []
#APPEND THE LAST 60 DAYS
X_test.append(last_60_days_scaled)
#convert the X_test data set to np array
X_test = np.array(X_test)
#Reshape
X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
#get predicted scaled price
pred_price = model.predict(X_test)
pred_price = scaler.inverse_transform(pred_price)

tomorrow_pred = []
tomorrow_pred.append(pred_price)
#print(pred_price)
#nifty_quote

# %%


# %%



