from Buy_Sell import Buy_Sell


class Trade:
    def __init__(self, market, buy: Buy_Sell):
        self.market = market
        self.buy = buy
