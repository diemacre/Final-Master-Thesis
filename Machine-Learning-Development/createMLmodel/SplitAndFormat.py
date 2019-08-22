import pandas as pd
import numpy as np

def filterData(data, building, floor):
    data = data.loc[data['t_building'] == building]
    print(data.loc[data['b_floor'] == 1.0]['b_floor'].size)
    data = data.loc[data['b_floor'] == floor].reset_index()
    return data

def formatData(data):
    newcolums = []
    for i, row in data.iterrows():
        values = row['testid'].split('-')
        newcolums.append([int(values[0]), int(values[1])])
    ndf = pd.DataFrame(np.array(newcolums).reshape(-1, 2),columns=['t_pos', 't_num'])
    data = pd.concat([data, ndf], axis=1)
    return data

def split(building, floor, data, save):
    # .drop(['t_pos', 't_num'], axis=1)
    test2 = data.loc[data['t_pos'] > 49]

    data = data.loc[data['t_pos'] < 50]

    train = data.loc[data['t_num'] < 26]
    test = data.loc[data['t_num'] > 25]

    if save:
        train.to_csv(
            '../Datasets/ML_trained/Building_'+str(building)+'/floor_'+str(floor)+'/database_train_ML.csv', index=False)
        test.to_csv(
            '../Datasets/ML_trained/Building_'+str(building)+'/floor_'+str(floor)+'/database_test_ML.csv', index=False)
        if test2 is not None:
            test2.to_csv('../Datasets/ML_trained/Building_'+str(building)+'/floor_'+str(floor)+'/database_test_ML_extra_points.csv', index=False)
    return train, test, test2
