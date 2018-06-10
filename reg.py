#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Hikari Software
# Y-Enterprise

import numpy as np
import pandas as pd
import re

def main():
    # Index(['Name', 'Total', 'Ticket_Value', 'Price', 'Maturity', 'Rate','Payment_Date', 'Place', 'Institution', 'Payment_Method','Issuing_Method', 'Type', 'Year'],dtype='object')
    data=pd.read_csv("bond.csv")
    data['Year'] = [int(re.findall(r'\d+',s)[0]) for s in data['Name']]
    data['Year'][data['Year']<30] += 2000 # 06年等省略
    data['Year'][data['Year']<100] += 1900 # 99年等省略


if __name__ == "__main__":
    main()


