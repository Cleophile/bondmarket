#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import math
import numpy as np
import pandas as pd
from sympy import *
import re

def main():
    log_file = open('log.txt','a')
    log_file.write('-'*30 + '\n\n')
    # Index(['Name', 'Total', 'Ticket_Value', 'Price', 'Maturity', 'Rate','Payment_Date', 'Place', 'Institution', 'Payment_Method','Issuing_Method', 'Type', 'Year'],dtype='object')
    data=pd.read_csv("bond.csv")
    data['Year'] = [int(re.findall(r'\d+',s)[0]) for s in data['Name']]
    data['Year'][data['Year']<30] += 2000 # 06年等省略
    data['Year'][data['Year']<100] += 1900 # 99年等省略
    del data['Ticket_Value']
    # irrelavent
    data['Payment_Interval'] = None  # 利息支付的时间
    data['Duration'] = None # 久期, 用于度量利率风险，用于time_real
    # set(data['Payment_Interval'])
    #  {nan, '一次还本息', '半年付', '年付', '月付', '贴现'}
    data['Payment_Interval'][data['Payment_Method'] == '年付'] = 1.0
    data['Payment_Interval'][data['Payment_Method'] == '半年付'] = 0.5
    data['Payment_Interval'][data['Payment_Method'] == '月付'] = 1/12
    data['Payment_Interval'][data['Payment_Method'] == '贴现'] = data['Maturity'][data['Payment_Method'] == '贴现']
    data['Payment_Interval'][data['Payment_Method'] == '一次还本息'] = data['Maturity'][data['Payment_Method'] == '一次还本息']
    # Payment_Interval is SET

    # 是否是国债
    data['isGov'] = None
    data['isGov'][data['Institution']=='财政部'] = 1
    data['isGov'][data['Institution']!='财政部'] = 0

    # 折价发行利率（折现率）
    # 使用连续复利模型，抹平时间的因素！
    # interest_rate是连续复利的年收益率

    def yearly(interest_rate, years):
        def func(x):
            return (1-(100/(100+x))**years)*100*interest_rate/x + 100/((1+x/100)**years)
        return func

    data['Real_Interest']=None
    for i in range(len(data)):
        years=data.loc[i,'Maturity']
        price=data.loc[i,'Price']
        r=data.loc[i,'Rate']
        interest_rate=0
        if data.xs(i)['Payment_Method'] == '年付':
            func=yearly(r,years)
            x=Symbol('x')
            solutions=solve(func(x)-price,x)
            for s in solutions:
                flag=False
                try :
                    interest_rate=float(s)
                    flag=True
                except TypeError :
                    flag=False
            data.loc[i,'Real_Interest'] = interest_rate
            log_file.write(str(interest_rate) + '\n')
            continue

        if data.loc[i,'Payment_Method'] == '半年付':
            years *= 2
            r /= 2
            func=yearly(r,years)
            x=Symbol('x')
            solutions=solve(func(x)-price,x)
            for s in solutions:
                flag=False
                try :
                    interest_rate=float(s)
                    flag=True
                except TypeError :
                    flag=False

            interest_rate = (1+x/100) + (1+x/100)**2 -1
            interest_rate *= 100
            data.loc[i,'Real_Interest'] = interest_rate
            log_file.write(str(interest_rate) + '\n')
            continue

        if data.loc[i,'Payment_Method'] == '月付':
            years *= 12
            r /= 12
            func=yearly(r,years)
            x=Symbol('x')
            solutions=solve(func(x)-price,x)
            for s in solutions:
                flag=False
                try :
                    interest_rate=float(s)
                    flag=True
                except TypeError :
                    flag=False
            r_ele=0
            for count in range(1,13):
                r_ele += (1+interest_rate/100) ** count
            interest_rate = (r_ele-1)*100
            data.loc[i,'Real_Interest'] = interest_rate
            log_file.write(str(interest_rate) + '\n')
            continue

        if data.loc[i,'Payment_Method'] == '一次还本付息':
            if data.loc[i,'Maturity'] == 1.0 :
                interest_rate = r
            else :
                interest_rate = ((100*(1+r*years)/price) ** (1/years) - 1)*100
                
            data.loc[i,'Real_Interest'] = interest_rate
            log_file.write(str(interest_rate) + '\n')
            continue

        if data.loc[i,'Payment_Method'] == '贴现':
            r=100/price
            interest_rate = (math.exp(math.log(r)/years)-1)*100
            data.loc[i,'Real_Interest'] = interest_rate
            log_file.write(str(interest_rate) + '\n')
            continue


    # 设定通货膨胀率
    # 今年和去年的通货膨胀率，内在关系？
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

    print(data.head())
    print(data.tail())
    data.to_csv("alterred.csv",index=False)


if __name__ == "__main__":
    main()


