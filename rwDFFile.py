import tushare as ts
import pandas as pd

ts.set_token('25359f18ae0615ffbc8dd81531b01a7a792f9bcae93a1a8e9fcb7377')
pro = ts.pro_api()
df = pro.daily(ts_code='000957.SZ', start_date='20180701')
#002230.SZ
#688090.SH
#000957.SZ

df.to_csv('000957.csv', index=False)

# 从CSV文件读取数据到DataFrame
df_read = pd.read_csv('000957.csv')

# 显示读取的DataFrame
print(df_read)