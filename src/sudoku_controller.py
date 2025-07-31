from PySide6.QtCore import QThread
from sudoku_solver import SudokuSolver
from sudoku_visualizer import SudokuGUIVisualizer

class SudokuController:

	def __init__(self):
		self.solver = SudokuSolver()
		self.visualizer = SudokuGUIVisualizer() #change later

	def startSolving(self):
		#this functions will be connected to the solve button	
		pass
	
	def setupUI(self):
		#make app
		#make window
		pass

	def showUI(self):
		#show the window
		pass

	def _setupConnections(self):
		#connect the GUI to the various backend functions
		pass

	def _setupThread(self):
		pass
		#setup the thread, connections and moves the solver to that thread

	

