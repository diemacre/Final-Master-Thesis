'''
This file formats and creates the matrices for the machine learning study. It takes the raw measures and transform each taken 
measure into a single row. This row contains all the detected beacons associated with its meadian rssi during that measure.
'''

import pandas as pd
import numpy as np
import math

'''
This function created an empty dataframe than contains the possible beacons for the studied building.
'''
def createEmptyDataFrame(data):
    values = np.array(data['b_minor'].value_counts().keys())
    values = np.append(values, ['t_x','t_y'])
    values = np.append(['testid'],values)
    return pd.DataFrame(columns=values)

def fillDataframe(data, dataframe):
    colums = dataframe.columns[1:-2]
    colums2 = dataframe.columns
    dicti={}
    values = np.asarray(data['b_minor'].value_counts().keys())
    for val in values:
        dicti[str(val)] = data.loc[data['b_minor']==val, ['rssi']].mean()['rssi']

    array = []

    array.append(data['testid'].unique()[0])
    for item in colums:
        if item in dicti.keys():
            array.append(dicti[item])
        else:
            array.append(0)
    array.append(data['t_x'].mean())
    array.append(data['t_y'].mean())

    ap = pd.DataFrame(data = np.array(array).reshape(1,-1), columns = colums2)
    dataframe = dataframe.append(ap, ignore_index=True)
    return dataframe


def creatreRSSIm(data, dataframe, building, floor, save, name):
    dataframe = dataframe.copy()
    max_num = int(data['t_num'].max())
    max_pos = int(data['t_pos'].max())
    min_num=int(data['t_num'].min())
    min_pos=int(data['t_pos'].min())

    for i in range(min_pos, max_pos+1):
        dat = data.loc[data['t_pos'] == i]
        for j in range(min_num, max_num+1):
            dt = dat.loc[dat['t_num'] == j]
            if dt.empty:
                pass
            else:
                dataframe = fillDataframe(dt[['testid','b_minor', 'rssi', 't_x', 't_y']], dataframe)
    if save:
        dataframe.to_csv('../Datasets/ML_trained/Building_'+str(building)+'/floor_'+str(floor)+'/matrix_'+name+'_ML.csv', index=False)
    return dataframe

