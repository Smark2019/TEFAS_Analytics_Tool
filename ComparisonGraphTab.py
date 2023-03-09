import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QTableWidget, QTableWidgetItem,QTabWidget
from PyQt5.QtCore import QDate, Qt

class ComparisonGraphTab(QWidget):
    def __init__(self):
        super().__init__()

        # create layout for tab
        tab_layout = QVBoxLayout()
        self.setLayout(tab_layout)

        # create label for displaying current values
        self.current_values_label = QLabel()
        tab_layout.addWidget(self.current_values_label)

        # create matplotlib figure and canvas for graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        tab_layout.addWidget(self.canvas)

        # initialize x and y data
        self.x_data = []
        self.y_data = []

        # create event for mouse motion
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_motion)

    def on_mouse_motion(self, event):
        if event.inaxes:
            x = event.xdata
            y = event.ydata
            self.current_values_label.setText(f'Current values: x={x}, y={y}')

    def update_graph(self, x_data, y_data):
        # clear previous plot
        self.figure.clear()

        # create plot and add to figure canvas
        ax = self.figure.add_subplot()
        ax.plot(x_data, y_data)
        self.canvas.draw()

        # update x and y data
        self.x_data = x_data
        self.y_data = y_data
