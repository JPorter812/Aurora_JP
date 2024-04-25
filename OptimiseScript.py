import pandas as pd
from Battery_energy_trader import Battery_energy_trader
from Helper import market_data_file, sheet1
import Helper
import logging
from OptimalTime_Strat import Optimal_time_strat
from pyswarm import pso
from TransactionWriter import TransactionWriter
import sys


def main():
    market_data = pd.read_excel(market_data_file, sheet_name=sheet1, usecols=[0, 1, 2])
    optimal_trading_parameters, f_opt = pso(
        lambda x: -profit_given_data(x, market_data=market_data[0:4000]),
        lb=[0, 0],
        ub=[24, 24],
        maxiter=5,
        swarmsize=24,
    )

    print(
        "optimal trading parameters: ",
        optimal_trading_parameters,
        " profit over training data: ",
        -f_opt,
    )

    if len(sys.argv) > 1 and sys.argv[1] == "w":
        transaction_writer = TransactionWriter(Helper.output_file)
    else:
        transaction_writer = None
    trader = Battery_energy_trader(transaction_writer)
    trader.trading_strat = Optimal_time_strat(optimal_trading_parameters)

    trade_length_of_data(market_data, trader)
    print(
        f"Profit over entire data: {trader.profit - 3*trader.battery.fixed_cost_per_year}"
    )
    if transaction_writer:
        transaction_writer.publish()


def profit_given_data(trading_strat_params, market_data: pd.DataFrame):
    logging.basicConfig(level=logging.INFO)

    trader = Battery_energy_trader()
    trader.trading_strat = Optimal_time_strat(trading_strat_params)

    trade_length_of_data(market_data, trader)

    return trader.profit


def trade_length_of_data(market_data, trader):
    for index, market_prices in market_data.iterrows():
        try:
            trader.trade_markets_for_half_hour(market_prices)
        except ValueError as e:
            logging.error(f"Error occurred: {e}")
            pass


if __name__ == "__main__":
    main()
