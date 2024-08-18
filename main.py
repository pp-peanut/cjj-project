import tushare as ts
import pandas as pd
from pandas import DataFrame,Series
import numpy as nm

ts.set_token('25359f18ae0615ffbc8dd81531b01a7a792f9bcae93a1a8e9fcb7377')
pro = ts.pro_api()
df = pro.daily(ts_code='002230.SZ', start_date='20180701')
#df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

print(df)

for row in df.itertuples(index=True, name='ts_code'):
    print(f"ts_code: {row.ts_code}, trade_date: {row.trade_date}, open: {row.open}")