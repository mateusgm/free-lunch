
from dataclasses import dataclass
from typing import Optional
from collections import defaultdict
import pandas as pd

@dataclass
class Balance:
    eur: Optional[float] = 0
    coins: Optional[float] = 0

    def market_value(self, price):
        return self.coins * price

    def move(self, vol, price):
        self.coins += vol/price
        self.eur = self.market_value(price)

class Exchange:
    TAKER_FEE = 0.26 / 100
    MAKER_FEE = 0.15 / 100
    balances = defaultdict(Balance)

    def buy(instr, vol, prices):
        return Exchange.update(instr, vol, prices[instr], fee=Exchange.TAKER_FEE)

    def sell(instr, vol, prices):
        return Exchange.update(instr, -vol, prices[instr], fee=Exchange.MAKER_FEE)
    
    def update(instr, vol, price, fee=0):
        if vol + Exchange.balances[instr].market_value(price) < 0:
            return False
        Exchange.balances[instr].move(vol, price)
        Exchange.balances['eur'].move(-abs(vol)*fee, 1)
        return True

    def balance(prices):
        total = 0
        for k,b in Exchange.balances.items():
            total += b.market_value(prices.get(k,1))
        return total

class DataProvider:
    def stream(self, path='data.csv'):
        df = pd.read_csv(path).sort_values('ts').ffill().dropna()
        df['date'] = pd.to_datetime(df['ts'],unit='s')
        for i,r in df.iterrows():
            yield r

