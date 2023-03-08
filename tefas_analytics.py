from tefas import Crawler
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
import pandas as pd


tefas = Crawler()

def print_df(data):
    for index, row in data.iterrows():

  
        print(row['date'], row['price'])

def date_parser(start_date, end_date):
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
        data = tefas.fetch(start=start_str, end=end_str, name="OSD", columns=["code", "date", "price", "title"])
        price_data = pd.concat([price_data, data])
        start_date = next_date + timedelta(days=1)

    return price_data.sort_values(by='date',ascending=True)





if __name__ == "__main__":

    data = date_parser(start_date="2021-11-15", end_date="2023-03-05")
    print_df(data)
        
        

    import matplotlib.pyplot as plt
    #x_axis = list(range(len(balance_list_sc)))
    plt.plot(data[("date")], data[("price")])
    plt.title("OSD Prices")
    plt.show()

