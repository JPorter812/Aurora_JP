from Buy_Sell import Buy_Sell
from Helper import battery_file
from Trading_Strat import Trading_Strat
from Battery_1 import Battery
import pandas as pd
from TransactionWriter import TransactionWriter


class Battery_energy_trader:
    def __init__(self, transaction_writer: TransactionWriter = None):
        self.battery = Battery(battery_file)
        self._profit = 0.0
        self._annual_profit = 0.0
        self.transaction_writer = transaction_writer

    @property
    def trading_strat(self):
        return self._trading_strat

    @trading_strat.setter
    def trading_strat(self, strat: Trading_Strat):
        self._trading_strat = strat

    @property
    def profit(self):
        return self._profit

    def trade_markets_for_half_hour(self, market_prices) -> float:
        timestamp: pd.Timestamp = market_prices.iloc[0]
        if trade := self.trading_strat.decide_trade(market_prices):
            if trade.buy == Buy_Sell.Buy:
                if self.buy(
                    price=market_prices[trade.market],
                    time=0.5,
                ):
                    if self.transaction_writer:
                        self.transaction_writer.WriteTrade(
                            timestamp, self.battery.max_charging
                        )
            if trade.buy == Buy_Sell.Sell:
                if self.sell(
                    price=market_prices[trade.market],
                    time=0.5,
                ):
                    if self.transaction_writer:
                        self.transaction_writer.WriteTrade(
                            timestamp, -self.battery.max_discharge
                        )
        if (
            self.transaction_writer
            and timestamp.month == 12
            and timestamp.day == 31
            and timestamp.hour == 23
            and timestamp.minute == 30
        ):
            self._annual_profit = self.profit - self._annual_profit
            self.transaction_writer.write_profit(
                timestamp.year, self._annual_profit - self.battery.fixed_cost_per_year
            )

    def buy(self, price, time):
        if self.battery.charge(time):
            self._profit -= price * self.battery.max_charging * time
            return True
        return False

    def sell(self, price, time):
        if self.battery.discharge(time):
            self._profit += (
                self.battery.max_discharge
                * price
                * time
                * (1 - self.battery.discharge_efficiency)
                * (1 - self.battery.charge_efficiency)
            )
            return True
        return False
