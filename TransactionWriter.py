import pandas as pd


class TransactionWriter:
    def __init__(self, outputfile):
        self.data = {"Timestamp": [], "Rate of energy purchase (MW)": []}
        self.outputfile = outputfile
        self.yearlyProfit = {"Year": [], "Profit": []}

    def WriteTrade(self, timestamp, battery_activity):
        self.data["Timestamp"].append(timestamp)
        self.data["Rate of energy purchase (MW)"].append(battery_activity)

    def write_profit(self, year, profit):
        self.yearlyProfit["Year"].append(year)
        self.yearlyProfit["Profit"].append(profit)

    def publish(self):
        df = pd.DataFrame(self.data)
        df2 = pd.DataFrame(self.yearlyProfit)

        with pd.ExcelWriter(self.outputfile, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Half-hourly purchases", index=False)
            df2.to_excel(writer, sheet_name="Annual profit", index=False)
