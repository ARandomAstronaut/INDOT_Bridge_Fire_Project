# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 10:53:04 2025

@author: Phong Pham
"""

from pathlib            import Path
from skimage            import io, color
from skimage.filters    import threshold_otsu
from openpyxl           import load_workbook
import numpy            as np
import pandas           as pd
import cv2

def process_and_export(
    input_dir: str,
    output_path: str,
    sheet_name: str,
    crop_right: int = 450):
    """
    - input_dir:    folder containing your .jpg files
    - output_path:  full path to the .xlsx workbook
    - sheet_name:   name of the sheet to create/replace
    - crop_right:   pixels to trim off the right side of each image
    """
    #Converts the string input_dir into a Path object using pathlib
    #Path objects are more robust and flexible than strings for working with file paths (e.g., easy to join paths or use .glob()).
    input_dir  = Path(input_dir) 
    output_xl  = Path(output_path)

    # 1) Gather all .jpg’s
    files  = sorted(input_dir.glob("*.jpg")) #Searches the input_dir for all files ending with .jpg and return them, then sort them
    labels = [f.stem for f in files]

    fractions = []
    for fpath in files:
        img = cv2.imread(str(fpath))
        if img is None: raise FileNotFoundError(f"Could not load '{fpath}'")

        h, w = img.shape[:2]
        x1, x2 = 0, w - crop_right
        y1, y2 = 0, h
        
        x1, x2 = max(0, x1), min(w, x2) # clamp
        if x1 >= x2: raise ValueError(f"Invalid crop for '{fpath}': x1={x1}, x2={x2}")

        crop = img[y1:y2, x1:x2] # crop
        gray = color.rgb2gray(crop) # grayscale
        th   = threshold_otsu(gray)# Otsu threshold
        binv = gray > th #binary mask

        # compute fractions
        fer = np.mean(binv)    # ferrite = True
        pea = np.mean(~binv)   # pearlite = False
        fractions.append((pea, fer))

        print(f'{fpath.stem:9s} - Pearlite {pea:.1%}, Ferrite {fer:.1%}')

    # 2) Build DataFrame
    df = pd.DataFrame(
        fractions,
        columns=["Pearlite Fraction", "Ferrite Fraction"],
        index=labels
    )
    df.index.name = "Sample"

    # 3) Export into Excel, preserving any existing sheets
    if not output_xl.exists():
        # first time: write from scratch
        df.to_excel(output_xl, sheet_name=sheet_name)
    else:
        # append/replace just this sheet
        book = load_workbook(output_xl)
        with pd.ExcelWriter(
            output_xl,
            engine="openpyxl",
            mode="a",
            if_sheet_exists="replace"
        ) as writer:
            writer.book   = book
            writer.sheets = {ws.title: ws for ws in book.worksheets}
            df.to_excel(writer, sheet_name=sheet_name)

    print(f" '{sheet_name}' sheet saved to {output_xl!s}")

# ── Example usage for Ambient: ────────────────────────────────────────────────
process_and_export(
    r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Ambient",
    r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Microstructure Result.xlsx", "Ambient"
)

## Air Cooled
process_and_export(r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Air Cooled", 
r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Microstructure Result.xslsx", "Air Cooled")


## Water Cooled
process_and_export(r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Water Cooled", 
r"c:\Users\truph\Desktop\Purdue\Summer '25\Bowen Lab Research\Microstructures\Image Processing\Microstructure Result.xlsx", "Water Cooled")
