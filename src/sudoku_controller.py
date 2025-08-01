import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from sudoku_solver import SudokuSolver
from sudoku_visualizer import SudokuGUIVisualizer

class SudokuController():

    def __init__(self, board: list[list[int]]):
        self.solver = SudokuSolver(board)
        
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.solver._step)

    #this functions will be connected to the solve button
    def startSolving(self):
        self.timer.start(int(0 * 1000))
        self.solver.solve()
    
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

        self.solver.finished.connect(self.stopButtonClicked)
        self.view.stop_button.clicked.connect(self.stopButtonClicked)

        self.view.solve_button.clicked.connect(lambda: self.view.toggleEverySidebarWidgetExcept("disable", exceptions=[self.view.stop_button, self.view.quit_button]))
        self.view.stop_button.clicked.connect(lambda: self.view.toggleEverySidebarWidgetExcept("enable", exceptions=[self.view.stop_button]))
        self.solver.finished.connect(lambda: self.view.toggleEverySidebarWidgetExcept("enable", exceptions=[self.view.solve_button]))

        
    def stopButtonClicked(self):
        self.timer.stop()

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
    

