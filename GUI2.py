import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem,QTabWidget
from PyQt5.QtCore import QDate, Qt
import numpy as np
import pandas as pd
from tefas_analytics import date_parser, get_CAGR
from ComparisanGraphTab import ComparisonGraphTab


class MainWindow(QMainWindow):
    def on_mouse_move(self,event):
        if event.inaxes :
            
            x, y = event.xdata, event.ydata
            
            x_str = str(x)
            y_str = str(y)
            
            self.current_values_label.setText(f'Price: {y_str}')
        
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
        # create tabs for statistics and comparison graph
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)


        # create matplotlib figure and canvas for graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        main_layout.addWidget(self.canvas)
        
        # create label to show current x and y value
        self.current_values_label= QLabel("Current Values:")
        main_layout.addWidget(self.current_values_label)
        # create table for statistics

       # create statistics tab
        stats_tab = QWidget()
        stats_layout = QVBoxLayout()
        stats_tab.setLayout(stats_layout)
        self.stats_table = QTableWidget(1, 3)
        self.stats_table.setHorizontalHeaderLabels(['Standard Deviation', 'CAGR', 'Total Return'])
        stats_layout.addWidget(self.stats_table)
        self.tabs.addTab(stats_tab, 'Statistics')

        # create comparison graph tab
        comparison_tab = ComparisonGraphTab()
        self.tabs.addTab(comparison_tab, 'Comparison Graph')
        
    def plot_graph(self):
    
        
        
        # clear previous plot
        self.figure.clear()

        # get data for plot (random data for demonstration purposes)
        
        start_date_string = self.start_date_edit.date()
        end_date_string = self.end_date_edit.date()
        
        start_date_string = '{0}-{1}-{2}'.format(start_date_string.year(), start_date_string.month(), start_date_string.day())
        end_date_string = '{0}-{1}-{2}'.format(end_date_string.year(), end_date_string.month(), end_date_string.day())
        x = pd.DataFrame()
        y = pd.DataFrame()
        whole_df = pd.DataFrame()
        
        try:
            
	    
            if(self.fund_edit.text() == ""):
                   
                    self.fund_edit.setText("GEÇERLİ FON KODU GİRİNİZ:")
                    raise Exception()
            whole_df = date_parser(start_date=start_date_string, end_date=end_date_string, fund_code=self.fund_edit.text())
            x = whole_df["date"]
            y = whole_df["price"] 
	    



            # calculate return for selected date range

            beginning_price = whole_df.iloc[0]["price"]
            ending_price = whole_df.iloc[-1]["price"]
            return_for_prices = ((ending_price / beginning_price) -1 )* 100
            # create plot and add to figure canvas
            ax = self.figure.add_subplot()
            ax.plot(x, y)
            self.canvas.draw()
            # update table with statistics (random data for demonstration purposes)
            stats_table = self.centralWidget().findChild(QTableWidget)
            stats_table.setItem(0, 0, QTableWidgetItem(str(round(y.std(),2))))
            stats_table.setItem(0, 1, QTableWidgetItem(str(get_CAGR(whole_df))))
            stats_table.setItem(0, 2, QTableWidgetItem(str(round(return_for_prices,2)) + " %"))
            stats_table.resizeColumnsToContents()               
            
		
		
        except:
            print("Entered except block.")
		
        
            

                
                



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())