import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from video_thread import VideoThread
from canvas_widgets import MplCanvas
from alert_indicator import AlertIndicator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drowsiness Detection Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Left panel
        left_panel = QVBoxLayout()
        self.video_label = QLabel("Waiting for video...")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        left_panel.addWidget(self.video_label)
        
        alert_group = QGroupBox("Alert Status")
        alert_layout = QVBoxLayout()
        self.alert_indicator = AlertIndicator()
        alert_layout.addWidget(self.alert_indicator)
        alert_group.setLayout(alert_layout)
        left_panel.addWidget(alert_group)
        
        # Right panel
        right_panel = QVBoxLayout()
        self.ear_canvas = MplCanvas(self, 5, 4)
        self.mar_canvas = MplCanvas(self, 5, 4)
        self.prob_canvas = MplCanvas(self, 5, 4)
        right_panel.addWidget(self.ear_canvas)
        right_panel.addWidget(self.mar_canvas)
        right_panel.addWidget(self.prob_canvas)
        
        layout.addLayout(left_panel, 40)
        layout.addLayout(right_panel, 60)
        
        # Video thread
        self.thread = VideoThread()
        self.thread.change_pixmap.connect(self.update_image)
        self.thread.update_data.connect(self.update_graphs)
        self.thread.alert_signal.connect(self.update_alert)
        self.thread.start()
        
        self.counter = 0
        
    @pyqtSlot("QImage")
    def update_image(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))
        
    @pyqtSlot(float, float, float)
    def update_graphs(self, ear, mar, prob):
        self.counter += 1
        if self.counter % 2 == 0:
            self.ear_canvas.update_plot(self.counter, ear)
            self.mar_canvas.update_plot(self.counter, mar)
            self.prob_canvas.update_plot(self.counter, prob)
        
    @pyqtSlot(str)
    def update_alert(self, color):
        self.alert_indicator.set_color(color)
        
    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
