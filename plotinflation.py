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
import matplotlib.pyplot as plt

def main():
    data=pd.read_csv('alterred.csv')
    yearly_data = pd.pivot_table(data,index=['Year'],values=['Real_Interest'],aggfunc=np.mean,columns=['isGov'])
    # yearly_data.dropna(axis=0,how='any')
    yearly_inflation_rate={
            1997 : 2.8,
            1998 : -0.8,
            1999 : -1.4,
            2000 : 0.4,
            2001 : 0.7,
            2002 : -0.8,
            2003 : 1.2,
            2004 : 3.9,
            2005 : 1.8,
            2006 : 1.5,
            2007 : 4.8,
            2008 : 5.9,
            2009 : -0.7,
            2010 : 3.3,
            2011 : 5.4,
            2012 : 2.6,
            2013 : 3.2,
            2014 : 3.3,
            2015 : 3.0,
            2016 : 8.5,
            2017 : 7.5
            }
    inflation = pd.Series(yearly_inflation_rate)
    plt.plot(yearly_data['Real_Interest'][1],label='Interest Rate')
    plt.plot(inflation,label='Inflation Rate')
    plt.legend(loc='upper left')
    plt.xlabel = 'Year'
    plt.ylabel = 'Rate'
    plt.xticks(list(range(1999,2020,4)))
    plt.grid=True
    plt.show()


    
    

if __name__ == "__main__":
    main()


