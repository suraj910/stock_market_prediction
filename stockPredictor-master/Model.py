from json import load
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential, Model, model_from_json
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.applications import vgg16
from keras.layers import Input
import matplotlib.pyplot as plt
import os
import cv2
from contextlib import suppress
import pickle
import pandas as pd
from pandas_datareader import data as pdr
import tensorflow as tf
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
import json

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
CACHE_PATH = os.path.join(ROOT_PATH, '@cache')
ASSET_PATH = os.path.join(ROOT_PATH, 'Atemp')
STORE_PATH = os.path.join(ROOT_PATH, 'Storage')
MODEL_PATH = os.path.join(STORE_PATH, 'exported_model')


# switch to cpu if gpu is unavailable in the system
if (len(tf.config.experimental.list_physical_devices('GPU'))) < 1:
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

yf.pdr_override()  # <== that's all it takes :-)

# download dataframe
today = date.today()


def stockReader(stock, start, end):
    if not end:
        end = today
    return pdr.get_data_yahoo("^NSEI", start=start, end=end)


# df = stockReader("^NSEI", "2018-01-01", end=today)

def ModelPredictor(date='2018-01-01') -> float:
    try:
        loaded_model = keras.models.load_model(MODEL_PATH)

        scaler = MinMaxScaler(feature_range=(0, 1))

        # get the quote
        nifty_quote = stockReader('^NSEI', start=date, end=today)

        # create a new dataframe
        new_df = nifty_quote.filter(['Close'])

        # get the last 60 day closing price values and convert the dataframe to an array
        last_range_days = new_df[-60:].values

        obj = scaler.fit(last_range_days)

        # # #scale the data to be values between 0 and 1
        last_range_days_scaled = obj.transform(last_range_days)

        # # #create an empty list
        X_test = []

        # # #APPEND THE LAST 60 DAYS
        X_test.append(last_range_days_scaled)

        # # #convert the X_test data set to np array
        X_test = np.array(X_test)

        pred_price = loaded_model.predict(X_test)
        final_price = obj.inverse_transform(pred_price)[0]

        return final_price
    except(Exception) as e:
        print("--------- Errrorrrrrr ------")
        return -1.0


if __name__ == '__main__':
    result = ModelPredictor()

    with open(file='result.json', mode='w+') as f:
        string_res = json.dumps({
            "result": str(result[0])
        })
        f.write(string_res)
