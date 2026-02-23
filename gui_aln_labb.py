from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTextEdit, QPushButton, QScrollArea, QTabWidget, QLabel, QHeaderView, QHBoxLayout, QButtonGroup
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap
import alignment
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
        QTabWidget::pane {   
          border-top: 0px;
          background-color: #dca7e6;      
        }
        
        QPushButton {
          background-color: white;
          border-style: outset;
          border-width: 2px;
          border-radius: 10px;
          border-color: #8b00a7;
          font: bold 14px;
          min-width: 10em;
          padding: 6px;
          color: black;
        }

        QPushButton:hover {
          background-color: #fbff92; 
        }

        QPushButton:pressed {
          background-color: #f6ff00;
          border-style: inset;
        }

        QPushButton:checked {
          background-color: #fff93d;
          border-style: inset;
          color: black;
        
        }
                                """)

        # Configs
        self.setWindowTitle('Alinhador LABB')
        self.title = QLabel('<h1>Alinhador LABB<h1>', self)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        base = os.path.dirname(os.path.abspath(__file__))
        pixmap = QPixmap(base + '/logo.jpg')
        self.logo = QLabel(self)
        self.logo.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

        # Set layout for the main window
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Initialize tabs
        self.tab1 = QWidget()
        self.layout1 = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.logo)
        self.header_layout.addWidget(self.title)
        self.header_layout.setSpacing(5)
        self.layout1.addLayout(self.header_layout)
        self.tab1.setLayout(self.layout1)

        # Textboxes for sequences input
        self.seq1_textbox = QTextEdit()
        self.seq2_textbox = QTextEdit()
        self.layout1.addWidget(self.seq1_textbox)
        self.layout1.addWidget(self.seq2_textbox)

        # Buttons for defining alignment algorithm
        self.alignment = "needle"
        needle_button = QPushButton('Needleman-Wunsch')
        needle_button.setCheckable(True)
        needle_button.clicked.connect(lambda: self.set_alignment("needle"))

        water_button = QPushButton('Smith-Waterman')
        water_button.setCheckable(True)
        water_button.clicked.connect(lambda: self.set_alignment("water"))
        
        group = QButtonGroup(self)
        group.setExclusive(True)
        group.addButton(needle_button)
        group.addButton(water_button)

        self.layout1.addWidget(needle_button)
        self.layout1.addWidget(water_button)

        # Running alignment
        self.run_button = QPushButton('Alinhar!')
        self.run_button.clicked.connect(self.run_aln)
        self.layout1.addWidget(self.run_button)
        self.layout1.addStretch(1)

        # Set page 2 to display matrix
        self.tab2 = QWidget()
        self.layout2 = QHBoxLayout()
        self.tab2.setLayout(self.layout2)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.tab2)
        self.scroll.setWidgetResizable(True)
        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout2.addWidget(self.table)
        self.alignment_label = QLabel()
        self.layout2.addWidget(self.alignment_label)
        self.alignment_label.setStyleSheet("font-size: 16px; font-family: Courier New;")

        # Handling tabs
        self.tabs.addTab(self.tab1, "Alinhar")
        self.tabs.addTab(self.scroll, "Matriz com scores")
        main_layout.addWidget(self.tabs)
    
    # Making the score matrix a heatmap
    def show_matrix_heatmap(self, matrix, path_coords):
        #getting sequences to display in column and row names
        
        if len(self.seq1) < len(self.seq2):
            self.seq1, self.seq2 = self.seq2, self.seq1

        self.seq1 = "-" + self.seq1.upper().lstrip("-")
        self.seq2 = "-" + self.seq2.upper().lstrip("-")

        rownames = list(self.seq1)
        colnames = list(self.seq2)

        #creating the table
        rows = len(matrix)
        cols = len(matrix[0])

        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.table.setHorizontalHeaderLabels(colnames)
        self.table.setVerticalHeaderLabels(rownames)

        # Find min/max for normalization
        min_val = min(min(row) for row in matrix)
        max_val = max(max(row) for row in matrix)

        for i in range(rows):
            for j in range(cols):
                value = matrix[i][j]
                item = QTableWidgetItem(str(value))
                
                # Green values for path cells
                if (i, j) in path_coords:
                  color = QColor(0, 255, 0)
                  item.setBackground(color)
                  self.table.setItem(i, j, item)

                # Heatmap values for other cells
                else:
                  # Normalize 0–1
                  norm = (value - min_val) / (max_val - min_val + 1e-9)

                  # Color scale (blue → red)
                  r = int(255 * norm)
                  b = int(255 * (1 - norm))
                  color = QColor(r, 0, b)

                  item.setBackground(color)
                  self.table.setItem(i, j, item)

    def show_aln(self, metrics):
        aln_1 = metrics["align1"]
        aln_2 = metrics["align2"]
        score = metrics["Score"]
        alignment_text = f"{aln_1}\n{aln_2}\nPontuação do alinhamento:{score}"

        self.alignment_label.setText(alignment_text)

    def set_alignment(self, alignment):
        self.alignment = alignment

    def run_aln(self):
        self.seq1 = self.seq1_textbox.toPlainText()
        self.seq2 = self.seq2_textbox.toPlainText() 

        if len(self.seq1) < len(self.seq2):
            self.seq1, self.seq2 = self.seq2, self.seq1
        
        # Checking if both sequences were input
        if not self.seq1 or not self.seq2:
            self.run_button.setText("Preencha os campos!")
            return
        
        # Runs the alignment and stores matrix_score, matrix_pointer, metrics in result object
        self.run_button.setText("Aligning...")
        if self.alignment == "needle":
            result = alignment.needle(self.seq1, self.seq2)
        elif self.alignment == "water":
            result = alignment.water(self.seq1, self.seq2)
        else:
            self.run_button.setText("Escolha um método!")
            return
        
        self.show_matrix_heatmap(result.matrix_score, result.path_coords)
        if result.matrix_score:
            self.run_button.setText("Alinhado!")
            self.tabs.setCurrentIndex(1)
            self.show_aln(result.metrics)



app = QApplication([])
window = MainWindow()
window.show()
app.exec()
