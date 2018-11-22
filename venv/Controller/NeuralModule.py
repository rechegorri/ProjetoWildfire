from Controller.GridMap import GridMap
from Controller.GridMap import GridCell
from Controller.GridMap import Wind
import numpy as np
import random as rd

#input: cellStaus(0-3);windSpeed;windDirection

inputs = np.array([rd.choice(0,3)],[rd.choice(0,359)],[rd.choice(1,45)])

output = np.array([0],[0.5],[1])

weight0 = np.random