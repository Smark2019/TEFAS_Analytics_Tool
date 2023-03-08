import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDate, Qt
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fund Analyzer')
        self.setGeometry(100, 100, 800, 600)

        # create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # create layout for main widget
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # create line edit for fund name
        fund_label = QLabel('Fund Name:')
        self.fund_edit = QLineEdit()
        fund_layout = QHBoxLayout()
        fund_layout.addWidget(fund_label)
        fund_layout.addWidget(self.fund_edit)
        main_layout.addLayout(fund_layout)

        # create date range picker
        date_label = QLabel('Date Range:')
        self.start_date_edit = QDateEdit(QDate.currentDate().addYears(-1))
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        date_layout = QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(self.end_date_edit)
        main_layout.addLayout(date_layout)

        # create button to plot graph
        plot_button = QPushButton('Plot Graph')
        plot_button.clicked.connect(self.plot_graph)
        main_layout.addWidget(plot_button)

        # create matplotlib figure and canvas for graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # create table for statistics
        stats_table = QTableWidget(1, 3)
        stats_table.setHorizontalHeaderLabels(['Standard Deviation', 'CAGR', 'Total Return'])
        main_layout.addWidget(stats_table)

    def plot_graph(self):
        # clear previous plot
        self.figure.clear()

        # get data for plot (random data for demonstration purposes)
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # create plot and add to figure canvas
        ax = self.figure.add_subplot()
        ax.plot(x, y)
        self.canvas.draw()

        # update table with statistics (random data for demonstration purposes)
        stats_table = self.centralWidget().findChild(QTableWidget)
        stats_table.setItem(0, 0, QTableWidgetItem('0.05'))
        stats_table.setItem(0, 1, QTableWidgetItem('0.1'))
        stats_table.setItem(0, 2, QTableWidgetItem('0.2'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
