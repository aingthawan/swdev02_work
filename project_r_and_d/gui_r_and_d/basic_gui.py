import sys
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search GUI Basic v1.0")
        self.resize(800, 600)
        
        # Create widgets
        self.search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Start Search")
        self.output_area = QTextEdit()
        self.insert_label = QLabel("Insert:")
        self.insert_input = QLineEdit()
        # set box size
        self.insert_input.setFixedWidth(200)
        self.insert_button = QPushButton("Insert")
        self.delete_button = QPushButton("Delete")

        # Set widget properties
        self.search_input.setObjectName("searchInput")
        self.search_button.setObjectName("searchButton")
        self.output_area.setObjectName("outputArea")
        self.insert_input.setObjectName("insertInput")
        self.insert_button.setObjectName("insertButton")
        self.delete_button.setObjectName("deleteButton")

        # Create layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.search_label)
        left_layout.addWidget(self.search_input)
        left_layout.addWidget(self.search_button)
        left_layout.addWidget(self.output_area)
        
        # Add stretch to push widgets to the top
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.insert_label)
        right_layout.addWidget(self.insert_input)
        right_layout.addWidget(self.insert_button)
        right_layout.addWidget(self.delete_button)
        right_layout.addStretch()

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Set the layout for the widget
        self.setLayout(main_layout)

        # Set the stylesheet for the widget
        # Maybe make a separate file for this VVVVVVVVVVVVV
        style_sheet = """
            QWidget {
                background-color: #333333;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: bold;
            }
            QLineEdit#searchInput, QLineEdit#insertInput {
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
                font-size: 16px;
                background-color: #222222;
                color: #FFFFFF;
            }
            QPushButton#searchButton, QPushButton#insertButton, QPushButton#deleteButton {
                background-color: #fcba03;
                color: #0d0d0d;
                font-size: 16px;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QTextEdit#outputArea {
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
                font-size: 16px;
                background-color: #222222;
                color: #FFFFFF;
            }
        """
        self.setStyleSheet(style_sheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    search_widget = SearchWidget()
    search_widget.show()
    sys.exit(app.exec_())
