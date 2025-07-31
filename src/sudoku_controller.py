from sudoku_solver import SudokuSolver
from sudoku_visualizer import SudokuGUIVisualizer, SudokuTerminalVisualizer
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QThread, QObject, Signal, Qt
import sys


class SudokuController( ):

    def __init__(self, board: list[list[int]], time_delay: float = 0):
        super().__init__()
        self.time_delay = time_delay
        self.current_thread = QThread.currentThread()
        self.solver = SudokuSolver(board, time_delay, self.current_thread)

        self.solver_thread: QThread = QThread()
        self.solver.moveToThread(self.solver_thread)
        self.solver_thread.started.connect(self.solver.solve)

    def solveButtonClicked(self):
        self.visualizer.setTableFocus(False)
        if self.solver_thread.isFinished():
            self.solver_thread = QThread()
            
            self.solver.moveToThread(self.solver_thread)
            self.solver_thread.started.connect(self.solver.solve)

            self._setupConnections()

            self.solver.is_stopped = False
            self.solver_thread.start()
        else:
            self.solver_thread.start()

    def _setupConnections(self): #must execute after the visualizer has been instantiated
        self.visualizer.solve_button.clicked.connect(self.solveButtonClicked) #connect solve button to solver's solve

        self.solver.session_ended.connect(self.enableCellEditing)
        self.solver.session_started.connect(self.disableCellEditing)

        self.solver.value_changed.connect(self.valueChanged)
        self.visualizer.board.cellChanged.connect(self.cellChanged)

        self.visualizer.load_example.clicked.connect(self.loadBoard)
        self.visualizer.clear_button.clicked.connect(self.clearBoard)

        self.visualizer.quit_button.clicked.connect(self.quit)
        self.visualizer.stop_button.clicked.connect(self.stopButtonClicked)

        self.solver.started_solving.connect(lambda: self.visualizer.clear_button.setDisabled(True))
        self.solver.stop_solving.connect(lambda: self.visualizer.clear_button.setDisabled(False))
        self.solver.started_solving.connect(lambda: self.visualizer.clear_button.setDisabled(False))
    
        self.solver.started_solving.connect(lambda: self.visualizer.solve_button.setDisabled(True))
        self.solver.stop_solving.connect(lambda: self.visualizer.solve_button.setDisabled(False))
        self.solver.done_solving.connect(lambda: self.visualizer.solve_button.setDisabled(False))

        self.solver.started_solving.connect(lambda: self.visualizer.time_delay_lineedit.setDisabled(True))
        self.solver.stop_solving.connect(lambda: self.visualizer.time_delay_lineedit.setDisabled(False))
        self.solver.done_solving.connect(lambda: self.visualizer.time_delay_lineedit.setDisabled(False))

        self.solver.started_solving.connect(lambda: self.visualizer.load_example.setDisabled(True))
        self.solver.stop_solving.connect(lambda: self.visualizer.load_example.setDisabled(False))
        self.solver.done_solving.connect(lambda: self.visualizer.load_example.setDisabled(False))


        self.visualizer.time_delay_lineedit.textChanged.connect(self.timeDelayLineEditChanged)
        self.visualizer.solve_mode_combo_box.currentTextChanged.connect(self.solveModeChanged)

        

    def enableCellEditing(self):
        self.visualizer.disableCellEditing(False)
    
    def disableCellEditing(self):
        self.visualizer.disableCellEditing(True)

    def stopButtonClicked(self):
        self.visualizer.setTableFocus(True)
        self.solver.is_stopped = True
        self.solver_thread.quit()
        self.solver_thread.wait()

    def clearBoard(self):
        self.visualizer.setTableFocus(True)
        self.solver.clearBoard()

    #Done by the user
    def cellChanged(self, row: int, column: int):
        if self.visualizer.board.item(row, column) is self.visualizer.board.currentItem():
            print("Current Item: ", self.visualizer.board.currentItem())
            print("cell Changed")
            possible: bool = True
            value: str = self.visualizer.board.item(row, column).text()
            if value.isdigit():
                possible = self.solver.setCellValue(row, column, int(value))
            elif len(value) == 0:
                self.solver.setCellValue(row, column, 0)
                self.visualizer.board.item(row, column).setText("")
                print("Enter a number!")

            if not possible:
                self.visualizer.board.item(row, column).setText("")

    #When a value on the board is changed by the solver
    def valueChanged(self, row: int, column: int, value: int):
        print("value Changed")
        if value == 0:
            self.visualizer.board.item(row, column).setText("")
        else:
            self.visualizer.board.item(row, column).setText(str(value))
        self.solver_thread.msleep(self.time_delay)

    #---------------------------------------------------
    #Initializing UI
    #---------------------------------------------------
    def makeApp(self):
        self.app: QApplication = QApplication(sys.argv)

    def showUI(self, visualizer: SudokuGUIVisualizer):
        self.visualizer: SudokuGUIVisualizer = visualizer
        self.visualizer.time_delay_lineedit.setText(str(self.time_delay))
        self._setupConnections()
        self.visualizer.show()
        sys.exit(self.app.exec())   

    def solveModeChanged(self, text):
        if text == "Fast":
            self.visualizer.time_delay_lineedit.setDisabled(True)
        elif text == "Slow":
            self.visualizer.time_delay_lineedit.setDisabled(False)

    def timeDelayLineEditChanged(self, time: str):
        if time.isdigit():
            self.time_delay = float(time)
            self.solver.time_delay = float(time)
        else:
            self.visualizer.time_delay_lineedit.setText("")
            print("Please enter a valid time delay value")

    def loadBoard(self):
        for y in range(self.solver.state.board_size):
            for x in range(self.solver.state.board_size):
                value: int = self.solver.state.board[y][x]
                if value == 0:
                    self.visualizer.board.item(y, x).setText("")
                else:
                    self.visualizer.board.item(y, x).setText(str(value)) 
    

    #---------------------------------------------------
    #Closing the application
    #---------------------------------------------------
    def quit(self):
        self.solver.is_stopped = True
        self.solver_thread.quit()
        self.solver_thread.wait()
        self.visualizer.close()

    
