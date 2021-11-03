#! /usr/bin/env python3

"""Aggregate values with repeated x in a csv file"""

import tkinter.filedialog as fd
import numpy as np
import pandas as pd


if __name__ == "__main__":
    print("="*80)

    # get filename
    myFd = fd.askopenfile()
    fname = myFd.name

    print(f"Selected file: {fname}")

    # read csv
    df = pd.read_csv(fname)
    print("Original data looks like:")
    print(df.head())

    if not np.all(df.iloc[:, 0].value_counts() == 1):
        # do the aggregation
        xind = df.columns[0]
        print(f"Aggregating by column {xind}")

        dfM = df.groupby(xind).mean()
        dfE = df.groupby(xind).std()
        dfN = df.groupby(xind).count()
        df = dfM.join(dfE, on=xind, rsuffix="_std")
        df = df.join(dfN, on=xind, rsuffix="_n")

        print("Now data looks like:")
        print(df.head())

    else:
        print("Data is already aggregated.")

    savename = f"{fname[:-4]}_aggregated.csv"
    print(f"Saving to {savename}")
    df.to_csv(savename)

    print("="*80)
