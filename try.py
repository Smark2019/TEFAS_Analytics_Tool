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
        export_button = QPushButton()
        export_button.setIcon(QIcon('excel_icon.png'))
        export_button.setFixedSize(25, 25)
        export_button.clicked.connect(self.export_to_excel)
        plot_layout.addWidget(export_button)

        # create tabs for statistics and comparison graph
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # create matplotlib figure and canvas for graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        main_layout.addWidget(self.canvas)

        # create label to show current x and y value
        self.current_values_label = QLabel("Current Values:")
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
