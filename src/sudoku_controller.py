import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread

from sudoku_solver import SudokuSolver
from sudoku_visualizer import SudokuGUIVisualizer

class SudokuController:

    def __init__(self, board: list[list[int]]):
        self.solver = SudokuSolver(board)

    #this functions will be connected to the solve button
    def startSolving(self):
        self.solver.solve()
    
    def setupUI(self):
        self.app: QApplication = QApplication(sys.argv)
        self.view: SudokuGUIVisualizer = SudokuGUIVisualizer()
        self._setupConnections()
        pass

    def showUI(self):
        self.view.show()
        sys.exit(self.app.exec())

    def _setupThread(self):
        pass
        #setup the thread, connections and moves the solver to that thread

    #connect the GUI to the various backend functions
    def _setupConnections(self):
        self.solver.value_changed.connect(self.valueChanged)

        self.view.solve_button.clicked.connect(self.startSolving)
        self.view.load_example.clicked.connect(self.loadBoard)
        self.view.quit_button.clicked.connect(self.quit)

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

    def quit(self):
        self.view.close()
    

