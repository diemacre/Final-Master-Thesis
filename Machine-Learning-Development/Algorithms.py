
import lmfit, math, numpy as np
from collections import Counter

def loc_model1(params, x, y, prox):
	
    x0 = params['x0']
    y0 = params['y0']
    t = (x - x0)**2 + (y - y0)**2 - prox
    t = t**2/prox**2
	
    return np.sqrt(t)

	
def loc_model2(params, x, y, prox):

    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2) - prox
    t = t**2/prox**2
	
    return np.sqrt(t)

	
def loc_model3(params, x, y, prox):
	
    x0 = params['x0']
    y0 = params['y0']
    t = np.sqrt((x - x0)**2 + (y - y0)**2)
    t = t/prox**2
	
    return np.sqrt(t)

	
def find_floor_simple(floor, proximity, building_id):
    # making a list of tuples (floor, building_id)
    zipped = list(zip(floor, building_id))
    
    # counter object that has key(tuple) and value(count)
    c = Counter(x for x in zipped)
    
    # getting the 1 most common keys, gets a list of tuples(key, count) return the first tuple's key   
    return c.most_common(1)[0][0]

	
def find_floor_fancy(floor, proximity, building_id):
    zipped = list(zip(floor, proximity))
    
    # floor = sum(floor/proximity) / sum(1/proximity)
    t = sum(map(lambda bt: bt[0] * 1.0 / bt[1], zipped))
    b = sum(map(lambda bt: 1.0 / bt[1], zipped))
    flr = int(round(t / b))
    # the most occuring building id.
    bldg = Counter(building_id).most_common(1)[0][0] 
    
    return flr, bldg


loc_algorithms = [
	0, 
	(1, loc_model1),
	(2, loc_model2),
	(3, loc_model3)
]

floor_algorithms = [
	0, 
	(1, find_floor_simple),
	(2, find_floor_fancy)
]

bin_strategies = [
	0, 
	(1, [(-70, 15), (-60, 7), (-50, 3), (0, 2)]),					#Very old bins
	(2, [(-70, 9), (-60, 5), (-50, 2), (0, 1)]),					#Old bins
	(3, [(-143, 12), (-83, 9), (-51, 3), (0, 1)]),					#New bins (intervals=all)
	(4, [(-142, 9), (-89, 7), (-37, 2), (0, 1)]),					#New bins (interval=5sec)
	(5, [(-139, 12), (-87, 11), (-27, 4), (0, 1)]),					#New bins (interval=10sec)
	(6, [[-103, 9], [-82, 4.2], [-40, 2.2], [0, 1.1]]),				#New bins (interval = 5sec)
	(7, [[-92, 7.6], [-80, 5.4], [-50, 2.4], [0, 1.2]]),			#New bins (interval=10sec)
	(8, [[-96.3, 21.3], [-81.3, 12.3], [-50.1, 2.5], [0, 1.1]]),	#New bins (interval=10sec)
	(9, [[-92, 7.6], [-80, 5.4], [-50, 2.4], [0, 1.2]]),			#New bins (interval=10sec)
	(10, [[-130.3, 24.4], [-81.3, 20.4], [-21.7, 14.4], [0, 4.4]]),	#New bins (interval=10sec)
]




