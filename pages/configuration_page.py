import qtawesome as qta  # qtawesome 모듈 가져오기
from PyQt6.QtWidgets import QWidget, QComboBox, QTabWidget, QTableWidget, QListWidget, QListWidgetItem, QStackedWidget, QVBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, QHBoxLayout, QFileDialog
from PyQt6.QtCore import Qt, QRect # 커서를 변경하기 위한 모듈
# from modules import title_widget  # 타이틀 모듈 임포트
from functools import partial

class ConfigurationPage(QWidget):
    def __init__(self, project_name, user_name, parent=None):
        super().__init__(parent)

        self.user_name = user_name
        self.project_name = project_name

        #Add main panel
        self.frame_layout = QHBoxLayout()
        self.frame_layout.setContentsMargins(10,10,10,10)
        self.frame_layout.setObjectName('grey_bg')

        #Add left panel
        self.left_panel = self.create_left_panel()
        self.frame_layout.addLayout(self.left_panel)

        # Add right panel
        self.rightPanel = QVBoxLayout()
        self.existingtrains_label = QLabel("Select from existing trains")
        self.existingtrains_selection = QComboBox()
        self.existingtrains_selection.addItem('selection 1')
        self.existingtrains_selection.addItem('selection 2')
        self.existingtrains_selection.addItem('selection 3')
        self.existingtrains_selection.addItem('selection 4')

        self.configurationtext = QLabel()
        self.configurationtext.setObjectName('configurationlabel')
        self.rightPanel.addWidget(self.configurationtext)

        # Add configuration tabs to right panel
        self.configurationtabwidget = self.create_configuration_tabs()
        self.rightPanel.addWidget(self.configurationtabwidget)
        self.run_button = QPushButton('Run simulation')
        self.run_button.setFixedWidth(150)
        self.rightPanel.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.frame_layout.addLayout(self.rightPanel)
        self.setLayout(self.frame_layout)
        self.setObjectName('configuration_page')

    def create_left_panel(self):

        self.leftPanel = QVBoxLayout()
        self.projectLabel = QHBoxLayout()

        # add project name and train selection label
        self.project_name_label1 = QLabel('Project name: ')
        self.project_name_label1.setObjectName('project_name1')
        self.project_name_label2 = QLabel(self.project_name)
        self.project_name_label2.setObjectName('project_name2')
        self.train_selection_label = QLabel('Select an existing train')
        self.train_selection_label.setObjectName('h2_heading')
        self.projectLabel.addWidget(self.project_name_label1)
        self.projectLabel.addWidget(self.project_name_label2)
        self.leftPanel.addLayout(self.projectLabel)
        self.leftPanel.addWidget(self.train_selection_label)

        # adjust layout height / spacing
        self.projectLabel.setSpacing(0)
        self.leftPanel.setSpacing(0)
        self.projectLabel.setContentsMargins(0, 0, 0, 0)
        self.leftPanel.setContentsMargins(0, 0, 0, 0)

        # train 1 dropdown options
        self.left_dropdown1 = QComboBox()
        self.left_dropdown1.addItem('select train 1') #dummy train data
        self.leftPanel.addWidget(self.left_dropdown1)

        self.left_trainInfo = QLabel('Train Summary')
        self.left_trainInfo.setObjectName('h1_heading')

        self.leftPanel.addWidget(self.left_trainInfo)
        self.trainInfo_name = QLabel('Train Name')

        # create dropdown list for locomotive, bin & brakevan
        self.locomotiveLabel = QLabel('locomotive(s):')
        self.locomotiveLabel.setObjectName('small_label')
        self.locomotiveList = QListWidget()
        self.locomotiveList.setFixedSize(80,150)
        self.leftPanel.addWidget(self.locomotiveLabel)
        self.leftPanel.addWidget(self.locomotiveList)

        self.binLabel = QLabel('bin(s):')
        self.binLabel.setObjectName('small_label')
        self.binList = QListWidget()
        self.binList.setFixedSize(200,150)
        self.leftPanel.addWidget(self.binLabel)
        self.leftPanel.addWidget(self.binList)

        self.brakevanLabel = QLabel('brake van(s):')
        self.brakevanList = QListWidget()
        self.brakevanLabel.setObjectName('small_label')
        self.brakevanList.setFixedSize(200,150)
        self.leftPanel.addWidget(self.brakevanLabel)
        self.leftPanel.addWidget(self.brakevanList)
        
        return self.leftPanel
    
    def create_configuration_tabs(self):
        # Create configuration tab
        self.configurationTab = QTabWidget()
        self.configurationTab.setObjectName("grey_bg")

        locomotiveHeadings = ["locoID", "locoName", "locoWeight", "locoPower", "locoWheelBaseType","locoEngineType", "batteryName", "batteryMinCapacity", "batteryMaxCapacity"]
        locomotiveSelections = [" selection 1", "selection 2"]
        trackHeadings =  ["locoID", "locoName", "locoWeight", "locoPower", "locoWheelBaseType","locoEngineType", "batteryName", "batteryMinCapacity", "batteryMaxCapacity"]
        trackSelections = [" selection 1", "selection 2"]
        cartHeadings = ["locoID", "locoName", "locoWeight", "locoPower", "locoWheelBaseType","locoEngineType", "batteryName", "batteryMinCapacity", "batteryMaxCapacity"]
        cartSelections = [" selection 1", "selection 2"]
        brakevanHeadings = ["locoID", "locoName", "locoWeight", "locoPower", "locoWheelBaseType","locoEngineType", "batteryName", "batteryMinCapacity", "batteryMaxCapacity"]
        brakevanSelections = [" selection 1", "selection 2"]
        engineHeadings = ["locoID", "locoName", "locoWeight", "locoPower", "locoWheelBaseType","locoEngineType", "batteryName", "batteryMinCapacity", "batteryMaxCapacity"]
        engineSelections =  [" selection 1", "selection 2"]

        # Add locomotive, cart, brake van, engine and train tabs
        self.trackTab = self.create_tab(locomotiveSelections, locomotiveHeadings)
        self.locomotiveTab = self.create_tab(trackSelections, trackHeadings)
        self.cartTab = self.create_tab(cartSelections, cartHeadings)
        self.brakevanTab = self.create_tab(brakevanSelections, brakevanHeadings)
        self.engineTab = self.create_tab(engineSelections, engineHeadings)

        self.configurationTab.addTab(self.trackTab, "track")
        self.configurationTab.addTab(self.locomotiveTab, "locomotive")
        self.configurationTab.addTab(self.cartTab, "cart")
        self.configurationTab.addTab(self.brakevanTab, "brake van")
        self.configurationTab.addTab(self.engineTab, "engine")

        self.configurationTab

        self.configurationTab.setCurrentIndex(0)

        return self.configurationTab
    
    def create_tab(self, tabSelections, listHeadings):
        tab = QWidget()
        self.horizontallayout = QHBoxLayout(tab)
        self.verticallayout = QVBoxLayout()
        self.verticallayout2 = QVBoxLayout()
        self.verticallayout_widget = QWidget()
        self.verticallayout3 = QVBoxLayout(self.verticallayout_widget)
        self.verticallayout_widget.setFixedWidth(390)
        self.horizontallayout.addLayout(self.verticallayout)
        self.horizontallayout.addLayout(self.verticallayout2)
        self.horizontallayout.addWidget(self.verticallayout_widget)

        #create table widget for configuration information
        table_label = QLabel('Add new:')
        select_label = QLabel('Use existing data:')
        view_label = QLabel('Locomotive (s):')
        table_label.setObjectName('bold_small')
        select_label.setObjectName('bold_small')
        view_label.setObjectName('bold_small')

        # Create locomotive selection combobox and push buttons
        button1 = QPushButton('+ Add existing')
        button2 = QPushButton('+ Add to list')
        button3 = QPushButton('+ Add new row')
        button4 = QPushButton('Delete row')

        button1.setFixedWidth(100)
        button1.setFixedHeight(30)
        button1.setObjectName('grey_btn')

        #create selection dropdown and options
        dropdown = QComboBox()
        for selection in tabSelections: 
            dropdown.addItem(selection)
        
        dropdown.setFixedHeight(38)
        dropdown.setFixedWidth(150)
        
        # create locomotive view table
        view_table = QTableWidget()
        view_table.setColumnCount(9)
        view_table.setHorizontalHeaderLabels(listHeadings)
        view_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.verticallayout.addWidget(select_label)
        self.verticallayout.addWidget(dropdown)
        self.verticallayout.addWidget(table_label)

        #add editing tables with headers and rows
        listHeadings_split = [listHeadings[i:i+5] for i in range(0, len(listHeadings), 5)]
        editing_tables = {}
        for i, chunk in enumerate(listHeadings_split, 1):
            editing_tables[i] = QTableWidget(parent=tab) 
            editing_tables[i].setHorizontalHeaderLabels(chunk)
            editing_tables[i].setColumnCount(len(chunk))
            editing_tables[i].setRowCount(1)
            editing_tables[i].setObjectName("editing_table")
            editing_tables[i].setFixedHeight(70)
            self.verticallayout.addWidget(editing_tables[i])
        
        # clear and add rows buttons
        button3.clicked.connect(partial(self.addRow, editing_tables[1], editing_tables[2]))
        button4.clicked.connect(partial(self.deleteRow, editing_tables[1], editing_tables[2]))
        button3.setObjectName('grey_btn')
        button4.setObjectName('grey_btn')

        #connect locomotive edit table data to view table
        button2.clicked.connect(partial(self.addToList, editing_tables, view_table))
        button2.setObjectName('grey_btn')

        self.verticallayout.addStretch(0)
        self.verticallayout.setContentsMargins(0, 0, 0, 0)

        self.verticallayout2.addStretch(18)
        self.verticallayout2.addWidget(button1)
        self.verticallayout2.addStretch(14)
        self.verticallayout2.addWidget(button2)
        self.verticallayout2.addStretch(3)
        self.verticallayout2.addWidget(button3)
        self.verticallayout2.addStretch(3)
        self.verticallayout2.addWidget(button4)
        self.verticallayout2.addStretch(140)

        self.verticallayout3.addWidget(view_label)
        self.verticallayout3.addWidget(view_table)

        return tab
    
    def deleteRow(self, table1, table2):
        current_row1 = table1.rowCount()
        current_row2 = table2.rowCount()
        table1.removeRow(current_row1 - 1)
        table2.removeRow(current_row2 - 1)

        #reduce height of the 2 tables
        table1.setFixedHeight(table1.height() - 31)
        table2.setFixedHeight(table2.height() - 31)
    
    def addRow(self, table1, table2):
        table1.setRowCount(table1.rowCount() + 1)
        table2.setRowCount(table2.rowCount() + 1)

        # set height of table to increase with each additional row
        table2_height = table2.height()
        table1_height = table1.height()
        table1.setFixedHeight(table1_height + 31)
        table2.setFixedHeight(table2_height + 31)
    
    def addToList(self, editing_tables, viewTable):
        total_col = 0
        for table in editing_tables:
            for row_index in range(table.rowCount()):
                target_row = viewTable.rowCount()
                viewTable.insertRow(target_row)

                for col in range(table.columnCount()):
                    item = table.takeItem(row_index, col)
                    if item:
                        viewTable.setItem(target_row, total_col, item)
                        total_col = total_col + 1
                
                self.delete_row(table, row_index)

    def errorHandling():
        return "found missing information"

    def delete_row(self, table, row_index):
        table.setRowCount(0)
        table_height = table.height()
        table.setFixedHeight(table_height - 31 * (1 + row_index))
    





        