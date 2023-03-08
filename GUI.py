import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from dateutil.parser import parse
from tefas_analytics import date_parser


# Retrieve the price data
data = date_parser(start_date="2021-11-15", end_date="2023-03-05", fund_code="RPD")

# Create a Qt application and main window
app = QApplication(sys.argv)
window = QMainWindow()

# Create a chart and add a line series to it
chart = QChart()
series = QLineSeries()

# Populate the line series with the price data
for index, row in data.iterrows():
    date = parse(row['date'])
    price = row['price']
    series.append(date.toMSecsSinceEpoch(), price)

# Add the line series to the chart and set the title
chart.addSeries(series)
chart.setTitle("RPD Prices")

# Create a chart view and set the chart on it
chart_view = QChartView(chart)
chart_view.setRenderHint(QPainter.Antialiasing)

# Set the chart view as the central widget of the main window
window.setCentralWidget(chart_view)
window.resize(800, 600)
window.show()

# Start the event loop
sys.exit(app.exec_())
