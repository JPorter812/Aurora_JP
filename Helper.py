from datetime import time

market1 = "Market 1 Price [£/MWh]"
market2 = "Market 2 Price [£/MWh]"

output_file = "TransactionsAndProfits.xlsx"

market_data_file = r"Second Round Technical Question - Attachment 2.xlsx"
battery_file = r"Second Round Technical Question - Attachment 1.xlsx"
sheet1 = "Half-hourly data"


def convert_to_time(float_hours) -> time:
    # Convert float hours to hours and minutes
    hours = int(float_hours)
    minutes = int((float_hours - hours) * 60)

    # Create a time object
    time_obj = time(hour=hours, minute=minutes)

    return time_obj
