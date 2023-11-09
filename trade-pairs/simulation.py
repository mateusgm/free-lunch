from helpers import DataProvider, Exchange

Ex = Exchange(balance=2000)

class ArbitrageBot:

    THRESHOLD = 2

    def __init__(self, instr1, instr2):
        self.i1 = instr1
        self.i2 = instr2

    def loop(self, data, stake=1000, k=10, verbose=True):
        btc, eth = self.i1, self.i2
        steps = movement = 0
        results = []
        change = 'BEGN'

        orig_prices = next(data)
        orig_ratio = ratio = orig_prices[btc] / orig_prices[eth]
        Ex.buy(btc, eur=stake, price=orig_prices[btc])
        Ex.buy(eth, eur=stake, price=orig_prices[eth])
        step_sizes = { btc: Ex.balances[btc] / k, eth: Ex.balances[eth] / k }

        for i,r in enumerate(data):
            change and verbose and \
                print("{} | {} | Ratio {:.2f} Change {:.1f}%\t| Positions BTC:{:.5f} ETH:{:.5f} EUR:{:.1f}\t| {:.2f} {:.2f}".format( \
                    r['date'], change, ratio, movement, \
                    Ex.balances[btc], \
                    Ex.balances[eth], \
                    Ex.balances['eur'], \
                    Ex.balance(r), \
                    r[btc] \
                ), flush=True)

            ratio = r[btc] / r[eth]
            movement = 100*ratio/orig_ratio - 100
            change = False
           
            if movement >= (steps+1)*self.THRESHOLD:
                if Ex.sell(btc, step_sizes[btc], price=r[btc]):
                    Ex.buy(eth, step_sizes[eth], price=r[eth])
                    steps += 1
                    change = 'SHRT'

            if movement <= (steps-1)*self.THRESHOLD:
                if Ex.sell(eth, step_sizes[eth], price=r[eth]):
                    Ex.buy(btc, step_sizes[btc], price=r[btc])
                    steps -= 1
                    change = 'LONG'
        
        print(Ex.balances)

if __name__ == '__main__':
    data = DataProvider().stream('data.csv') #, since='2023-10-23 22:41:08')
    bot = ArbitrageBot( 'BTC/USD', 'ETH/USD' )
    bot.loop(data)

