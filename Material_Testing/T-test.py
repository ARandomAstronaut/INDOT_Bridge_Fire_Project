# Importing the libraries
import scipy.stats as stats
import numpy as np
import pandas as pd

def main():

    # read by default 1st sheet of an excel file
    xls = pd.ExcelFile('Hardness data4.xlsx')
    sheetX = xls.parse(0)

    titles = sheetX['Location']
    R1 = sheetX['R1']
    R2 = sheetX['R2']
    R3 = sheetX['R3']
    R4 = sheetX['R4']
    R5 = sheetX['R5']

    # Clean data by removing NaNs and converting to lists
    titles = titles[titles.notna()].tolist()
    R1 = R1[R1.notna()].tolist()
    R2 = R2[R2.notna()].tolist()
    R3 = R3[R3.notna()].tolist()
    R4 = R4[R4.notna()].tolist()
    R5 = R5[R5.notna()].tolist()

    # Flange results
    amb_fl1 = np.array([R1[0], R2[0], R3[0], R4[0], R5[0]])
    amb_fl2 = np.array([R1[1], R2[1], R3[1], R4[1], R5[1]])
    amb_fl = (amb_fl1 + amb_fl2) / 2

    amb_wb = np.array([R1[2], R2[2], R3[2], R4[2], R5[2]])

    # Loop through flange results
    for i in range(3, len(titles) - 2):
        dat = np.array([R1[i], R2[i], R3[i], R4[i], R5[i]])
        tt = testtype(amb_fl, dat)
        p = stats.ttest_ind(amb_fl, dat, equal_var=tt)
        print(f"The p-value based on the t-test for {titles[i]} flange is {p.pvalue:.4f}")

    # Loop through web results
    for i in range(len(titles) - 2, len(titles)):
        dat = np.array([R1[i], R2[i], R3[i], R4[i], R5[i]])
        tt = testtype(amb_wb, dat)
        p = stats.ttest_ind(amb_wb, dat, equal_var=tt)
        print(f"The p-value based on the t-test for {titles[i]} web is {p.pvalue:.4f}")

def testtype(a, b):
    p = stats.levene(a, b)
    if p.pvalue > 0.05:
        # Variances are equal
        return True
    else:
        # Variances are not equal
        return False

# Run the main function
if __name__ == "__main__":
    main()
