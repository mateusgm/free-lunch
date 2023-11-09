
from dataclasses import dataclass
from typing import Optional
from collections import defaultdict
import pandas as pd

@dataclass
class Balance:
    eur: Optional[float] = 0
    coins: Optional[float] = 0

    def value(self, price):
        return self.coins * price

    def add(self, vol):
        self.coins += vol

class Exchange:
    TAKER_FEE = 0.26 / 100
    MAKER_FEE = 0.15 / 100

    def __init__(self, balance):
        self.balances = defaultdict(Balance)
        self.balances['eur'].add( balance )

    def buy(self, instr, coins=None, eur=None, price=None):
        return self.order(instr, coins or eur/price, price, fee=self.TAKER_FEE)

    def sell(self, instr, coins=None, eur=None, price=None):
        return self.order(instr, -coins or -eur/price, price, fee=self.MAKER_FEE)
   
    def balance(self, prices):
        total = 0
        for k,b in self.balances.items():
            total += b.value(prices.get(k,1))
        return total

    def order(self, instr, coins, price, fee=0):
        if coins + self.balances[instr].coins < 0:
            return False
        self.balances[instr].add(coins)
        self.balances['eur'].add(-coins*price)
        self.balances['eur'].add(-abs(coins*price)*fee)
        return True

class DataProvider:
    def stream(self, path='data.csv', since='2001-01-01'):
        df = pd.read_csv(path).sort_values('ts').ffill().dropna()
        df['date'] = pd.to_datetime(df['ts'],unit='s')
        df = df[df['date'] > since]
        for i,r in df.iterrows():
            yield r

