#! /usr/bin/env python3

"""Aggregate values with repeated x in a csv file."""

# import tkinter as tk
import tkinter.filedialog as fd
# from tkinter import ttk
from collections import namedtuple
# import numpy as np
import pandas as pd
import logging
import sys


def main():
    """Do the main function."""
    print("\nAGGREGATOR\n")
    print("="*80)

    # get filename
    fname = chooseFile()
    if fname is None:
        sys.exit(0)
    print(f"File chosen: {fname}")

    # get dataframe
    df = pd.read_csv(fname)
    df = omitRemove(df)
    print("Original data looks like:")
    print(df.head())

    myVars = chooseVars(list(df.columns))

    print(myVars)

    dfS = splitBy(df, myVars.s, myVars.se)
    if dfS is None:
        print("Goodbye.")
        sys.exit(1)

    dfT, dfF = dfS
    dfTa = aggregate(dfT, myVars.x)

    if len(dfF) >= 0:
        dfFa = aggregate(dfF, myVars.x)

        fnameT = fname[:-4] + "_splitT.csv"
        fnameF = fname[:-4] + "_splitF.csv"

        saved = [fnameT, fnameF]

        dfFa.to_csv(fnameF)

    else:
        fnameT = fname[:-4] + "_aggregate.csv"
        saved = [fnameT]

    dfTa.to_csv(fnameT)

    print("File saved to:")
    for n in saved:
        print("    " + n)

    print("="*80)


def chooseFile() -> str:
    """Choose a file to process."""
    return fd.askopenfilename()


AgVars = namedtuple("AgVars", ['x', 's', 'se'])


def chooseVars(names: list) -> AgVars:
    """Choose the variables for the analysis."""
    for i, x in enumerate(names):
        print(f"{i} {x}")
    # prompt for variables
    ncol = len(names)
    x_ans = colPrompt('x', ncol)
    s_ans, s_expr = splitVarExprPrompt(ncol) if splitPrompt() else (None, None)
    return AgVars(names[x_ans], names[s_ans], s_expr)


def colPrompt(varname, ncol):
    """Prompt for a column index."""
    while True:
        ans = int(input(f"Insert index of {varname} column [0-{ncol-1}]: "))
        if (ans < 0) or (ans >= ncol):
            print("Value not good.")
        else:
            return ans


def splitPrompt():
    """Ask if you want to split."""
    while True:
        ans = input("Do you want to split file? [y/n] ").lower()
        if ans in ['y', 'yes']:
            return True
        if ans in ['n', 'no']:
            return False
        # if not returned, input value not correct
        print("Answer not understood. Say 'y' or 'n' (without quotes).")


def splitVarExprPrompt(ncol):
    """Prompt for split variable and expression."""
    s_ans = colPrompt('split', ncol)
    s_expr = input("Insert split expression in s (e.g. s>10) ")
    return s_ans, s_expr


def splitBy(df: pd.DataFrame, splitVar: str, splitExpr: str) -> tuple:
    """Split in two dataframes depending on truth of splitExpr(splitVar)."""
    if splitVar is None:
        filtlist = True * len(df)
    vals = df[splitVar]
    try:
        filtlist = [eval(splitExpr, None, {'s': a}) for a in vals]
    except (TypeError, NameError) as e:
        logging.error(str(e))
        return None

    opplist = list(map(lambda x: not x, filtlist))

    return (df[filtlist], df[opplist])


def aggregate(df, xvar: str):
    """Compute mean of xval column."""
    groupedDf = df.select_dtypes('float64').groupby([xvar])
    meanDf = groupedDf.mean()
    cnt = groupedDf.size()
    errDf = groupedDf.std().transform(
        lambda x: x / cnt.astype('float64')
    )
    errNames = {x: x+'_err' for x in errDf.columns}
    errDf.rename(columns=errNames, inplace=True)
    joinDf = meanDf.join(errDf)
    joinDf['cnt'] = cnt
    return joinDf


def omitRemove(df: pd.DataFrame) -> pd.DataFrame:
    """Remove omitted rows."""
    if 'Omit' not in df.columns:
        return df

    dfOut = df.copy()
    dfOut.loc[dfOut['Omit'].isna(), 'Omit'] = False
    return dfOut[~ dfOut['Omit'].astype(bool)]


if __name__ == "__main__":
    main()
