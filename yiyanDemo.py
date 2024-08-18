import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import tushare as ts
import numpy as np

def fetch_stock_data(stock_symbol, start_date, end_date):
    # ts.set_token('25359f18ae0615ffbc8dd81531b01a7a792f9bcae93a1a8e9fcb7377')
    # pro = ts.pro_api()
    # df = pro.daily(ts_code=stock_symbol, start_date=start_date)
    # print(df)
    # print(df.columns)
    # Index(['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'],
    code = '000001.SZ.csv'
    df = pd.read_csv(f"E://workspace//python//stocks//stock_df//{code}")
    return df


def generate_signals(df, short_window=40, long_window=100):
    """生成买卖信号"""
    signals = pd.DataFrame(index=df.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # 生成信号
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]
                                                > signals['long_mavg'][short_window:], 1.0, 0.0)
    signals['positions'] = signals['signal'].diff()
    return signals


def plot_data(df, signals):
    """绘制股票价格和信号"""
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['close'], label='close Price', alpha=0.35)
    plt.plot(df.index, signals['short_mavg'], label='Short MA')
    plt.plot(df.index, signals['long_mavg'], label='Long MA')
    plt.scatter(signals.loc[signals.positions == 1.0].index,
                df['close'][signals.positions == 1.0],
                label='Buy Signal', marker='^', color='g')
    plt.scatter(signals.loc[signals.positions == -1.0].index,
                df['close'][signals.positions == -1.0],
                label='Sell Signal', marker='v', color='r')
    plt.title('Stock Price and Trading Signals')
    plt.legend()
    plt.show()


# 股票代码和日期
stock_symbol = '002230.SZ'
start_date = '2020-01-01'
end_date = '2023-01-01'

# 获取数据
df = fetch_stock_data(stock_symbol, start_date, end_date)

# 生成信号
signals = generate_signals(df)

# 绘制数据和信号
plot_data(df, signals)