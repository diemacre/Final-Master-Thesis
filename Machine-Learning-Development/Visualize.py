
import pandas as pd
from TestData import *
import datetime
import numpy as np

def formatData(data):
    newcolums = []
    for i, row in data.iterrows():
        values = row['testid'].split('-')
        newcolums.append([int(values[0]), int(values[1])])
    ndf = pd.DataFrame(np.array(newcolums).reshape(-1, 2),
                       columns=['t_pos', 't_num'])
    data = pd.concat([data, ndf], axis=1)
    return data


def load_results(path):

	"""
	This function will load the results of the test cases
	into a pandas dataframe.
	
	Inputs:
		path: the location of the test data results from TestAlgorithm.py
	Return:
		A pandas dataframe of test results
	"""

	return pd.read_csv(path, header=0)

	
def get_img_path(building, floor, portrait=False):

	"""
	This function will acquire the path to the map file being
	queried. This function assumes that the set of maps is
	in the current working directory.
	
	Inputs:
		building: the building we are finding a map for
		floor: the exact floor of this building we are finding a map of
		portrait: whether we are going to use the portrait (tall) or landscape (long) version of the map
	"""

	if portrait:
		return "./Maps/{}-{:02d}.html".format(building, floor)
	else:
		return "./Maps/{}-{:02d}-R.html".format(building, floor)
	
	
def view_tests(
	df, tests=None, building="SB", floor=2, days=None, interval=5,
	loc_alg=2, floor_algorithm=1, bin_strategy=1, top_n=3,
	results=(0, 459), portrait=False, save_path=None
):
	
	"""
	This function displays the test data from a certain testing day on
	a map of the floor tested on.
	
	It will display the tester's position in green and the estimated positions
	in purple.
	
	Inputs:
		df: 				a pandas dataframe consisting of all test case results (from TestAlgorithm)
		tests:				a pandas dataframe of the test data (including beacon positions)
		building: 			the building the tests occurred in
		floor: 				the floor of the building the tests occurred on
		days: 				the range of days at which tests were made (Year, Month, Day)
		loc_alg: 			the algorithm used to estimate xy position
		floor_algorithm: 	the algorithm used to estimate the floor
		bin_strategy:		the binning strategy used for converting RSSI to distance
		top_n: 				the number of beacons factored when estimating xy position
		results: 			the range of results to display from the dataframe
		portrait:			whether to use the portrait or landscape form of the building map
		save_path: 			the path to save the image to
	"""
	
	#Get the html we will be modifying
	img_file = open(get_img_path(building, floor, portrait))
	img = img_file.read()
	
	#Get the data we will displaying
	code = BuildingStrToCode[building]
	
		
	#Convert the portrait boolean to a string
	if portrait:
		portrait = "true"
	else:
		portrait = "false"
	
	#Get the file with the map javascript data
	map_file = open("./Maps/map.js")
	map = map_file.read()
	img += map
	
	#Start the javascript
	img += "<script>\n"
	
	#Write the test cases to the screen
	for i in range(results[0], results[1]+1):
		idx = df.index[i]
		img += "render_test_case("
		img += "\"" + df.loc[idx, "testid"] + "\"" + ","
		img += str(df.loc[idx, "t_x"]) + ","
		img += str(df.loc[idx, "t_y"]) + ","
		img += str(df.loc[idx, "p_x"]) + ","
		img += str(df.loc[idx, "p_y"]) + ","
		img += str(df.loc[idx, "error"]) + ","
		img += portrait
		img += ")\n"
	
	#Display bluetooth beacons on floor
	
	
	#End the javascript
	img += "</script>\n"
	
	#End the html file
	img += "</html>"
	save = open(save_path, "w")
	save.write(img)

def filterMax(data):
	cols = data.columns
	val = data['t_pos'].unique()
	result =[]
	for v in val:
		dat = data.loc[data['t_pos'] == v]
		maxi = dat['error'].max()
		result.append(dat.loc[(dat['error'] == maxi) & (data['t_pos'] == v)].values[0])
	df = pd.DataFrame(data = np.array(result), columns = cols)
	return df


def filterMin(data):
	cols = data.columns
	val = data['t_pos'].unique()
	result =[]
	for v in val:
		dat = data.loc[data['t_pos'] == v]
		mini = dat['error'].min()
		result.append(dat.loc[(dat['error'] == mini) & (data['t_pos'] == v)].values[0])
	df = pd.DataFrame(data = np.array(result), columns = cols)
	return df


#global test using parametric equations
database_test_parametric_equations = load_results("./Datasets/ML_trained/Building_31/floor_1.0/results/database_test_parametric_equations.csv")
database_test_parametric_equations = database_test_parametric_equations.rename({'x_true': 't_x', 'y_true': 't_y','x_est': 'p_x', 'y_est': 'p_y', 'xy_error': 'error'}, axis=1)
database_test_parametric_equations = formatData(database_test_parametric_equations)

#small visualization for max and min errors
database_test_parametric_equations_MAX = filterMax(database_test_parametric_equations)
database_test_parametric_equations_MIN = filterMin(database_test_parametric_equations)


#extra test for outliers using parametric equations
extra_database_test_parametric_equations = load_results("./Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_database_test_parametric_equations.csv")
extra_database_test_parametric_equations = extra_database_test_parametric_equations.rename({'x_true': 't_x', 'y_true': 't_y', 'x_est': 'p_x', 'y_est': 'p_y', 'xy_error': 'error'}, axis=1)
extra_database_test_parametric_equations = formatData(extra_database_test_parametric_equations)
#global test using gb
results_GB_1_no_filter_optimized_param = load_results("./Datasets/ML_trained/Building_31/floor_1.0/results/results_GB_1_no_filter_optimized_param.csv")
results_GB_1_no_filter_optimized_param = formatData(results_GB_1_no_filter_optimized_param)
#small visualization for max and min errors
results_GB_1_no_filter_optimized_param_MAX = filterMax(results_GB_1_no_filter_optimized_param)
results_GB_1_no_filter_optimized_param_MIN = filterMin(results_GB_1_no_filter_optimized_param)

#extra test for outliers
extra_results_GB_1_no_filter_optimized_param = load_results(
	"./Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_results_GB_1_no_filter_optimized_param.csv")
extra_results_GB_1_no_filter_optimized_param = formatData(extra_results_GB_1_no_filter_optimized_param)
#visualize all 
view_tests(database_test_parametric_equations, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/database_test_parametric_equations.html", interval=5, results=(0, 459))

view_tests(results_GB_1_no_filter_optimized_param, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/results_GB_1_no_filter_optimized_param.html", interval=5, results=(0, 459))


view_tests(extra_database_test_parametric_equations, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/extra_database_test_parametric_equations.html", interval=5, results=(0, 8))
view_tests(extra_results_GB_1_no_filter_optimized_param, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/extra_results_GB_1_no_filter_optimized_param.html", interval=5, results=(0, 8))


view_tests(database_test_parametric_equations_MAX, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/database_test_parametric_equations_MAX.html", interval=5, results=(0, 45))
view_tests(database_test_parametric_equations_MIN, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/database_test_parametric_equations_MIN.html", interval=5, results=(0, 45))

view_tests(results_GB_1_no_filter_optimized_param_MAX, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/results_GB_1_no_filter_optimized_param_MAX.html", interval=5, results=(0, 45))
view_tests(results_GB_1_no_filter_optimized_param_MIN, building="SB", loc_alg=2, floor=1, days=[
           (2019, 5, 10), (2019, 6, 10)], bin_strategy=7, save_path="Visualizations/results_GB_1_no_filter_optimized_param_MIN.html", interval=5, results=(0, 45))
