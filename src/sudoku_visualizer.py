from typing import ClassVar
import sys
import time

from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QPushButton, QLineEdit, QComboBox, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QHeaderView, QTableWidgetItem, QStyledItemDelegate
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPen, QColor


class ANSIColors:
    YELLOW_BOLD: ClassVar[str]  = "\033[1;33m"
    GREEN_BOLD:  ClassVar[str]  = "\033[1;32m"
    WHITE_BOLD:  ClassVar[str]  = "\033[1;37m"
    END:         ClassVar[str]  = "\033[0m"
    
class SudokuDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Draw the default cell content
        super().paint(painter, option, index)

        rect = option.rect 
        row = index.row()
        col = index.column()

        # Set base thin pen
        thin_pen = QPen(QColor(0, 0, 0), 1)  # normal grid line
        thick_pen = QPen(QColor(0, 0, 0), 3) # thicker grid line

        # Draw borders manually
        # Top border
        painter.setPen(thick_pen if row % 3 == 0 else thin_pen)
        painter.drawLine(rect.topLeft(), rect.topRight())

        # Left border
        painter.setPen(thick_pen if col % 3 == 0 else thin_pen)
        painter.drawLine(rect.topLeft(), rect.bottomLeft())

        # Bottom border (only for last row or if it's 3rd row)
        if row == index.model().rowCount() - 1:
            painter.setPen(thick_pen)
        else:
            painter.setPen(thick_pen if (row + 1) % 3 == 0 else thin_pen)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

        # Right border (only for last column or if it's 3rd column)
        if col == index.model().columnCount() - 1:
            painter.setPen(thick_pen)
        else:
            painter.setPen(thick_pen if (col + 1) % 3 == 0 else thin_pen)
        painter.drawLine(rect.topRight(), rect.bottomRight())

class SudokuObserver:

    def run(self):
        pass

    def renderUI(self):
        pass


class SudokuTerminalVisualizer(SudokuObserver):
    def __init__(self, time_delay: int = 0):
        print("\033[2J\033[H")
        self.time_delay = time_delay

    def print(self, state):
        sys.stdout.write("\033[H") #moves the cursor to the top (doesnt clear screen)

        # BOARD_SIZE * PUZZLE_HORIZONTOL_SPACE is for every number
        # BOARD_SIZE//BOX_WIDTH is the number of |'s in the puzzle. Multiply it with PUZZLE_HORIZONTOL_SPACE to get the full space
        # + 1 for the last |
        horizontol_line_length: int = (
            (state.board_size * state.horizontal_spacing)
            + ((state.board_size // state.box_size) * state.horizontal_spacing)
            + 1
        )

        board_row: str = ""
        for y in range(state.board_size):
            if y % state.box_size == 0:  # put horizontol line at top
                board_row += (f"{ANSIColors.WHITE_BOLD}{'-' * horizontol_line_length}{ANSIColors.END}\n")

            for x in range(state.board_size):
                if x % state.box_size == 0:  # put | every BOX_WIDTH
                    board_row += (f"{ANSIColors.WHITE_BOLD}{'|':<{state.horizontal_spacing}}{ANSIColors.END}")

                # Print the numbers (if original board is given then solution numbers are colored differently)
                value: int = state.board[y][x]
                if value == 0: # Empty cells
                    board_row += (f"{ANSIColors.YELLOW_BOLD}{'-':<{state.horizontal_spacing}}{ANSIColors.END}")
                elif state.original_board and value != state.original_board[y][x]: #solution values
                    board_row += (f"{ANSIColors.GREEN_BOLD}{value:<{state.horizontal_spacing}}{ANSIColors.END}")
                else:  # given numbers
                    board_row += (f"{ANSIColors.WHITE_BOLD}{value:<{state.horizontal_spacing}}")

                if x == state.board_size - 1:  # put | at the right edge
                    board_row += (f"{ANSIColors.WHITE_BOLD}|{ANSIColors.END}\n")

            if y == state.board_size - 1:
                board_row += (f"{ANSIColors.WHITE_BOLD}{'-' * horizontol_line_length}{ANSIColors.END}")
            
        sys.stdout.write(board_row)
        sys.stdout.flush()

        if self.time_delay > 0:
            time.sleep(self.time_delay)


class SudokuGUIVisualizer(QMainWindow, SudokuObserver):
    def __init__(self, window_geometry: QRect = QRect(500, 200, 1200, 800)):
        super().__init__()
        self.window_geometry: QRect = window_geometry
        self.initUI()

    def __new__(cls, window_geometry: QRect= QRect(500, 200, 1200, 800)):
        if not hasattr(cls, "instance"):
            cls.instance: SudokuGUIVisualizer = super(SudokuGUIVisualizer, cls).__new__(cls, window_geometry)
        return cls.instance
    
    def initUI(self):
        self.setGeometry(self.window_geometry)
        self.setMinimumWidth(750)
        #Central Widget
        self.central_widget: QWidget = QWidget(self)
        self.horizotal_layout: QHBoxLayout = QHBoxLayout()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.horizotal_layout)

        #StyleSheets
        self.button_stylesheet = """
        QPushButton 
        {
            background-color: #121212;
            color: white;
            border-radius: 10px;
            padding: 12px;
            font-size: 16px;
        }

        QPushButton::hover
        {
            background-color: #383838;
        }

        QPushButton#quit_button
        {
            background-color: #fc392b;
        }

        QPushButton#quit_button:hover
        {
            background-color: #ff6054;
        }

        QLineEdit 
        {
            border-radius: 10px;
            background-color: white;
            color: black;
            padding: 12px;
            font-size: 16px;
        }

        QComboBox
        {
            border-radius: 10px;
            background-color: white;
            color: black;
            padding: 12px;
            font-size: 16px;
        }

        QGroupBox 
        {
            border-radius: 5px;
            background-color:#949494;
            font-size: 16px;
        }

        QTableWidget 
        {
            border-radius: 10px;
            font-size: 35px;
            color: white;
        }

        QLabel
        {
            font-size: 16px;
            color: white;
        }
        """
        self.setStyleSheet(self.button_stylesheet)

        #Sidebar
        self.sidebar: QGroupBox = QGroupBox(self.central_widget)
        self.vertical_layout: QVBoxLayout = QVBoxLayout()
        self.sidebar.setLayout(self.vertical_layout)
        self.horizotal_layout.addWidget(self.sidebar)

        #QTimer
        self.timer: QTimer = QTimer(self)

        #QTableWidget
        self.board: QTableWidget = QTableWidget(self.central_widget)
        self.horizotal_layout.addWidget(self.board)
        self.board.setColumnCount(9)
        self.board.setRowCount(9)
        self.board.verticalHeader().setVisible(False)
        self.board.horizontalHeader().setVisible(False)
        self.board.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.board.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.board.setItemDelegate(SudokuDelegate(self.board))
        self.board.setSelectionMode(QTableWidget.NoSelection)

        for y in range(9):
            for x in range(9):
                self.board.setItem(y, x, QTableWidgetItem())
                self.board.item(y, x).setTextAlignment(Qt.AlignCenter)
        self.sidebar_widgets: list[QWidget] = []
        #Load example button
        self.load_example: QPushButton = QPushButton("Load Example Puzzle")
        self.sidebar_widgets.append(self.load_example)

        #Create puzzle example
        self.create_puzzle: QPushButton = QPushButton("Create Random Puzzle")
        self.sidebar_widgets.append(self.create_puzzle)


        #Fast/Slow solve combo box
        self.solve_mode_combo_box: QComboBox = QComboBox()
        self.solve_mode_combo_box.addItem("Fast")
        self.solve_mode_combo_box.addItem("Slow")
        self.sidebar_widgets.append(self.solve_mode_combo_box)

        #Time Delay line edit
        self.time_delay: QLineEdit = QLineEdit()
        self.time_delay.setText("0")
        self.sidebar_widgets.append(self.time_delay)

        if self.solve_mode_combo_box.currentText() == "Fast":
            self.time_delay.setDisabled(True)

        #Solve button
        self.solve_button: QPushButton = QPushButton("Solve Puzzle")
        self.sidebar_widgets.append(self.solve_button)

        #Stop button
        self.stop_button: QPushButton = QPushButton("Stop Solving")
        self.sidebar_widgets.append(self.stop_button)


        #Clear button
        self.clear_button: QPushButton = QPushButton("Clear Board")
        self.sidebar_widgets.append(self.clear_button)

        #Time label
        self.time_label: QLabel = QLabel("Timer: ")
        self.sidebar_widgets.append(self.time_label)

        #Quit button
        self.quit_button: QPushButton = QPushButton("Quit")
        self.quit_button.setObjectName("quit_button")
        self.sidebar_widgets.append(self.quit_button)

        self.horizotal_layout.setStretch(0, 20)
        self.horizotal_layout.setStretch(1, 80)


        for widget in self.sidebar_widgets:
            self.vertical_layout.addWidget(widget)
            self.vertical_layout.addStretch(8)
        

    