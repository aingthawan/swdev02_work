from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from ELT_searching import invertedIndexSearch

class SearchWidget(QtWidgets.QWidget):
    """Search widget GUI"""

    def __init__(self):
        super().__init__()
        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchLineEdit = QtWidgets.QLineEdit()
        self.searchResultList = QtWidgets.QListWidget()
        self.initUI()

    def initUI(self):
        """initialize the GUI"""
        # self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Search Widget')

        vbox = QtWidgets.QVBoxLayout()

        # Add a label "Search : " beside the box
        label = QtWidgets.QLabel("Search : ")
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(self.searchLineEdit)
        vbox.addLayout(hbox)

        vbox.addWidget(self.searchButton)
        vbox.addWidget(self.searchResultList)
        self.setLayout(vbox)

        self.searchButton.clicked.connect(self.search)

    def search(self):
        """search function"""
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
        # self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Main Window')
        self.resize(800, 600)

        self.searchWidget = SearchWidget()
        self.setCentralWidget(self.searchWidget)

        self.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
