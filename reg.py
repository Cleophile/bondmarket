#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import numpy as np
import pandas as pd
import re
import sympy as sp

def main():
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

    # 折价发行利率（折现率）
    data['Real_Interest']=None
    data['Real_Interest'][data['Price'] == 100.0]

    # 久期计算，久期体现了所有的时间长短和付息间隔的时间长度


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


if __name__ == "__main__":
    main()


