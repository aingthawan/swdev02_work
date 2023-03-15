import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Spatial Map Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a Matplotlib figure and canvas
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        # Create a scatter plot of spatial data
        ax = self.fig.add_subplot(111)
        x = np.random.rand(100)
        y = np.random.rand(100)
        ax.scatter(x, y)

        # Add the canvas to the main window
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
