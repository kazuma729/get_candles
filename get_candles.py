#!/usr/bin/env python
# coding: utf-8

import ccxt
from pprint import pprint
import pandas as pd

from datetime import datetime
import time
import calendar, ccxt

now = datetime.utcnow() # 現在時刻のUTC naiveオブジェクト
chart_time = 15          # 時間足の設定(分)
chart_amount = 40        # 足の本数

# UTC naiveオブジェクト -> UnixTime
unixtime = calendar.timegm(now.utctimetuple())

# 5分前のUnixTime( !!!ミリ秒!!!! )
since = (unixtime - 60 * chart_time * chart_amount) * 1000

# 価格データ取得
base = ccxt.binance()
candles = base.fetch_ohlcv( symbol='BTC/USDT',                   # 暗号資産[通貨]
                            timeframe = str(chart_time) + 'm',  # 時間足('1m', '5m', '1h', '1d')
                            since=since,                        # 取得開始時刻(Unix Timeミリ秒)
                            limit=500,                         # 取得件数(デフォルト:100、最大:500)
                            )

# 取得したローソク足データをdataframeに格納する
for i in range(len(candles)):
    candles[i][5] = round(candles[i][5],10) # Volumeを有効数字内に収める
df = pd.DataFrame(candles, columns=['datetime', 'op','hi', 'lo', 'cl', 'volume'])

# 取得したローソク足のなかで最も最新のローソク足の時間をUTC時間を取得(tail_time)
unixtimes = df['datetime'].values
tail_unixtime = unixtimes[-1].item() / 1000

# datetime型の時間取得用
import datetime
tail_time = datetime.datetime.fromtimestamp(tail_unixtime)