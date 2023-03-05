from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from ELT_searching import invertedIndexSearch
import qdarkstyle


class SearchWidget(QtWidgets.QWidget):
    """Search widget GUI"""

    def __init__(self):
        super().__init__()
        # create the search button
        self.searchButton = QtWidgets.QPushButton("Search")
        # make bold the text
        # self.searchButton.setStyleSheet("font-weight: bold")
        # change the font size
        # self.searchButton.setStyleSheet("font-size: 18px")
        
        # create the search line edit
        self.searchLineEdit = QtWidgets.QLineEdit()
        # resize the search line edit font
        # self.searchLineEdit.setStyleSheet("font-size: 18px")
        # create the update line edit
        self.updateLineEdit = QtWidgets.QLineEdit()
        # self.updateLineEdit.setStyleSheet("font-size: 18px")
        
        # create the search result list
        self.searchResultList = QtWidgets.QListWidget()
        # change search result list font size
        # self.searchResultList.setStyleSheet("font-size: 16px")
        self.initUI()

    def initUI(self):
        """initialize the GUI"""

        vbox = QtWidgets.QVBoxLayout()

        # Add a label "Search : " beside the box
        label = QtWidgets.QLabel("Search : ")
        # set label font size
        # label.setStyleSheet("font-size: 20px")
        
        
        # create a horizontal box layout to put the label and the search line edit
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.searchLineEdit)
        # hbox
        # - label : Search + Search Line
        vbox.addLayout(hbox)
        
        # create a vertical box layout to put the search button and the search result list
        vbox.addWidget(self.searchButton)
        vbox.addWidget(self.searchResultList)
        # vbox
        # - label : Search + Search Line
        # - Search Button
        # - Search Result List
        
        
        vbox2 = QtWidgets.QVBoxLayout()
        # add update label 
        update_label = QtWidgets.QLabel("Update : ")
        vbox2.addWidget(update_label)
        # add update line edit
        vbox2.addWidget(self.updateLineEdit)
        # add update/remove button
        update_button = QtWidgets.QPushButton("Update")
        vbox2.addWidget(update_button)
        remove_button = QtWidgets.QPushButton("Remove")
        vbox2.addWidget(remove_button)
        # add stretch to push widgets to the top
        vbox2.addStretch()
         
        
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addLayout(vbox)
        hbox2.addLayout(vbox2)
        
        # set the layout for the widget
        self.setLayout(hbox2)

        # create the search function and connect it to the search button
        self.searchButton.clicked.connect(self.search)

        # Apply the dark theme
        app.setStyleSheet(qdarkstyle.load_stylesheet())

    def search(self):
        """search function"""
        self.searchResultList.clear()
        self.searchResultList.addItem(QtWidgets.QListWidgetItem("Searching . . ."))
        
        # get the query from the search line edit
        query = self.searchLineEdit.text()
        # create the inverted index search object
        file_name = 'database_elt_main_backup.db'
        database_file = 'project\database\\' + file_name
        search = invertedIndexSearch(database_file)
        # get the list of url from the query
        links = search.full_search(query)
        search.close()
        # clear the search previous result list
        self.searchResultList.clear()
        # check if there is any result
        if links != None:
            for link in links:
                self.searchResultList.addItem(QtWidgets.QListWidgetItem(link[0]))
        else:
            self.searchResultList.addItem(QtWidgets.QListWidgetItem("No result found"))


class MainWindow(QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        """initialize the GUI"""
        self.setWindowTitle('Basic Search GUI')
        self.resize(800, 600)

        self.searchWidget = SearchWidget()
        self.setCentralWidget(self.searchWidget)

        self.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
