# -*- coding: utf-8 -*-
"""***** 2. MANUAL GITAML 2023 STOCK MARKET PREDICTOR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U7xN577t1fceaWRedUQKljL4-DlqsjdF
"""

ranst = "A" # @param {type:"string"}
!pip install yfinance --upgrade --no-cache-dir
!pip install mysql-connector-python
!pip install requests_html
!pip install yahoo_fin
!pip install plotly
!pip install finplot
!pip install technic
!pip install matplotlib
!pip insall keras
!pip install sklearn
import finplot as fplt
import matplotlib.dates as mpl_dates
import mysql.connector as mysql
import math
import os, sys
!pip install --upgrade pandas-datareader
!pip install selenium
!apt-get update
!apt install chromium-chromedriver
from selenium import webdriver
import pandas_datareader as pdr
import numpy as np
import pandas as pd
from datetime import date
from datetime import date, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.linear_model import LinearRegression
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import yfinance as yf
import sys
from termcolor import cprint

import decimal
from decimal import Decimal
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import get_analysts_info
plt.style.use('fivethirtyeight')
import random
from yahoo_fin import stock_info as si
import random

df1 = pd.DataFrame(si.tickers_dow() )
df2 = pd.DataFrame(si.tickers_nasdaq() )
df3 = pd.DataFrame(si.tickers_sp500() )

df5 = pd.DataFrame(si.tickers_other() )
sym1 = set( symbol for symbol in df1[0].values.tolist() )
sym2 = set( symbol for symbol in df2[0].values.tolist() )
sym3 = set( symbol for symbol in df3[0].values.tolist() )

sym5 = set( symbol for symbol in df5[0].values.tolist() )
symbols = set.union( sym1, sym2, sym3, sym5 )
my_list = ['W', 'R', 'P', 'Q']
del_set = set()
sav_set = set()
for symbol in symbols:
    if len( symbol ) > 4 and symbol[-1] in my_list:
        del_set.add( symbol )
    else:
        sav_set.add( symbol )
sto = list(sav_set)
#sto = str(sav_set)
print( f'Removed {len( del_set )} unqualified stock symbols...' )
print( f'There are {len( sav_set )} qualified stock symbols...' )
print(sto)
import random
random.shuffle(sto)
rans = sto[2]
print(rans)
#ranst = rans.replace("$", "-")
    #ransto

ransto = str(ranst)
ransto

#sp500.index
#sp500.drop(['Open', 'High', 'Low', 'Dividends', 'Volume','Stock Splits'],axis=1,inplace=True)

sp500 = yf.Ticker(ransto)
#sp500 = yf.Ticker("AAPL")
sp500 = sp500.history(period="max")

import os
del sp500["Dividends"]
del sp500["Stock Splits"]
sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)
sp500 = sp500.loc["1990-01-01":].copy()
model = RandomForestClassifier(n_estimators=100,min_samples_split=100,random_state=1)

train = sp500.iloc[:-100]
test = sp500.iloc[-100:]

predictors = ["Close","Volume","Open","High","Low"]
model.fit(train[predictors], train["Target"])

preds = model.predict(test[predictors])
preds = pd.Series(preds, index=test.index)
precision_score(test["Target"], preds)

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict(test[predictors])
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

def backtest(data, model, predictors, start=2500, step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()
        predictions = predict(train, test, predictors, model)
        all_predictions.append(predictions)

    return pd.concat(all_predictions)

predictions = backtest(sp500, model, predictors)

predictions["Predictions"].value_counts()

precision_score(predictions["Target"], predictions["Predictions"])

predictions["Target"].value_counts() / predictions.shape[0]

horizons = [2,5,60,250,1000]
new_predictors = []

for horizon in horizons:
    rolling_averages = sp500.rolling(horizon).mean()

    ratio_column = f"Close_Ratio_{horizon}"
    sp500[ratio_column] = sp500["Close"] / rolling_averages["Close"]

    trend_column = f"Trend_{horizon}"
    sp500[trend_column] = sp500.shift(1).rolling(horizon).sum()["Target"]

    new_predictors+= [ratio_column, trend_column]

sp500 = sp500.dropna(subset=sp500.columns[sp500.columns != "Tomorrow"])

sp500

model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

def predict(train, test, predictors, model):
    model.fit(train[predictors], train["Target"])
    preds = model.predict_proba(test[predictors])[:,1]
    preds[preds >=.6] = 1
    preds[preds <.6] = 0
    preds = pd.Series(preds, index=test.index, name="Predictions")
    combined = pd.concat([test["Target"], preds], axis=1)
    return combined

predictions = backtest(sp500, model, new_predictors)

predictions["Predictions"].value_counts()

precision_score(predictions["Target"], predictions["Predictions"])

predictions["Target"].value_counts() / predictions.shape[0]

predictions