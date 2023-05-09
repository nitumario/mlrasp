import pandas as pd
import numpy as np

from glob import glob

import cv2
import matplotlib.pylab as plt

plt.style.use("ggplot")

tyler = glob("../input/tyler/*.png")

img_mpl = plt.imread(tyler[20])
img_cv2 = cv2.imread(tyler[20])
img_mpl.shape, img_cv2.shape

pd.Series(img_mpl.flatten()).plot(kind = "hist",
                                  bins = 50,
                                  title = "Distribution of Pixel Values")
plt.show()
