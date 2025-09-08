# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 10:53:04 2025

@author: sharm368
"""

from skimage import io, color
from skimage.filters import threshold_otsu
import numpy as np
import matplotlib.pyplot as plt

# Load and convert to grayscale
image = io.imread('Flange2-1.jpg')
gray_image = color.rgb2gray(image)

# Optional: clean up noise
# from scipy.ndimage import median_filter
# gray_image = median_filter(gray_image, size=3)

# Thresholding
threshold_value = threshold_otsu(gray_image)
binary_image = gray_image > threshold_value  # white: ferrite, black: pearlite

# Area computation
total_area = gray_image.size
pearlite_area = np.sum(gray_image < threshold_value)
ferrite_area = np.sum(gray_image >= threshold_value)

# Fractions
pearlite_fraction = pearlite_area / total_area
ferrite_fraction = ferrite_area / total_area

print(f'Fraction of Pearlite: {pearlite_fraction:.2%}')
print(f'Fraction of Ferrite: {ferrite_fraction:.2%}')

plt.figure()
plt.imshow(binary_image, cmap='gray')
plt.title('Binary Image (Pearlite vs Ferrite)')
plt.show()
