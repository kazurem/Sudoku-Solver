import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QObject, Signal

from sudoku_solver import SudokuSolver
from sudoku_visualizer import SudokuGUIVisualizer

class SudokuController(QObject):
    session_started: Signal = Signal()
    session_ended: Signal = Signal()

    def __init__(self, board: list[list[int]], time_delay: float = 0):
        super().__init__()
        self.solver = SudokuSolver(board)
        self.time_delay: float = time_delay
        
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.solver._step)

    #this functions will be connected to the solve button
    def startSolving(self):
        self.session_started.emit()
        self.solver.solve()
        self.timer.start(int(self.time_delay * 1000))
    
    def setupUI(self):
        self.app: QApplication = QApplication(sys.argv)
        self.view: SudokuGUIVisualizer = SudokuGUIVisualizer()
        self._setupConnections()
        pass

    def showUI(self):
        self.view.show()
        sys.exit(self.app.exec())

    #connect the GUI to the various backend functions
    def _setupConnections(self):
        self.solver.value_changed.connect(self.valueChanged)

        self.view.solve_button.clicked.connect(self.startSolving)
        self.view.load_example.clicked.connect(self.loadBoard)
        self.view.quit_button.clicked.connect(self.quitApplication)
        self.view.solve_mode_combo_box.currentTextChanged.connect(self.solveModeChanged)
        self.view.time_delay.returnPressed.connect(self.timeDelayChanged)
        self.view.clear_button.clicked.connect(self.clearBoardButtonClicked)

        self.solver.finished.connect(self.stopButtonClicked)
        self.view.stop_button.clicked.connect(self.stopButtonClicked)

        self.view.solve_button.clicked.connect(lambda: self.view.toggleEverySidebarWidgetExcept("disable", exceptions=[self.view.stop_button, self.view.quit_button]))
        self.view.stop_button.clicked.connect(lambda: self.view.toggleEverySidebarWidgetExcept("enable", exceptions=[self.view.stop_button]))
        self.solver.finished.connect(lambda: self.view.toggleEverySidebarWidgetExcept("enable", exceptions=[self.view.stop_button]))

        self.session_started.connect(lambda: self.view.toggleEditCells("disable"))
        self.session_ended.connect(lambda: self.view.toggleEditCells("enable"))

    def clearBoardButtonClicked(self):
        self.solver.clearBoard()
        self.session_ended.emit()
        
    def stopButtonClicked(self):
        self.timer.stop()

    def timeDelayChanged(self):
        try:
            self.time_delay = float(self.view.time_delay.text())
        except:
            print("Must be a number")

    def solveModeChanged(self, index: int):
        current_text: str = self.view.solve_mode_combo_box.currentText()
        if current_text == "Fast":
            self.view.time_delay.setDisabled(True)
        else:
            self.view.time_delay.setDisabled(False)

    def valueChanged(self, row: int, column: int, value: int):
        if value == 0:
            self.view.board.item(row, column).setText("")
        else:
            self.view.board.item(row, column).setText(str(value))

    def loadBoard(self):
        board_size: int = self.solver.state.board_size
        for y in range(board_size):
            for x in range(board_size):
                value: int = self.solver.state.board[y][x]
                if value == 0:
                    self.view.board.item(y, x).setText("")
                else:
                    self.view.board.item(y, x).setText(str(value))

    def quitApplication(self):
        self.view.close()
    

