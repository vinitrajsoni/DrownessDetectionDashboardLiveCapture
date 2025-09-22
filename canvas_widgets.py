from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import deque

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.x_data = deque(maxlen=100)
        self.y_data = deque(maxlen=100)
        self.line, = self.axes.plot([], [])
        self.axes.set_ylim(0, 1)
        self.axes.set_xlim(0, 100)
        
    def update_plot(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)
        self.line.set_data(range(len(self.y_data)), self.y_data)
        self.axes.set_xlim(0, max(100, len(self.y_data)))
        self.draw()
