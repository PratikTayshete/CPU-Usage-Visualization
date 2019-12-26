import sys
from PySide2 import QtWidgets
from PySide2 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import cpu_process
import cpu_usage_design


class MainClass(QtWidgets.QMainWindow, cpu_usage_design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainClass, self).__init__(parent)
        # Load the UI
        self.setupUi(self)

        # Create and load the Matplotlib UI
        self.canvas = FigureCanvasQTAgg(Figure())
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.addWidget(self.canvas)
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.widget.setLayout(v_layout)
        self.x_val = []
        self.y_val = []
        self.index_val = 0
        self.canvas.axes.set_ylim([0, 100])
        self.canvas.axes.set_xlim(left=0)
        self.canvas.axes.set_xlabel("Time [in secs]")
        self.canvas.axes.set_ylabel("CPU Use [in %]")
        self.canvas.axes.set_title("Monitoring CPU Usage")

        # The Thread class instance to handle ProgressBar and Graph
        self.updatethread = UpdateThread()
        self.updatethread.connect(self.updatethread, QtCore.SIGNAL("signal(int)"), self.updateProgress)
        self.updatethread.connect(self.updatethread, QtCore.SIGNAL("signal(int)"), self.updateGraph)
        self.updatethread.start()



    # Method that updates the graph with the cpu usage count.
    def updateGraph(self, cpu_data):
        self.x_val.append(self.index_val)
        self.y_val.append(cpu_data)
        self.canvas.axes.clear()
        self.canvas.axes.set_ylim([0, 100])
        self.canvas.axes.set_xlim(left=max(0, self.index_val-20), right=self.index_val+20)
        self.canvas.axes.set_xlabel("Time [in secs]")
        self.canvas.axes.set_ylabel("CPU Use [in %]")
        self.canvas.axes.set_title("Monitoring CPU Usage")
        self.canvas.axes.plot(self.x_val, self.y_val)
        self.index_val += 1
        self.canvas.draw()


    # Method that updates the ProgressBar count.
    def updateProgress(self, cpu_data):
        self.progressBar.setValue(cpu_data)


# Thread class that gets the CPU percentage count and emits it as a signal.
class UpdateThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(UpdateThread, self).__init__(parent)

    def run(self):
        while True:
            cpu_data = cpu_process.get_process_percent()
            self.emit(QtCore.SIGNAL("signal(int)"), cpu_data)

    def stop(self):
        self.stop()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainClass()
    main_window.show()
    app.exec_()

