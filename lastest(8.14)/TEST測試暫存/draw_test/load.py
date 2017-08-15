
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy


image = mpimg.imread("test.png")
plt.imshow(image)
plt.show()
"""
import matplotlib.pyplot as plt
import cv2

fig = plt.figure("fig_1")
ax = fig.add_subplot(1, 1, 1)

image = cv2.imread("test.png")
ax.imshow(image)

plt.show()
"""