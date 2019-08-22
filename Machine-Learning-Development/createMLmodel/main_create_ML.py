from CreateRSSImatrix import *
from PossitionEstimationML import *
from SplitAndFormat import *
from Download import *

import pandas as pd


from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor

def main2():

	#define the building and floor of the study
	building = 31
	floor = 1.0
	'''
	GET DATA FROM DATABASE: 
		-define de path to save the datavase
		-define variable saveDatabase to true if want to save database
	'''
	path = '../Datasets/databaseML2.csv'
	saveDatabase = True

	#data  = download_test_dataML(saveDatabase, out=path)
	data = pd.read_csv('../Datasets/databaseML.csv')

	data = formatData(data)
	saveSplits = False
	train, test, test_extra = split(building, floor, data, saveSplits)

	print(test_extra)


def main():
	#define the building and floor of the study
	building = 31
	floor = 1.0
	'''
	GET DATA FROM DATABASE: 
		-define de path to save the datavase
		-define variable saveDatabase to true if want to save database
	'''
	path = '../Datasets/databaseML.csv'
	saveDatabase = False
	#data  = download_test_dataML(saveDatabase, out=path)
	data = pd.read_csv('../Datasets/databaseML.csv')

	#filter data by floor and building
	#data = data.loc[data["t_floor"] == floor]
	#data = data.loc[data["t_building"] == building]
	print('data downloaded')

	'''
	FILTER DATA: 
		- BY BUILDING
		- BY FLOOR
	Only the readings with beacons from the same floor as the test will be considered
		- uncomment next line
	'''
	#data = filterData(data, building, floor)

	'''
	SPLIT DATA (TRAIN, TEST) and save it: into train and test: The split is done in this study. However if the experiment result succesfully the whole dataset can be used for creating
	the machine learning model (use all data as training)
		- format to add to colums corresponding to test number and test position for handle better after
		- make the split 
	'''

	'''
	data  = formatData(data)
	saveSplits = False
	train , test = split(building, floor, data, saveSplits)
	
	print('data splited')
	'''
	

	'''
	FORMAT DATA INTO MATRIX:
		- For each test all the readings fron the diferent beacons are converted into a single row that contains:
			-Columns: each beacon id (minor) and the original test position
			-Columns value: average RSSI from that sensor, if not detected is equal to 0
	'''
	
	'''
	saveMatrix = False
	matrixHeaderFrame = createEmptyDataFrame(data)
	test_matrix = creatreRSSIm(test, matrixHeaderFrame, building, floor, saveMatrix, 'test')
	#test_matrix_extra = creatreRSSIm(test_extra, matrixHeaderFrame, building, floor, saveMatrix, 'test_extra')
	print('matrix test created')
	train_matrix = creatreRSSIm(train, matrixHeaderFrame, building, floor, saveMatrix, 'train')
	print('matrix train created')
	test_matrix_extra = creatreRSSIm(test_extra, matrixHeaderFrame,building, floor, saveMatrix, 'test_extra')
	'''

	test_matrix = pd.read_csv('../Datasets/ML_trained/Building_31/floor_1.0/matrix_test_ML.csv')
	train_matrix = pd.read_csv('../Datasets/ML_trained/Building_31/floor_1.0/matrix_train_ML.csv')
	test_extra_matrix = pd.read_csv('../Datasets/ML_trained/Building_31/floor_1.0/matrix_TEST_extra_ML.csv')
	

	'''
	MODEL CREATION:
		-Variables: Beacons from that bulding and floor
		-Labels: test position (x, y)
	'''

	colum = train_matrix.columns[1:-2]
	#train variables
	Y_train = train_matrix[['t_x','t_y']]
	X_train = train_matrix[colum]
	#test variables
	Y_test = test_matrix[['t_x', 't_y']]
	X_test = test_matrix[colum]
	#test_extra variables

	Y_test_extra = test_extra_matrix[['t_x', 't_y']]
	X_test_extra = test_extra_matrix[colum]

	print('\npredicting.......linear')
	model = LinearRegression()
	Y_pred = prediction(X_train, Y_train, X_test, Y_test, model)
	frame = createdataframe(test_matrix['testid'], np.array(Y_test), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error',frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#frame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/results_linear_1_no_filter.csv', index=False)

	print('\npredicting.......random forest')
	model = RandomForestRegressor(random_state=0)
	Y_pred = prediction(X_train, Y_train, X_test, Y_test, model)
	frame = createdataframe(
		test_matrix['testid'], np.array(Y_test), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error', frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#frame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/results_RF_1_no_filter.csv', index=False)

	print('\npredicting.......random forest optimized')
	model = RandomForestRegressor(max_depth=15, random_state=0, n_estimators=15)
	Y_pred = prediction(X_train, Y_train, X_test, Y_test, model)
	frame = createdataframe(test_matrix['testid'], np.array(Y_test), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error', frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#frame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/results_RF_1_no_filter_optimized_param.csv', index=False)

	print('\npredicting.......gradient boosting')
	model = MultiOutputRegressor(GradientBoostingRegressor(random_state=0))
	Y_pred = prediction(X_train, Y_train, X_test, Y_test, model)
	frame = createdataframe(test_matrix['testid'], np.array(Y_test), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error', frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#frame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/results_GB_1_no_filter.csv', index=False)

	print('\npredicting.......gradient boosting optimized')
	model = MultiOutputRegressor(GradientBoostingRegressor(random_state=0, max_depth=6))
	Y_pred = prediction(X_train, Y_train, X_test, Y_test, model)
	frame = createdataframe(test_matrix['testid'], np.array(Y_test), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error', frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#rame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/results_GB_1_no_filter_optimized_param.csv', index=False)



	#frame.to_csv('../Datasets/results_filtered_ML_3.csv', index=False)
	#print(np.sort(np.array(frame['error'])))

	print('EXTRA TEST OUTLIERS')

	print('\npredicting.......gradient boosting optimized FOR OUTLIERS')
	model = MultiOutputRegressor(GradientBoostingRegressor(random_state=0, max_depth=6))
	Y_pred = prediction(X_train, Y_train, X_test_extra, Y_test_extra, model)
	frame = createdataframe(test_extra_matrix['testid'], np.array(Y_test_extra), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error', frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#frame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_results_GB_1_no_filter_optimized_param.csv', index=False)

	print('EXTRA TEST OUTLIERS')

	print('\npredicting.......fandom forest optimized FOR OUTLIERS')
	model = RandomForestRegressor(max_depth=15, random_state=0, n_estimators=15)
	Y_pred = prediction(X_train, Y_train, X_test_extra, Y_test_extra, model)
	frame = createdataframe(test_extra_matrix['testid'], np.array(Y_test_extra), np.array(Y_pred))
	print('max error:', frame['error'].max())
	print('mean error', frame['error'].mean())
	print('description error', frame['error'].describe(percentiles=[.5, .75, .9]))
	#frame.to_csv('../Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_results_RF_1_no_filter_optimized_param.csv', index=False)

if __name__ == "__main__":
	main()
