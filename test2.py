import time
from PySide6 import QtCore, QtGui

class Thread(QtCore.QThread):
    def __init__(self, parent=None):
        super(Thread, self).__init__(parent)
        self.runs = True

    def run(self):
        self.commence_working()
        self.stop()
        # self.finished.emit()   # this one is not even necessary

    def stop(self):
        self.runs = False

    def commence_working(self):
        loop = 0
        while self.runs and loop <= 100:
            print("I am processing...")
            time.sleep(2) # short time pause to simulate work being done
            loop += 1

class GUI(QtGui.QDialog):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)

        self.l = QtGui.QLabel("Hello World", self)

        self.b = QtGui.QPushButton(self)
        self.b.setText("abort thread")

        self.sb = QtGui.QPushButton(self)
        self.sb.setText("start thread")

        self.vb = QtGui.QHBoxLayout()
        self.vb.addWidget(self.l)
        self.vb.addWidget(self.b)
        self.vb.addWidget(self.sb)
        self.setLayout(self.vb)

        self.b.clicked.connect(self.on_userAbort_clicked)
        self.sb.clicked.connect(self.start_thread_clicked)

    def on_userAbort_clicked(self):
        self.l.setText("aborting the thread...")
        self.thread.stop()
        self.thread.wait()

    def start_thread_clicked(self):
        self.thread = Thread()
        self.thread.finished.connect(self.thread_finished)
        self.l.setText("The thread is running")
        self.thread.start()

    def thread_finished(self):
            self.l.setText("The thread stopped")


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    g = GUI()
    g.show()
    sys.exit(app.exec_())