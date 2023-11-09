
import ccxt
import ccxt.pro as cpro
import os
import sys
import asyncio
import pandas as pd
from asyncio import run
from collections import defaultdict

async def ticks(con):
    tick = await con.watch_ticker('BTC/EUR')
    print(con.iso8601(tick['timestamp']), '****', tick['last'], sep="\t", flush=True)

async def trades(con):
    data = await con.watch_trades('BTC/EUR')
    for t in data:
        print(con.iso8601(t['timestamp']), t['side'], t['price'], sep="\t", flush=True)

async def stream():
    try:
        con = cpro.kraken()
        while True:
            await ticks(con)
            await trades(con)
    except asyncio.exceptions.CancelledError:
        pass
    finally:    
        await con.close()

def historic_trades(since=None):
    con = ccxt.kraken()
    data = defaultdict(dict)

    for p in [ 'BTC/USD', 'ETH/USD' ]:
        last_ts = since
        trades = [0] * 1000
        while len(trades) == 1000:
            trades = con.fetch_trades(p, last_ts, limit=1000)
            for t in trades:
                last_ts = t['timestamp']
                data[last_ts // 1000][p] = t['price']
            print((last_ts - since) // 1000 / 3600 / 24)
    
            df = pd.DataFrame.from_dict(data, orient='index').rename_axis('ts').reset_index()
            df.to_csv('data.csv', index=False)
    
if sys.argv[1] == 'stream':
    run(main())

else:
    historic_trades(since=1696776173000)

