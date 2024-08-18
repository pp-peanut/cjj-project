import pandas as pd
import numpy as np
import tushare as ts

# 读取股票数据，假设数据已经存在一个DataFrame中，包含日期、开盘价、最高价、最低价、收盘价
# df = pd.read_csv('stock_data.csv', parse_dates=['date'])

# 示例数据生成
# ts.set_token('25359f18ae0615ffbc8dd81531b01a7a792f9bcae93a1a8e9fcb7377')
# pro = ts.pro_api()
# df = pro.daily(ts_code='002230.SZ', start_date='20180701')
code = '002230.SZ.csv'
df = pd.read_csv(f"E://workspace//python//stocks//stock_df//{code}")
df = df.iloc[::-1]
# 设置突破期
breakout_period = 30

# 计算买入信号：价格突破过去N天的最高点
df['high_breakout'] = df['high'].rolling(window=breakout_period).max().shift(1)
df['buy_signal'] = df['close'] > df['high_breakout']

# 计算卖出信号：价格跌破过去N天的最低点
sell_breakout_period = 10
df['low_breakout'] = df['low'].rolling(window=sell_breakout_period).min().shift(1)
df['sell_signal'] = df['close'] < df['low_breakout']

# 生成交易信号
df['signal'] = np.where(df['buy_signal'], 'Buy', np.where(df['sell_signal'], 'Sell', 'Hold'))

# 输出交易信号
# print(df[['trade_date', 'close', 'signal']])
filtered_df = df.query('signal == "Buy" or signal == "Sell"')
print(filtered_df[['trade_date', 'close', 'signal']])

lastOperation = 'Buy'
buyPrice = df.iloc[0, 2]
buyDate = df.iloc[0, 1]
print(f"buyDate={buyDate} buyPrice={buyPrice}")
profit = 0.0
profitPercent = 0.0
for index, row in filtered_df.iterrows():
    operation = row.signal
    closePrice = row.close
    tradeDate = row.trade_date
    # print(f"tradeDate={tradeDate} operation={operation}  closePrice={closePrice}")
    if lastOperation == 'Buy' and operation == 'Buy':
        continue
    elif lastOperation == 'Buy' and operation == 'Sell':
        profit = profit + (closePrice - buyPrice)
        profitPercent = profit + (closePrice - buyPrice)
        print(f"buyDate={buyDate} buyPrice={buyPrice}  sellDate={tradeDate} sellPrice={closePrice} profit += {(closePrice - buyPrice)}")
        lastOperation = 'Sell'
    elif lastOperation == 'Sell' and operation == 'Buy':
        buyPrice = closePrice
        lastOperation = 'Buy'
        buyDate = tradeDate
    elif lastOperation == 'Sell' and operation == 'Sell':
        continue

print(f"profit={profit} profitPercent={()}")

# 可视化交易信号
# import matplotlib.pyplot as plt
#
# plt.figure(figsize=(14, 7))
# plt.plot(df['trade_date'], df['close'], label='Close Price', color='black')
# plt.scatter(df[df['signal'] == 'Buy']['trade_date'], df[df['signal'] == 'Buy']['close'], marker='^', color='green', label='Buy Signal')
# plt.scatter(df[df['signal'] == 'Sell']['trade_date'], df[df['signal'] == 'Sell']['close'], marker='v', color='red', label='Sell Signal')
# plt.title('Turtle Trading Strategy')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.legend()
# plt.show()