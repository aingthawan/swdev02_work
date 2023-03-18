import sys
import time
import json
import folium
import webbrowser
import pandas as pd
from PyQt5 import QtWidgets
from ELT_transform import main_database
from ELT_searching import invertedIndexSearch
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget

class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        file_name = 'database_elt_main.db'
        self.database_file = 'project\\database\\' + file_name        
        self.folium_file = 'project\\database\\for_spatial\\folium_map.html'
        
        with open('project\\database\\for_spatial\\custom.geo.json', encoding='utf-8') as f:
            # keep data in json format
            self.world_data = json.load(f)
        
        # clean new map
        m = folium.Map(location=[10, 0], tiles='cartodbdark_matter', zoom_start=2)
        m.save(self.folium_file)
        self.webEngineView = QWebEngineView()
        self.load_html()
        self.load_coor()
        
        self.setWindowTitle("Search GUI Basic v1.0")
        left_widget_width = 600
        # Create widgets
        self.search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(left_widget_width) # set box size
        self.search_button = QPushButton("Start Search")
        self.search_button.setFixedWidth(left_widget_width) # set box size
        self.output_area = QtWidgets.QListWidget()
        self.output_area.setFixedWidth(left_widget_width) # set box size
        self.output_area.setFixedHeight(200)
        
        self.insert_label = QLabel("Update:")
        self.insert_input = QLineEdit() # Update input box
        self.insert_input.setFixedWidth(300) # set box size
        self.insert_button = QPushButton("Insert")
        self.delete_button = QPushButton("Delete")
        self.result_len = QLabel("")
        self.log_label = QLabel("Log:")
        self.log_area = QtWidgets.QListWidget()
        self.log_area.setFixedHeight(125) # set box size
        self.log_area.setFixedWidth(300)

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
        # left_layout.addStretch()
        
        # Add stretch to push widgets to the top
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.insert_label)
        right_layout.addWidget(self.insert_input)
        right_layout.addWidget(self.insert_button)
        right_layout.addWidget(self.delete_button)
        right_layout.addWidget(self.log_label)
        right_layout.addWidget(self.log_area)

        # Create main layout
        main_info_layout = QHBoxLayout()
        main_info_layout.addLayout(left_layout)
        main_info_layout.addLayout(right_layout)
        # add map at the bottom
        main_layout = QVBoxLayout()
        main_layout.addLayout(main_info_layout)
        main_layout.addWidget(self.webEngineView)
        
        self.search_button.clicked.connect(self.search)
        self.insert_button.clicked.connect(self.insert)
        self.delete_button.clicked.connect(self.remove)
        
        # double click to open url
        self.output_area.itemDoubleClicked.connect(self.open_url)
        # single click to append url to input box
        self.output_area.itemClicked.connect(self.append_url)

        # Set the layout for the widget
        self.setLayout(main_layout)

        # Set the stylesheet for the widget
        style_sheet = """
            QWidget {
                background-color: #0a0a0a;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 22px;    
                font-weight: bold;
            }
            QLineEdit#searchInput, QLineEdit#insertInput {
                border: 2px solid #242323;
                border-radius: 4px;
                padding: 6px;
                font-size: 16px;
                background-color: #121111;
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
                border: 2px solid #242323;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
                background-color: #121111;
                color: #FFFFFF;
            }
        """
        self.setStyleSheet(style_sheet)
    
    def load_coor(self):
        # load country coordinate
        with open('project\\database\\for_spatial\\country_lat_long.csv', 'r') as f:
            self.country_coordinate = pd.read_csv(f)
    
    def map_plotter(self, country_dict):
        
        m = folium.Map(location=[10, 0], tiles='cartodbdark_matter', zoom_start=2)
        
        for country, freq in country_dict.items():
            lat = self.country_coordinate[self.country_coordinate['country'] == country]['lat'].values[0]
            long = self.country_coordinate[self.country_coordinate['country'] == country]['long'].values[0]
            # set marker for country name and frequency
            if freq is max(country_dict.values()):
                folium.Marker([lat, long], popup=(country).upper() + ' : ' + str(freq), icon=folium.Icon(color="red", icon='info-sign')).add_to(m)
            else:
                folium.Marker([lat, long], popup=country.upper(), icon=folium.Icon(color="orange", icon='info-sign')).add_to(m)
        
        # info_dict_new = {}
        # for key, value in country_dict.items():
        #     info_dict_new[key.title()] = value
        # # add choropleth layer
        # folium.Choropleth(
        #     geo_data=self.world_data,  # path to GeoJSON file
        #     name='choropleth',
        #     data=info_dict_new,
        #     columns=['Country', 'Frequency'],
        #     key_on='feature.properties.name',
        #     fill_color='YlOrRd',
        #     fill_opacity=0.7,
        #     line_opacity=0.2,
        #     legend_name='Frequency'
        # ).add_to(m)
        
        m.save(self.folium_file)
        self.load_html()
        
    def load_html(self):
        with open(self.folium_file, "r") as f:
            self.map_html = f.read()
        self.webEngineView.setHtml(self.map_html)
        self.webEngineView.update()



    def append_url(self, item):
        """append url to input box"""
        url = item.text()
        self.insert_input.setText(url)
    
    def open_url(self, item):
        url = item.text()
        webbrowser.open_new_tab(url)
    
    def search(self):
        """search function"""
        
        # get the query from the search line edit
        query = self.search_input.text()
        # check if input is not empty
        if not query:
            self.log_area.addItem(QtWidgets.QListWidgetItem("Please enter a query"))
            return
        
        try:
            # start timer
            search_start = time.time()
            # create the inverted index search object
            search = invertedIndexSearch(self.database_file)
            # get the list of url from the query
            links = search.full_search(query)
            search.close()
            search_time = time.time() - search_start
            
            self.map_plotter(links[1])
                        
        except Exception as e:
            self.log_area.addItem(QtWidgets.QListWidgetItem("Failed to search"))
            self.log_area.addItem(QtWidgets.QListWidgetItem(str(e)))
            return

        # clear the search previous result list
        self.output_area.clear()
        # check if there is any result
        if links:
            self.output_area.addItems([link[0] for link in links[0]])
            # display log in the log area
            self.log_area.addItem(QtWidgets.QListWidgetItem("Search completed : " + query))
            # print search time
            self.log_area.addItem(QtWidgets.QListWidgetItem("Search time : " + str(search_time)))
        else:
            self.log_area.addItem(QtWidgets.QListWidgetItem("No result found"))
            self.output_area.addItem(QtWidgets.QListWidgetItem("No result found"))
        self.log_area.scrollToBottom()
    
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
                self.log_area.addItem(QtWidgets.QListWidgetItem("Insert Process completed"))
                return
            except Exception as e:
                self.log_area.addItem(QtWidgets.QListWidgetItem("Failed to insert"))
                print("Insert Error : ", e)
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
                tf.close()
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
