#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import math
import numpy as np
import pandas as pd
from sympy import *
import re
from sklearn.linear_model import LinearRegression

def main():
    df=pd.read_csv("alterred.csv")
    df.dropna(inplace=True)
    # dataSet_inflation = df.loc[:, 'Inflation'].as_matrix(columns=None)
    # dataSet_institution = df.loc[:, 'isGov'].as_matrix(columns=None)
    # dataSet_duration = df.loc[:, 'Duration'].as_matrix(columns=None)
    # X=np.array(list(zip(dataSet_inflation,dataSet_institution,dataSet_duration)))
    X=df.drop(['Name', 'Total', 'Price', 'Maturity', 'Rate', 'Payment_Date', 'Place',
       'Institution', 'Payment_Method', 'Issuing_Method', 'Type', 'Year',
       'Payment_Interval'],1)
    Y = df.loc[:, 'Real_Interest'].as_matrix(columns=None)
    print(type(Y))
    model = LinearRegression()
    model.fit(X,Y)
    print('R-squared: %.2f' % model.score(X[-20:], Y[-20:]))

if __name__ == "__main__":
    main()


