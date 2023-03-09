import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget
from ELT_searching import invertedIndexSearch
from ELT_transform import main_database

class SearchWidget(QWidget):
    def __init__(self):
        # file_name = 'database_elt_main.db'
        file_name = 'database_elt_main_small.db'
        # self.database_file = 'project\database\\' + file_name
        self.database_file = 'project\database\\for_dev\\' + file_name
        
        super().__init__()

        self.setWindowTitle("Search GUI Basic v1.0")
        self.resize(400, 600)
        
        left_widget_width = 600
        # Create widgets
        self.search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(left_widget_width) # set box size
        
        self.search_button = QPushButton("Start Search")
        self.search_button.setFixedWidth(left_widget_width) # set box size
        
        self.output_area = QtWidgets.QListWidget()
        self.output_area.setFixedWidth(left_widget_width) # set box size
        
        self.insert_label = QLabel("Update:")
        self.insert_input = QLineEdit() # Update input box
        self.insert_input.setFixedWidth(200) # set box size
        self.insert_button = QPushButton("Insert")
        self.delete_button = QPushButton("Delete")
        self.result_len = QLabel("")
        self.log_label = QLabel("Log:")
        self.log_area = QtWidgets.QListWidget()
        self.log_area.setFixedHeight(100) # set box size
        self.log_area.setFixedWidth(200)

        # Set widget properties
        self.search_input.setObjectName("searchInput")
        self.search_button.setObjectName("searchButton")
        self.output_area.setObjectName("outputArea")
        self.insert_input.setObjectName("insertInput")
        self.insert_button.setObjectName("insertButton")
        self.delete_button.setObjectName("deleteButton")
        self.log_area.setObjectName("logArea")

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
        # add log label
        right_layout.addWidget(self.log_label)
        # add log area
        right_layout.addWidget(self.log_area)
        # add stretch to push widgets to the top
        right_layout.addStretch()

        # Create main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        
        self.search_button.clicked.connect(self.search)
        self.insert_button.clicked.connect(self.insert)
        self.delete_button.clicked.connect(self.remove)

        # Set the layout for the widget
        self.setLayout(main_layout)

        # Set the stylesheet for the widget
        # Maybe make a separate file for this VVVVVVVVVVVVV
        style_sheet = """
            QWidget {
                background-color: #2f362d;
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
                background-color: #1e211d;
                color: #FFFFFF;
            }
            QPushButton#searchButton, QPushButton#insertButton, QPushButton#deleteButton {
                background-color: #fcba03;
                border: 2px solid #a37903;
                border-radius: 4px;
                padding: 6px;
                color: #0d0d0d;
                font-size: 16px;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QListWidget#outputArea, #logArea{
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
                background-color: #1e211d;
                color: #FFFFFF;
            }
        """
        self.setStyleSheet(style_sheet)

    def search(self):
        """search function"""
        
        # get the query from the search line edit
        query = self.search_input.text()
        # check if input is not empty
        if query == "":
            self.log_area.addItem(QtWidgets.QListWidgetItem("Please enter a query"))
            return
        else:    
            # create the inverted index search object
            search = invertedIndexSearch(self.database_file)
            # get the list of url from the query
            links = search.full_search(query)
            search.close()
            # clear the search previous result list
            self.output_area.clear()
            # check if there is any result
            if links != None:
                for link in links:
                    self.output_area.addItem(QtWidgets.QListWidgetItem(link[0]))
                # display log in the log area
                self.log_area.addItem(QtWidgets.QListWidgetItem("Search completed : " + query))
            else:
                self.log_area.addItem(QtWidgets.QListWidgetItem("No result found"))
                self.output_area.addItem(QtWidgets.QListWidgetItem("No result found"))
            
    def insert(self):
        """insert function"""
        # get the url from the insert line edit
        input_url = self.insert_input.text()
        # check if input is not empty
        if input_url == "":
            self.log_area.addItem(QtWidgets.QListWidgetItem("Please enter a url"))
            return
        else:
            try:
                # create the data pipeline object
                tf = main_database(self.database_file)
                tf.direct_update_link(input_url)
                tf.close()
                # clear the insert line edit
                self.insert_input.clear()
                # display log in the log area
                self.log_area.addItem(QtWidgets.QListWidgetItem("Insert completed"))
                return
            except Exception as e:
                self.log_area.addItem(QtWidgets.QListWidgetItem("Failed to insert"))
                self.log_area.addItem(QtWidgets.QListWidgetItem(str(e)))
                return
        
    def remove(self):
        """remove function"""
        # get the url from the insert line edit
        input_url = self.insert_input.text()
        # check if input is not empty
        if input_url == "":
            self.log_area.addItem(QtWidgets.QListWidgetItem("Please enter a url"))
            return
        else:
            try:
                # remove all the data related to the url
                tf = main_database(self.database_file)
                tf.removeData(input_url)
                # clear the insert line edit
                self.insert_input.clear() 
                # display log in the log area
                self.log_area.addItem(QtWidgets.QListWidgetItem("Remove completed"))
                return
            # except and keep error message then display it in the log area
            except Exception as e:
                self.log_area.addItem(QtWidgets.QListWidgetItem("Failed to remove"))
                self.log_area.addItem(QtWidgets.QListWidgetItem(str(e)))
                return
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    search_widget = SearchWidget()
    search_widget.show()
    sys.exit(app.exec_())
