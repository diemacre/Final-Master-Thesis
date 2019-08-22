import pandas as pd
import numpy as np
import math

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

'''
This function loads the file from a given path.
'''


def distance(x_beacon, y_beacon, x_test, y_test):
    x = (x_beacon - x_test)**2
    y = (y_beacon - y_test)**2
    dist = math.sqrt(x + y)
    return dist


def createdataframe(data, test_data, pred_data):

    test_data = pd.DataFrame(test_data, columns= ['t_x','t_y'])
    pred_data = pd.DataFrame(pred_data, columns=['p_x', 'p_y'])
    frame = pd.concat([data, test_data, pred_data], axis=1, sort=False)
    error = []
    for i, row in frame.iterrows():
        error.append(distance(float(row['t_x']), float(row['t_y']), float(row['p_x']), float(row['p_y'])))
    error = pd.DataFrame(error, columns=['error'])

    frame = frame = pd.concat([frame, error], axis=1, sort=False)
    return frame


def prediction(X_train, Y_train, X_test, Y_test, model):

    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)

    mean_absolute = mean_absolute_error(Y_test, Y_pred)
    mean_squared = mean_squared_error(Y_test, Y_pred)
    r2 = r2_score(Y_test, Y_pred)


    print('Used model: ',model)
    print('mean_absolute_error: ', mean_absolute)
    print('mean_squared_error: ', mean_squared)
    print('r2_score: ', r2)


    return Y_pred



