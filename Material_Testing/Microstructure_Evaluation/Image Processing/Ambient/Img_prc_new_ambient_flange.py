# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 10:53:04 2025
last modified Wed Jul 23

@author: sharm368, Pham162
"""

from skimage import io, color
from skimage.filters import threshold_otsu
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from glob import glob
import pandas as pd


os.chdir(r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Ambient")
files = sorted(glob("*.jpg")) #grab and sort jpg file
labels = [os.path.splitext(f)[0] for f in files] # remove the jpg extension

# load, threshold, compute fractions
binaries = []
fractions = []
for fname in files:
    img  = color.rgb2gray(io.imread(fname))
    th   = threshold_otsu(img)
    binv = img > th
    binaries.append(binv)
    p_frac = np.mean(~binv)  # pearlite = dark = False
    f_frac = np.mean(binv)   # ferrite = light = True
    fractions.append((p_frac, f_frac))

# print results
for label, (p, f) in zip(labels, fractions):
    print(f'{label:9s} - Pearlite: {p:.2%}, Ferrite: {f:.2%}')

## plot in 2×2 grid, leave last empty
fig, axs = plt.subplots(1, len(labels), figsize=(10, 8))
fig.suptitle('Binary Image (Pearlite (Dark) vs Ferrite (Light))', fontsize=18)

axes = axs.flatten()
for ax, binv, label in zip(axes, binaries, labels):
    ax.imshow(binv, cmap='gray')
    ax.set_title(label)
    ax.axis('off')

#axes[-1].axis('off')  # unused

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

## build a DataFrame and export to Excel ---
df = pd.DataFrame(fractions, columns=["Pearlite Fraction", "Ferrite Fraction"], index=labels)
df.index.name = "Sample"
# path to your output Excel file (change directory as needed)
output_path = r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Microstructure Result.xlsx"
# write out (requires openpyxl or xlsxwriter)
df.to_excel(output_path, sheet_name="Ambient")
print(f"Fractions table saved to: {output_path}")
