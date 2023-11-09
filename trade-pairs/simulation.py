from helpers import DataProvider, Exchange

class ArbitrageBot:

    THRESHOLD = 2

    def __init__(self, instr1, instr2):
        self.i1 = instr1
        self.i2 = instr2

    def loop(self, data, stake=1000, k=10, verbose=True):
        btc, eth = self.i1, self.i2
        steps = 0
        results = []

        orig_prices = next(data)
        orig_ratio = orig_prices[btc] / orig_prices[eth]
        Exchange.buy(btc, vol=stake, prices=orig_prices)
        Exchange.buy(eth, vol=stake, prices=orig_prices)
        verbose and print("Start | Ratio {:.2f} | Balance ETH 1000 BTC 1000".format(orig_ratio))

        for i,r in enumerate(data):
            ratio = r[btc] / r[eth]
            movement = 100*ratio/orig_ratio - 100
           
            if movement >= (steps+1)*self.THRESHOLD:
                if Exchange.sell(btc, vol=stake/k, prices=r):
                    Exchange.buy(eth, vol=stake/k, prices=r)
                    steps += 1
                    verbose and print("{} | Ratio {:.2f} Change {:.1f}% | Sell: 100@BTC Buy: 100@ETH | Positions {:.1f}@BTC {:.1f}@ETH".format( r['date'], ratio, movement, Exchange.balances[btc].market_value(r[btc]), Exchange.balances[eth].market_value(r[eth]) ), flush=True)

            if movement <= (steps-1)*self.THRESHOLD:
                if Exchange.sell(eth, vol=stake/k, prices=r):
                    Exchange.buy(btc, vol=stake/k, prices=r)
                    steps -= 1
                    verbose and print("{} | Ratio {:.2f} Change {:.1f}% | Buy: 100@BTC Sell: 100@ETH | Positions {:.1f}@BTC {:.1f}@ETH".format( r['date'], ratio, movement, Exchange.balances[btc].market_value(r[btc]), Exchange.balances[eth].market_value(r[eth]) ), flush=True)

            results.append( Exchange.balance(r) )
            if i % 10000 == 0:
                benchmark = sum([ r[i] * stake/orig_prices[i] for i in [btc, eth] ])
                not verbose and print("{}\t{:.2f}\t{:.2f}\t{}".format(r['date'], results[-1], benchmark, steps), flush=True, sep="\t")
        
        print(Exchange.balances)

if __name__ == '__main__':
    bot = ArbitrageBot( 'BTC/USD', 'ETH/USD' )
    data = DataProvider()
    bot.loop(data.stream('data.csv'))

