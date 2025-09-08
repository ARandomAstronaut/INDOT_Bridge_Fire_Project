# Importing the libraries
import scipy.stats as stats
import numpy as np
import pandas as pd


def main():
    # read by default 1st sheet of an excel file
    xls = pd.ExcelFile('Hardness data4.xlsx')
    sheetX = xls.parse(0) #parse the first sheet into variable sheetX

    titles = sheetX['Location'] #column labled position 
    R1 = sheetX['R1'] #column labled R1 
    R2 = sheetX['R2'] #column labled R2
    R3 = sheetX['R3'] # and so on
    R4 = sheetX['R4']
    R5 = sheetX['R5']
    R6 = sheetX['R6']
    R7 = sheetX['R7']
    R8 = sheetX['R8']
    R9 = sheetX['R9']
    R10 = sheetX['R10']


    # Clean data by removing NaNs and converting to lists
    titles = titles[titles.notna()].tolist() 
    R1 = R1[R1.notna()].tolist()
    R2 = R2[R2.notna()].tolist()
    R3 = R3[R3.notna()].tolist()
    R4 = R4[R4.notna()].tolist()
    R5 = R5[R5.notna()].tolist()
    R6 = R6[R6.notna()].tolist()
    R7 = R7[R7.notna()].tolist()
    R8 = R8[R8.notna()].tolist()
    R9 = R9[R9.notna()].tolist()
    R10 = R10[R10.notna()].tolist()


    # Ambient Flange results
    amb_fl = np.array([R1[0], R2[0], R3[0], R4[0]], R5[0])

    # Loop through flange results
    for i in range(3, len(titles)):
        dat = np.array([R1[i], R2[i], R3[i], R4[i], R5[i], R6[i], R7[i], R8[i], R9[i], R10[i]])
        tt = testtype(amb_fl, dat) # define test type boolean
        p = stats.ttest_ind(amb_fl, dat, equal_var=tt)
        print(f"The p-value based on the t-test for {titles[i]} flange is {p.pvalue:.4f}")


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
