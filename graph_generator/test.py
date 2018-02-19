import random

import numpy as np
import matplotlib.pyplot as plt

clusters = []
for i in range(0,750):
	idxs = []
	for j in range(0,50):
		idxs.append(random.randint(0,10000-1))
	clusters.append(idxs)
	
y = [0]*10000

for c in clusters:
	for i in c:
		y[i] = y[i] + 1

list.sort(y)	
plt.plot(np.linspace(0,10000,10000),y)
plt.show()