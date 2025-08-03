import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QObject, Signal, QElapsedTimer

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
        
        self.elapsed_timer: QElapsedTimer = QElapsedTimer()
        self.elapsed_time: float = 0
        

    #this functions will be connected to the solve button
    def startSolving(self):
        self.elapsed_timer.start()
        self.view.board.setCurrentCell(-1, -1)
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
        self.view.time_delay_lineedit.returnPressed.connect(self.timeDelayChanged)
        self.view.clear_button.clicked.connect(self.clearBoardButtonClicked)
        self.view.board.cellChanged.connect(self.cellEdited)

        self.solver.finished.connect(self.stopButtonClicked)
        self.view.stop_button.clicked.connect(self.stopButtonClicked)

        self.view.solve_button.clicked.connect(lambda: self.view.toggleEverySidebarWidgetExcept("disable", exceptions=[self.view.stop_button, self.view.quit_button]))
        self.view.stop_button.clicked.connect(lambda: self.view.toggleEverySidebarWidgetExcept("enable", exceptions=[self.view.stop_button]))
        self.solver.finished.connect(lambda: self.view.toggleEverySidebarWidgetExcept("enable", exceptions=[self.view.stop_button]))

        self.session_started.connect(lambda: self.view.toggleEditCells("disable"))
        self.session_started.connect(lambda: self.view.setTableFocus(False))
        self.session_ended.connect(lambda: self.view.toggleEditCells("enable"))
        self.session_ended.connect(lambda: self.view.setTableFocus(True))

    def cellEdited(self, row: int, column: int):
        if self.view.board.item(row, column) is self.view.board.currentItem():
            possible: bool = True
            value: str = self.view.board.item(row, column).text()

            if value.isdigit():
                possible = self.solver.setCellValue(row, column, int(value))
            else:
                self.solver.setCellValue(row, column, 0)
                self.view.board.item(row, column).setText("")

            if not possible:
                self.view.board.item(row, column).setText("")

    def clearBoardButtonClicked(self):
        self.solver.clearBoard()
        self.session_ended.emit()
        self.elapsed_time = 0
        self.view.time_label.setText("Timer: 0")
        
    def stopButtonClicked(self):
        self.elapsed_time += self.elapsed_timer.elapsed()
        self.timer.stop()
        if self.view.solve_mode_combo_box.currentText() == "Fast":
            self.loadBoard()

    def timeDelayChanged(self):
        try:
            self.time_delay = float(self.view.time_delay_lineedit.text())
        except:
            print("Must be a number")

    def solveModeChanged(self, index: int):
        current_text: str = self.view.solve_mode_combo_box.currentText()
        if current_text == "Fast":
            self.view.time_delay_lineedit.setDisabled(True)
        else:
            self.view.time_delay_lineedit.setDisabled(False)

    def valueChanged(self, row: int, column: int, value: int):
        if self.view.solve_mode_combo_box.currentText() != "Fast":
            if value == 0:
                self.view.board.item(row, column).setText("")
            else:
                self.view.board.item(row, column).setText(str(value))
        self.view.time_label.setText("Timer: " + str((self.elapsed_timer.elapsed() + self.elapsed_time)/1000))

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
    

