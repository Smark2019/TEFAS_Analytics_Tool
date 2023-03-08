from tefas import Crawler
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
import pandas as pd
from tabulate import tabulate

tefas = Crawler()

def print_df(data):
    for index, row in data.iterrows():

  
        print(row['date'], row['price'])

def date_parser(start_date, end_date, fund_code):
    delta = relativedelta(months=3)
    price_data = pd.DataFrame()
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while start_date < end_date:
        next_date = start_date + delta
        if next_date > end_date:
            next_date = end_date
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = next_date.strftime("%Y-%m-%d")
        data = tefas.fetch(start=start_str, end=end_str, name=fund_code, columns=["code", "date", "price", "stock"])
        price_data = pd.concat([price_data, data])
        start_date = next_date + timedelta(days=1)

    return price_data.sort_values(by='date',ascending=True)





if __name__ == "__main__":

    
    from dateutil.parser import parse
    # Retrieve the price data
    data = date_parser(start_date="2019-01-01", end_date="2023-03-01", fund_code="OSD")

    # Convert the date strings to datetime objects
    #data["date"] = data["date"].apply(parse)

    # Calculate the beginning and ending values of the fund's price data
    beginning_value = data.iloc[0]["price"]
    ending_value = data.iloc[-1]["price"]

    # Calculate the number of years between the beginning and ending dates of the fund's price data
    num_years = (data.iloc[-1]["date"] - data.iloc[0]["date"]).days / 365.25

    # Calculate the CAGR of the fund's price data
    cagr = (ending_value / beginning_value) ** (1 / num_years) - 1

    print("CAGR: {:.2%}".format(cagr))

        
        

    import matplotlib.pyplot as plt
    #x_axis = list(range(len(balance_list_sc)))
    plt.plot(data[("date")], data[("price")])
    plt.title("RPD Prices")
    plt.show()

    print(tabulate(data.reset_index(drop=True), headers = 'keys', tablefmt = 'pretty'))

    
