import requests
import json
import itertools
import tushare as ts
import pandas as pd


def fetch_stock_code_and_name(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        encoding = 'UTF-8'
        content = response.content.decode(encoding)
        # print(f"stock code is: {content}")
        beginIndex = content.find('(') + 1
        endIndex = len(content) - 2
        truncated_string = content[beginIndex:endIndex]
        print(f"after stock code is: {truncated_string}")
        stockPage = json.loads(truncated_string)
        data = stockPage["data"]
        if data:
            return data["diff"]
        else:
            return 0
    except requests.RequestException as e:
        # 捕捉并处理请求异常
        print(f"request error: {e}")


pageUrl = "https://83.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124021407173762726472_1723627676280&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f3&fs=m:1+t:23&fields=f12,f14&_=1723627676442"

ts.set_token('25359f18ae0615ffbc8dd81531b01a7a792f9bcae93a1a8e9fcb7377')
pro = ts.pro_api()
counter = itertools.count()
try:
    for i in counter:
        currUrl = f"{pageUrl}+&pn={i+1}"
        print(f"loading page: {i+1}")
        resp = fetch_stock_code_and_name(currUrl)
        if resp == 0:
            break

        for item in resp:
            # print(f"{item['f12']}")
            code = ''
            if item['f12'].startswith("6"):
                code = f"{item['f12']}.SH"
            elif item['f12'].startswith("3"):
                code = f"{item['f12']}.SZ"
            elif item['f12'].startswith("0"):
                code = f"{item['f12']}.SZ"
            else:
                break
            df = pro.daily(ts_code=code, start_date='19900101')
            print(df)
            df.to_csv(f"E://workspace//python//stocks//stock_df//{code}.csv", index=False)
except KeyboardInterrupt:
    # 处理用户中断（如Ctrl+C），以便用户可以安全地退出程序
    print("程序被用户中断")


print("end game")