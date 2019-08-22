
from TestData import *
from TestAlgorithm import *


	

def main_compare_ML_not_filtered():
	cases = TestCases(out="./Datasets/ML_trained/Building_31/floor_1.0/results/EXTRA_database_test_parametric_equations.csv")
	cases.open_test_data(path="./Datasets/ML_trained/Building_31/floor_1.0/database_test_ML_extra_points.csv", building="SB", interval=5)
	cases.test_algorithm(loc_alg=loc_algorithms[2], floor_alg=floor_algorithms[1], bin_strategy=bin_strategies[7], to_csv=True)
	print(cases.net_xy_error)


def main():
	#main_optimize_bins()
	#main_test_alg2_interval_bins()
	#main_visualize()
	#main_optimize_algorithm_bins()
	#main_test_alg123()
	#main_compare_algorithms()
	main_compare_ML_not_filtered()

if __name__ == "__main__":
	main()

	
	
	
