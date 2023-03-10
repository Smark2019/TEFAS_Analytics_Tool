import sys
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMessageBox,QDialog,QProgressBar,QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem,QTabWidget
from PyQt5.QtCore import QDate, Qt,QThread, pyqtSignal
import numpy as np
import pandas as pd
from tefas_analytics import date_parser, get_CAGR,get_all_fund_codes
from ComparisonGraphTab import ComparisonGraphTab
from FundCodeSelectionPopup import FundCodeSelectionPopup
from datetime import datetime
from PyQt5.QtGui import QIcon


class Thread(QThread):
    _signal = pyqtSignal(int)
    def __init__(self,waits_for = 0.05):
        super(Thread, self).__init__()
        self.waits_for = waits_for

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.05)
            self._signal.emit(i)


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
        
        # create a progress bar
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        main_layout.addWidget(self.pbar)

        # create line edit for fund name
        fund_label = QLabel('Fund Name:')
        self.fund_edit = QLineEdit()
        fund_layout = QHBoxLayout()
        fund_layout.addWidget(fund_label)
        fund_layout.addWidget(self.fund_edit)
        main_layout.addLayout(fund_layout)

        # create date range picker
        date_label = QLabel('Date Range:')
        self.start_date_edit = QDateEdit(QDate.currentDate().addMonths(-3))
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        date_layout = QHBoxLayout()
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.start_date_edit)
        date_layout.addWidget(self.end_date_edit)
        main_layout.addLayout(date_layout)

        # create layout for plot and export buttons
        plot_layout = QHBoxLayout()
        main_layout.addLayout(plot_layout)

        # create button to plot graph
        self.plot_button = QPushButton('Plot Graph')
        self.plot_button.clicked.connect(self.plot_graph)
        plot_layout.addWidget(self.plot_button)
        
        # create button to export to Excel
        self.tiny_export_button = QPushButton()
        self.tiny_export_button.setIcon(QIcon('excel_icon.png'))
        self.tiny_export_button.setFixedSize(90, 25)
        self.tiny_export_button.clicked.connect(self.only_one_export_to_excel)
        self.tiny_export_button.setEnabled(False)
        plot_layout.addWidget(self.tiny_export_button)

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
        comparison_tab.update_graph()

        main_layout.addWidget(self.pbar)

        # create button to export to Excel
        export_button = QPushButton('Export Chosen Funds to Excel ')
        export_button.clicked.connect(self.export_to_excel)
        main_layout.addWidget(export_button)

    def only_one_export_to_excel(self):      # exporting chosen ONE fund price data to excel sheet.
        
        start_date_string = self.start_date_edit.date()
        end_date_string = self.end_date_edit.date()
        
        start_date_string = '{0}-{1}-{2}'.format(start_date_string.year(), start_date_string.month(), start_date_string.day())
        end_date_string = '{0}-{1}-{2}'.format(end_date_string.year(), end_date_string.month(), end_date_string.day())
        # getting data
        current_fund_price_df = date_parser(start_date = start_date_string, end_date = end_date_string, fund_code = self.fund_edit.text(), columns= ["all"])
        writer = pd.ExcelWriter(path =self.fund_edit.text()+".xlsx",engine='xlsxwriter')   
                
        # format the date column as "dd-mm-yyyy" and then splitting
        current_fund_price_df['date'] = pd.to_datetime(current_fund_price_df['date'], errors='coerce')
        
        #dataframe['date'] = dataframe['date'].dt.strftime('%d-%m-%Y')
        current_fund_price_df.loc[:, 'date'] = current_fund_price_df['date'].dt.strftime('%d-%m-%Y')
        # writing to excel
        current_fund_price_df.to_excel(writer,sheet_name=self.fund_edit.text(),startrow=0 , startcol=0)   
        
        writer.save()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The export to Excel was successful.")
        msg.setInformativeText("The data has been exported correctly.")
        msg.setWindowTitle("Export Successful")
        msg.exec_()
            

    def export_to_excel(self):      # exporting chosen fund price data to excel sheet.
        
        self.btnFunc(waits_for= 0.06)
        func_codes_list = get_all_fund_codes() # gettin all actual fund codes ...
        popup = FundCodeSelectionPopup(func_codes_list)
        
        if popup.exec_() == QDialog.Accepted:
            print('Selected Fund Codes:', popup.selected_fund_codes)
        if(len(popup.selected_fund_codes) != 0):
            self.btnFunc()
            start_date_string = self.start_date_edit.date()
            end_date_string = self.end_date_edit.date()
            
            start_date_string = '{0}-{1}-{2}'.format(start_date_string.year(), start_date_string.month(), start_date_string.day())
            end_date_string = '{0}-{1}-{2}'.format(end_date_string.year(), end_date_string.month(), end_date_string.day())
            # init df list to hold price df s:
            price_dfs_list = []
            for fund_code in popup.selected_fund_codes:
                current_fund_price_df = date_parser(start_date = start_date_string, end_date = end_date_string, fund_code = fund_code,columns=["code", "date", "price", "stock"])
                price_dfs_list.append(current_fund_price_df)

            # finding most late date for chosen funds
            most_late_date = datetime(1900, 1, 1)
            for dataframe in price_dfs_list:
                dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')
                if(dataframe['date'].iloc[0] > most_late_date ):
                    most_late_date = dataframe['date'].iloc[0]
            
            # calling multiple_dfs func:
            self.multiple_dfs(price_dfs_list, most_late_date= most_late_date)


    # funtion
    def multiple_dfs(self,df_list, sheets = "Prices Sheet", file_name = "Prices.xlsx", spaces = 2,most_late_date = datetime(1900, 1, 1)):
        writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
        col = 0
        
        for dataframe in df_list:
            
            # format the date column as "dd-mm-yyyy" and then splitting
            dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')
            
            dataframe = dataframe[dataframe['date'] >= most_late_date]
            #dataframe['date'] = dataframe['date'].dt.strftime('%d-%m-%Y')
            dataframe.loc[:, 'date'] = dataframe['date'].dt.strftime('%d-%m-%Y')
            # writing to excel
            dataframe.to_excel(writer,sheet_name=sheets,startrow=0 , startcol=col)   
            col = col + len(dataframe.columns) + spaces + 1
        writer.save()

        # QMessageBox demo:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The export to Excel was successful.")
        msg.setInformativeText("The data has been exported correctly.")
        msg.setWindowTitle("Export Successful")
        msg.exec_()


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
            
	    
            if(self.fund_edit.text() == "" or len(self.fund_edit.text()) > 3 ):
                   
                    self.fund_edit.clear()
                    self.fund_edit.setPlaceholderText("       GEÇERLİ FON KODU GİRİNİZ !       ")
                    raise Exception()
            # activate progress bar
            self.btnFunc()
            whole_df = date_parser(start_date=start_date_string, end_date=end_date_string, fund_code=self.fund_edit.text(), columns=["code", "date", "price"])
            x = whole_df["date"]
            y = whole_df["price"] 
	    



            # calculate return for selected date range

            beginning_price = whole_df.iloc[0]["price"]
            ending_price = whole_df.iloc[-1]["price"]
            return_for_prices = ((ending_price / beginning_price) -1 )* 100
            # create plot and add to figure canvas
            ax = self.figure.add_subplot()
            
            self.figure.suptitle(f'{self.fund_edit.text()} Prices Between {start_date_string} and {end_date_string}', fontsize=10)
            
            
            ax.set_xlabel("Date",fontsize=10)
            ax.set_ylabel("Price",fontsize=10)
            ax.plot(x, y)
            self.canvas.draw()
            # update table with statistics (random data for demonstration purposes)
            stats_table = self.centralWidget().findChild(QTableWidget)
            stats_table.setItem(0, 0, QTableWidgetItem(str(round(y.std(),2))))
            stats_table.setItem(0, 1, QTableWidgetItem(str(get_CAGR(whole_df))))
            stats_table.setItem(0, 2, QTableWidgetItem(str(round(return_for_prices,2)) + " %"))
            stats_table.resizeColumnsToContents()

            # lets user to use Tiny exporting excel button:
            self.tiny_export_button.setEnabled(True)
            self.tiny_export_button.setText(self.fund_edit.text())
            
		
		
        except:
            print("GEÇERSİZ FON GİRİŞİ !")

    
    def btnFunc(self, waits_for = 0.05):
        self.thread = Thread(waits_for = 0.05)
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        self.plot_button.setEnabled(False)

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)
            self.plot_button.setEnabled(True)	
        
            

                
                



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


