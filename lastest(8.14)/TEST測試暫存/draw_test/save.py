import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()

plt.scatter(np.random.rand(20), np.random.rand(20),figure = fig) 
plt.ylabel("concentration")
plt.xlabel("distance")
plt.savefig('555.png')
plt.show()
