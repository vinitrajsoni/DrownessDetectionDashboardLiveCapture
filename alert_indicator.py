from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont

class AlertIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 100)
        self.color = QColor(200, 200, 200)
        
    def set_color(self, color_name):
        if color_name == "red":
            self.color = QColor(255, 0, 0)
        elif color_name == "yellow":
            self.color = QColor(255, 255, 0)
        elif color_name == "green":
            self.color = QColor(0, 255, 0)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.drawEllipse(10, 10, 80, 80)
        
        painter.setPen(QColor(0, 0, 0))
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)
        
        if self.color == QColor(255, 0, 0):
            painter.drawText(25, 55, "ALERT!")
        elif self.color == QColor(255, 255, 0):
            painter.drawText(15, 55, "CAUTION")
        elif self.color == QColor(0, 255, 0):
            painter.drawText(20, 55, "NORMAL")
