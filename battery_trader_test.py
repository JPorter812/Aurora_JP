import pandas as pd
from Battery_energy_trader import Battery_energy_trader
from Helper import market1, market2
import Helper
import logging
from pandas import Timestamp

from OptimalTime_Strat import Optimal_time_strat


def test_trader():
    trader = Battery_energy_trader()
    trader.trading_strat = Optimal_time_strat([4, 17])

    market_price_1 = pd.Series(
        {0: Timestamp("1/1/18 4:00"), market1: 37.55, market2: 38.9}
    )
    market_price_2 = pd.Series(
        {0: Timestamp("1/1/18 17:00"), market1: 63.07, market2: 74.56}
    )

    trader.trade_markets_for_half_hour(market_price_1)
    trader.trade_markets_for_half_hour(market_price_2)

    assert trader.profit == 0.95 * 0.95 * 74.56 - 37.55


def test_trader_with_file():
    logging.basicConfig(level=logging.INFO)

    trader = Battery_energy_trader()
    trader.trading_strat = Optimal_time_strat([4, 16])

    market_data = pd.read_excel(
        Helper.market_data_file, sheet_name=Helper.sheet1, usecols=[0, 1, 2]
    )

    for index, market_prices in market_data.iterrows():
        try:
            trader.trade_markets_for_half_hour(market_prices)
        except ValueError as e:
            logging.error(f"Error occurred: {e}")
            pass

    logging.info(trader.profit)


if __name__ == "__main__":
    test_trader_with_file()
