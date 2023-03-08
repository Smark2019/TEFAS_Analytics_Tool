from tefas import Crawler

tefas = Crawler()

data = tefas.fetch(start="2022-09-01", end="2022-12-01", name="OSD", columns=["code", "date", "price","title"])
print(data.describe())


"""
import matplotlib.pyplot as plt
#x_axis = list(range(len(balance_list_sc)))
plt.plot(data[("date")], data[("price")], label="Prices")
plt.title("OSD Prices")
plt.show()

"""