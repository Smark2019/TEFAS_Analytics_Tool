from tefas import Crawler
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt



def print_df(data):
    print(tabulate(data.reset_index(drop=True), headers = 'keys', tablefmt = 'pretty'))


def date_parser(start_date, end_date, fund_code):
    tefas = Crawler()

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

    return price_data.sort_values(by='date',ascending=True) # returns df


def get_CAGR(price_data_df):
    # Calculate the beginning and ending values of the fund's price data
    beginning_value = price_data_df.iloc[0]["price"]
    ending_value = price_data_df.iloc[-1]["price"]

    # Calculate the number of years between the beginning and ending dates of the fund's price data
    num_years = (price_data_df.iloc[-1]["date"] - price_data_df.iloc[0]["date"]).days / 365.25

    # Calculate the CAGR of the fund's price data
    cagr = (ending_value / beginning_value) ** (1 / num_years) - 1

    return ("CAGR: {:.2%}".format(cagr))        # returns string



def plot_graph(price_data_df):
    plt.plot(price_data_df[("date")], price_data_df[("price")])
    plt.title("RPD Prices")
    plt.show()

if __name__ == "__main__":

    

    # Retrieve the price data
    #data = date_parser(start_date="2019-01-01", end_date="2023-03-01", fund_code="")

    #print(get_CAGR(data))
    #plot_graph(data)
    tefas = Crawler()
    data = tefas.fetch(start="2020-11-20")[("code")]
    data = data.reset_index(drop=True)
    print(data)



    


    
