
"""
For a certain test position, what does the distribution
of signals look like?
	- My guess is normal distribution
"""

import os, shutil
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import pandas as pd
from TestAlgorithm import *

def ModelTestPositions(building="SB", floor=None, out_qq=None, out_dist_df=None):

	"""
	This function will calculate the mean/standard deviation of RSSI for each
	beacon at every test position and show how well a normal distribution
	models the rssis. It will do this by computing the p-value for the
	shapiro test for normality and by plotting a QQ-plot.
	
	Inputs:
		building: The building where tests occurred.
		floor: The floor in that building of interest.
		out_qq: Where to save QQ plots for normality testing
		out_dist_df: Where to save the signal distribution pandas dataframe (CSV format)
		
	Return:
		A pandas dataframe with the following schema:
		[testid][timestamp][interval][t_building][t_floor][t_x][t_y][beacon_id][b_major][b_floor][b_minor][b_x][b_y][shapiro][mean][dev]
	"""
	
	dist_df = pd.DataFrame(columns=[
		"testid","timestamp","interval",
		"t_building","t_floor","t_x","t_y",
		"beacon_id","b_major","b_minor",
		"b_floor","b_x","b_y",
		"shapiro","mean","dev"
	])
	
	#Remove all data from the output folder
	if out_qq is not None:
		if os.path.isdir(out_qq):
			shutil.rmtree(out_qq, ignore_errors=True)
		os.mkdir(out_qq)

	#Get the test data
	print("Opening test data")
	cases = TestCases()
	cases.open_test_data(building = building)
	df = cases.test_data
	
	#Get all unique test positions for building
	print("Unique test positions")
	code = BuildingStrToCode[building]
	testpos = df[df["t_building"] == code]
	if floor is not None:
		testpos = testpos[testpos["t_floor"] == floor]
	testpos = df[["t_x", "t_y", "t_floor"]].drop_duplicates()
	
	#For each unique test position
	print("Finding distribution of beacons for each test position")
	id = -1
	for index,row in testpos.iterrows():
	
		id+=1
		
		#Create a new folder for this test position
		if out_qq is not None:
			test_pos_dir = "TestPos-({:.4f}-{:.4f}-{:.4f})".format(row["t_x"], row["t_y"], row["t_floor"])
			test_pos_dir = os.path.join(out_qq, test_pos_dir)
		
		#Get the subset of test data for this position
		data = df[
			(df["t_x"] == row["t_x"]) &
			(df["t_y"] == row["t_y"]) &
			(df["t_floor"] == row["t_floor"])
		]
		
		#Find the unique beacons detected at that position
		beacons = data[["b_x", "b_y", "b_floor", "b_major", "b_minor", "beacon_id"]].drop_duplicates()
		
		#For each unique beacon
		for b_idx, b_row in beacons.iterrows():
						
			#Get the subset of test data for this beacon
			rssis = data[
				(data["b_x"] == b_row["b_x"]) &
				(data["b_y"] == b_row["b_y"]) &
				(data["b_floor"] == b_row["b_floor"])
			]
			rssis = rssis["rssi"]
			if(len(rssis) < 10):
				continue
			
			#Normality
			mean = np.mean(rssis)
			dev = math.sqrt(np.var(rssis))
			normal_test = stats.shapiro(rssis)
			
			#Normality plot
			if out_qq:
			
				#Get the path to save distribution info to
				plot_fn = "Beacon-({:.4f}-{:.4f}-{:.4f}).png".format(b_row["b_x"], b_row["b_y"], b_row["b_floor"])
				plot_path = os.path.join(test_pos_dir, plot_fn)
				if not os.path.exists(test_pos_dir):
					os.mkdir(test_pos_dir)
			
				#Create and save QQ plot
				fig = plt.figure()
				qq = fig.add_subplot(1, 1, 1)
				stats.probplot(rssis, plot=qq)
				qq.set_title("n={:d}, mean={:.4f}, std={:.4f},shapiro={:.4f}".format(len(rssis), mean, dev, normal_test[1]))
				fig.savefig(plot_path)
				plt.close()
			
			#Add to the list
			dist_df.loc[len(dist_df)] = [
				id,"0000-01-01 00:00:00",0,
				BuildingStrToCode[building], row["t_floor"], row["t_x"], row["t_y"], 
				b_row["beacon_id"], b_row["b_major"], b_row["b_minor"], 
				b_row["b_floor"], b_row["b_x"], b_row["b_y"],
				normal_test[1], mean, dev
			]
	
	if out_dist_df is not None:
		dist_df.to_csv(out_dist_df)
	return dist_df
			

def SimulateTestPosition(building="SB", floor=None, interval = 5, period=.5, cases_per_pos = 20, info=None, out="./SimulatedData.csv"):
	
	"""
	This function will simulate the RSSIs received from
	nearby beacons at a certain test position. This will
	produce a synthetic data set that should resemble the
	true data.
	
	Input:
		building: The building with which the simulation is performed
		floor: The floor of that building with which this simulator is performed
		interval: the number of seconds we generate test data for
		period: The number of seconds until beacons resend a signal (.5 seconds for AXAs)
		info: The file that contains the distribution information for each beacon in each test case
		cases_per_pos: The number of test cases to generate per test position
		out: where to save the synthetic data set
		
	The synthetic data will have the following type:
	[testid][timestamp][interval][t_building][t_floor][t_x][t_y][beacon_id][b_major][b_floor][b_minor][b_x][b_y][rssi]
	"""
	
	#Get the beacon distributions for each test position
	print("Opening distribution data")
	if info is None:
		dist = ModelTestPositions(building, floor)
	else:
		dist = pd.read_csv(info)
	
	#Create output dataframe
	df = pd.DataFrame(columns=[
		"testid","timestamp","interval",
		"t_building","t_floor","t_x","t_y",
		"beacon_id","b_major","b_minor",
		"b_floor","b_x","b_y",
		"rssi"
	])
	expanse = pd.DataFrame(columns=[
		"testid","timestamp","interval",
		"t_building","t_floor","t_x","t_y",
		"beacon_id","b_major","b_minor",
		"b_floor","b_x","b_y",
		"shapiro","mean","dev"
	])
	
	
	#Expand test cases
	#Essentially, duplicate each record "cases_per_pos" times
	print("Adding test cases")
	for idx, row in dist.iterrows():
		for i in range(0, cases_per_pos):
			expanse.loc[len(expanse)] = row
			expanse.loc[len(expanse)-1, "testid"] = cases_per_pos*row["testid"] + i
			expanse.loc[len(expanse)-1, "interval"] = interval
		sys.stdout.write(str((idx+1)/len(dist)) + "          \r")
	
	#Estimate RSSIs
	print("Packing test cases with RSSIs")
	for idx, row in expanse.iterrows():
		for i in range(0, int(interval/period)):
			df.loc[len(df)] = row[[
				"testid","timestamp","interval",
				"t_building","t_floor","t_x","t_y",
				"beacon_id","b_major","b_minor",
				"b_floor","b_x","b_y"
			]]
			df.loc[len(df)-1, "rssi"] = np.random.normal(row["mean"], row["dev"])
		sys.stdout.write(str((idx+1)/len(expanse)) + "          \r")
			
	#Save synthetic data set
	df.to_csv(out)
	
	
	
def main():
	#ModelTestPositions(building="SB", floor=1, out_dist_df="./RssiDistribution.csv")
	SimulateTestPosition(building="SB", info="./RssiDistribution.csv", cases_per_pos=10)
	
if __name__ == "__main__":
	main()

	
	
	
	
			