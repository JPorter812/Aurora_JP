from Buy_Sell import Buy_Sell
from Trade import Trade
from Trading_Strat import Trading_Strat
from Helper import market1, market2
import pandas as pd


# a trading strat determines what market to sell on, and at what rate. The strat should never give parameters outside the constraints of the battery. The battery
# should send an error up to the user if it does. The trading strategy has access to data up to the current datetime
# A generator company who has a single battery with which to trade energy.
class Optimal_time_strat(Trading_Strat):

    # define two key time points in the day: market_max_time, market__min_time (self explanatory)
    # min time =
    def __init__(self, parameters: list[float]) -> None:
        self._buy_time = parameters[0]
        self._sell_time = parameters[1]

    def decide_trade(self, market_prices: pd.Series):
        timestamp = market_prices.iloc[0]
        time = timestamp.hour + timestamp.minute / 60
        if self._buy_time <= time < self._buy_time + 2:
            market_with_lowest_price = market_prices[[market1, market2]].idxmin()
            return Trade(market_with_lowest_price, Buy_Sell.Buy)
        if self._sell_time <= time < self._sell_time + 2:
            market_with_highest_price = market_prices[[market1, market2]].idxmax()
            return Trade(market_with_highest_price, Buy_Sell.Sell)
