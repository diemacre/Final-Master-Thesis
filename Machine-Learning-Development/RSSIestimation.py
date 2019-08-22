import pandas as pd
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
#from sklearn.impute import IterativeImputer

Pt = 4 # transmssion power of beacon
Gt = 2.15 # gain of beacon antenna
Gr = 2.15  # gain of mobile antenna
Freq = 2400000000 #frequency of bluetooth


def loadFile():
    data = pd.read_csv('./Datasets/databaseML.csv', delimiter=',')
    print('file loaded')
    return data


def formatData(data):
    newcolums=[]
    for i, row in data.iterrows():
        values = row['testid'].split('-')
        newcolums.append([values[0],values[1]])
    ndf = pd.DataFrame(np.array(newcolums).reshape(-1,2), columns=['t_pos', 't_num'])
    data = pd.concat([data, ndf], axis=1)
    return data

def landa(frequency):
    c = 299792458
    l = c/frequency
    return l

def distance(x_beacon, y_beacon, x_test, y_test):
    x = (x_beacon - x_test)**2
    y = (y_beacon - y_test)**2
    dist = math.sqrt(x + y)
    return dist

def pathLoss(distance, landa, pathLossExp = 3.5):
    loss = 10*math.log10(16*math.pi*(distance**pathLossExp)/landa)
    return loss

def friss(Pt, Gr, Gt, loss):
    Pr = Pt + Gt + Gr - loss
    return Pr

def estimateRSSI(data):
    newRSSIs=[]
    land = landa(Freq)
    for i, row in data.iterrows():
        pathLossExp = 3.5
        if row['b_floor'] != row['t_floor']:
            pathLossExp = 5
        x_beacon = row['b_x']
        y_beacon = row['b_y']
        x_test = row['t_x']
        y_test = row['t_y']
        dist = distance(x_beacon, y_beacon, x_test, y_test)
        loss = pathLoss(dist, land, pathLossExp)
        newRSSI = friss(Pt, Gr, Gt, loss)
        newRSSIs.append(newRSSI)
    ndf = pd.DataFrame(np.array(newRSSIs).reshape(-1, 1), columns=['newRSSI'])
    data = pd.concat([data, ndf], axis=1)
    return data


def split_data(data, testsize=0.2):
    data = data[data["testid"].str.contains('-36') != True]
    pass

def main():
    data = loadFile()
    print(data.head())
    data2 = data[['t_floor', 'rssi', 'testid', 'timestamp','t_x', 't_y', 'b_floor', 'b_x', 'b_y', 'b_minor']]
    print(data2.head())
    data2 = formatData(data2)
    print(data2.head())
    data2 = estimateRSSI(data2)
    print(data2.head())

    X = data2[['rssi','t_floor', 'b_x', 'b_y']]
    y = data2['newRSSI']
    #values = np.asarray(data2['testid'].value_counts().keys())
    #print(values)

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

    linear = LinearRegression()
    linear.fit(X_train, y_train)

    y_pred = linear.predict(X_test)
    mean_absolute = mean_absolute_error(y_test, y_pred)
    mean_squared = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print('mean_absolute_error: ', mean_absolute)
    print('mean_squared_error: ', mean_squared)
    print('r2_score: ',r2)


if __name__ == "__main__":
    main()
