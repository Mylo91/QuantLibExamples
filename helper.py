# -*- coding: utf-8 -*-
"""
Helper functions for quantLib examples
"""

"""
Reads the yield curve data points from excel sheet and creates
the term structure object
"""
import pandas as pd
import QuantLib as ql

def createYieldCurve(filename, sheetName, rateColumnName):
    yc = pd.read_excel(filename, sheet_name=sheetName)
    dates = []
    dfs = []
    for i, row in yc.iterrows():
        # Create dates
        y = row["Date"].year
        m = row["Date"].month
        d = row["Date"].day
        dates.append(ql.Date(d, m, y))
        dfs.append(row[rateColumnName])
    
    day_count = ql.ActualActual()
    
    term_structure = ql.YieldTermStructureHandle(ql.DiscountCurve(dates, dfs, day_count))
    
    return term_structure

"""
Reads the forward curve data points from excel sheet and creates
the term structure object
"""
def createForwardCurve(filename, sheetName, rateColumnName):
    yc = pd.read_excel(filename, sheet_name=sheetName)
    dates = []
    dfs = []
    for i, row in yc.iterrows():
        # Create dates
        y = row["Date"].year
        m = row["Date"].month
        d = row["Date"].day
        dates.append(ql.Date(d, m, y))
        dfs.append(row[rateColumnName])
    
    day_count = ql.ActualActual()
    
    term_structure = ql.YieldTermStructureHandle(ql.ForwardCurve(dates, dfs, day_count))
    
    return term_structure

"""
Reads the volatility surface from excel sheet and creates
the quantLib vola surface
"""
def createVolaSurface(referenceDate, filename, sheetName):
    
    df = pd.read_excel(filename, sheet_name=sheetName)
    
    # retrieve strikes in 1st row
    strikes = [float(i) for i in df.columns.to_list()[1:]]
    
    npDF = df.to_numpy()
    # get expiries in 1st col
    expiryDates = [ql.Date(d.day, d.month, d.year) for d in npDF[:, 0]]
    # get vola surface
    rawVolaM = npDF[:, 1:]
    volMatrix = ql.Matrix(len(strikes), len(expiryDates))
    
    # Fill in vola surface - note raw surface is transposed
    for i in range(len(strikes)):
        for j in range(len(expiryDates)):
            volMatrix[i][j] = rawVolaM[j][i]
    
    
    volSurface = ql.BlackVarianceSurface(referenceDate, ql.NullCalendar(), expiryDates, strikes, volMatrix, ql.ActualActual())
    return volSurface
    
